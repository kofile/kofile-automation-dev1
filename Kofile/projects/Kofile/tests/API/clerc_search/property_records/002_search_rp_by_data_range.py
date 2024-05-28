from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):
    place, dep_id = "cs", 1
    search_page_limit = 50
    data_list = ["cs_first_rp_order", "copy_first_rp_order", "certified_copy_first_rp_order",
                 "re_capture_first_rp_order", "re_index_first_rp_order"]
    used_docs = list()

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        now = self.datetime.now()
        data = self.api_test_data.cs_search_rp_data.copy()
        data["DepartmentId"] = str(self.dep_id)
        data["DefaultEndDate"] = now.strftime('%m/%d/%Y 12:00:00 AM')
        data["Filters"]["RecordedDate"]["ToDate"] = now.strftime('%m/%d/%Y')
        data["Filters"]["DocumentGroups"]["$values"] = [i['Id'] for i in self.get("cs_rp_doc_groups") if i['Id'] != 0]
        data["DocGroupsNames"] = ['All', ]
        data["Filters"]["PartyTypes"]["$values"] = [i['Code'] for i in self.get("cs_rp_party_names") if i['Id'] != 0]
        data["PartyTypesNames"] = ['All', ]
        data["SearchFields"] = [i['FieldName'] for i in self.get("cs_rp_search_fields") if i['FieldName'] != "All"]
        data["SearchFieldsNames"] = ['All', ]
        data["UseAnd"] = True
        return data

    @property
    def schema(self):
        return self.api_test_data.cs_search_schema

    def __before__(self):
        self.run_dependencies(("cs_rp_doc_groups", "cs_rp_party_names", "cs_rp_search_fields"))

    def __test__(self, page=1):
        self.set_content_type('application/json')
        self.response = self.session.post(self.get_url(self.api_urls.DocumentSearch % self.dep_id,
                                                       domain_key="cs_domain"), json=self.post_data,
                                          params={"pageNo": page})
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)
        result_set = self.response.json().get("ResultSet")
        assert result_set is not None, "Cant find ResultSet in response json"
        assert len(result_set) > 0, "ResultSet is blank"
        all_find = False
        data_list = dict()
        for item in result_set:
            if item["NumOfPages"]:
                data_list[item.get("Id")] = item
        if data_list:
            self.response = self.session.post(
                self.get_url(self.api_urls.GetDocumentsExtraInfo, domain_key="cs_domain"),
                json=[{"Id": i.get("Id"), "Path": i.get("Filename")} for i in data_list.values()])
            assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
            self.validate(instance=self.response.json(), schema=self.api_test_data.cs_ex_info_schema)
            for ex_info in self.response.json():
                if self.data_list:
                    if not ex_info.get("InWorkflow") and ex_info.get("Id") not in self.used_docs:
                        self.set(self.data_list.pop(0), data_list[ex_info.get("Id")])
                        self.used_docs.append(ex_info.get("Id"))
                else:
                    all_find = True
                    break
        if not all_find:
            count = self.response.json()["PagesCount"]
            prefix = f"Total pages: {count}, current page: {page} limit: {self.search_page_limit}"
            assert count > page, f"{prefix}, result with doc pages not found"
            assert self.search_page_limit >= page, f"{prefix}, result with doc pages not found"
            self.__test__(page=page + 1)


if __name__ == '__main__':
    run_test(__file__, browser="none")
