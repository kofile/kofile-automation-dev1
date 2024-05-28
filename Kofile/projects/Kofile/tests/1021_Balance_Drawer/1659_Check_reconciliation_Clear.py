from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS with admin user
    -> Create and finalize order with 'Check' payment method
    -> Go to Balance Drawer > Check Reconciliation screen
    -> Select all 'deposit' radiobutton
    -> Click 'Clear' button
    -> Check radiobutton(s) and actual amount
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
        self.lib.CRS.balance_drawer.click_check_reconciliation_deposit_radiobutton()
        # Click 'Clear' and check radiobutton(s) and actual amount
        self.lib.CRS.balance_drawer.clear_check_reconciliation()


if __name__ == '__main__':
    run_test(__file__)
