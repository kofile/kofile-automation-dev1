from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
        Open CRS ->
        Create and finalize order ->
        Scan document ->
        Make search in image viewer 1 on image ->
        Go to indexing step on this order ->
        Apply redaction on first page and get black pixel count ->
        Click restore secure document ->
        Get black pixel count and verify black pixel count < old black pixel count
        """

tags = ['48999_location_2']


class test(TestParent):                                                                                 # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        if not self.data['config'].config_file.OITs.get(self.data.OIT, {}).get("image_viewer", {}).get(
                "restore_secured_document"):
            self.logging.warning("restore secured document not configured for this tenant")
            return
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order, open_crs=True)

        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.crs.go_to_capture_queue()
        self.lib.general_helper.scroll_and_click(self.pages.CRS.capture_queue.btn_start_batch_scan)
        self.lib.CRS.capture.start_scan()
        self.lib.CRS.capture.open_image_in_image_viewer(timeout=60, retries=5)
        self.lib.image_recognition.verify_image_changes_on_viewer("1 origin")

        self.atom.CRS.capture.capture_and_map(scan=False, exp_indexing=True)
        self.lib.CRS.order_item_type.save_order_in_capture_step()
        self.lib.CRS.order_item_type.index_order()
        doc = "2 origin" if self.data['config'].test_data(f"{self.data.OIT}.indexing.first_page_to_last_page") \
            else "1 origin"
        self.lib.image_recognition.verify_image_changes_on_viewer(doc)

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.fit_height_button)
        f = self.lib.image_recognition.load_screenshot(
            self.lib.general_helper.find(self.pages.CRS.image_viewer.single_image_viewer_container))
        start_pixel_count = self.lib.image_recognition.get_black_pixel_count(f, rgb=True)
        f.close()

        self.lib.CRS.image_viewer.add_redaction("Indexing")

        second_pixel_count = 0
        for _ in range(10):
            f = self.lib.image_recognition.load_screenshot(
                self.lib.general_helper.find(self.pages.CRS.image_viewer.single_image_viewer_container))
            second_pixel_count = self.lib.image_recognition.get_black_pixel_count(f, rgb=True)
            f.close()
            if second_pixel_count > start_pixel_count + (start_pixel_count * 0.1):
                break
            self.actions.wait(3)
        second_pixel_count = second_pixel_count - (second_pixel_count * 0.1)
        assert start_pixel_count < second_pixel_count, "Redaction not added"

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.restore_secured_document_content_button)
        self.lib.general_helper.wait_for_spinner()
        self.lib.image_recognition.verify_image_changes_on_viewer(
            doc, element=self.pages.CRS.image_viewer.estamp_image_viewer_container)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.restore_secured_document_content_button)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.infobox_yes_button)
        self.lib.general_helper.wait_for_spinner()
        self.lib.image_recognition.verify_image_changes_on_viewer(doc)

        end_pixel_count = 0
        for _ in range(10):
            f = self.lib.image_recognition.load_screenshot(
                self.lib.general_helper.find(self.pages.CRS.image_viewer.single_image_viewer_container))
            end_pixel_count = self.lib.image_recognition.get_black_pixel_count(f, rgb=True)
            f.close()
            if end_pixel_count + (end_pixel_count * 0.1) < second_pixel_count:
                break
            self.actions.wait(3)

        assert end_pixel_count < second_pixel_count, "Document not restored"


if __name__ == '__main__':
    run_test(__file__)
