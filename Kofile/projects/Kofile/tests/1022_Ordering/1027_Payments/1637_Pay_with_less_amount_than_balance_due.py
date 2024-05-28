from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Go to CRS, create new order -> process order with 1 payment method(amount < balance due)
-> checkout button disabled
-> change amount to correct value
-> finalize order
    """

tags = ['48999_location_2']


class test(TestParent):                                                                          # noqa

    def __init__(self, data):
        data["current_oit"] = data["OIT"] = "Copies"
        data["orderheader"] = "email"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to CRS
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        # Click Order Summary Checkout button
        self.lib.CRS.order_summary.click_order_summary_checkout_button()
        # Add payment with balance_due / 2
        amount = self.lib.CRS.add_payment.get_balance_due_amount() / 2
        self.atom.CRS.add_payment.add_payments(amount=amount)
        self.lib.CRS.add_payment.check_add_payment_checkout_button(should_be_enabled=False)
        # Add correct amount
        self.atom.CRS.add_payment.add_payments()
        # Finalize
        self.lib.CRS.add_payment.click_add_payment_checkout_button()


if __name__ == '__main__':
    run_test(__file__)
