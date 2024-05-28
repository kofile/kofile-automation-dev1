from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
        Go to CRS ->
        Workflow Order Step ->
        Workflow Capture Step ->
        Open in index ->
        Add c1 stamp and get pixel count ->
        Remove the stamp and check new pixel count < pixel count from prev step        
        """

tags = ['48999_location_2']


class test(TestParent):                                                                                     # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order, open_crs=True)
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.order_item_type.scan_and_map()
        self.lib.CRS.order_item_type.save_order_in_capture_step()
        self.lib.CRS.order_item_type.index_order()

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.fit_height_button)
        doc = "2 origin" if self.data['config'].test_data(f"{self.data.OIT}.indexing.first_page_to_last_page") \
            else "1 origin"
        self.lib.image_recognition.verify_image_changes_on_viewer(doc)

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.fit_height_button)
        find_color = (0, 0, 0, 255)

        f = self.lib.image_recognition.load_screenshot(
            self.lib.general_helper.find(self.pages.CRS.image_viewer.single_image_viewer_container))
        pixels_without_stamp = self.lib.image_recognition.get_black_pixel_count(f, rgb=True, matrix=find_color,
                                                                                not_matrix=False)
        f.close()

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.icn_C1)
        self.lib.general_helper.wait_for_spinner()

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.icn_C1)
        self.lib.general_helper.wait_for_spinner()

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.fit_height_button)
        pixels_with_stamp = self.lib.image_recognition.check_uploaded_image(
            self.pages.CRS.image_viewer.single_image_viewer_container,
            "Stamp not added", px_c=pixels_without_stamp,
            matrix=find_color, not_matrix=False)

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.eStampCancel_button)
        self.lib.general_helper.wait_for_spinner()

        self.lib.image_recognition.check_uploaded_image(self.pages.CRS.image_viewer.single_image_viewer_container,
                                                        "Stamp not removed", bigger=False, px_c=pixels_with_stamp,
                                                        matrix=find_color, not_matrix=False)


if __name__ == '__main__':
    run_test(__file__)
