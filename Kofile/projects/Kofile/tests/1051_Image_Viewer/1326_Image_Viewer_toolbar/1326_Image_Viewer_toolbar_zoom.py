from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
        Open CRS ->
        Scan document ->
        Make search in image viewer 1 on image ->
        Fix black pixel count ->
        Click zoom in image and check black pixel count > before zoom ->
        Click zoom in second time image and check black pixel count > before zoom ->
        Click zoom out image 3 times and check black pixel count < start black pixel count ->
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
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.fit_height_button)
        self.actions.wait(2)
        self.lib.image_recognition.verify_image_changes_on_viewer("1 origin")

        f = self.lib.image_recognition.load_screenshot(
            self.lib.general_helper.find(self.pages.CRS.image_viewer.single_image_viewer_container))
        start_pixel_count = self.lib.image_recognition.get_black_pixel_count(f, rgb=True)
        f.close()

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.zoom_in_button)
        self.actions.wait(1)
        f = self.lib.image_recognition.load_screenshot(
            self.lib.general_helper.find(self.pages.CRS.image_viewer.single_image_viewer_container))
        pixel_count_after_first_zoom_in = self.lib.image_recognition.get_black_pixel_count(f, rgb=True)
        f.close()
        assert pixel_count_after_first_zoom_in > start_pixel_count, "Zoom in no zoom image"

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.zoom_in_button)
        self.actions.wait(1)
        f = self.lib.image_recognition.load_screenshot(
            self.lib.general_helper.find(self.pages.CRS.image_viewer.single_image_viewer_container))
        pixel_count_after_second_zoom_in = self.lib.image_recognition.get_black_pixel_count(f, rgb=True)
        f.close()
        assert pixel_count_after_second_zoom_in > pixel_count_after_first_zoom_in, "Zoom in no zoom image second time"

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.zoom_out_button)
        self.actions.wait(1)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.zoom_out_button)
        self.actions.wait(1)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.zoom_out_button)
        self.actions.wait(1)
        f = self.lib.image_recognition.load_screenshot(
            self.lib.general_helper.find(self.pages.CRS.image_viewer.single_image_viewer_container))
        pixel_count_after_zoom_out_twice = self.lib.image_recognition.get_black_pixel_count(f, rgb=True)
        f.close()
        self.actions.step(f"ZOOMS {pixel_count_after_zoom_out_twice} {start_pixel_count}")
        assert pixel_count_after_zoom_out_twice < start_pixel_count, "Zoom out no zoom image to start size"


if __name__ == '__main__':
    run_test(__file__)
