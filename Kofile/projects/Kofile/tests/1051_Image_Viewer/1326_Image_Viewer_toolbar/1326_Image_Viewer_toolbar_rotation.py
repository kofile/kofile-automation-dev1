from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
        Open CRS ->
        Scan document ->
        Make search in image viewer 1 on image ->
        Click rotate left image and make search rotated 1 in image viewer ->
        Click rotate right image and make search origin 1 in image viewer
        Click next page, check current page is 2 or no and make search in image viewer 2 on image ->
        Click rotate right image and make search rotated 2 in image viewer - >
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

        self.lib.general_helper.find_and_click(self.pages.CRS.capture_queue.rotate_left_button)
        self.lib.image_recognition.verify_image_changes_on_viewer("1 rotated left")
        self.lib.general_helper.find_and_click(self.pages.CRS.capture_queue.rotate_right_button)
        self.lib.image_recognition.verify_image_changes_on_viewer("1 origin")

        self.lib.general_helper.find_and_click(self.pages.CRS.capture_queue.pup_upload_btn_next_page)
        self.lib.general_helper.wait_attribute_in_element(
            self.pages.CRS.capture_queue.pup_upload_txt_current_page_number, "2")
        self.lib.image_recognition.verify_image_changes_on_viewer("2 origin")
        self.lib.general_helper.find_and_click(self.pages.CRS.capture_queue.rotate_right_button)
        self.lib.image_recognition.verify_image_changes_on_viewer("2 rotated right")
        self.lib.general_helper.find_and_click(self.pages.CRS.capture_queue.rotate_right_button)
        self.lib.image_recognition.verify_image_changes_on_viewer("2 rotated right twice")


if __name__ == '__main__':
    run_test(__file__)
