"""Test-Check order Queue in Order Search"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Finalize an order, find it in Order Search and check order Queue"""

tags = ['48999_location_2']


class test(TestParent):                                                                                   # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: Order is finalized and found in Order Search
        """
        self.data['current_oit'] = self.data.OIT
        # create order, finalize order, find order in Order Search (atom tests)
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
        # verify queue
        if self.data['config'].test_data(f"{self.data.OIT}.capture.step"):
            self.lib.CRS.order_search.verify_order_status_capture()
        else:
            self.lib.CRS.order_search.verify_order_status_archive()


if __name__ == '__main__':
    run_test(__file__)
