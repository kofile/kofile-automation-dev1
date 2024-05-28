from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Go to CRS, create new order -> process order -> finalize order with comment with special symbols
Edit order payments and check comment"""

tags = ['48999_location_2']


class test(TestParent):                                                                               # noqa
    payment_comment = "This is comment with few symbols( AaZz09().,$&'\\|/+@:?%-) for test"

    def __init__(self, data):
        data["current_oit"] = data["OIT"] = "Copies"
        data["orderheader"] = "account"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to CRS
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        # Finalize order with custom comment
        self.lib.CRS.order_summary.click_order_summary_checkout_button()
        self.atom.CRS.add_payment.add_payments(comment=self.payment_comment)
        self.lib.CRS.add_payment.click_add_payment_checkout_button()
        # Edit order payments and check 'comment' and 'amount' fields
        self.lib.CRS.order_finalization.click_edit_order_payments()
        balance_due = self.lib.CRS.add_payment.get_balance_due_amount()
        amount = self.lib.CRS.add_payment.get_payment_method_amount(1)
        comment = self.lib.CRS.add_payment.get_payment_method_comment(1)
        assert self.payment_comment == comment, f"Expected comment '{self.payment_comment}' isn't " \
                                                f"equal to actual: '{comment}'"
        assert amount == balance_due, f"Balance due '{balance_due}' isn't equal payment amount: '{amount}'"


if __name__ == '__main__':
    run_test(__file__)
