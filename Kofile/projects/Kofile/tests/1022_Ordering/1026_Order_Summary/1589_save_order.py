"""save order from order summary test"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """From Order Summary Save Order, Verify Order status in Order Queue.
                Verify that order is found in Order Search by order number"""

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: Order Queue
        Post-conditions: Order is saved
        """
        self.data["current_oit"] = self.data.OIT
        self.lib.general_helper.check_order_type()
        # atom
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.order_summary.save_order)
        self.atom.CRS.order_queue.check_status_of_order("Save_status")
        # go to search tab
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
        # verify order status
        self.lib.CRS.order_search.verify_order_status("Save_status")


if __name__ == '__main__':
    run_test(__file__)
