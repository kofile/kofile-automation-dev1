from datetime import datetime
from projects.Kofile.Lib.test_parent import LibParent


class FrontOffice(LibParent):
    def __init__(self):
        super(FrontOffice, self).__init__()

    def go_to_front_office(self):
        self._general_helper.find_and_click(self._pages.CRS.general.lbl_front_office)

    def go_to_name_type_ahead(self):
        self.go_to_front_office()
        if self._general_helper.find(self._pages.CRS.front_office.lnk_menu_system, timeout=5, should_exist=False):
            self._general_helper.find_and_click(self._pages.CRS.front_office.lnk_menu_system)
        self._general_helper.find_and_click(self._pages.CRS.front_office.lnk_sub_menu_name_type_ahead)

    def go_to_order_queue(self):
        self._general_helper.scroll_and_click(self._pages.CRS.front_office.lnk_go_to_orders)

    def get_breadcrumb(self):
        return self._general_helper.find(self._pages.CRS.front_office.front_office_breadcrumb, get_text=True)

    def fill_in_account_code_field(self, code):
        self._general_helper.find_and_send_keys(self._pages.CRS.front_office.txt_ca_account_code, str(code))

    def fill_in_account_name_field(self, code):
        self._general_helper.find_and_send_keys(self._pages.CRS.front_office.txt_ca_company_account_name, str(code))

    def click_search_button(self):
        self._general_helper.find_and_click(self._pages.CRS.front_office.btn_ca_search)
        self._general_helper.find(self._pages.CRS.front_office.ca_result_table)

    def click_new_row_button(self):
        self._general_helper.find_and_click(self._pages.CRS.front_office.lnk_ca_new_row)
        self._general_helper.find(self._pages.CRS.front_office.lnk_cae_users_table_new_user)

    def fill_in_new_account_code(self, code):
        self._general_helper.find_and_send_keys(self._pages.CRS.front_office.txt_cae_account_code, code)

    def fill_in_new_account_name(self, name):
        self._general_helper.find_and_send_keys(self._pages.CRS.front_office.txt_cae_company_name, name)

    def fill_in_new_account_phone(self):
        phone_fields = self._general_helper.find_elements(self._pages.CRS.front_office.txt_cae_company_phone)
        number = ["123", "456", "7890"]
        for i, n in list(zip(phone_fields, number)):
            i.send_keys(n)
        self._general_helper.find_and_click(self._pages.CRS.front_office.txt_cae_company_name)

    def fill_in_new_account_ds_per_package(self):
        self._general_helper.find_and_click(self._pages.CRS.front_office.radio_cae_ds_per_package)

    def fill_in_new_account_ds_no_fee(self):
        self._general_helper.find_and_click(self._pages.CRS.front_office.radio_cae_ds_no_fee)

    def fill_in_new_account_nightly_export_billing(self):
        self._general_helper.select_by_text(self._pages.CRS.front_office.ddl_cae_nightly_export_billing,
                                            "No Fee")
    # --------------------
    # Company Account Users table

    def click_new_user_button(self):
        self._general_helper.scroll_and_click(self._pages.CRS.front_office.lnk_cae_users_table_new_user)

    def fill_in_new_user_email(self, email):
        self._general_helper.find_and_send_keys(self._pages.CRS.front_office.txt_new_user_email_field, email)
        self._general_helper.find_and_click(self._general_helper.remake_locator(
            self._pages.CRS.front_office.found_new_user_email, f"[text()='{email}']"))

    def enable_company_account_user(self):
        self._general_helper.scroll_and_click(self._pages.CRS.front_office.cbx_company_account_user_enable)

    def enable_all_company_account_users(self):
        self._general_helper.scroll_and_click(self._pages.CRS.front_office.txt_new_user_email_field)
        users = self._general_helper.find_elements(self._pages.CRS.front_office.cbx_company_account_user_enable)
        for i in users:
            self._actions.step("Enable company user")
            i.click()

    def make_admin_company_account_user(self):
        self._general_helper.scroll_and_click(self._pages.CRS.front_office.cbx_company_account_user_admin)

    def make_admin_all_company_account_users(self):
        self._general_helper.scroll_and_click(self._pages.CRS.front_office.txt_new_user_email_field)
        users = self._general_helper.find_elements(self._pages.CRS.front_office.cbx_company_account_user_admin)
        for i in users:
            self._actions.step("Make company user administrator")
            i.click()

    # --------------------

    def click_list_all_button(self):
        # Click 'List All'
        self._general_helper.find_and_click(self._pages.CRS.front_office.lnk_ca_list_all)
        # Wait loading
        self._general_helper.wait_for_spinner()
        self._general_helper.find(self._pages.CRS.front_office.ca_result_table)
        # Check result table header columns
        expected = ['Account Code', 'Company Name', 'Name', 'Active']
        header = self._general_helper.find_elements(self._general_helper.remake_locator(
            self._pages.CRS.front_office.ca_result_table, "/thead/tr/th"), get_text=True)       # noqa
        assert all(i in header for i in expected), \
            f"Expected result table header '{expected}' no equal to actual '{header}'"
        # Assert result table isn't empty
        result = self._general_helper.find_elements(
            self._general_helper.remake_locator(self._pages.CRS.front_office.ca_result_table, "/tbody/tr"))  # noqa
        assert result, "Result table is empty!"

    def click_reset_search_button(self):
        self._general_helper.find_and_click(self._pages.CRS.front_office.lnk_ca_reset_search)
        self._general_helper.wait_disappear_element(self._pages.CRS.front_office.ca_found_company_edit_btn)
        self._general_helper.wait_disappear_element(self._pages.CRS.front_office.ca_result_table)

    def get_found_company_names(self):
        self._general_helper.find(self._pages.CRS.front_office.ca_found_company_name)
        elements = self._general_helper.find_elements(self._pages.CRS.front_office.ca_found_company_name)
        names = [i.get_attribute("value") for i in elements]
        return names

    def get_found_company_codes(self):
        self._general_helper.find(self._pages.CRS.front_office.ca_found_company_code)
        elements = self._general_helper.find_elements(self._pages.CRS.front_office.ca_found_company_code)
        codes = [i.get_attribute("value") for i in elements]
        return codes

    def click_on_account_edit_icon(self):
        self._general_helper.find_and_click(self._pages.CRS.front_office.ca_found_company_edit_btn)
        self._general_helper.wait_for_spinner()

    def click_on_active_checkbox(self):
        self._general_helper.find_and_click(self._pages.CRS.front_office.cbx_cae_account_active)

    def click_on_allow_ordering_checkbox(self):
        self._general_helper.find_and_click(self._pages.CRS.front_office.cbx_cae_allow_ordering)

    def click_on_allow_e_recording_checkbox(self):
        self._general_helper.find_and_click(self._pages.CRS.front_office.cbx_cae_allow_erecording)

    def click_on_allow_public_search_checkbox(self):
        self._general_helper.find_and_click(self._pages.CRS.front_office.cbx_cae_allow_public_search)

    def fill_in_credit_limit(self, new_limit):
        self._general_helper.find_and_send_keys(self._pages.CRS.front_office.txt_cae_credit_limit, str(new_limit))

    def check_credit_limit(self, expected_limit):
        limit = self._general_helper.find(self._pages.CRS.front_office.txt_cae_credit_limit).value
        assert str(expected_limit) == limit, f"Actual credit limit '{limit}' not equal to expected '{expected_limit}'"

    def click_on_save_button(self):
        # 48999 contains such DDL as required
        if not self._general_helper.check_if_element_exists(self._pages.CRS.front_office.btn_cae_save_enabled, 1):
            self.fill_in_new_account_nightly_export_billing()
        self._general_helper.scroll_and_click(self._pages.CRS.front_office.btn_cae_save_enabled)
        self._general_helper.wait_disappear_element(self._pages.CRS.front_office.btn_cae_save)

    def check_breadcrumb(self, expected_breadcrumb="Company Accounts"):
        actual_breadcrumb = self.get_breadcrumb()
        assert actual_breadcrumb == expected_breadcrumb, f"Actual breadcrumb '{actual_breadcrumb}' " \
                                                         f"not equal to expected '{expected_breadcrumb}'"

    def check_company_name(self, expected_comp_name):
        actual_comp_names = self.get_found_company_names()
        assert expected_comp_name in actual_comp_names, f"Expected company name '{expected_comp_name}' " \
                                                        f"not found in list '{actual_comp_names}'"

    def check_company_code(self, expected_comp_code):
        actual_comp_names = self.get_found_company_codes()
        assert expected_comp_code in actual_comp_names, f"Expected company name '{expected_comp_code}' " \
                                                        f"not found in list '{actual_comp_names}'"

    def search_account(self, name_or_code):
        # navigate to Front Office
        self.go_to_front_office()
        # select Company Account submenu
        self._actions.click(self._pages.CRS.front_office.lnk_sub_menu_company_accounts)
        # get Breadcrumb Value
        self.check_breadcrumb()
        # Search account By account code/name
        if name_or_code.isdigit():
            self.fill_in_account_code_field(name_or_code)
        else:
            self.fill_in_account_name_field(name_or_code)
        self.click_search_button()

    def edit_account(self):
        self.search_account(self._general_helper.get_data().front_office.account_code)
        # get actual company name
        self.check_company_name(self._general_helper.get_data().front_office.company_name)
        # click on edit icon
        self.click_on_account_edit_icon()

    def choose_allow_ordering_option(self, disable=False):
        account_code = self._general_helper.get_data().front_office.account_code
        # Check 'AllowOrdering' option enabled\disabled via api
        r = self._api.front_office(self._general_helper.get_data()).get_company_account_info(account_code)
        allow_ordering = r["AllowOrdering"]
        if allow_ordering != disable:
            self._actions.step(f"Option 'AllowOrdering' is already {allow_ordering}")
            return
        # Edit account in Front Office page
        self.edit_account()
        if not disable and not (r["IsEnabled"]):
            # Enable account if needed
            self.click_on_active_checkbox()
        self.click_on_allow_ordering_checkbox()
        # save changes
        self.click_on_save_button()

    def disable_company_account(self, disable=True):
        account_code = self._general_helper.get_data().front_office.account_code
        # Check 'IsEnabled' option enabled\disabled via api
        r = self._api.front_office(self._general_helper.get_data()).get_company_account_info(account_code)
        if not (r["AllowDeactivate"]):
            raise ValueError(f"Deactivation option is not allowed for account: '{account_code}'")
        is_enabled = r["IsEnabled"]
        if is_enabled != disable:
            self._actions.step(f"Option 'IsEnabled' is already {is_enabled}")
            return
        # Edit account in Front Office page
        self.edit_account()
        self.click_on_active_checkbox()
        # save changes
        self.click_on_save_button()

    def change_credit_limit(self, data, new_limit=50, check_after_save=True):
        # Edit account in Front Office page
        self.edit_account()
        self.fill_in_credit_limit(new_limit)
        # save changes
        self.click_on_save_button()
        if check_after_save:
            self.click_reset_search_button()
            self.fill_in_account_code_field(data.front_office.account_code)
            self.click_search_button()
            self.click_on_account_edit_icon()
            self.check_credit_limit(new_limit)
            self.click_reset_search_button()

    def create_new_account(self, unique_number=None, emails=None, allow_public_search=False, credit_limit=None):
        """
        Navigate to Front Office and create new account with provided code and email(s)
        If code not provided: code will be generated automatically
        If emails not provided: users will not be added to the account
        """
        unique_number = unique_number if unique_number else datetime.now().strftime("%Y%m%d%H%M%S")
        company_name = f"Auto{unique_number}"
        # Navigate to Front Office
        self.go_to_front_office()
        # select Company Account submenu
        self._actions.click(self._pages.CRS.front_office.lnk_sub_menu_company_accounts)
        # Click New Row button
        self.click_new_row_button()
        # Fill in account data
        self.fill_in_new_account_code(unique_number)
        self.fill_in_new_account_name(company_name)
        self.fill_in_new_account_phone()
        # The Direct Submission Processing Fee doesn't appear on 48999
        # self.fill_in_new_account_ds_per_package()
        self.fill_in_new_account_nightly_export_billing()
        if self._general_helper.check_if_element_exists(
                self._pages.CRS.front_office.radio_ds_processing_fee_req_options_first):
            # Check if we have required radiobuttons configured check the first one just to enable save button
            self._general_helper.find_and_click(self._pages.CRS.front_office.radio_ds_processing_fee_req_options_first)
        if emails:
            # Activate account
            self.click_on_active_checkbox()
            self.click_on_allow_ordering_checkbox()
            self.click_on_allow_e_recording_checkbox()
            if allow_public_search:
                self.click_on_allow_public_search_checkbox()
            emails = emails if isinstance(emails, list) else [emails]
            # Add users
            for email in emails:
                self.click_new_user_button()
                self.fill_in_new_user_email(email)
            # Enable users
            self.enable_all_company_account_users()
            # Make users administrator
            self.make_admin_all_company_account_users()
        if credit_limit:
            self._general_helper.find_and_send_keys(self._pages.CRS.front_office.txt_cae_credit_limit, credit_limit)
        # Save account
        self.click_on_save_button()
        self._actions.step(f"--> Account created: '{unique_number} - {company_name}' with users: {emails}")

    def select_department(self):
        data = self._general_helper.get_data()
        self._actions.select_by_text(self._pages.CRS.front_office.ddl_nta_select_department,
                                     data.front_office.type_ahead_department)
        self._general_helper.find_and_click(self._pages.CRS.front_office.btn_nta_search)

    def enable_name_and_select_by_name(self, checked):
        data = self._general_helper.get_data()
        account_name = data.config.order_header_fill(f'{data.orderheader}.value').lower()
        self._general_helper.find_and_send_keys(self._pages.CRS.front_office.txt_nta_party_name, account_name)
        self._general_helper.find_and_check_uncheck_checkbox(
            self._pages.CRS.front_office.ddl_nta_party_name_lbl_by_name(account_name), checked)
        self._general_helper.find_and_click(self._pages.CRS.front_office.btn_nta_save)
        self._actions.wait(1)

    def go_to_workflow_dates_sub(self):
        self._general_helper.find_and_click(self._pages.CRS.front_office.lnk_menu_document)
        self._general_helper.find_and_click(self._pages.CRS.front_office.lnk_sub_menu_workflow_dates)
        self._actions.wait_for_element_present(self._pages.CRS.front_office.workflow_dates_panel)
        self._actions.wait_for_element_displayed(self._pages.CRS.front_office.workflow_dates_panel)

    def click_edit_to_row_by_department(self):
        data = self._general_helper.get_data()
        self._general_helper.find_and_click(
            self._pages.CRS.front_office.get_row_path_workflow_dates_result_table_by_department(
                data.front_office.workflow_dates_department))
        self._actions.wait_for_element_present(self._pages.CRS.front_office.txt_wde_certified_end_date)

    def set_new_certified_end_date(self, date=None):
        check_date = date if date else datetime.now().strftime("%m/%d/%Y")
        self._general_helper.find_and_send_keys(self._pages.CRS.front_office.txt_wde_certified_end_date,
                                                check_date + self._keys.TAB)
        self._general_helper.find_and_click(self._pages.CRS.front_office.btn_wde_save)
        self._actions.wait_for_element_present(self._pages.CRS.front_office.workflow_dates_panel)
        return check_date

    def set_mail_back_date_by_recorded_date(self):
        self._general_helper.find_and_click(self._pages.CRS.front_office.rdb_mail_back_date_by_recorded_date)
        self._actions.wait_for_element_present(self._pages.CRS.front_office.workflow_dates_panel_start_date)
        self._actions.wait_for_element_displayed(self._pages.CRS.front_office.workflow_dates_panel_start_date)

    def set_date_range(self):
        date = datetime.now().strftime("%m/%d/%Y")
        self._general_helper.find_and_send_keys(self._pages.CRS.front_office.workflow_dates_panel_start_date, date)
        self._general_helper.find_and_send_keys(self._pages.CRS.front_office.workflow_dates_panel_end_date,
                                                date + self._keys.TAB)
        self._general_helper.find_and_click(self._pages.CRS.front_office.workflow_dates_panel_search_button)
        self._actions.wait_for_element_present(
            self._pages.CRS.front_office.workflow_dates_panel_search_result_first_row_edit)
        self._actions.wait_for_element_displayed(
            self._pages.CRS.front_office.workflow_dates_panel_search_result_first_row_edit)

    def edit_mail_back_date(self):
        self._general_helper.find_and_click(
            self._pages.CRS.front_office.workflow_dates_panel_search_result_first_row_edit)
        self._actions.wait_for_element_present(
            self._pages.CRS.front_office.workflow_dates_panel_search_result_first_row_new_date)
        self._actions.wait_for_element_displayed(
            self._pages.CRS.front_office.workflow_dates_panel_search_result_first_row_new_date)
        new_date = datetime.now().strftime("%m/%d/%Y")
        self._general_helper.find_and_send_keys(
            self._pages.CRS.front_office.workflow_dates_panel_search_result_first_row_new_date,
            new_date + self._keys.TAB)
        self._general_helper.find_and_click(
            self._pages.CRS.front_office.workflow_dates_panel_search_result_first_row_save_new_date)
        self._general_helper.wait_for_spinner()
        self._actions.assert_element_value(
            self._pages.CRS.front_office.workflow_dates_panel_search_result_first_row_date,
            new_date)
        return self._general_helper.find(
            self._pages.CRS.front_office.workflow_dates_panel_search_result_first_row_doc_count).text

    def verify_doc_count(self, prev_count):
        self._actions.wait_for_element_present(
            self._pages.CRS.front_office.workflow_dates_panel_search_result_first_row_error)
        self._actions.wait_for_element_displayed(
            self._pages.CRS.front_office.workflow_dates_panel_search_result_first_row_error)
        self._actions.assert_element_attribute(
            self._pages.CRS.front_office.workflow_dates_panel_search_result_first_row_error,
            "title",
            "Some documents have different mail back date")
        self._actions.assert_element_text(
            self._pages.CRS.front_office.workflow_dates_panel_search_result_first_row_doc_count,
            str(int(prev_count.strip()) + 1))

    def go_to_nsf_names_submenu(self):
        self._general_helper.find_and_click(self._pages.CRS.front_office.lnk_menu_financial)
        self._general_helper.find_and_click(self._pages.CRS.front_office.lnk_sub_menu_nsf_names)
        self._actions.wait_for_element_displayed(self._pages.CRS.fo_nsf_names.nsf_names_breadcrumb)

    def create_new_nsf_name(self, new_nsf_name_values):
        """
        new_nsf_name_values: dict of key value pairs where key = field name, value = value to enter
        """
        self._general_helper.find_and_click(self._pages.CRS.fo_nsf_names.lnk_nsf_new_row)
        self._actions.wait_for_element_displayed(self._pages.CRS.fo_nsf_names.txt_nsf_name)
        for key, value in new_nsf_name_values.items():
            if key.startswith("txt_"):
                self._general_helper.find_and_send_keys(getattr(self._pages.CRS.fo_nsf_names, key), value)
            elif key.startswith("chx_") and value is True:
                self._general_helper.find_and_click(getattr(self._pages.CRS.fo_nsf_names, key))
        self._general_helper.find_and_click(self._pages.CRS.fo_nsf_names.btn_save)
        self._general_helper.wait_for_spinner()

    def search_for_nsf_name(self, nsf_name):
        self._general_helper.find_and_send_keys(self._pages.CRS.fo_nsf_names.lookup_nsf_name, str(nsf_name))
        self._general_helper.find_and_click(self._pages.CRS.fo_nsf_names.btn_search)

    def get_nsf_names_in_search_results(self):
        return self._general_helper.find_elements(self._pages.CRS.fo_nsf_names.td_nsf_names, get_attribute="value")
