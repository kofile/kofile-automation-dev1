from projects.Kofile.Lib.test_parent import TestParent

from runner import run_test

description = """Add redaction on image and check it in further steps"""

tags = ['48999_location_2']


class test(TestParent):                                                                                 # noqa

    def __init__(self, data):
        data["use_doc_type_in_api_CS"] = True
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.data_helper.test_config()
        self.data["current_oit"] = self.data.OIT

        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        # if OIT is RP, reload homepage to navigate to another tab
        if self.data["OIT"] == "RP_Recordings":
            self.atom.CRS.general.go_to_crs()

        self.lib.CRS.order_item_type.capture_step()
        original_redaction_coordinates = None

        # if OIT has indexing step, add redaction in Indexing
        if self.data['config'].test_data(f"{self.data.OIT}.indexing.step"):
            is_self = self.data['config'].test_data(f"{self.data.OIT}.indexing.indexing_type") == 'self'
            if is_self:
                self.lib.CRS.order_item_type.index_order()
                original_redaction_coordinates = self.lib.CRS.image_viewer.add_redaction("Indexing",
                                                                                         close_second_window=True)
                # verify_redaction(data, original_redaction_coordinates, last_page=True, "Indexing")
                self.lib.CRS.order_item_type.save_order_in_index_entry()
                self.lib.CRS.order_item_type.next_order_in_index_summary()

        # if OIT has verification step, verify redaction in Verification
        if original_redaction_coordinates:
            if self.data['config'].test_data(f"{self.data.OIT}.verification.step"):
                # verify the order
                self.lib.CRS.order_item_type.index_order(self.lib.CRS.crs.go_to_verification_queue)
                self.lib.CRS.image_viewer.verify_redaction(
                    self.data, original_redaction_coordinates, last_page=False, step="Verification", pixel_count=10000)
                self.lib.CRS.order_item_type.re_key_in_verification()
                self.lib.CRS.order_item_type.save_order_in_verification_entry()
                self.lib.CRS.order_item_type.next_order_in_verification_summary(open_crs_in_end=False)

            # send the document to Re-Capture and verify redaction in Re-Capture
            self.lib.CS.general.send_created_doc_to_recapture(self.data, dept_id=self.data["test_config"]["dept_id"])
            self.lib.CRS.capture.open_image_in_image_viewer()
            self.lib.CRS.image_viewer.verify_redaction(
                self.data, original_redaction_coordinates, last_page=False, step="Re-Capture", pixel_count=9000)
            self.lib.CRS.order_item_type.save_order_in_capture_step()

        else:
            self.actions.step("No redaction was added in Indexing")


if __name__ == '__main__':
    run_test(__file__)
