from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Go to CRS -> Balance Drawer
-> Delete drawer session
-> Init drawer with 20$ Cash
-> Get current amounts >
        Over/Short = 20
        Deposit = 20
        Beginning Balance = -20
        Actual Balance = -20
        TOTAL CASH - 0
        TOTAL NON-CASH = 0
-> Create and finalize order with X cash and Y non-cash payment methods
-> Go to Balance Drawer > Compare actual and expected amounts >
        Over/Short = 20+X+Y
        Deposit = 20+X+Y
        Beginning Balance = -20
        Actual Balance = -20
        TOTAL CASH = X
        TOTAL NON-CASH = Y
-> Void order 
-> Go to Balance Drawer > Check total void amount
    """

tags = ["48999_location_2"]


class test(TestParent):                                                                     # noqa
    payment_methods = ["Cash", "Check"]
    user_index = 0
    init_balance = 20

    def __init__(self, data):
        data["orderheader"] = "guest"
        data["current_oit"] = data["OIT"] = "RP_Recordings"
        super(test, self).__init__(data, __name__)

    @staticmethod
    def check_values(drawer_table_data, init_amount, cash=0, non_cash=0):
        errors = []
        wire_transfer = float(drawer_table_data.get("Wire Transfer", {}).get("Expected", 0))
        over_short = float(drawer_table_data["Over/Short"]["Expected"])
        deposit = float(drawer_table_data["Deposit"]["Expected"])
        beg_balance = float(drawer_table_data["Beginning Balance"]["Expected"])
        act_balance = float(drawer_table_data["Actual Balance"]["Actual"])
        t_cash = float(drawer_table_data["TOTAL CASH"]["Expected"])
        t_non_cash = float(drawer_table_data["TOTAL NON-CASH"]["Expected"])

        if act_balance != beg_balance != float(init_amount):
            errors.append("Incorrect Actual/Beginning balance values!")
        os_dep_expected = round(wire_transfer + init_amount + float(cash) + float(non_cash), 2)
        if over_short != deposit != os_dep_expected:
            errors.append("Incorrect 'Over/Short'/'Deposit' values!")
        if t_cash == round(float(init_amount) + float(cash), 2):
            errors.append("Incorrect 'TOTAL CASH' values!")
        if t_non_cash != float(non_cash):
            errors.append("Incorrect 'TOTAL NON-CASH' values!")
        if errors:
            errors.append(f"Init balance: '{init_amount}', cash: '{cash}', non-cash: '{non_cash}'"
                          f"\n{drawer_table_data}")
            assert not errors, errors

    def __test__(self):

        # Go to CRS
        self.atom.CRS.general.go_to_crs(self.user_index)

        # Delete drawer session and init with 20$
        self.lib.db_with_vpn.delete_drawer_session(
            drawer_id=self.api.balance_drawer(self.data, self.user_index).get_drawer_id())
        self.lib.CRS.balance_drawer.go_to_balance_drawer(initialize=True, user_index=self.user_index,
                                                     init_amount=self.init_balance)
        self.lib.CRS.balance_drawer.fill_actual_amount_from_expected("Cash")
        self.actions.wait(1)

        # Check drawer data
        drawer_before = self.lib.CRS.balance_drawer.get_balance_drawer_data()
        self.logging.info("Check drawer data after initialization")
        self.check_values(drawer_before, self.init_balance)

        # Create and finalize order with cash and non-cash payment methods
        self.lib.CRS.crs.go_to_order_queue()
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.order_item_description()
        self.atom.CRS.order_entry.fill_order_header_name()
        self.atom.CRS.order_entry.one_oit_to_summary()
        self.lib.CRS.order_summary.click_order_summary_checkout_button()
        self.atom.CRS.add_payment.add_payments(payments=self.payment_methods)
        change = self.lib.CRS.add_payment.get_cash_change_due_amount()
        payments = {}
        # Collect all payments amounts
        for n, i in enumerate(self.payment_methods, 1):
            amount = self.lib.CRS.add_payment.get_payment_method_amount(n)
            if change and i == "Cash":
                amount = round(amount + change, 2)
            payments.update({i: amount})
        self.logging.info(f"Payments: {payments}")
        self.lib.CRS.add_payment.click_add_payment_checkout_button()

        # Back to CRS
        self.atom.CRS.general.go_to_crs(self.user_index)
        # Check drawer data after order
        self.lib.CRS.balance_drawer.go_to_balance_drawer()
        for i in self.payment_methods:
            self.lib.CRS.balance_drawer.fill_actual_amount_from_expected(i)
        self.actions.wait(1)
        drawer_after = self.lib.CRS.balance_drawer.get_balance_drawer_data()
        self.logging.info("Check drawer data after order finalization")
        self.check_values(drawer_after, self.init_balance, payments[self.payment_methods[0]],
                          payments[self.payment_methods[1]])

        # Search and edit order
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
        self.lib.general_helper.find_and_click(self.pages.CRS.order_search.results_edit_column)
        self.lib.general_helper.find_and_click(self.pages.CRS.order_search.pup_in_workflow_btn_yes, should_exist=False, timeout=3)
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
