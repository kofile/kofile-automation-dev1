"""69867_Return_to_Verification_Queue"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
                Steps:
                1. Create order and process to Verification
                2. Return order to Verification Queue
                3. Verify order status in Verification Queue
                """

tags = ["48999_location_2"]


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: no
        Post-conditions: Order in Verification Queue with status 'In Process'
        """
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
        self.lib.CRS.order_item_type.re_key_in_verification()
        self.lib.CRS.order_item_type.save_order_in_verification_entry()
        # Return Order to Verification Queue
        self.atom.CRS.verification.return_to_verification_queue()


if __name__ == '__main__':
    run_test(__file__)
