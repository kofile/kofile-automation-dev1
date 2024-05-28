from random import choice
from golem import actions
from projects.Kofile.api.api_services import ApiService
from projects.Kofile.api.JSONS import ClerkSearchJsons
from projects.Kofile.Lib.testdata_helpers import ClerkSearchTestDataHelpers
import logging


class ClerkSearch(ApiService):

    def __init__(self, data, user_index=0):
        ApiService.__init__(self, data, crs=False, user_index=user_index)
        if not self.test_config:
            self.test_config = ClerkSearchTestDataHelpers().test_config(oit=data.get("OIT"))

    def document_search(self, page_num=1, search_text=None):
        department = self.test_config.get("dept")
        doc_group = None if search_text else self.test_config.get("doc_group")
        doc_group_id = None if search_text else self.test_config.get("doc_group_id")
        department_id = self.test_config.get("dept_id")
        doc_type_in_cs = None if search_text else self.test_config.get("doc_type_in_cs").replace(',', '')
        search_text = search_text + ' ' + self.test_config.get("doc_type_in_cs") if actions.get_data().get(
            "use_doc_type_in_api_CS") else search_text
        actions.step(f"-> API -> Documents search: *{doc_group if doc_group else search_text if search_text else ''} "
                     f"in '{department}[{department_id}]' - ( {page_num} page )*")
        url = f"{self.domain}/Document/Search/{department_id}"
        data = ClerkSearchJsons.document_search(department_id, doc_group, doc_group_id, page_num, doc_type_in_cs,
                                                search_text)
        r = self.request_("POST", url, json_=data).json()
        return r

    def get_document_price(self, document_id, arg):
        department_id = self.test_config.get("dept_id")
        url = f"{self.domain}/ShoppingCart/GetDocumentPriceDetails" \
              f"?documentId={document_id}&departmentId={department_id}"
        r = self.request_("GET", url).json()
        return r.get(arg)

    def search_document_with_price(self, arg="TotalPrice", limit=1, exclude_in_workflow=False):
        page_num = 1
        while page_num <= 20:
            docs = self.document_search(page_num)
            page_num += 1
            if docs.get("TotalRecords"):
                doc_search_results = docs.get("ResultSet")
                if exclude_in_workflow:
                    data = [{"Id": i.get("Id"), "Path": i.get("Filename")} if i.get("Filename") else {"Id": i.get("Id")}
                            for i in doc_search_results]
                    url = f"{self.domain}/Image/GetDocumentsExtraInfo"
                    res = self.request_("POST", url, json_=data).json()
                    doc_search_result_dict = {i["Id"]: i["Number"] for i in doc_search_results}
                    results = [{"Id": i.get("Id"), "Number": doc_search_result_dict.get(i.get("Id"))}
                               for i in res if not i.get("InWorkflow") and i.get("ImageExists")]
                else:
                    results = doc_search_results
                for i in results:
                    price = self.get_document_price(i.get("Id"), arg)
                    doc_num = i.get("Number")
                    if price >= limit and doc_num is not None:
                        self.env_data.doc_num = doc_num  # For Clerk Search
                        self.env_data.doc_price = price
                        self.env_data.doc_number = doc_num.split('-', 1)[1] if '-' in str(
                            doc_num) else doc_num  # For Order Search
                        return doc_num
            else:
                raise ValueError(f"Documents not found: {docs}")
        raise ValueError(f"No document with price found")

    def get_documents_extra_info(self, documents: dict):
        """
        documents - {doc_number: {doc_id: filename}, ...}
        return [document numbers] 'not in workflow'
        """
        doc_data = list(documents.values())
        data = [{"Id": k, "Path": v} for i in doc_data for k, v in i.items()]
        logging.info(f"-> API -> Get documents({len(data)}) extra info")
        url = f"{self.domain}/Image/GetDocumentsExtraInfo"
        r = self.request_("POST", url, json_=data).json()
        # collect doc ids 'not in workflow'
        not_in_wf = [i.get("Id") for i in r if not (i.get("InWorkflow"))]
        # collect doc numbers 'not in workflow'
        not_in_wf_docs = [k for i in not_in_wf for k, v in documents.items() if i in v.keys() and k]
        return not_in_wf_docs

    def get_document_number(self, page_num=1, not_in_workflow=False, num_of_page=0, max_page_search=20):
        """
        not_in_workflow - should be 'True' for Re-Index and Re-Capture
        """
        docs = self.document_search(page_num)
        doc_type_in_cs = self.test_config.get("doc_type_in_cs")
        logging.info(f"-> API -> Get {doc_type_in_cs if doc_type_in_cs else ''} document numbers")
        if docs.get("TotalRecords"):
            pages_count = int(docs.get("PagesCount", 1))
            max_page_search = pages_count if pages_count < max_page_search else max_page_search
            results = docs.get("ResultSet")
            d_type = "Id" if not_in_workflow else "DocType"
            if doc_type_in_cs:
                all_docs = {i.get("Number"): {i.get(d_type): i.get("Filename")} for i in results
                            if (i.get("Number") and " " not in i.get("Number"))
                            and (i.get("Filename") and i.get("NumOfPages") and doc_type_in_cs in i.get("DocType")
                                 .replace('</span>', '').replace('<span class="highlighted">', ''))}
            else:
                all_docs = {i.get("Number"): {i.get(d_type): i.get("Filename")} for i in results
                            if ("VOID" not in i.get("DocType") and (i.get("Number") and " " not in i.get("Number")))
                            and (i.get("Filename") and i.get("NumOfPages") > num_of_page)}
            if not all_docs:
                # if expected doc type not found -> search on next pages
                if page_num < max_page_search:
                    logging.info(f"Documents {doc_type_in_cs} not found on {page_num}/{pages_count} page."
                                 f" Search on next page...")
                    return self.get_document_number(page_num + 1, not_in_workflow, num_of_page, max_page_search)
                else:
                    raise ValueError(f"Documents {doc_type_in_cs} not found on {page_num} pages!")
            docs = list(all_docs.keys())
            if not_in_workflow:
                docs = self.get_documents_extra_info(all_docs)
                if not docs:
                    # if 'Not in workflow' documents not found -> search on next pages
                    logging.info(f"'Not in workflow' documents not found on {page_num}/{pages_count} page."
                                 f" Search on next page...")
                    return self.get_document_number(page_num + 1, not_in_workflow, num_of_page, max_page_search)
            doc_num = choice(docs)
            logging.info(f"-> API -> Found({len(docs)}) Return: '{doc_num}'")
            self.env_data.doc_num = doc_num  # For Clerk Search
            self.env_data.doc_number = doc_num.split('-', 1)[1] if '-' in str(doc_num) else doc_num  # For Order Search
            return doc_num
        else:
            raise ValueError(f"Documents not found: {docs}")

    def search_by_doc_number(self, doc_number, retries=15, wait=10, check_doctype=None):
        r = self.document_search(search_text=doc_number)["ResultSet"]
        for i in r:
            dn = i.get("Number").replace('</span>', '').replace('<span class="highlighted">', '')
            if doc_number == dn:
                i.update({"Number": dn})
                logging.info(f"Found: {i}")
                if not check_doctype:
                    return i
                else:
                    if check_doctype not in i["DocType"] and not retries:
                        assert False, f"Document '{doc_number}' is not {check_doctype}:\n{r}"
        retries -= 1
        if retries:
            actions.wait(wait)
            return self.search_by_doc_number(doc_number, retries, wait)
        else:
            assert False, f"Document '{doc_number}' not found in CS:\n{r}"

    def clear_inbox(self):
        """
        Clear inbox for current user
        """
        logging.info(f"-> API -> Clear inbox")
        url = f"{self.domain}/ShoppingCart/ClearInboxCart"
        r = self.request_("POST", url)
        return r
