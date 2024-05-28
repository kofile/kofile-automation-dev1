from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
        Create a document in CRS and find it in Clerk Search by doc number while still in workflow ->
        "Document in Workflow" red triangle is displayed on the row in CS
        Add this document to Inbox and open the Inbox ->
        Only "Certified Copy" and "Copy" order types are available in Inbox. Re-Capture and Re-Index options are not.
        """

tags = ['48999_location_2']


class test(TestParent):                                                                               # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__, precondition=self._precondition)

    def __test__(self):
        self.atom.CS.general.go_to_cs()
        self.lib.PS.ps_main_page.clear_inbox_()
        # dept list
        req_dept_tab = self.data.get("test_config").get("dept")
        self.lib.PS.ps_main_page.click_on_department_tab(req_dept_tab)
        doc_num = self.data['doc_year-doc_num']
        order_type = self.data.get("test_config").get("order_type")
        # enter doc number to search field
        self.lib.PS.ps_main_page.search_field(doc_num)
        # narrow search
        self.lib.PS.ps_main_page.click_more_options_button()
        # set recorded date range 'to' date
        self.lib.PS.ps_main_page.date_to_set(req_dept_tab)
        if "Doc#" in self.lib.PS.ps_main_page.get_checkbox_names():
            self.lib.PS.ps_main_page.click_checkbox("Doc#")
        self.lib.PS.ps_main_page.click_search_button()

        if self.lib.PS.ps_main_page.is_search_successful():
            self.lib.PS.ps_main_page.click_row_with_doc_number(doc_num, not_in_workflow=True if order_type in
                                                               ["Re-Index", "Re-Capture"] else False)
            self.lib.PS.ps_preview.click_tab("Summary")
            self.lib.PS.ps_summary_tab.document_preview_summary()
            self.actions.wait_for_element_displayed(self.pages.PS.summary_tab.in_workflow)
            self.lib.PS.ps_preview.click_add_to_inbox(1)
            self.lib.PS.ps_preview.click_close()
            self.lib.PS.ps_main_page.click_inbox()
            options = self.lib.general_helper.find(
                self.pages.PS.summary_tab.order_type_list).find_elements_by_tag_name("option")
            assert len(options) == 2, f"Count of options {self.pages.PS.summary_tab.order_type_list[2]} must bee 2"
            options_text = [i.text for i in options]
            assert "Copy" in options_text, f"Copy not in {self.pages.PS.summary_tab.order_type_list[2]}"
            assert "Certified Copy" in options_text, \
                f"Certified Copy not in {self.pages.PS.summary_tab.order_type_list[2]}"
        else:
            raise ValueError("Search failed!")

    def _precondition(self):
        self.lib.data_helper.test_config()
        self.atom.CS.api_helper.initialize_drawer()
        self.atom.CS.api_helper.create_order()
        self.lib.db_with_vpn.scheduler_job_update_for_set_export_document(self.data["test_config"]["dept_id"])


if __name__ == '__main__':
    run_test(__file__)
