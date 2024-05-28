from random import randint
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS, create new order -> process order and finalize
    -> edit order and change 'No of pages' -> confirm 'balance due' changing
    -> add new payment and checkout -> check total amount
    -> Void order and check total amount and status
        """

tags = ['48999_location_2']


class test(TestParent):

    def __init__(self, data):
        data["current_oit"] = data["OIT"] = "Copies"
        data["orderheader"] = "guest"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to CRS
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        # Click Order Summary Checkout button
        self.lib.CRS.order_summary.click_order_summary_checkout_button()
        # Add payment
        self.atom.CRS.add_payment.add_payments()
        # Finalize
        balance_due = self.lib.CRS.add_payment.get_balance_due_amount()
        self.lib.CRS.add_payment.click_add_payment_checkout_button(expected_total=balance_due)
        # Edit order, add 5 - 20 pages and save
        self.lib.CRS.order_finalization.click_edit_order(add_pages=randint(5, 20))
        # Add payment
        balance_due = self.lib.CRS.add_payment.get_balance_due_amount()
        p2_amount = balance_due - self.lib.CRS.add_payment.get_payment_method_amount(1)
        # check if Refund payment method is added as default, delete refund payment method row
        delete_row_icons = self.lib.general_helper.find_elements(self.pages.CRS.order_summary.btn_oit_delete_all)
        number_delete_row_icons = len(delete_row_icons)
        if number_delete_row_icons == 2:
            self.actions.click(delete_row_icons[-1])

        self.atom.CRS.add_payment.add_payments(start_from=2, amount=p2_amount)
        # Finalize
        self.lib.CRS.add_payment.click_add_payment_checkout_button(expected_total=balance_due)
        # Void order
        self.lib.CRS.order_finalization.process_void_order()
        self.lib.CRS.order_finalization.click_finalize_void_button(expected_total=0.00)


if __name__ == '__main__':
    run_test(__file__)
