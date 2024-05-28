from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test
from datetime import datetime

description = """
    Create an order in CRS, finalize it, scan image in Capture step, map it to the document and save 
    -> Order is moved to Indexing step
    Index the document data and process the order to Archive -> Order is moved to Archive step
    Execute the CS export scheduler and find the document in Clerk Search 
    -> Document is found and displayed in search results
    Click on the document row and view the indexing data in Summary tab in Preview window 
    -> Summary tab correctly displays the data indexed in Indexing step
       """

tags = []


class test(TestParent):                                                                                   # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__, precondition=self._precondition)

    def __test__(self):
        self.atom.CS.general.go_to_cs()

        order_type = self.data.get("test_config").get("order_type")
        req_dept_tab = self.data.get("test_config").get("dept")
        doc_num = self.data.get("doc_num")
        doc_year = self.data.get("doc_year")
        # dept list
        self.lib.PS.ps_main_page.click_on_department_tab(req_dept_tab)
        # enter doc number to search field
        self.lib.PS.ps_main_page.search_field(doc_num)
        # narrow search
        self.lib.PS.ps_main_page.click_more_options_button()
        # set recorded date range 'to' date
        self.lib.PS.ps_main_page.date_to_set(req_dept_tab)
        if "Doc#" in self.lib.PS.ps_main_page.get_checkbox_names():
            self.lib.PS.ps_main_page.click_checkbox("Doc#")
        self.lib.PS.ps_main_page.click_search_button()
        assert self.lib.PS.ps_main_page.is_search_successful(), "No search result"
        self.lib.PS.ps_main_page.click_row_with_doc_number(
            f"{doc_year}-{doc_num}", not_in_workflow=True if order_type in ["Re-Index", "Re-Capture"] else False)
        self.lib.PS.ps_preview.click_tab("Summary")
        self.lib.PS.ps_summary_tab.document_preview_summary()
        assert self.data["prev_sum"]["doc_number"] == doc_num, "Different doc number in summery"
        assert datetime.now().strftime("%m/%d/%Y") in self.data["prev_sum"]["rec_datetime"], "Different date in summery"


    def _precondition(self):
        self.lib.data_helper.test_config()
        self.atom.CS.api_helper.initialize_drawer()
        self.atom.CS.api_helper.create_order()
        self.atom.CS.api_helper.capture_document()
        self.atom.CS.api_helper.index_document()
        self.atom.CS.api_helper.verify_document()
        self.lib.db_with_vpn.scheduler_job_update_for_set_export_document(self.data["test_config"]["dept_id"])

if __name__ == '__main__':
    run_test(__file__)
