from selenium.webdriver.common.keys import Keys
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
        Open CRS ->
        Scan document ->
        Make search in image viewer 1 on image ->
        Click next page, check current page is 2 or no and make search in image viewer 2 on image ->
        Click last page, check current page is last page (4) or no and make search in image viewer 4 on image ->
        Click prev page, check current page is prev page (3) or no and make search in image viewer 3 on image ->
        Click first page, check current page is first page (1) or no and make search in image viewer 1 on image ->
        Type in page number field page 3 and pres enter, then make search in image viewer 3 on image
        """

tags = ['48999_location_2']


class test(TestParent):                                                                                   # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs()

        self.lib.CRS.order_item_type.start_batch_scan()
        self.lib.CRS.capture.start_scan()
        self.lib.CRS.capture.open_image_in_image_viewer(timeout=60, retries=5)
        self.lib.image_recognition.verify_image_changes_on_viewer("1 origin")

        image_count = self.lib.general_helper.find(self.pages.CRS.image_viewer.lbl_total_images, get_text=True)
        self.lib.general_helper.find_and_click(self.pages.CRS.capture_queue.pup_upload_btn_next_page)
        self.lib.general_helper.wait_attribute_in_element(
            self.pages.CRS.capture_queue.pup_upload_txt_current_page_number, "2")
        self.lib.image_recognition.verify_image_changes_on_viewer("2 origin")

        self.lib.general_helper.find_and_click(self.pages.CRS.capture_queue.pup_upload_btn_last_page)
        self.actions.assert_element_value(self.pages.CRS.capture_queue.pup_upload_txt_current_page_number, image_count)
        self.lib.image_recognition.verify_image_changes_on_viewer(f"{image_count} origin")

        self.lib.general_helper.find_and_click(self.pages.CRS.capture_queue.pup_upload_btn_previous_page)
        self.lib.general_helper.wait_attribute_in_element(
            self.pages.CRS.capture_queue.pup_upload_txt_current_page_number,
            str(int(image_count) - 1))
        self.lib.image_recognition.verify_image_changes_on_viewer(f"{str(int(image_count) - 1)} origin")

        self.lib.general_helper.find_and_click(self.pages.CRS.capture_queue.pup_upload_btn_first_page)
        self.actions.assert_element_value(self.pages.CRS.capture_queue.pup_upload_txt_current_page_number, "1")
        self.lib.image_recognition.verify_image_changes_on_viewer("1 origin")

        self.lib.general_helper.find_and_send_keys(self.pages.CRS.capture_queue.pup_upload_txt_current_page_number,
                                                   "3" + Keys.ENTER)
        self.lib.general_helper.wait_attribute_in_element(
            self.pages.CRS.capture_queue.pup_upload_txt_current_page_number, "3")
        self.lib.image_recognition.verify_image_changes_on_viewer("3 origin")


if __name__ == '__main__':
    run_test(__file__)
