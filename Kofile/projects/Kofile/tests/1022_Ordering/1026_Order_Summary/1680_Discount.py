"""Order Summary Test Case - Discount"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Discount"""

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: no
        Post-conditions: Order Finalization page: order price is 0$
        """
        self.lib.general_helper.check_order_type()
        # Create OIT
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        # Order Summary page
        initial_order_price = self.actions.get_element_text(self.pages.CRS.order_summary.price_by_row_index())
        # Apply 100% discount
        current_order_price = self.lib.CRS.order_summary.apply_discount(discount_type="100%",
                                                                        comment="test-comment-1")
        # Verify that order price is 0$
        self.actions.assert_equals(current_order_price, self.names.zero_price)
        # Reset Discount
        self.actions.click(self.pages.CRS.order_summary.btn_discount_reset)
        self.lib.general_helper.wait_for_spinner()
        current_order_price = self.actions.get_element_text(self.pages.CRS.order_summary.price_by_row_index())
        # Verify that order price equals initial price
        self.actions.assert_equals(current_order_price, initial_order_price)
        # Apply 100% discount
        current_order_price = self.lib.CRS.order_summary.apply_discount(discount_type="100%",
                                                                        comment="test-comment-2")
        # Verify that order price is 0$
        self.actions.assert_equals(current_order_price, self.names.zero_price)
        # Finalize order without payments
        self.actions.click(self.pages.CRS.order_summary.btn_checkout)
        self.actions.wait_for_element_displayed(self.pages.CRS.order_finalization.btn_void_order)
        current_order_price = self.actions.get_element_text(self.pages.CRS.order_summary.price_by_row_index())
        # Verify that order price is 0$
        self.actions.assert_equals(current_order_price, self.names.zero_price)


if __name__ == '__main__':
    run_test(__file__)
