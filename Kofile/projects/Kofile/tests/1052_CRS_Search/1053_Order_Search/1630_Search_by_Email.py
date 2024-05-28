"""Test-Search by Email"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Finalize an order and find it in Order Search by email"""

tags = ['48999_location_2']


class test(TestParent):                                                                                    # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: Order is finalized and found in Order Search
        """
        # customer email
        self.data['email'] = self.data['config'].order_header_fill(f'{self.data.orderheader}.value')

        # create order, finalize order, search order in Order Search by email (atom tests)
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        self.atom.CRS.order_search.search_orders_by_email()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data['order_number'])


if __name__ == '__main__':
    run_test(__file__)
