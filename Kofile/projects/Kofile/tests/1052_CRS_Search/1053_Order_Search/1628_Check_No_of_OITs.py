"""Test-Check Number of OITs in Order Search"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Finalize an order with several OITs, find it in Order Search and 
verify number of OITs in search result"""

tags = ['48999_location_2']


class test(TestParent):                                                                                    # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: Order with several OITs is finalized and found in Order Search
        """
        # create order with several OITs, finalize order, search order in Order Search
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order,
                                                               summary=self.atom.CRS.order_entry.many_oits_to_summary)
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
        self.lib.CRS.order_search.verify_count_of_oits_by_order_number(self.data['order_number'],
                                                                       self.data['count_of_OITs'])


if __name__ == '__main__':
    run_test(__file__)
