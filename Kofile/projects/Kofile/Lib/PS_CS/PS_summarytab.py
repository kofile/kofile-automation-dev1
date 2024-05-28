"""Properties and methods of Preview popup/Summary tab"""

from projects.Kofile.Lib.test_parent import LibParent


class PSSummaryTab(LibParent):
    def __init__(self):
        super(PSSummaryTab, self).__init__()

    def document_summary(self):
        """
        Returns list of lists where each inner list is a combination
        of row header and its value. Order Summary page should be visible.
        """
        self._general_helper.find(self._pages.PS.summary_tab.doc_sum_last_section)
        all_summary = (
            "xpath", "//*[@id='documentSummaryArea']/table/tbody/tr[2]/td/table/tbody/tr", "All S table fields")
        all_ = self._general_helper.find_elements(all_summary, True)
        ret_lst = [i.replace(": ", ":").split(":") for i in all_]
        return ret_lst

    def document_preview_summary(self):
        self._general_helper.find(self._pages.PS.summary_tab.doc_sum_last_section)
        all_ = self._general_helper.find_elements(self._pages.PS.summary_tab.all_summary, True)
        if not all_:
            raise ValueError("Failed to parse data from Preview Summary")
        ret_lst = [i.replace(": ", ":").split(":") for i in all_]
        ret_dict = {i[0]: i[1] for i in ret_lst}
        self._actions.store("prev_sum", {"doc_num": ret_dict.get("Document Number"),
                                         "doc_number": ret_dict.get("Document Number").split('-', 1)[1],
                                         "num_of_pages": ret_dict.get("Number of Pages"),
                                         "rec_datetime": ret_dict.get("Recorded Date/Time"),
                                         "doc_status": ret_dict.get("Document Status"),
                                         "doc_bvp": ret_dict.get("Book/Volume/Page"),
                                         "doc_instr_date": ret_dict.get("Instrument Date"),
                                         "doc_type": self.document_type()})
        return ret_lst

    def document_type(self):
        """
        Returns document type from Summary tab. Empty string otherwise.
        Summary tab should be active before calling this method
        """
        res = self._general_helper.find(self._pages.PS.summary_tab.doc_type, get_text=True)
        return res

    def document_parties(self):
        """
        Returns a list of lists in a format:
        [
        [Name, Party Type, Full Address], ...,
        ]
        If list is empty, it means that there is no Parties section or exception occured.
        """
        ret_lst = []
        hdr = self._general_helper.find(self._pages.PS.summary_tab.doc_parties_header)
        if hdr.text == "Parties":
            # this section is Parties section
            row_count = len(self._general_helper.find_elements(self._pages.PS.summary_tab.doc_parties_row))
            if row_count > 0:
                for i in range(1, row_count + 1):
                    # read each row, element by element
                    temp_lst = []
                    res = self._general_helper.find(self._general_helper.remake_locator(
                        self._pages.PS.summary_tab.doc_parties_row, f"[{i}]/td[1]/a"))
                    temp_lst.append(res)
                    res = self._general_helper.find(self._general_helper.remake_locator(
                        self._pages.PS.summary_tab.doc_parties_row, f"[{i}]/td[2]"))
                    temp_lst.append(res)
                    ret_lst.append(temp_lst)
        return ret_lst

    def document_another_section_list(self):
        """
        Returns a list of available section names, except document summary and Parties sections.
        """
        ret_lst = []
        self._general_helper.find(
            self._general_helper.remake_locator(self._pages.PS.summary_tab.doc_table_row, "[last()]"))
        row_count = self._general_helper.find_elements(self._pages.PS.summary_tab.doc_table_row)
        if row_count >= 3:
            for i in range(3, row_count + 1):
                try:
                    res = self._general_helper.find(self._general_helper.remake_locator(
                        self._pages.PS.summary_tab.doc_table_row, f"[{i}]/td[1]/div[1]"))
                except Exception as e:
                    print(e)
                    # irregular section is located
                    res = self._general_helper.find(self._general_helper.remake_locator(
                        self._pages.PS.summary_tab.doc_table_row, f"[{i}]/td[1]/span"))
                if res.text != "Parties":
                    ret_lst.append(res.text)
        return ret_lst

    def document_legal(self):
        """
        Returns a list of Legal Descriptions or Cattle Brands
        description (if applicable)
        """
        ret_lst = []
        row_number = self.__rownumber("Legal Description")
        if row_number == 0:
            row_number = self.__rownumber("Cattle Brand Description")
        if row_number != 0:
            # get data rows
            try:
                res = self._general_helper.find_elements(self._general_helper.remake_locator(
                    self._pages.PS.summary_tab.doc_table_row, f"[{row_number}]/td[1]/div[2]/ul/li"))
                if len(res) > 0:
                    for i in range(1, len(res) + 1):
                        elem = self._general_helper.find(self._general_helper.remake_locator(
                            self._pages.PS.summary_tab.doc_table_row, f"[{row_number}]/td[1]/div[2]/ul/li[{i}]/div"))
                        ret_lst.append(elem.text)
                return ret_lst
            except Exception as e:
                print(e)
                elem = self._general_helper.find(self._general_helper.remake_locator(
                    self._pages.PS.summary_tab.doc_table_row, f"[{row_number}]/td[1]/div[2]/em"))
                ret_lst.append(elem.text)
                return ret_lst
        return ret_lst

    def document_marginal_refs(self):
        """
        Returns a list of lists of Marginal References in a format:
        [
        [DOC ... BOOK ..., Ref doc type, Ref recorded], [...]
        ]
        """
        ret_lst, temp_lst = [], []
        ret_lst = []
        row_number = self.__rownumber("Marginal References")
        if row_number != 0:
            # get data rows
            try:
                res = self._general_helper.find_elements(self._general_helper.remake_locator(
                    self._pages.PS.summary_tab.doc_table_row, f"[{row_number}]/td[1]/div[2]/table/tbody/tr"))
                if len(res) > 0:
                    # get row's columns
                    for i in range(1, len(res) + 1):
                        temp_lst = []
                        res = self._general_helper.find(self._general_helper.remake_locator(
                            self._pages.PS.summary_tab.doc_table_row,
                            f"[{row_number}]/td[1]/div[2]/table/tbody/tr[{i}]/td[1]/a"))
                        temp_lst.append(res.text)
                        res = self._general_helper.find(self._general_helper.remake_locator(
                            self._pages.PS.summary_tab.doc_table_row,
                            f"[{row_number}]/td[1]/div[2]/table/tbody/tr[{i}]/td[4]"))
                        temp_lst.append(res.text)
                        res = self._general_helper.find(self._general_helper.remake_locator(
                            self._pages.PS.summary_tab.doc_table_row,
                            f"[{row_number}]/td[1]/div[2]/table/tbody/tr[{i}]/td[5]"))
                        temp_lst.append(res.text)
                        ret_lst.append(temp_lst)
                return ret_lst
            except Exception as e:
                print(e)
                elem = self._general_helper.find(self._general_helper.remake_locator(
                    self._pages.PS.summary_tab.doc_table_row, f"[{row_number}]/td[1]/div[2]/em"))
                temp_lst.append(elem.text)
                ret_lst.append(temp_lst)
                return ret_lst
        else:
            return ret_lst

    def document_return_address(self):
        """
        Returns a list of string containing addresses
        """
        ret_lst, temp_lst = [], []
        row_number = self.__rownumber("Return Address")
        if row_number != 0:
            # get data rows
            try:
                res = self._general_helper.find_elements(self._general_helper.remake_locator(
                    self._pages.PS.summary_tab.doc_table_row, f"[{row_number}]/td[1]/table/tbody/tr"))
                if len(res) > 0:
                    # get row's columns
                    for i in range(1, len(res) + 1):
                        res = self._general_helper.find(self._general_helper.remake_locator(
                            self._pages.PS.summary_tab.doc_table_row,
                            f"[{row_number}]/td[1]/table/tbody/tr[{i}]/td[1]/span"))
                        ret_lst.append(res.text)
                return ret_lst
            except Exception as e:
                print(e)
                res = self._general_helper.find(self._general_helper.remake_locator(
                    self._pages.PS.summary_tab.doc_table_row, f"[{row_number}]/td[1]/table/tbody/tr[1]/td[1]/span"))
                ret_lst.append(res.text)
                return ret_lst
        else:
            return ret_lst

    def document_tracking(self):
        """
        Returns a list of lists in a format:
        [
        [Serial Number, Order Number, Order Date], [...]
        ]
        Applicable to Birth and Death Records tabs only
        """
        ret_lst, temp_lst = [], []
        row_number = self.__rownumber("Tracking")
        if row_number != 0:
            # get data rows
            try:
                res = self._general_helper.find_elements(self._general_helper.remake_locator(
                    self._pages.PS.summary_tab.doc_table_row, f"[{row_number}]/td[1]/div[2]/table/tbody/tr"))
                if len(res) > 0:
                    # get row's columns
                    for i in range(1, len(res) + 1):
                        temp_lst = []
                        res = self._general_helper.find(self._general_helper.remake_locator(
                            self._pages.PS.summary_tab.doc_table_row,
                            f"[{row_number}]/td[1]/div[2]/table/tbody/tr[{i}]/td/[1]"))
                        temp_lst.append(res.text[14:])
                        res = self._general_helper.find(self._general_helper.remake_locator(
                            self._pages.PS.summary_tab.doc_table_row,
                            f"[{row_number}]/td[1]/div[2]/table/tbody/tr[{i}]/td/[2]/a"))
                        temp_lst.append(res.text)
                        res = self._general_helper.find(self._general_helper.remake_locator(
                            self._pages.PS.summary_tab.doc_table_row,
                            f"[{row_number}]/td[1]/div[2]/table/tbody/tr[{i}]/td/[3]"))
                        temp_lst.append(res.text[11:])
                        ret_lst.append(temp_lst)
                return ret_lst
            except Exception as e:
                print(e)
                elem = self._general_helper.find(self._general_helper.remake_locator(
                    self._pages.PS.summary_tab.doc_table_row, f"[{row_number}]/td[1]/div[2]/em"))
                temp_lst.append(elem.text)
                ret_lst.append(temp_lst)
                return ret_lst
        else:
            return ret_lst

    def document_remarks(self):
        """
        Returns a list of strings of Document Remarks section
        """
        ret_lst, temp_lst = [], []
        row_number = self.__rownumber("Document Remarks")
        if row_number != 0:
            # get data rows
            try:
                res = self._general_helper.find_elements(self._general_helper.remake_locator(
                    self._pages.PS.summary_tab.doc_table_row, f"[{row_number}]/td[1]/div[2]/ul/li"))
                if len(res) > 0:
                    for i in range(1, len(res) + 1):
                        elem = self._general_helper.find(self._general_helper.remake_locator(
                            self._pages.PS.summary_tab.doc_table_row, f"[{row_number}]/td[1]/div[2]/ul/li[{i}]"))
                        ret_lst.append(elem.text)
                return ret_lst
            except Exception as e:
                print(e)
                elem = self._general_helper.find(self._general_helper.remake_locator(
                    self._pages.PS.summary_tab.doc_table_row, f"[{row_number}]/td[1]/div[2]/em"))
                ret_lst.append(elem.text)
                return ret_lst
        return ret_lst

    def __rownumber(self, section):
        """
        Returns row number as integer of specified section name.
        Returns 0 in case of exception
        """
        row_count = len(self._general_helper.find_elements(self._pages.PS.summary_tab.doc_table_row))
        if row_count >= 3:
            for i in range(3, row_count + 1):
                try:
                    # try to find regular section
                    res = self._general_helper.find(self._general_helper.remake_locator(
                        self._pages.PS.summary_tab.doc_table_row, f"[{i}]/td[1]/div[1]"))
                except Exception as e:
                    print(e)
                    # irregular section is located
                    res = self._general_helper.find(self._general_helper.remake_locator(
                        self._pages.PS.summary_tab.doc_table_row, f"[{i}]/td[1]/span"))
                if res.text == section:
                    return i
        return 0
