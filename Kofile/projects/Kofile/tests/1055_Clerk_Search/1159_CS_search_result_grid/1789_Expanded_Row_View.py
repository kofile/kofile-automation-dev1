from datetime import datetime
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
        Create several orders in CRS, finalize it, scan images in Capture step, map them to the document and save ->
        Orders are moved to Indexing step
        Index all data absent from Order step tabs -> Orders are moved to Archive step
        Execute the CS export scheduler and find the documents in Clerk Search 
            -> Documents are found and displayed in search results
        Click on Expanded All Rows icon -> Additional info appears in tabs below each result row
        Navigate through tabs and check the data displayed in tabs 
            -> Tabs correctly display the data entered for each tab during order creation
        """

tags = ['48999_location_2']


class test(TestParent):                                                                                # noqa

    def __init__(self, data):
        self.add_remark = True
        self.cs_search_with_doc_year = False
        super(test, self).__init__(data, __name__, precondition=self._precondition)

    def __48000__(self):
        # on the 48000 the add new remark link is absent
        self.add_remark = False
        # on the 48000 every year doc num pull resets
        self.cs_search_with_doc_year = True

    def __48999__(self):
        # on the 48999 the add new remark link is absent
        self.add_remark = False

    def __test__(self):
        self.atom.CS.general.go_to_cs(clerk=True)

        # search document
        self.lib.PS.general.search_document_by_number(with_year=self.cs_search_with_doc_year)
        if self.lib.PS.ps_main_page.is_search_successful():
            self.lib.general_helper.find_and_click(self.pages.PS.main_page.expand_all_btn)
            grantor = self.lib.general_helper.find(self.pages.PS.main_page.grantor_tab_view, get_text=True,
                                                   should_exist=False, timeout=2)
            grantee = self.lib.general_helper.find(self.pages.PS.main_page.grantee_tab_view, get_text=True,
                                                   should_exist=False, timeout=1)
            self.lib.general_helper.find_and_click(self.pages.PS.main_page.legal_description_tab)
            legal_desc = self.lib.general_helper.find(self.pages.PS.main_page.legal_desc, get_text=True)
            self.lib.general_helper.find_and_click(self.pages.PS.main_page.marginal_references_tab)
            ref_book = self.lib.general_helper.find(self.pages.PS.main_page.ref_book, get_text=True)
            ref_type = self.lib.general_helper.find(self.pages.PS.main_page.ref_type, get_text=True)
            ref_record = self.lib.general_helper.find(self.pages.PS.main_page.ref_record, get_text=True)
            ref_record = datetime.strptime(ref_record.split("T")[0], "%Y-%m-%d")
            self.lib.general_helper.find_and_click(self.pages.PS.main_page.document_remarks_tab)
            document_remarks = self.lib.general_helper.find(self.pages.PS.main_page.document_remarks, get_text=True,
                                                            should_exist=False, timeout=1)
            self.lib.general_helper.find_and_click(self.pages.PS.main_page.return_address_tab)
            return_address = self.lib.general_helper.find(self.pages.PS.main_page.return_address, get_text=True)

            self.lib.PS.ps_main_page.get_found_document_numbers()[0].click()
            self.lib.PS.ps_preview.click_tab("Summary")
            self.actions.wait_for_element_displayed(self.pages.PS.summary_tab.doc_summary_table)
            if grantor:
                self.actions.assert_element_text(self.pages.PS.summary_tab.grantor, grantor)
            if grantee:
                self.actions.assert_element_text(self.pages.PS.summary_tab.grantee, grantee)
            self.actions.assert_element_text(self.pages.PS.summary_tab.legal_description_link, legal_desc)
            self.actions.assert_element_text(self.pages.PS.summary_tab.marginal_ref_link, ref_book)
            self.actions.assert_element_text(self.pages.PS.summary_tab.ref_doc_type, ref_type)
            date = self.lib.general_helper.find(self.pages.PS.summary_tab.ref_record, get_text=True)
            assert datetime.strptime(date.split(" ")[0], "%m/%d/%Y") == ref_record, "Recorded date not equals"
            if document_remarks:
                self.actions.assert_element_text(self.pages.PS.summary_tab.doc_remarks, document_remarks)
            self.actions.assert_element_text(self.pages.PS.summary_tab.return_address, return_address)
        else:
            raise ValueError("Search failed!")

    def _precondition(self):
        self.atom.CS.api_helper.initialize_drawer()
        self.atom.CS.api_helper.create_order()
        if self.data["async"] == "1":
            with self.lib.db as db:
                db.scheduler_job_update_for_export(scheduler_job_code="OrderItemContentExport")
        self.atom.CS.api_helper.capture_document()
        self.lib.data_helper.get_dept_id()
        with self.lib.db as db:
            vol, page = db.get_exist_doc_vol_and_page_by_department()
        self.atom.CS.api_helper.index_document(prop_type=True, add_remark=self.add_remark, set_ref=(vol, page))
        self.lib.db_with_vpn.scheduler_job_update_for_set_export_document(self.data.departments.RP)


if __name__ == '__main__':
    run_test(__file__)
