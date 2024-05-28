from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Create an order in CRS, finalize it, scan image in Capture step, map it to the document and save 
    -> Order is moved to Indexing step
    Index the document data and process the order to Archive -> Order is moved to Archive step
    Execute the CS export scheduler and find the document in Clerk Search 
    -> Document is found and displayed in search results
    Click on the document row and view the image in Image tab in Preview window -> 
    Document image in Clerk Search correctly displays the document image with cover page, correct number of pages, 
    recording stamps and latest image modifications (redaction, crop, rotation, page addition, custom stamps etc.)
       """

tags = []


class test(TestParent):                                                                                # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__, precondition=self._precondition)

    def __test__(self):
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.order_item_type.index_order()
        self.lib.CRS.image_viewer.rotate_image("Indexing")
        custom_stamp_text = self.data['config'].get_stamp_text(f"Stamp_text.{self.data['custom_stamp']}.value")
        self.lib.CRS.image_viewer.add_redaction("Indexing")
        self.lib.CRS.image_viewer.add_custom_stamp(self.pages.CRS.image_viewer.icn_C1, "Indexing")
        self.lib.CRS.order_item_type.save_order_in_index_entry()
        self.lib.CRS.order_item_type.next_order_in_index_summary()
        self.atom.CS.api_helper.verify_document()
        self.lib.db_with_vpn.scheduler_job_update_for_set_export_document(self.data["test_config"]["dept_id"])

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
        self.lib.CRS.image_viewer.verify_text_on_image(
            self.data, f"{self.data['doc_num']}", last_page=False, crop=True, step="CS", should_exist=True)
        self.lib.CRS.image_viewer.verify_text_on_image(self.data, custom_stamp_text, last_page=False, step="CS")
        rotation_parameters_step = self.lib.CRS.image_viewer.get_rotated_image_parameters("CS")
        _, w, h = rotation_parameters_step
        assert w > h, "Rotation Vertical, but should ben Horizontal in CS"
        # without redaction 67745 with 145646
        self.lib.CRS.image_viewer.find_redaction_on_image(self.data, False, 120000)

    def _precondition(self):
        self.lib.data_helper.test_config()
        self.atom.CS.api_helper.initialize_drawer()
        self.atom.CS.api_helper.create_order()
        self.atom.CS.api_helper.capture_document()


if __name__ == '__main__':
    run_test(__file__)
