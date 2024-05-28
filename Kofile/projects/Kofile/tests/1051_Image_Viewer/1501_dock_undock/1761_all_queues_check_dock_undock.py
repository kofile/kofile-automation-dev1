from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Create Order Finalize Process to Capture Queue. In Capture Summary page dock image, add redaction, undock image. Check 
Redaction available in undock mode. Process order to Indexing Step. Dock Image, check redaction exist. Undock image,
process to Verification step. Dock Image, check redaction exist. Undock image.
"""

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        original_redaction_coordinates = None

        self.lib.data_helper.test_config()
        self.data["current_oit"] = self.data.OIT

        self.lib.general_helper.check_order_type()
        # atom - create and finalize order
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        # if OIT is RP, reload the page to navigate further
        if self.data["OIT"] == "RP_Recordings":
            self.atom.CRS.general.go_to_crs()
        # if OIT has Capture step, scan and map
        if self.data['config'].test_data(f"{self.data.OIT}.capture.step"):
            self.lib.CRS.order_item_type.scan_and_map()
            self.actions.click(self.pages.CRS.capture_summary.img_capture_summary)
            self.actions.step('CAPTURE')
            # check if dock/undock mode is available
            if self.lib.general_helper.check_if_element_exists(self.pages.CRS.image_viewer.icn_dock_viewer):
                self.lib.general_helper.wait_for_spinner()
                self.actions.wait(3)
                total_images = self.actions.get_element_text(self.pages.CRS.image_viewer.lbl_total_images)
                self.lib.CRS.image_viewer.dock_image(total_images)
                original_redaction_coordinates = self.lib.CRS.image_viewer.add_redaction('Capture')
                self.lib.CRS.image_viewer.undock_image()
                if original_redaction_coordinates:
                    self.lib.CRS.image_viewer.find_redaction_on_image(self.data, False, pixel_count=2000)
                else:
                    self.actions.step("No redaction is added")
            # save the order
            self.lib.CRS.order_item_type.save_order_in_capture_step()

        # if OIT has indexing step, index
        if self.data['config'].test_data(f"{self.data.OIT}.indexing.step"):
            is_self = self.data['config'].test_data(f"{self.data.OIT}.indexing.indexing_type") == 'self'
            if is_self:
                # index the order
                self.lib.CRS.order_item_type.index_order()
                # print from image viewer in indexing entry
                self.actions.step('INDEXING')
                total_images = self.actions.get_element_text(self.pages.CRS.image_viewer.lbl_total_images)
                if self.lib.general_helper.check_if_element_exists(self.pages.CRS.image_viewer.icn_dock_viewer):
                    self.lib.CRS.image_viewer.check_dock_undock_func_with_redaction(
                        self.data, original_redaction_coordinates, total_images, pixel_count=9000)
                self.lib.CRS.order_item_type.save_order_in_index_entry()
                # print from image viewer in indexing summary
                self.actions.click(self.pages.CRS.indexing_summary.image())
                self.actions.step('INDEXING SUMMARY')
                # click next order
                self.lib.CRS.order_item_type.next_order_in_index_summary()

        # if OIT has verification step, verify
        if self.data['config'].test_data(f"{self.data.OIT}.verification.step"):
            # verify the order
            self.lib.CRS.order_item_type.index_order(self.lib.CRS.crs.go_to_verification_queue)
            self.lib.CRS.order_item_type.re_key_in_verification()
            self.actions.step('VERIFICATION ENTRY')
            total_images = self.actions.get_element_text(self.pages.CRS.image_viewer.lbl_total_images)
            if self.lib.general_helper.check_if_element_exists(self.pages.CRS.image_viewer.icn_dock_viewer):
                self.lib.CRS.image_viewer.check_dock_undock_func_with_redaction(
                    self.data, original_redaction_coordinates, total_images, pixel_count=9000)
            # save the order
            self.lib.CRS.order_item_type.save_order_in_verification_entry()
            # print from image viewer in verification summary
            self.actions.click(self.pages.CRS.verification_summary.img_table_data)
            self.actions.step('VERIFICATION SUMMARY')
            # click next order
            self.lib.CRS.order_item_type.next_order_in_verification_summary(open_crs_in_end=False)


if __name__ == '__main__':
    run_test(__file__)
