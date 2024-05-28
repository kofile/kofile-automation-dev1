from datetime import datetime
from random import randint
from selenium.webdriver.common.keys import Keys

from projects.Kofile.Lib.test_parent import LibParent
from projects.Kofile.Lib.DB import DB


class BalanceDrawer(LibParent):
    def __init__(self):
        super(BalanceDrawer, self).__init__()

    cash_reconciliation_fields = ["pennies", "nickles", "dimes", "quarters", "onedollar", "fivedollar",
                                  "tendollar", "twentydollar", "fiftydollar", "hundreddollar"]

    def go_to_balance_drawer(self, initialize=False, user_index=0, init_amount=300):
        if initialize:
            self._api.balance_drawer(self._actions.execution.data, user_index=user_index).initialize_drawer(
                init_amount=init_amount)
        self._general_helper.find_and_click(self._pages.CRS.balance_drawer.lbl_Balance_Drawer_tab)
        self._general_helper.find(self._pages.CRS.balance_drawer.btn_settle)

    def navigate_to_balance_drawer(self):
        # CRS_functions.go_to_order_queue()
        self._actions.wait_for_element_displayed(self._pages.CRS.balance_drawer.lbl_Balance_Drawer_tab, 30)
        self._general_helper.find_and_click(self._pages.CRS.balance_drawer.lbl_Balance_Drawer_tab)
        self._general_helper.wait_for_page_load()

    def go_to_initialize_drawer(self, should_be_initialized=None):
        self._general_helper.find_and_click(self._pages.CRS.balance_drawer.lbl_initialize_Drawer_tab)
        self._general_helper.find(self._pages.CRS.balance_drawer.btn_cancel_initialize_Drawer)
        if should_be_initialized is True:
            assert self._general_helper.find(self._pages.CRS.balance_drawer.btn_submit_initialize_Drawer_disabled), \
                "Balance Drawer unexpectedly NOT initialized"
        elif should_be_initialized is False:
            assert self._general_helper.find(self._pages.CRS.balance_drawer.btn_submit_initialize_Drawer), \
                "Balance Drawer unexpectedly initialized"
        else:
            return self._general_helper.find(self._pages.CRS.balance_drawer.btn_submit_initialize_Drawer_disabled, 3,
                                             should_exist=False)

    def initialize_drawer_for_another_user(self, user_name):
        self._general_helper.find_and_click(self._pages.CRS.balance_drawer.btn_initialize_Drawer__admin_key)
        date = datetime.now().strftime("%m/%d/%Y")
        self._general_helper.find_and_send_keys(self._pages.CRS.balance_drawer.inp_recording_date, date + self._keys.TAB)
        self._general_helper.scroll_and_click(
            ("xpath", f"//label[contains({self._general_helper.x_translate(user_name.lower())})]",
             f"'{user_name}' user checkbox"))
        self.click_submit_drawer_initialization()
        self._general_helper.wait_until(lambda: "/ShowGroupDrawerInitialization" not in self._actions.get_current_url(), 45)

    def click_submit_drawer_initialization(self):
        self._actions.wait_for_element_enabled(self._pages.CRS.balance_drawer.btn_submit_initialize_Drawer)
        self._general_helper.find_and_click(self._pages.CRS.balance_drawer.btn_submit_initialize_Drawer)

    def search_closed_drawer_sessions(self):
        date = datetime.now().strftime("%m/%d/%Y")
        self._general_helper.find_and_send_keys(self._pages.CRS.balance_drawer.inp_initialize_Drawer__post_date,
                                                date).send_keys(Keys.TAB)
        self._general_helper.find_and_click(self._pages.CRS.balance_drawer.btn_initialize_Drawer__search)

    def restore_closed_drawer_session(self, user_name):
        self.search_closed_drawer_sessions()
        session = (
            "xpath",
            f"//table[@id='sessionlist']//label[contains({self._general_helper.x_translate(user_name.lower())})]",
            f"{user_name} closed session")
        if self._actions.get_browser().element_is_present(session):
            self._general_helper.find_and_click(session)
            self._general_helper.find_and_click(
                self._pages.CRS.balance_drawer.btn_initialize_Drawer__submit_posted_date)
            self._general_helper.wait_disappear_element(session)

    def click_reconciliation_button(self, payment_method="Cash"):
        suffix = f"contains(text(),'{payment_method}')" if payment_method != "Check" \
            else f"contains(text(),'{payment_method}') and not(contains(text(),'Cashiers'))"
        reconciliation = ("xpath", f"//td[contains(@class,'paymentMethodText') and {suffix}]"
                                   f"/..//following-sibling::td/a[@class='reconcilCash']",
                          f"'{payment_method}' Reconciliation button")
        self._general_helper.wait_for_page_load()
        self._general_helper.find_and_click(reconciliation)
        self._actions.wait_for_window_present_by_partial_url("econciliation")

    def click_settle_button(self):
        self._general_helper.wait_for_page_load()
        self._general_helper.scroll_and_click(self._pages.CRS.balance_drawer.btn_settle)
        self._general_helper.wait_for_spinner()
        exp_msg = "Drawer was successfully settled."
        msg = self._general_helper.find(self._pages.CRS.balance_drawer.lbl_drawer_message, get_text=True)
        assert msg == exp_msg, f"Actual message '{msg}' is not equal to expected: '{exp_msg}'"

    def click_print_drawer_summary_lnk(self, exp_msg="Success"):
        self._general_helper.wait_for_page_load()
        self._general_helper.scroll_and_click(self._pages.CRS.balance_drawer.lnk_print_drawer_sumamry)
        self._general_helper.wait_for_spinner()
        msg = self._general_helper.find(self._pages.CRS.balance_drawer.pup_success_print_drawer_summary, get_text=True)
        assert msg == exp_msg, f"Actual message '{msg}' is not equal to expected: '{exp_msg}'"

    def click_cancel_button(self):
        self._general_helper.find_and_click(self._pages.CRS.balance_drawer.btn_cancel)

    def click_submit_button(self):
        self._general_helper.find_and_click(self._pages.CRS.balance_drawer.btn_submit)

    def get_payments_with_reconciliation_button(self):
        self._general_helper.wait_for_page_load()
        all_ = self._general_helper.find_elements(self._pages.CRS.balance_drawer.lbl_payments_with_reconciliation_icons,
                                                  get_text=True)
        payments = [i.split(' (')[0] for i in all_]
        return payments

    # POST DIFFERENCE

    def click_post_difference(self, post=False, cancel=False):
        self._general_helper.scroll_and_click(self._pages.CRS.balance_drawer.lnk_post_difference)
        self._general_helper.find(self._pages.CRS.balance_drawer.pup_post_diffenece)
        if post:
            self.click_post_difference__post()
        elif cancel:
            self.click_post_difference__cancel()

    def select_post_difference_payment(self):
        self._actions.select_by_index(self._pages.CRS.balance_drawer.pup_post_difference_ddl_payment_method, 1)

    def add_post_difference_comment(self, comment):
        self._general_helper.find_and_send_keys(self._pages.CRS.balance_drawer.pup_post_difference_fld_comment, comment)

    def click_post_difference__post(self, select_payment=True, comment="Some POST DIFFERENCE comment"):
        if select_payment:
            self.select_post_difference_payment()
        if comment:
            self.add_post_difference_comment(comment)
        self._general_helper.find_and_click(self._pages.CRS.balance_drawer.pup_post_difference_btn_Post)
        self._general_helper.wait_for_spinner()
        self._actions.assert_url_contains("/ShowOrderQueue")

    def click_post_difference__cancel(self):
        self._general_helper.find_and_click(self._pages.CRS.balance_drawer.pup_post_difference_btn_cancel)
        self._general_helper.wait_disappear_element(self._pages.CRS.balance_drawer.pup_post_diffenece)

    # CASH reconciliation

    def click_submit_cash_reconciliation(self):
        self._general_helper.find_and_click(self._pages.CRS.balance_drawer.btn_cash_reconciliation_submit)

    def fill_in_cash_reconciliation_field(self, field="pennies", value=None):
        value = value if value else randint(1, 10)
        self._general_helper.find_and_send_keys(("xpath", f"//input[@name='{field}']", f"{field} field"), value)

    def get_cash_reconciliation_field_value(self, field):
        return self._general_helper.find(("xpath", f"//input[@name='{field}']/..//following-sibling::div/div",
                                          f"{field} field amount"), get_text=True)

    def get_cash_reconciliation_total_fee(self):
        return self._general_helper.find(self._pages.CRS.balance_drawer.lbl_cash_reconciliation_total_fee,
                                         get_text=True).replace('$', '')

    def get_cash_reconciliation_expected_fee(self):
        return self._general_helper.find(self._pages.CRS.balance_drawer.lbl_cash_reconciliation_expected_fee,
                                         get_text=True).replace('$',
                                                                '')

    def fill_cash_reconciliation(self, check_total=True):
        self.click_reconciliation_button(payment_method="Cash")
        total = 0
        for i in self.cash_reconciliation_fields:
            self.fill_in_cash_reconciliation_field(i)
            total += float(self.get_cash_reconciliation_field_value(i).split("$")[1])
        total = round(total, 2)
        if check_total:
            total_fee = self.get_cash_reconciliation_total_fee()
            assert float(total_fee) == total, f"Expected TOTAL fee '{total}' not equal to ACTUAL '{total_fee}'"
        return total

    def clear_cash_reconciliation(self, check_fields=True):
        self._general_helper.find_and_click(self._pages.CRS.balance_drawer.lnk_cash_reconciliation_clear)
        self._actions.wait(0.5)
        # Check fields after "Clear"
        if check_fields:
            for i in self.cash_reconciliation_fields:
                value = self.get_cash_reconciliation_field_value(i)
                assert value == '=', f"Unexpected default value '{value}' for '{i} field'"
            total_fee = self.get_cash_reconciliation_total_fee()
            assert not total_fee, f"Unexpected TOTAL fee: {total_fee}"

    # CHECK reconciliation

    def get_check_reconciliation_actual_amount(self):
        return self._general_helper.find(self._pages.CRS.balance_drawer.lbl_cheque_reconciliation_actual_amount,
                                         get_text=True).replace('$', '')

    def get_check_reconciliation_expected_amount(self):
        return self._general_helper.find(self._pages.CRS.balance_drawer.lbl_cheque_reconciliation_expected_amount,
                                         get_text=True).replace('$', '')

    def click_check_reconciliation_deposit_radiobutton(self, click_all=True):
        before = float(self.get_check_reconciliation_actual_amount())
        if click_all:
            deposit_rb = self._general_helper.find_elements(
                self._pages.CRS.balance_drawer.rdb_cheque_reconciliation_deposit)
            for i in deposit_rb:
                self._general_helper.scroll_into_view(i)
                i.click()
        else:
            self._general_helper.find_and_click(self._pages.CRS.balance_drawer.rdb_cheque_reconciliation_deposit)
        after = float(self.get_check_reconciliation_actual_amount())
        assert after > 0.00, f"Incorrect actual amount: before = '{before}'| after = '{after}'"
        return after

    def click_submit_check_reconciliation(self):
        self._general_helper.find_and_click(self._pages.CRS.balance_drawer.btn_cheque_reconciliation_submit)

    def clear_check_reconciliation(self, check_fields=True):
        self._general_helper.find_and_click(self._pages.CRS.balance_drawer.lnk_check_reconciliation_clear)
        if check_fields:
            deposit_rb = self._general_helper.find_elements(
                self._pages.CRS.balance_drawer.rdb_cheque_reconciliation_deposit)
            assert all(not (i.is_selected()) for i in deposit_rb), "Not all radiobutton cleared"
            assert self.get_check_reconciliation_actual_amount() == "0.00"

    # Balance Drawer Summary

    def get_balance_drawer_current_session_id(self):
        """Return selected session ID from dropdown list"""
        # only for ADMIN users
        return self._general_helper.find(self._pages.CRS.balance_drawer.ddl_drawer_sessions, get_attribute="value")

    def select_balance_drawer_session(self, session_id_or_user_name):
        """Select from session dropdown list by session_id or user_name"""
        self._general_helper.find_and_click(self._pages.CRS.balance_drawer.lbl_Balance_Drawer_tab)
        self._general_helper.find_and_click(self._pages.CRS.balance_drawer.ddl_drawer_sessions)
        session_el = (
            "xpath", f"(//option[contains({self._general_helper.x_translate(session_id_or_user_name)})])[last()]",
            f"Drawer session with text '{session_id_or_user_name}'")
        self._general_helper.find(session_el, get_text=True)
        self._general_helper.find_and_click(session_el)
        self._actions.wait(3)  # wait loading page

    def fill_actual_amount_from_expected(self, payment_method="Cash", expected_val=None):
        suffix = f"contains(text(),'{payment_method}')" if payment_method != "Check" \
            else f"contains(text(),'{payment_method}') and not(contains(text(),'Cashiers'))"
        prefix = f"//td[{suffix} and contains(@class,'paymentMethodText')]/following-sibling::td"
        if not expected_val:
            expected = ("xpath", f"{prefix}[@id='expectedAmount']", f"'{payment_method}' expected amount")
            expected_val = self._general_helper.find(expected, get_text=True)
        actual = ("xpath", f"{prefix}/input[contains(@data-bind, 'ActualAmount')]",
                  f"'{payment_method}' actual amount")
        self._general_helper.find_and_send_keys(actual, expected_val)

    def get_balance_drawer_data(self):
        self._actions.step("...Get Balance Drawer data...")
        """Parse Balance Drawer table data to dict like:
                          {...'Check': {'count': '9', 'Expected': '213.23', 'Actual': ''},...}"""
        if "/Balance/ShowDrawer" not in self._actions.get_current_url():
            self.go_to_balance_drawer()
        self._general_helper.wait_for_spinner()
        d_table = self._pages.CRS.balance_drawer.drawer_table_body
        d_table2 = self._pages.CRS.balance_drawer.drawer_table_footer
        p_methods = {}
        for table in [d_table, d_table2]:
            rows = self._general_helper.find_elements(table)
            for n, i in enumerate(rows, 1):
                payment = self._general_helper.find(self._general_helper.remake_locator(table, f"[{n}]/td[1]"),
                                                    get_text=True)
                if "(" in payment:
                    payment, payment_count = payment.replace(")", "").split("(")
                else:
                    payment_count = ""
                actual = self._general_helper.find(self._general_helper.remake_locator(table, f"[{n}]/td[3]/input"),
                                                   timeout=0.1, should_exist=False)
                diff = self._general_helper.find(self._general_helper.remake_locator(table, f"[{n}]/td[4]/div"),
                                                 timeout=0.1, should_exist=False)
                p_methods.update({str(payment).strip(): {"count": payment_count,
                                                         "Expected": self._general_helper.find(
                                                             self._general_helper.remake_locator(table, f"[{n}]/td[2]"),
                                                             get_text=True),
                                                         "Actual": actual.value if actual else
                                                         self._general_helper.find(
                                                             self._general_helper.remake_locator(table, f"[{n}]/td[3]"),
                                                             get_text=True),
                                                         "Difference": diff.text if diff else ""}})
        self._logging.info(f"Balance Drawer data: \n{p_methods}")
        return p_methods
