from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
                Steps:
                1. Create order and process to Verification
                2. Send order to Administrator
                3. Verify order status in Verification Queue
                4. Send order to index
                5. Check notes and edit grantor name
                6. Check grantor name in verification step
                """

tags = []  # Send back to indexing link is absent on qa-1 48999, skipped until config added


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.general_helper.check_order_type()
        # Create and Finalize order
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        if self.data["OIT"] == "RP_Recordings":
            self.atom.CRS.general.go_to_crs()
        # Capture order
        self.lib.CRS.order_item_type.capture_step()
        # Indexing Queue
        self.lib.CRS.order_item_type.indexing_step()
        # Verification Queue
        self.lib.CRS.order_item_type.index_order(self.lib.CRS.crs.go_to_verification_queue)

        self.lib.CRS.verification_entry.send_document_to_indexing(self.data["reason"])
        self.lib.CRS.verification_entry.cancel_verification(self.data["reason"], self.data["desc"])
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.order_item_type.index_order(verify_status_before="Reprocess_status",
                                                 verify_notes=self.data["reason"])

        self.lib.general_helper.find_and_send_keys(self.pages.CRS.indexing_entry.grantor_name_input,
                                                   self.data["name"])
        self.lib.CRS.order_item_type.save_order_in_index_entry()
        self.lib.CRS.order_item_type.next_order_in_index_summary()
        self.lib.CRS.order_item_type.index_order(self.lib.CRS.crs.go_to_verification_queue)
        self.actions.assert_element_value(self.pages.CRS.indexing_entry.grantor_name_input, self.data["name"])


if __name__ == '__main__':
    run_test(__file__)
