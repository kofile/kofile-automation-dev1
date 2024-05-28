from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Go to CRS, create new order -> process order with 3 payment methods 
-> delete 3 payment method and check 'Total'
-> add 2 other payment methods and check 'Total'
-> finalize order
    """

tags = ['48999_location_2']


class test(TestParent):                                                                          # noqa

    def __init__(self, data):
        data["current_oit"] = data["OIT"] = "Copies"
        data["orderheader"] = "guest"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to CRS
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        # Click Order Summary Checkout button
        self.lib.CRS.order_summary.click_order_summary_checkout_button()
        # Get all available payment methods
        all_payments = self.lib.CRS.add_payment.get_all_payment_methods(remove_credit_card=False)
        # Add credit card if it is available for OIT, as from general function it was removed
        if "Credit Card" in self.data['config'].test_data(f"{self.data.OIT}.payment_methods"):
            all_payments.append("Credit Card")
        # Add first 3 available payments and checkout
        self.atom.CRS.add_payment.add_payments(all_payments[:3])
        self.lib.CRS.add_payment.click_add_payment_checkout_button()
        # Edit order payments
        self.lib.CRS.order_finalization.click_edit_order_payments()
        # Get amount from rows before deletion
        amount3 = self.lib.CRS.add_payment.get_payment_method_amount(3)
        amount2 = self.lib.CRS.add_payment.get_payment_method_amount(3)
        # Get total amount
        total = self.lib.CRS.add_payment.get_total_amount()
        # Delete 3rd and 2nd payments
        self.lib.CRS.add_payment.delete_payment_method(3)
        self.lib.CRS.add_payment.delete_payment_method(2)
        # Get total amount after deletion
        total_after = self.lib.CRS.add_payment.get_total_amount()
        exp_total = round(total - amount2 - amount3, 2)
        assert total_after == exp_total, f"Expected 'Total': '{exp_total}' after payment DELETE." \
                                         f" Actual : '{total_after}'"
        # Add payments with 4-th and 5-th payment methods from list
        self.atom.CRS.add_payment.add_payments([all_payments[3]], amount=amount2, start_from=2)
        self.atom.CRS.add_payment.add_payments([all_payments[4]], amount=amount3, start_from=3)
        # Get total amount after add new payments
        total += self.lib.CRS.add_payment.get_processing_fee()
        total2 = self.lib.CRS.add_payment.get_total_amount()
        assert total == total2, f"Expected 'Total': '{total}' after payment ADD. Actual : '{total2}'"
        # Finalize
        self.lib.CRS.add_payment.click_add_payment_checkout_button()


if __name__ == '__main__':
    run_test(__file__)
