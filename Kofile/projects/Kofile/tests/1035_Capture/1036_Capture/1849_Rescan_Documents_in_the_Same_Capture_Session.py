"""79685 Rescan Documents in the Same Capture Session"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Test cases:
                 1. Create and finalize first order
                 2. Save Document Number and Order Number
                 3. Create and finalize second order
                 4. Scan document and map to the second order
                 5. Scan document, apply redaction and map to the same (second) order
                 6. Scan document and map to the same (second) order
                 7. Scan document and map to the first order
                 8. Collapse document row
                 9. Verify that Order Status is not displayed for collapsed row
                 10. Save orders
              """

tags = ["48999_location_2"]


class test(TestParent):  # noqa

    def __init__(self, data):
        self.go_to_crs = self.go_to_crs_adjusted
        super(test, self).__init__(data, __name__)

    def go_to_crs_adjusted(self):
        self.lib.general_helper.find_and_click(self.pages.CRS.order_finalization.btn_order_queue)

    def __test__(self):
        """
        Pre-conditions: no
        Post-conditions: Both orders are mapped and saved
        """
        self.lib.general_helper.check_order_type()
        # Create and finalize the first order
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        first_doc_num = self.data["doc_number"]
        first_order_num = self.data["order_number"]

        self.go_to_crs()
        # Create and finalize the second order
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order,
                                                               open_crs=False)
        self.go_to_crs()
        # Save (add) the doc number from the first order
        self.data["doc_numbers"].append(first_doc_num)
        # Navigate to Capture Queue and start scan
        self.lib.CRS.order_item_type.start_batch_scan()
        # Scan an image and map it to the second order
        self.atom.CRS.capture.capture_and_map()
        # Scan another image
        self.lib.CRS.capture.start_scan()
        self.lib.CRS.capture.open_image_in_image_viewer()
        # Apply redaction
        self.lib.CRS.image_viewer.add_redaction("Capture")
        # Map the redacted image to the same (second) order
        self.atom.CRS.capture.capture_and_map(scan=False)
        # Scan additional pages for the same order
        self.lib.CRS.capture.start_scan()
        self.lib.CRS.capture.click_edit_icon(mapped=True)
        # Calculate image count after scan
        image_count = self.lib.general_helper.find(self.pages.CRS.capture_summary.images_mapped_by_row_index(
            order_num=self.data["order_number"]), get_text=True, wait_displayed=True)
        # Update the number of pages
        self.lib.general_helper.find_and_send_keys(self.pages.CRS.capture_summary.pages_edit_mapped_by_row_index(
            order_num=self.data["order_number"]), image_count)
        self.lib.CRS.capture.click_edit_icon(mapped=True)
        self.lib.general_helper.wait_for_spinner()
        self.lib.general_helper.wait_for_spinner(spinner_in=10, spinner_out=150,
                                                 locator_spinner=self.pages.CRS.image_viewer.image_viewer_spinner[
                                                     1])
        # Close the image viewer
        self.lib.CRS.capture.open_image_in_image_viewer()
        # Scan another image and map to the first order
        self.atom.CRS.capture.capture_and_map(oit_num=2)
        # Click on the "Collapse" button
        self.lib.general_helper.find_and_click(
            self.lib.general_helper.make_locator(self.pages.CRS.capture_summary.btn_collapse, 1))
        # Verify that Order Status is not displayed for collapsed document row
        self.actions.verify_element_not_displayed(
            self.pages.CRS.capture_summary.status_mapped_by_row_index(first_order_num, row_num=1))
        # Save the orders
        self.lib.CRS.order_item_type.save_order_in_capture_step()


if __name__ == '__main__':
    run_test(__file__)
