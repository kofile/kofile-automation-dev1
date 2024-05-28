"""order status checking for crs origin"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """ Create test data, orders in order queue in re-entry statuses:
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
        # RE_ENTRY STATUS
        self.actions.step("RE_ENTRY STATUS")
        self.atom.CS.general.process_order_from_cs_to_order_summary()
        self.atom.CRS.order_summary.cancel_order()
        # go to search tab
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
        # send order back to order queue
        self.actions.click(
            self.pages.CRS.order_search.send_back_cancelled_order_by_order_number(self.data['order_number']))
        # go to order queue
        self.lib.CRS.crs.go_to_order_queue()
        # atom test
        self.atom.CRS.order_queue.check_status_of_order(status='Re_Entry')
        self.atom.CRS.order_entry.check_order_data_after_origin_search('Re_Entry')


if __name__ == '__main__':
    run_test(__file__)
