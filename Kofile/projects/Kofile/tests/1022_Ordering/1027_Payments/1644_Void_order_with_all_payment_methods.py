from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS, create new order 
    -> process order with all payment methods(company account available only for accounts) and finalize
    -> Void order -> Original and Voided payment methods and amounts should be the same
    -> delete one of voided payment methods -> Void Refund payment method should appear
    -> finalize void and check status
        """

tags = ['48999_location_2']


class test(TestParent):                                                                         # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to CRS
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        # Click Order Summary Checkout button
        self.lib.CRS.order_summary.click_order_summary_checkout_button()
        # Add ALL payments
        self.atom.CRS.add_payment.add_payments(payments="ALL", forbidden_payments="Company Account")
        # Finalize
        self.lib.CRS.add_payment.click_add_payment_checkout_button()
        # Void order
        self.lib.CRS.order_finalization.process_void_order()
        # Check payments and amounts
        payments = self.lib.CRS.order_finalization.void_order_payments__get_all_payment_method_names()
        pay_count = len(payments)
        self.lib.CRS.order_finalization.void_order_payments__get_all_payment_method_amounts(check_amounts=True)
        if "Void Refund" not in payments:
            orig_payments, void_payments = payments[:pay_count // 2], payments[pay_count // 2:]
            assert orig_payments == void_payments, f"Original payment methods '{orig_payments}' " \
                                                   f"not equal to void '{void_payments}'"
            # Remove last but one payment method
            self.lib.CRS.add_payment.delete_payment_method(pay_count - 1)
            # "Void Refund" should appear instead of deleted payment method
            payments = self.lib.CRS.order_finalization.void_order_payments__get_all_payment_method_names()
            assert "Void Refund" in payments, f"'Void Refund' not found in void payments table: {payments}"
            self.lib.CRS.order_finalization.void_order_payments__get_all_payment_method_amounts(check_amounts=True)
        # Fill in 'Address' fields if needed
        self.lib.CRS.order_entry.check_address_required_error(should_exist=False)
        # Finalize void
        self.lib.CRS.order_finalization.click_finalize_void_button()


if __name__ == '__main__':
    run_test(__file__)
