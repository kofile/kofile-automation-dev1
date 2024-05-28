from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
        Open CRS ->
        Scan document ->
        Make search in image viewer 1 on image ->
        Click print button ->
        Verify image 1 in printing preview window ->
        Apply printing ->
        Verify printing popup 
        """

tags = ['48999_location_2']


class test(TestParent):                                                                               # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs()

        self.lib.CRS.order_item_type.start_batch_scan()
        self.lib.CRS.capture.start_scan()
        self.lib.CRS.capture.open_image_in_image_viewer(timeout=60, retries=5)
        self.lib.image_recognition.verify_image_changes_on_viewer("1 origin")

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.btn_print_icon)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            "1 origin", element=self.pages.CRS.image_viewer.print_option_bubble_imageCont)
        self.lib.general_helper.scroll_and_click(self.pages.CRS.image_viewer.lnk_print)

        self.actions.wait_for_element_present(self.pages.CRS.image_viewer.pup_print_dialog, timeout=120)
        self.actions.assert_element_text(self.pages.CRS.image_viewer.pup_print_dialog, "Success")
        self.actions.assert_element_text(self.pages.CRS.image_viewer.print_document_success, "Print document success")
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.btn_close_pup_print)
        self.actions.wait_for_element_not_present(self.pages.CRS.image_viewer.pup_print_dialog)


if __name__ == '__main__':
    run_test(__file__)
