"""69698 Send Order Back to Capture from Indexing step"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
                Test cases:
                 1. Create order and process to Indexing
                 2. Send order Back to Capture from Indexing Entry page
                 3. Process order in Capture (verify 'Reprocess' status)
                 4. Process order in Indexing (verify 'Review' status)
                 5. Send order Back to Capture from Indexing Summary page
                 6. Process order in Capture (verify 'Reprocess' status)
                 7. Process order in Indexing (verify 'Review' status)
                 """

tags = ["48999_location_2"]


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: no
        Post-conditions: Order in Verification
        """
        self.lib.general_helper.check_order_type()
        # Create and Finalize order
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        if self.data["OIT"] == "RP_Recordings":
            self.atom.CRS.general.go_to_crs()
        # Capture order
        self.lib.CRS.order_item_type.capture_step()
        # Execute scheduler job: update DM_PAGE_COUNT after scan in DOC_MASTER table for order with async export
        if self.data['async'] == '1':
            self.lib.db_with_vpn.scheduler_job_update_for_export(
                scheduler_job_code="OrderItemContentExport")
        # Indexing Queue
        self.lib.CRS.order_item_type.index_order()
        # Send Back order to Capture Queue from Indexing Entry page
        self.atom.CRS.indexing.send_back_to_capture()
        # Capture Queue: Process 'Reprocess' order
        self.atom.CRS.capture.process_reprocess_order()
        # Indexing Queue: Process 'Review' order
        self.atom.CRS.indexing.process_review_order()
        # Send Back order to Capture Queue from Indexing Summary page
        self.atom.CRS.indexing.send_back_to_capture()
        # Capture Queue: Process 'Reprocess' order
        self.atom.CRS.capture.process_reprocess_order()
        # Indexing Queue: Process 'Review' order
        self.atom.CRS.indexing.process_review_order()
        self.lib.CRS.order_item_type.next_order_in_index_summary()


if __name__ == '__main__':
    run_test(__file__)
