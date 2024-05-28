"""Test-Add Attachment via Scan"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Add a scanned attachment to OI on Order Summary step and 
                 check the presence of attachment in Indexing and Verification"""

tags = ['48999_location_2']


class test(TestParent):                                                                         # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.order_queue.create_and_action_with_order(action=None)
        filename = self.lib.CRS.order_summary.scan_attachment()
        self.atom.CRS.add_payment.finalize_order()
        self.lib.CRS.order_item_type.capture_step()
        self.lib.CRS.order_item_type.index_order()
        self.lib.CRS.indexing_entry.verify_attachment(filename)
        self.lib.CRS.order_item_type.save_order_in_index_entry()
        self.lib.CRS.order_item_type.next_order_in_index_summary()
        self.lib.CRS.crs.go_to_verification_queue()
        self.atom.CRS.order_queue.assign_order()
        self.lib.CRS.crs.click_running_man()
        self.lib.CRS.indexing_entry.verify_attachment(filename)


if __name__ == '__main__':
    run_test(__file__)
