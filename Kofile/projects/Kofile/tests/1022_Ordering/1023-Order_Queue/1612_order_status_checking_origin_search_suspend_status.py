"""order status checking for crs origin"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """ Create test data, orders in order queue in suspended statuses:
                Origin Search
                From Order Queue Click Running man next to each order, edit order and save.
                Navigate to any queue then back to order queue
                Verify that order in status "In Process" and assigned to the Clerk"""

tags = ['48999_location_2']


class test(TestParent):                                                                             # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.data["current_oit"] = self.data.OIT
        #  SUSPENDED STATUS
        self.actions.step("SUSPENDED STATUS")
        self.atom.CS.general.process_order_from_cs_to_order_summary()
        # atom test
        self.atom.CRS.order_summary.save_order()
        # go to order queue
        self.lib.CRS.crs.go_to_order_queue()
        # atom test
        self.atom.CRS.order_queue.check_status_of_order(status='Save_status')
        self.atom.CRS.order_entry.check_order_data_after_origin_search('Pending')


if __name__ == '__main__':
    run_test(__file__)
