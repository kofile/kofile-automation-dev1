from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Go to CRS, create new order -> process order with ALL payment methods 
-> check fee grid
-> finalize order and check status
    """

tags = ['48999_location_2']


class test(TestParent):                                                                             # noqa

    def __init__(self, data):
        data["current_oit"] = data["OIT"] = "Copies"
        data["orderheader"] = "email"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to CRS
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        # Click Order Summary Checkout button
        self.lib.CRS.order_summary.click_order_summary_checkout_button()
        # Add ALL available payments and checkout
        all_payments = self.atom.CRS.add_payment.add_payments(payments="ALL")
        # Get amount from all rows
        amount = 0.0
        for n, i in enumerate(all_payments, 1):
            amount += self.lib.CRS.add_payment.get_payment_method_amount(n)
        amount = round(amount, 2)
        # Get total amount
        total = self.lib.CRS.add_payment.get_total_amount()
        assert total == amount, f"Payments 'amount': '{amount}' not equal to 'Total' : '{total}'"
        # Finalize and check status
        self.lib.CRS.add_payment.click_add_payment_checkout_button()


if __name__ == '__main__':
    run_test(__file__)
