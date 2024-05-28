from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Log in to Clerk Search as a Clerk -> Property Records Search default page with clerk name is displayed
    Click on any multi-page image row -> Document Preview window is displayed
    Click on Add to Inbox button, select custom pages and add them to Inbox -> Item Saved Successfully message appears
    Check the pages in Inbox -> Only the selected pages out of the whole document are added to Inbox
        """

tags = ['48999_location_2']


class test(TestParent):                                                                                    # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CS.general.go_to_cs()

        # Get random doc number for OIT
        doc_num = self.api.clerc_search(self.data).get_document_number(num_of_page=2)
        # Submit document to CRS

        data = self.lib.general_helper.get_data()
        order_type = data.get("test_config").get("order_type")
        req_dept_tab = data.get("test_config").get("dept")
        self.lib.PS.ps_main_page.clear_inbox_()
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
        assert self.lib.PS.ps_main_page.is_search_successful(), "Not result in search"
        self.lib.PS.ps_main_page.click_row_with_doc_number(
            doc_num, not_in_workflow=True if order_type in ["Re-Index", "Re-Capture"] else False)
        self.lib.PS.ps_preview.click_add_to_inbox(3, "2")
        self.lib.PS.ps_preview.click_close()
        self.lib.PS.ps_main_page.click_inbox()
        self.lib.PS.ps_main_page.verify_number_of_page("2")


if __name__ == '__main__':
    run_test(__file__)
