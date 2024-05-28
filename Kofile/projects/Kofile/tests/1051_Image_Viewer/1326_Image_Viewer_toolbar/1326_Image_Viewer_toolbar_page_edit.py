from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
        Open CRS ->
        Scan document ->
        Make search in image viewer 1 on image ->
        Click edit page button ->
        Rotate to right and verify changes ->
        Rotate to left 2 times and verify changes ->
        Click un do page edit button and verify changes ->
        Delete first page and verify image 2 on first page 
        """

tags = ['48999_location_2']


class test(TestParent):                                                                                 # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs()

        self.lib.CRS.order_item_type.start_batch_scan()
        self.lib.CRS.capture.start_scan()
        self.lib.CRS.capture.open_image_in_image_viewer(timeout=60, retries=5)
        self.lib.image_recognition.verify_image_changes_on_viewer("1 origin")

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.icn_page_edit)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.icn_rotate_right)
        self.lib.image_recognition.verify_image_changes_on_viewer("1 rotated right")
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.icn_rotate_left)
        self.actions.wait(1)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.icn_rotate_left)
        self.lib.image_recognition.verify_image_changes_on_viewer("1 rotated left")
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.un_do_page_edit_button)
        self.lib.image_recognition.verify_image_changes_on_viewer("1 origin")

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.icn_page_edit)
        self.actions.wait(2)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.multi_selectdoc_delete_button)
        img = self.lib.general_helper.find(self.pages.CRS.image_viewer.image)
        assert "opacity: 0.4" in img.get_attribute("style"), "Page not mark to delete"
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.icn_page_edit)
        self.lib.image_recognition.verify_image_changes_on_viewer("2 origin")

        self.actions.assert_element_text(self.pages.CRS.image_viewer.lbl_total_images, "3")


if __name__ == '__main__':
    run_test(__file__)
