from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    1.Open document from preconditions in CS
    2.Open document image Preview
    3.Click Thumbnail view
    4.Check first 10 or 20 images
       """

tags = ["48000"]


class test(TestParent):                                                                               # noqa
    scan_count = 4
    pages_in_pdf = 4

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

        self.actions.wait_for_element_present(self.pages.CS.main_page.multidoc_btn)
        self.lib.general_helper.find_and_click(self.pages.CS.main_page.multidoc_btn)
        self.actions.wait_for_element_present(self.pages.CS.main_page.multidoc_images)
        all_images = self.lib.general_helper.find_elements(self.pages.CS.main_page.multidoc_images)
        assert len(all_images) == self.scan_count * self.pages_in_pdf, \
            f"Thumbnail View present {len(all_images)}, but must be {self.scan_count * self.pages_in_pdf}"
        check_list = list(range(2, self.pages_in_pdf + 1)) + [1] if self.data['config'].test_data(
            f"{self.data.OIT}.indexing.first_page_to_last_page") else list(range(1, self.pages_in_pdf + 1))
        for row in range(self.scan_count):
            for a, image_position in enumerate(check_list):
                self.lib.image_recognition.verify_image_changes_on_viewer(
                    f'{image_position} origin small',
                    element=self.lib.general_helper.make_locator(self.pages.CS.main_page.multidoc_image,
                                                                 row + 1, a + 1), click_fit=False)

    def _precondition(self):
        self.lib.data_helper.test_config()
        self.atom.CS.api_helper.initialize_drawer()
        self.atom.CS.api_helper.create_order()
        self.atom.CS.api_helper.capture_document(self.scan_count)
        self.atom.CS.api_helper.index_document()
        self.atom.CS.api_helper.verify_document()
        self.lib.db_with_vpn.scheduler_job_update_for_set_export_document(self.data["test_config"]["dept_id"])


if __name__ == '__main__':
    run_test(__file__)
