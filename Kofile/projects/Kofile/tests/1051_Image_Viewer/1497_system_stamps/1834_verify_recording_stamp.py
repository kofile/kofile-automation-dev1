from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Add customer stamp to image and check it in further steps"""

tags = ['48999_location_2']


class test(TestParent):                                                                                # noqa

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

        # if OIT has indexing step, add stamp in Indexing
        if self.data['config'].test_data(f"{self.data.OIT}.indexing.step") and \
                self.data['config'].test_data(f"{self.data.OIT}.indexing.indexing_type") == 'self':
            # index the order
            self.lib.CRS.order_item_type.index_order()
            self.lib.CRS.image_viewer.verify_text_on_image(self.data, f"{self.data['doc_number']}", last_page=False,
                                                           crop=True, step="Indexing")
            self.lib.CRS.order_item_type.save_order_in_index_entry()
            self.lib.CRS.order_item_type.next_order_in_index_summary()

        # if OIT has verification step, verify stamp in Verification
        self.lib.CRS.order_item_type.verification_step()

        # send the document to Re-Capture and verify stamp in Re-Capture
        self.lib.CS.general.send_created_doc_to_recapture(self.data, dept_id=self.data["test_config"]["dept_id"])
        self.lib.CRS.capture.open_image_in_image_viewer()
        self.lib.CRS.image_viewer.verify_text_on_image(self.data, f"{self.data['doc_number']}", last_page=False,
                                                       crop=True, step="Re-Capture", should_exist=False)
        self.lib.CRS.order_item_type.save_order_in_capture_step()


if __name__ == '__main__':
    run_test(__file__)
