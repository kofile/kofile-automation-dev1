from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
                Steps:
                1. Create order with multiple oit and process to Verification
                2. Send order to Administrator
                3. Mark doc #2 as send to index and send order to index
                4. Check notes and edit grantor name
                5. Check grantor name on verification step in document #2
                """

tags = []  # Send back to indexing link is absent on qa-1 48999, skipped until config added


class test(TestParent):

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        oi_count = int(self.data["oi_count"])
        self.lib.general_helper.check_order_type()
        # Create and Finalize order
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order,
                                                               oi_count=oi_count)
        if self.data["OIT"] == "RP_Recordings":
            self.atom.CRS.general.go_to_crs()
        # Capture order
        self.lib.CRS.order_item_type.capture_step(oi_count=oi_count)
        # Indexing Queue
        self.lib.CRS.order_item_type.index_order()
        old_url = self.actions.get_current_url()
        for _ in range(oi_count)[:-1]:
            self.lib.general_helper.find_and_click(self.pages.CRS.indexing_entry.btn_save_and_advance)
            self.lib.general_helper.wait_url_change(old_url)
            old_url = self.actions.get_current_url()
        self.lib.CRS.order_item_type.save_order_in_index_entry()
        self.lib.CRS.order_item_type.next_order_in_index_summary()

        # Verification Queue
        self.lib.CRS.order_item_type.index_order(self.lib.CRS.crs.go_to_verification_queue)

        old_url = self.actions.get_current_url()
        self.lib.general_helper.find_and_click(self.pages.CRS.indexing_entry.next_doc_link)
        self.lib.general_helper.wait_url_change(old_url)

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
        self.actions.assert_element_value_is_not(self.pages.CRS.indexing_entry.grantor_name_input,
                                                 self.data["name"])
        self.lib.general_helper.find_and_click(self.pages.CRS.indexing_entry.next_doc_link)
        self.lib.general_helper.wait_url_change(old_url)
        self.actions.wait_for_element_present(self.pages.CRS.indexing_entry.grantor_name_input)
        self.actions.assert_element_value(self.pages.CRS.indexing_entry.grantor_name_input, self.data["name"])


if __name__ == '__main__':
    run_test(__file__)
