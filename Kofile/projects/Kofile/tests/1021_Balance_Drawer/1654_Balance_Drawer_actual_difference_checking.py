from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
`Go to CRS
-> Create and finalize order with ALL payment methods
-> Go to Balance Drawer and check Difference results
-> Do Reconciliation for all payment methods and check actual and difference amount
    """

tags = ["48999_location_2"]


class test(TestParent):                                                                   # noqa
    user_index = 0

    def __init__(self, data):
        data["orderheader"] = "guest"
        data["current_oit"] = data["OIT"] = "Copies"
        super(test, self).__init__(data, __name__)

    def check_amounts(self, payment_method_list, drawer_table_data):
        errors = {}
        for p in payment_method_list:
            expected = drawer_table_data[p]["Expected"]
            actual = drawer_table_data[p]["Actual"]
            difference = drawer_table_data[p]["Difference"]
            self.logging.info({p: {"Expected": expected, "Actual": actual, "Difference": difference}})
            actual = float(drawer_table_data[p]["Actual"]) if actual else 0.0
            if round(abs(float(actual) - float(expected)), 2) != float(difference):
                errors.update({p: {"Expected": expected, "Actual": actual, "Difference": difference}})
        assert not errors, f"Wrong amount(s) found: {errors}"

    def __test__(self):
        # Go to CRS
        self.atom.CRS.general.go_to_crs(self.user_index)
        # Create and finalize order with ALL payment methods
        self.lib.CRS.crs.go_to_order_queue()
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.order_item_description()
        self.atom.CRS.order_entry.fill_order_header_name()
        self.atom.CRS.order_entry.one_oit_to_summary()
        self.lib.CRS.order_summary.click_order_summary_checkout_button()
        payment_methods = self.atom.CRS.add_payment.add_payments(payments="ALL")
        self.lib.CRS.add_payment.click_add_payment_checkout_button()
        # Get drawer data after order
        drawer_after = self.lib.CRS.balance_drawer.get_balance_drawer_data()
        # Collect and check drawer data
        self.check_amounts(payment_methods, drawer_after)

        # Do 'Reconciliation' for all payment methods
        reconciliation_icons = self.lib.CRS.balance_drawer.get_payments_with_reconciliation_button()
        payments = [i for i in payment_methods if i in reconciliation_icons]
        for i in payments:
            if i == "Cash":
                # Fill cash reconciliation fields and check total
                self.lib.CRS.balance_drawer.fill_cash_reconciliation()
            else:
                self.lib.CRS.balance_drawer.click_reconciliation_button(payment_method=i)
                # Select all deposit radiobutton
                self.lib.CRS.balance_drawer.click_check_reconciliation_deposit_radiobutton()
            self.lib.CRS.balance_drawer.click_submit_button()
            self.actions.wait_for_window_present_by_partial_url("/Balance/ShowDrawer")

        # Get drawer data
        drawer_data = self.lib.CRS.balance_drawer.get_balance_drawer_data()
        # Collect and check drawer data after reconciliation
        self.check_amounts(payments, drawer_data)


if __name__ == '__main__':
    run_test(__file__)
