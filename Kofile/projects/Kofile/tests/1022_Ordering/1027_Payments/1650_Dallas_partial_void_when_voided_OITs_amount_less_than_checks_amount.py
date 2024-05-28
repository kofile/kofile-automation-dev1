from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS, create new order with 2 OITs
    -> process order with 'Check' payment method and finalize
    -> Void order -> Edit payment methods -> One check payment method row exist, with non voided OIT amount
    -> check Balance Drawer 
    -> Balance Drawer display the final counts and amounts of Check, Total Voids amount is not changed
        """

tags = ['dallas']


class test(TestParent):                                                                             # noqa
    payment = "Check"

    def __init__(self, data):
        data["current_oit"] = data["OIT"] = "RP_Recordings"
        data["orderheader"] = "email"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to CRS
        self.atom.CRS.general.go_to_crs()
        # Get Balance Drawer data
        drawer_data = self.lib.CRS.balance_drawer.get_balance_drawer_data()
        payment_data = drawer_data[self.payment]
        payment_amount_before = float(payment_data["Expected"])
        voids_before = drawer_data["TOTAL VOIDS"]
        # Go to Orders Queue
        self.lib.CRS.crs.go_to_order_queue()
        # Add new order and process it
        self.atom.CRS.order_queue.create_and_action_with_order(None, open_crs=False,
                                                               summary=self.atom.CRS.order_entry.many_oits_to_summary)
        # Click Order Summary Checkout button
        self.lib.CRS.order_summary.click_order_summary_checkout_button()
        # Add payment
        self.atom.CRS.add_payment.add_payments(payments=self.payment)
        # Finalize
        amount_before = self.lib.CRS.add_payment.get_payment_method_amount(1)
        expected_after = amount_before / 2
        self.lib.CRS.add_payment.click_add_payment_checkout_button(expected_status=["Finalized", "Finalized"])
        # Partial Void 1-st OIT
        self.lib.CRS.order_finalization.process_void_order(void_oit=1)
        self.lib.CRS.add_payment.void_order__copy_transaction_id()
        # Finalize void, check OIT statuses and TOTAL
        self.lib.CRS.order_finalization.click_finalize_void_button(
            expected_status=["Voided", "Finalized"], expected_total=expected_after,
            trigger=self.pages.CRS.order_finalization.btn_scan_all_doc)
        # Edit order payments and check payment method 'amount' field
        self.lib.CRS.order_finalization.click_edit_order_payments()
        amount_after = self.lib.CRS.add_payment.get_payment_method_amount(1)
        assert amount_after == expected_after, f"Payment method 'amount': '{amount_after}' after partial void " \
                                               f"not equal to expected: '{expected_after}'"
        # Get Balance Drawer data
        drawer_data_after = self.lib.CRS.balance_drawer.get_balance_drawer_data()
        payment_data_after = drawer_data_after[self.payment]
        payment_amount_after = float(payment_data_after["Expected"])
        exp_payment_amount_after = round(payment_amount_before + expected_after, 2)
        voids_after = drawer_data_after["TOTAL VOIDS"]
        errors = []
        # Check Balance Drawer data after partial void
        if payment_data_after["count"] <= payment_data["count"]:
            errors.append(f"Actual '{self.payment}' count({payment_data_after['count']}) "
                          f"not increased: ({payment_data['count']})")
        if payment_amount_after != exp_payment_amount_after:
            errors.append(f"Actual '{self.payment}' amount: '{payment_amount_after}' "
                          f"not equal to expected: '{exp_payment_amount_after}'")
        if voids_before["count"] != voids_after["count"]:
            errors.append(f"'TOTAL voids' count: '{voids_before['count']}' before isn't equal to\n"
                          f"Actual 'TOTAL voids' count: '{voids_after['count']}'")
        if voids_before["Actual"] != voids_after["Actual"]:
            errors.append(f"'TOTAL voids' amount: '{voids_before['Actual']}' before isn't equal to\n"
                          f"Actual 'TOTAL voids' amount: '{voids_after['Actual']}'")
        assert not errors, errors


if __name__ == '__main__':
    run_test(__file__)
