from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
        Open CRS ->
        Scan document ->
        Make search in image viewer 1 on image ->
        
        """

tags = []


class test(TestParent):                                                                               # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order,
                                                               open_crs=True)

        self.lib.general_helper.find_and_click(self.pages.CRS.order_finalization.btn_scan_all_doc)
        self.lib.CRS.capture.start_scan()
        self.lib.CRS.capture.open_image_in_image_viewer(timeout=60, retries=5)
        self.lib.image_recognition.verify_image_changes_on_viewer("1 origin")

        self.atom.CRS.capture.capture_and_map(scan=False, exp_indexing=False)

        self.actions.wait_for_element_enabled(self.pages.CRS.capture_summary.btn_save_and_exit)
        self.lib.general_helper.scroll_and_click(self.pages.CRS.capture_summary.btn_save_and_exit)
        self.lib.general_helper.wait_for_spinner()
        self.actions.wait_for_element_present(self.pages.CRS.image_viewer.first_oit_on_show_order_finalization)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.first_oit_on_show_order_finalization)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            "2 origin" if self.data['config'].test_data(f"{self.data.OIT}.indexing.first_page_to_last_page")
            else "1 origin")

        # TODO To be completed when 78682 is fixed


if __name__ == '__main__':
    run_test(__file__)
