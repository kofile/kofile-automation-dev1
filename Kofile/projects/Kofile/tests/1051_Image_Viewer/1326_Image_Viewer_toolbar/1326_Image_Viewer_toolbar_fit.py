from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
        Open CRS ->
        Scan document ->
        Make search in image viewer 1 on image ->
        Fit by height and check top midl pixel = white and left midl pixel = grey ->
        Fit by width and left midl pixel = white ->
        Fit by best and check top midl pixel = white and left midl pixel = grey ->
        Go to next page and check top midl pixel = white and left midl pixel = grey ->
        Change rotation and check top midl pixel = grey and left midl pixel = grey ->
        Fit by height and check top midl pixel = white and left midl pixel = grey ->
        Fit by width and left midl pixel = white
        """

tags = ['48999_location_2']


class test(TestParent):                                                                                     # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs()

        self.lib.CRS.order_item_type.start_batch_scan()
        self.lib.CRS.capture.start_scan()
        self.lib.CRS.capture.open_image_in_image_viewer(timeout=60, retries=5)
        self.lib.image_recognition.verify_image_changes_on_viewer("1 origin")

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.fit_height_button)
        self.lib.image_recognition.check_fit(pos="h")

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.fit_width_button)
        self.lib.image_recognition.check_fit(pos="w")

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.fit_best_button)
        self.lib.image_recognition.check_fit(pos="h")

        self.lib.general_helper.find_and_click(self.pages.CRS.capture_queue.pup_upload_btn_next_page)
        self.lib.image_recognition.check_fit(pos="h")
        self.lib.general_helper.find_and_click(self.pages.CRS.capture_queue.rotate_right_button)
        self.lib.image_recognition.check_fit(pos="n")

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.fit_height_button)
        self.lib.image_recognition.check_fit(pos="h")

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.fit_width_button)
        self.lib.image_recognition.check_fit(pos="w")


if __name__ == '__main__':
    run_test(__file__)
