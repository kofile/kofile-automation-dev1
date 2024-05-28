from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Go to CRS, create new order -> process order with 2 payment methods 
-> delete 1 payment method and check 'Total'
-> add 1 more payment method and check 'Total'
-> finalize order
    """

tags = ['48999_location_2']


class test(TestParent):                                                                           # noqa

    def __init__(self, data):
        data["current_oit"] = data["OIT"] = "Copies"
        data["orderheader"] = "guest"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to CRS
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        # Click Order Summary Checkout button
        self.lib.CRS.order_summary.click_order_summary_checkout_button()
        # Add payments
        self.atom.CRS.add_payment.add_payments(['Cash', 'Check'])
        # Get amount from row before deletion
        amount = self.lib.CRS.add_payment.get_payment_method_amount(1)
        # Get total amount
        total = self.lib.CRS.add_payment.get_total_amount()
        # Delete 1st payment
        self.lib.CRS.add_payment.delete_payment_method(1)
        # Get total amount after deletion
        total_after = self.lib.CRS.add_payment.get_total_amount()
        exp_total = total - amount
        assert total_after == exp_total, f"Expected 'Total': '{exp_total}' after payment DELETE. " \
                                         f"Actual : '{total_after}'"
        # Add payment
        self.atom.CRS.add_payment.add_payments(amount=amount, start_from=2)
        # Get total amount after add new payment
        total2 = self.lib.CRS.add_payment.get_total_amount()
        assert total == total2, f"Expected 'Total': '{total}' after payment ADD. Actual : '{total2}'"
        # Finalize
        self.lib.CRS.add_payment.click_add_payment_checkout_button()


if __name__ == '__main__':
    run_test(__file__)
