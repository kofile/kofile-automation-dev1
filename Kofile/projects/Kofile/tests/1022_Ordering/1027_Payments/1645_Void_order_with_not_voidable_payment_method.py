from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Navigate to DB and update IS_VOIDABLE flag to 0 for payment method
    Go to CRS, create new order -> process order with payment method and finalize
    -> Void order and check error message
        """

tags = ['48999_location_2']


class test(TestParent):                                                                             # noqa

    def __init__(self, data):
        data["current_oit"] = data["OIT"]
        super(test, self).__init__(data, __name__)

    def __test__(self):
        payment_method = self.data["payment_method"]
        # TODO: Navigate to DB and update IS_VOIDABLE flag to 0 for payment method
        # Go to CRS
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        # Click Order Summary Checkout button
        self.lib.CRS.order_summary.click_order_summary_checkout_button()
        # Add payments
        self.atom.CRS.add_payment.add_payments(payments=payment_method)
        # Finalize
        self.lib.CRS.add_payment.click_add_payment_checkout_button()
        # Void order - "Order cannot be voided..." error message should appear
        # TODO Uncomment after DB methods added
        # ProcessOrder().click_void_order_button(voidable=False)


if __name__ == '__main__':
    run_test(__file__)
