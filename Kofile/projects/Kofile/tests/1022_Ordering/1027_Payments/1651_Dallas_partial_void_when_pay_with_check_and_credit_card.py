from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS, create new order with 3 OITs
    -> process order with "Check" and "Credit Card" payment methods and finalize
    -> Void order -> "Check", "Credit Card", "Void Refund" must be available as payment methods
    -> choose "Credit Card" and finalize void
    -> Edit payment methods -> "Check" and "Credit Card" payment method rows exist, with non voided OIT amount
    -> check Balance Drawer 
    -> Balance Drawer display the final counts and amounts of Check/CreditCard, Total Voids amount is not changed
        """

tags = ['dallas']


class test(TestParent):                                                                               # noqa
    credit_card = 'Credit Card'
    check = "Check"
    payment = [check, credit_card]

    def __init__(self, data):
        data["current_oit"] = data["OIT"] = "RP_Recordings"
        data["orderheader"] = "email"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to CRS
        self.atom.CRS.general.go_to_crs()
        # Get Balance Drawer data
        drawer_data = self.lib.CRS.balance_drawer.get_balance_drawer_data()
        payment_data1 = drawer_data[self.payment[0]]
        payment_data2 = drawer_data[self.payment[1]]
        payment_amount1_before = float(payment_data1["Expected"])
        payment_amount2_before = float(payment_data2["Expected"])
        voids_before = drawer_data["TOTAL VOIDS"]
        # Go to Orders Queue
        self.lib.CRS.crs.go_to_order_queue()
        # Add new order and process it
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.order_item_description()
        self.atom.CRS.order_entry.fill_order_header_name()
        self.atom.CRS.order_entry.many_oits_to_summary(order_item_quantity=2)
        # Click Order Summary Checkout button
        self.lib.CRS.order_summary.click_order_summary_checkout_button()
        # Add payments
        self.atom.CRS.add_payment.add_payments(payments=self.payment)
        # Finalize
        amount = self.lib.CRS.add_payment.get_payment_method_amount(
            1) + self.lib.CRS.add_payment.get_payment_method_amount(2)
        expected_after = amount / 3 * 2
        self.lib.CRS.add_payment.click_add_payment_checkout_button(
            expected_status=["Finalized", "Finalized", "Finalized"])
        # Partial Void 1-st OIT
        self.lib.CRS.order_finalization.process_void_order(void_oit=1)
        self.lib.CRS.add_payment.void_order__copy_transaction_id(from_row=2, to_row=3)
        # Check available void payment methods
        void_payment_methods = self.lib.CRS.add_payment.get_all_payment_methods(3)
        expected_void_payment_methods = [self.check, self.credit_card, "Void Refund"]
        assert all(i in void_payment_methods for i in expected_void_payment_methods), \
            f"Actual void payment methods: '{void_payment_methods}'\n Expected: '{expected_void_payment_methods}'"
        # Edit 3-rd payment method
        self.atom.CRS.add_payment.add_payments(payments=self.credit_card, tr_id=None, comment=None, amount=None,
                                               start_from=3, edit_payment=True)
        # Finalize void, check OIT statuses and TOTAL
        self.lib.CRS.order_finalization.click_finalize_void_button(
            expected_status=["Voided", "Finalized", "Finalized"], expected_total=expected_after,
            trigger=self.pages.CRS.order_finalization.btn_scan_all_doc)
        # Edit order payments and check payment method 'amount' field
        self.lib.CRS.order_finalization.click_edit_order_payments()
        amount_after = self.lib.CRS.add_payment.get_payment_method_amount(
            1) + self.lib.CRS.add_payment.get_payment_method_amount(2)
        assert amount_after == expected_after, f"Payment method 'amount': '{amount_after}' after partial void " \
                                               f"not equal to expected: '{expected_after}'"
        # Get Balance Drawer data after partial void
        drawer_data_after = self.lib.CRS.balance_drawer.get_balance_drawer_data()
        errors = []
        # Check Balance Drawer data after partial void
        # Check - - - - -
        payment_data1_after = drawer_data_after[self.payment[0]]
        payment_amount1_after = float(payment_data1_after["Expected"])
        exp_payment_amount1_after = round(payment_amount1_before + amount / 2, 2)
        if payment_data1_after["count"] <= payment_data1["count"]:
            errors.append(f"Actual '{self.payment[0]}' count({payment_data1_after['count']}) "
                          f"not increased: ({payment_data1['count']})")
        if payment_amount1_after != exp_payment_amount1_after:
            errors.append(f"Actual '{self.payment[0]}' amount: '{payment_amount1_after}' "
                          f"not equal to expected: '{exp_payment_amount1_after}'")
        # Credit Card - - - - -
        payment_data2_after = drawer_data_after[self.payment[1]]
        payment_amount2_after = float(payment_data2_after["Expected"])
        exp_payment_amount2_after = round(payment_amount2_before + (amount / 2 - amount / 3), 2)
        if payment_data2_after["count"] <= payment_data2["count"]:
            errors.append(f"Actual '{self.payment[1]}' count({payment_data2_after['count']}) "
                          f"not increased: ({payment_data2['count']})")
        if payment_amount2_after != exp_payment_amount2_after:
            errors.append(f"Actual '{self.payment[1]}' amount: '{payment_amount2_after}' "
                          f"not equal to expected: '{exp_payment_amount2_after}'")
        # VOIDS - - - - -
        voids_after = drawer_data_after["TOTAL VOIDS"]
        if voids_before["count"] != voids_after["count"]:
            errors.append(f"'TOTAL voids' count: '{voids_before['count']}' before isn't equal to\n"
                          f"Actual 'TOTAL voids' count: '{voids_after['count']}'")
        if voids_before["Actual"] != voids_after["Actual"]:
            errors.append(f"'TOTAL voids' amount: '{voids_before['Actual']}' before isn't equal to\n"
                          f"Actual 'TOTAL voids' amount: '{voids_after['Actual']}'")
        assert not errors, errors


if __name__ == '__main__':
    run_test(__file__)
