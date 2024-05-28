"""Test-Search by Account Code and Name"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Finalize an order and find it in Order Search by account code/name"""

tags = ['48999_location_2']


class test(TestParent):                                                                                    # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: Order is finalized and found in Order Search
        """
        # customer account code
        account_tokens = self.data['config'].order_header_fill(f'{self.data.orderheader}.value').split()
        self.data['account_code'] = account_tokens[0]
        # create order, finalize order, search order in Order Search by account code
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        self.atom.CRS.order_search.search_orders_by_account_code()
        self.lib.CRS.order_search.verify_customer_by_order_number(self.data['order_number'], self.data['account_code'])
        # search order by name
        self.data['name'] = self.data['account_code']
        self.atom.CRS.order_search.search_orders_by_name()
        self.lib.CRS.order_search.verify_customer_by_order_number(self.data['order_number'], self.data['name'])


if __name__ == '__main__':
    run_test(__file__)
