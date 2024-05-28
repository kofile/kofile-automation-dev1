from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS with admin user
    -> Create and finalize order with 'Check' payment method
    -> Go to Balance Drawer > Check Reconciliation screen
    -> Select all 'deposit' radiobutton
    -> Click 'Submit' button
    -> Check actual amount in Drawer Summary page
        """

tags = ["48999_location_2"]


class test(TestParent):                                                                  # noqa

    def __init__(self, data):
        data["current_oit"] = data["OIT"] = "Copies"
        data["orderheader"] = "guest"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to CRS
        self.atom.CRS.general.go_to_crs()
        # Add new order and process it
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.order_item_description()
        self.atom.CRS.order_entry.fill_order_header_name()
        self.atom.CRS.order_entry.one_oit_to_summary()
        # Finalize order
        self.lib.CRS.order_summary.click_order_summary_checkout_button()
        self.atom.CRS.add_payment.add_payments(payments="Check")
        self.lib.CRS.add_payment.click_add_payment_checkout_button()
        # Go to Balance drawer
        self.lib.CRS.balance_drawer.go_to_balance_drawer()
        # Select all deposit radiobutton and check actual amount
        self.lib.CRS.balance_drawer.click_reconciliation_button("Check")
        actual_amount = self.lib.CRS.balance_drawer.click_check_reconciliation_deposit_radiobutton()
        # Click 'Submit'
        self.lib.CRS.balance_drawer.click_submit_check_reconciliation()
        # Get check actual amount from Drawer Summary and compare with actual amount from reconciliation screen
        actual = float(self.lib.CRS.balance_drawer.get_balance_drawer_data()["Check"]["Actual"])
        assert actual_amount == actual, f"Actual CHECK amount '{actual}' in Drawer Summary screen not equal to " \
                                        f"actual CHECK amount '{actual_amount}' in reconciliation screen"


if __name__ == '__main__':
    run_test(__file__)
