"""order status checking for crs origin"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Create test data, orders in order queue in suspended statuses:
                From Order Queue Click Running man next to each order, edit order and save. 
                Navigate to any queue then back to order queue
                Verify that order in status "In Process" and assigned to the Clerk"""

tags = ['48999_location_2']


class test(TestParent):                                                                          # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # assign our data file object to data['config']
        self.data["current_oit"] = self.data.OIT
        # atom
        self.actions.step("SUSPENDED STATUS")
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.order_summary.save_order)

        # go to order queue
        self.lib.CRS.crs.go_to_order_queue()
        # atom test
        self.atom.CRS.order_queue.check_status_of_order(status='Save_status')
        self.lib.CRS.order_queue.check_order_after_switching_between_queues()


if __name__ == '__main__':
    run_test(__file__)
