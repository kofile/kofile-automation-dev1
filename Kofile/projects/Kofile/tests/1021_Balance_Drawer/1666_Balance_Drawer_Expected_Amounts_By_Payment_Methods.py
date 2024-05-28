from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Go to CRS -> Balance Drawer
-> Get current amounts
-> Create and finalize order with ALL payment methods
-> Go to Balance Drawer > Compare actual and expected amounts
-> Void order 
-> Go to Balance Drawer > Check total void amount
    """

tags = ["48999_location_2"]


class test(TestParent):                                                                        # noqa
    user_index = 0

    def __init__(self, data):
        data["orderheader"] = "guest"
        data["current_oit"] = data["OIT"] = "Birth_Certificate_State"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        before, after, expected = {}, {}, {}
        # Go to CRS
        self.atom.CRS.general.go_to_crs(self.user_index)
        # Go to Balance drawer and restore closed drawer session
        if not self.api.balance_drawer(self.data).unpost_drawer_session(self.user_index):
            # init drawer if closed session not found
            self.lib.CRS.balance_drawer.go_to_balance_drawer(initialize=True, user_index=self.user_index)
        # Get drawer data
        drawer_before = self.lib.CRS.balance_drawer.get_balance_drawer_data()
        # Create and finalize order with ALL payment methods
        self.lib.CRS.crs.go_to_order_queue()
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.order_item_description()
        self.atom.CRS.order_entry.fill_order_header_name()
        self.atom.CRS.order_entry.one_oit_to_summary()
        self.lib.CRS.order_summary.click_order_summary_checkout_button()
        payment_methods = self.atom.CRS.add_payment.add_payments(payments="ALL")
        change = self.lib.CRS.add_payment.get_cash_change_due_amount()
        payments = {}
        # Collect all payments: amounts
        for n, i in enumerate(payment_methods, 1):
            amount = self.lib.CRS.add_payment.get_payment_method_amount(n)
            if change and i == "Cash":
                amount = round(amount + change, 2)
            payments.update({i: amount})
        self.logging.info(f"Payments: {payments}")
        self.lib.CRS.add_payment.click_add_payment_checkout_button()
        # Get drawer data after order
        drawer_after = self.lib.CRS.balance_drawer.get_balance_drawer_data()
        # Collect and check drawer data
        for i in payment_methods:
            before.update({i: float(drawer_before[i]["Expected"])})
            after.update({i: float(drawer_after[i]["Expected"])})
            expected.update({i: round(before[i] + payments[i], 2)})
        assert after == expected, f"Actual payment amounts: '{after}'\n\t not equal to expected: '{expected}'"

        # Search and edit order
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
        self.lib.general_helper.find_and_click(self.pages.CRS.order_search.results_edit_column)
        # Click 'Yes' button in 'In Workflow' pop-up if element exists (depends on orders step) otherwise skip it
        self.lib.general_helper.find_and_click(self.pages.CRS.order_search.pup_in_workflow_btn_yes, timeout=5,
                                               should_exist=False)

        # Void order
        self.lib.CRS.order_finalization.process_void_order()
        self.lib.CRS.order_entry.check_address_required_error(should_exist=False)
        self.lib.CRS.order_finalization.click_finalize_void_button()
        # Go to Balance drawer and get drawer data
        self.lib.CRS.crs.go_to_order_queue()
        void_amount_after = float(self.lib.CRS.balance_drawer.get_balance_drawer_data()["TOTAL VOIDS"]["Actual"])
        # expected = void amount before + order amount
        expected_void_amount = round(float(drawer_before["TOTAL VOIDS"]["Actual"]) + round(sum(payments.values()), 2),
                                     2)
        assert void_amount_after == expected_void_amount, f"Actual void amount '{void_amount_after}'\n\t " \
                                                          f"not equal to expected '{expected_void_amount}'"


if __name__ == '__main__':
    run_test(__file__)
