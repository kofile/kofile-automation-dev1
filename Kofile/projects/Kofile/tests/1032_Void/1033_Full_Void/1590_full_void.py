"""smoke test"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Go to CRS, create new order, finalize the order, void order"""

tags = ["48999_location_2"]


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: no
        Post-conditions: Order is voided,  Order Finalization screen is displayed
        """
        self.data["current_oit"] = self.data.OIT
        self.lib.general_helper.check_order_type()
        # create and finalize an order
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order,
                                                               open_crs=True)
        # void the order
        self.atom.CRS.order_finalization.void_order()
        # verify order status in Order Search
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
        self.lib.CRS.order_search.verify_order_status_voided()


if __name__ == '__main__':
    run_test(__file__)
