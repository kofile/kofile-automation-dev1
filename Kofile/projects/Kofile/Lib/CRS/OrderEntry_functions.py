from datetime import datetime
from random import randint
from golem.webdriver.extended_webelement import Select
from selenium.common.exceptions import StaleElementReferenceException
from projects.Kofile.Lib.CRS.CRS_functions import CRS
from projects.Kofile.Lib.CRS.OrderHeader_functions import OrderHeader
from projects.Kofile.Lib.Required_fields import RequiredFields
from projects.Kofile.Lib.test_parent import LibParent
from os.path import join, isfile
import time

CRS_functions, crs_required_fields = CRS(), RequiredFields()
check_header_validation_error = OrderHeader().check_header_validation_error


class OrderEntry(LibParent):
    total_text = "Total:"

    def __init__(self):
        super(OrderEntry, self).__init__()

    def fill_in_account_field(self, account_code, should_found=None, select=None):
        # enter the account code to the Account# field
        self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.inp_account_code, account_code)
        self._actions.wait(2)
        if not should_found:
            acc_search = self._general_helper.find(self._pages.CRS.order_entry.account_search_result, get_text=True)
            # Should not find any account
            assert "No results found" in acc_search, f"Account unexpectedly found: {acc_search}"
        else:
            # Should find account
            acc_search = self._general_helper.find_elements(
                self._general_helper.remake_locator(self._pages.CRS.order_entry.account_search_result, "/a"),
                get_text=True)
            assert all(i in acc_search for i in should_found), \
                f"Expected account '{should_found}' not found in: {acc_search}"
            if select:
                # Select account from list
                self._general_helper.find_and_click(
                    self._general_helper.remake_locator(self._pages.CRS.order_entry.account_search_result,
                                                        f"/a[contains(text(),'{select}')]"))

    def click_more_options(self):
        self._general_helper.find_and_click(self._pages.CRS.order_entry.lnk_more_options)
        self._general_helper.find(self._pages.CRS.order_entry.more_options_block)

    def click_start_batch_scan_button(self, expected_error=None):
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_start_batch_scan)
        if expected_error:
            check_header_validation_error(expected_error)
        else:
            self._actions.wait_for_window_present_by_partial_url("/Order/ScanDocuments", 60)

    def get_order_header_customer_info(self, save_to_data=False, get_name=True, state_name=True):
        self.click_more_options()
        state = self._general_helper.find(self._pages.CRS.order_entry.inp_customer__state, get_attribute='value')
        if state_name:
            state = self._general_helper.find(self._general_helper.make_locator(
                self._pages.CRS.order_entry.inp_customer__state_name, state), get_attribute='text')
            state = state if "--" not in state else ""
        customer_info = {
            "addr1": self._general_helper.find(self._pages.CRS.order_entry.inp_customer__addr1, get_attribute='value'),
            "zip": self._general_helper.find(self._pages.CRS.order_entry.inp_customer__zip, get_attribute='value'),
            "city": self._general_helper.find(self._pages.CRS.order_entry.inp_customer__city, get_attribute='value'),
            "state": state}
        if get_name:
            customer_info.update(
                {"name": self._general_helper.find(self._pages.CRS.order_entry.inp_customer__name,
                                                   get_attribute='value')})
        self._actions.store("customer_info", customer_info) if save_to_data else None
        return customer_info

    def new_registration(self, unique_number=None, email=None, first=None, last=None):
        self.click_more_options()
        # Clear account email field
        self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.inp_account_email, "")
        # Generate unique number
        unique_number = unique_number if unique_number else datetime.now().strftime("%Y%m%d%H%M%S")
        email = email if email else f"AutoTest{unique_number}@mail.ua"
        first = first if first else "FirstName"
        last = last if last else "LastName"
        # Fill in required fields
        self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.new_user_email_field, email)
        self._actions.wait(0.3)
        self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.new_user_first_name, first)
        self._actions.wait(0.3)
        self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.new_user_last_name, last)
        self._actions.wait(0.3)
        self._general_helper.find_and_click(self._pages.CRS.order_entry.new_user_first_name)
        # Click "New registration" link
        self._general_helper.find_and_click(self._pages.CRS.order_entry.lnk_new_registration)
        # Wait success text
        self._general_helper.find(self._pages.CRS.order_entry.lbl_success_registration, get_text=True)
        self._general_helper.find_and_click(self._pages.CRS.order_entry.lnk_less_options)

        return unique_number, email

    def clear_order_header_fields(self):
        # Clear account/email/name fields
        fields = [self._pages.CRS.order_entry.inp_account_code, self._pages.CRS.order_entry.inp_account_email,
                  self._pages.CRS.order_entry.inp_account_name]
        for i in fields:
            # If field NOT disabled
            if not self._general_helper.find(i, get_attribute="readonly"):
                # Clear field
                self._general_helper.find_and_send_keys(i, None)
                return

    def check_address_required_error(self, expected_error="Address is required!", fill_in_required_fields=True,
                                     should_exist=True):
        error = self._general_helper.find(("xpath", "//span[@class='error']", "Address is required!"),
                                          get_text=True, should_exist=should_exist)
        if should_exist:
            assert error == expected_error, f"Actual error '{error}' not equal to expected '{expected_error}'"
        if error and fill_in_required_fields:
            self.click_more_options()
            crs_required_fields.crs_required_fields(
                ("xpath", "//*[contains(@class, 'koValidationError')]", "Required fields"))

    def send_to_admin(self):
        # Wait for popup
        self._general_helper.wait_and_click(self._pages.CRS.order_entry.pup_orderadmin_bubble_sendtoadmin, scroll=True)
        # Wait for action reason popup, fill and submit
        CRS_functions.fill_reason(self._pages.CRS.order_entry.pup_action_reason)

    def click_add_to_order(self):
        self._general_helper.wait_and_click(self._pages.CRS.order_entry.btn_add_to_order, enabled=True, scroll=True)
        self._actions.wait_for_element_displayed(self._pages.CRS.order_summary.lbl_order_number)

    def select_doctype(self):
        data = self._general_helper.get_data()
        loc_order_item_tab = self._general_helper.make_locator(
            self._pages.CRS.order_entry.lnk_order_entry_tab, data['config'].get_tab_name("Tabs.Order_Item.value"))
        self._general_helper.scroll_and_click(loc_order_item_tab)
        loc_doc_type = self._pages.CRS.fields.document_type_ddl_by_oi_index()
        selected_doc_type = Select(self._actions.get_browser().find(loc_doc_type))
        data["doc_type"] = selected_doc_type.first_selected_option.text
        self._actions.step(str(data["doc_type"]))

    def wait_order_item_tab_displayed(self):
        loc_order_item_tab = self._general_helper.make_locator(
            self._pages.CRS.order_entry.lnk_order_entry_tab,
            self._general_helper.get_data()['config'].get_tab_name("Tabs.Order_Item.value"))
        self._actions.wait_for_element_displayed(loc_order_item_tab)

    def tab_locator(self, tab_name):
        tab = self._general_helper.get_data()['config'].get_tab_name(f"Tabs.{tab_name}.value")
        assert tab, f"Tab with name '{tab_name}' not found in config file!"
        locator = self._general_helper.make_locator(self._pages.CRS.order_entry.lnk_order_entry_tab, tab)
        return locator

    def save_entered_doc_type(self):
        """saves the selected doc type to test data"""
        data = self._general_helper.get_data()
        prev_doc_type = data.get("doc_types")
        doc_types = prev_doc_type if prev_doc_type else []
        if data['config'].test_data(f"{data['current_oit']}.doc_type"):
            self._general_helper.scroll_and_click(self.tab_locator("Order_Item"))
            doc_type_ddl = self._actions.get_browser().find(self._pages.CRS.fields.document_type_ddl_by_oi_index())
            data["doc_type"] = Select(doc_type_ddl).first_selected_option.text
        elif data['config'].test_data(f"{data['current_oit']}.default_doc_type") != '':
            data["doc_type"] = data['config'].test_data(f"{data['current_oit']}.default_doc_type")
        doc_types.append(data.get("doc_type"))
        data["doc_types"] = doc_types  # for tests with several OITs
        self._actions.step(f"Doc types: {data['doc_types']}")

    # Return by Mail - - - - - - - - - - - - - - - - - - - -

    def click_return_by_mail_checkbox(self):
        self._general_helper.scroll_and_click(self._pages.CRS.order_entry.cbx_return_by_mail)
        self._general_helper.find(self._pages.CRS.order_entry.return_by_mail_block, wait_displayed=True)

    def click_copy_from_prior_order_item_link(self):
        self.click_return_by_mail_checkbox()
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_copy_from_prior_order_item)

    def click_copy_from_order_header_link(self):
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_copy_from_order_header)

    def click_copy_mailing_address_link(self):
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_copy_mailing_address)

    def click_copy_to_return_by_mail_link(self):
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_copy_to_return_by_mail)

    def click_reverse_parties_link(self):
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_reverse_parties)

    def get_return_by_mail_values(self, save_to_data=False, state_name=False):
        """get values on current tab from 'return by mail' or 'owners' or 'applicant' or 'business' address"""
        addr1, name_el2 = None, None
        name_el = self._general_helper.find(self._pages.CRS.order_entry.inp_return_by_mail__owners_name,
                                            should_exist=False,
                                            timeout=1)
        if not name_el:  # Business tab
            name_el = self._general_helper.find(self._pages.CRS.order_entry.inp_business__name, should_exist=False,
                                                timeout=0.2)
        if name_el:  # if Business or Owner's tab
            addr1 = self._general_helper.find(self._pages.CRS.order_entry.inp_return_by_mail__name,
                                              get_attribute='value')
        if not name_el:  # Applicant tab with First and Last names
            name_el = self._general_helper.find(self._pages.CRS.order_entry.inp_applicant__first_name,
                                                should_exist=False,
                                                timeout=0.2)
            name_el2 = self._general_helper.find(self._pages.CRS.order_entry.inp_applicant__last_name,
                                                 should_exist=False,
                                                 timeout=0.2)
        if not name_el:  # Order Item tab
            name_el = self._general_helper.find(self._pages.CRS.order_entry.inp_return_by_mail__name,
                                                should_exist=False,
                                                timeout=0.2)
        # 'name' absent on 'applicant' tab
        name = f"{name_el.value}{name_el2.value}".rstrip() if name_el2 else "" if not name_el else name_el.value
        addr1 = addr1 if addr1 else self._general_helper.find(self._pages.CRS.order_entry.inp_return_by_mail__addr1,
                                                              get_attribute='value')
        zip_ = self._general_helper.find(self._pages.CRS.order_entry.inp_return_by_mail__zip, get_attribute='value')
        city = self._general_helper.find(self._pages.CRS.order_entry.inp_return_by_mail__city, get_attribute='value')
        state_el = self._general_helper.find(self._pages.CRS.order_entry.inp_return_by_mail__state, should_exist=False,
                                             timeout=1)
        state = state_el.value if state_el else \
            self._general_helper.find(self._pages.CRS.order_entry.inp_return_by_mail__state_code, get_attribute='value')
        if state_name and str(state).isdigit():
            state = self._general_helper.find(self._general_helper.make_locator(
                self._pages.CRS.order_entry.inp_business__state_name, state), get_text=True)
        return_by_mail = {"addr1": addr1, "zip": zip_, "city": city, "state": state}
        return_by_mail.update({"name": name}) if name else None
        self._actions.store("return_by_mail", return_by_mail) if save_to_data else None
        return return_by_mail

    def fill_return_by_mail_fields(self, name="ReturnByMailCustomerName", address1="ReturnByMailAddress1",
                                   address2=None, zip_code="123456789", city=None, state=None):
        self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.inp_return_by_mail__zip, zip_code)
        self._general_helper.find_and_click(self._pages.CRS.order_entry.inp_return_by_mail__addr2)
        self._general_helper.wait_for_spinner()
        self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.inp_return_by_mail__name, name)
        self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.inp_return_by_mail__addr1, address1)
        self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.inp_return_by_mail__addr2,
                                                address2) if address2 else None
        # City and State fields are autofilled in case of 'correct' ZipCode
        self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.inp_return_by_mail__city,
                                                city) if city else None
        self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.inp_return_by_mail__state,
                                                state) if state else None
        return self.get_return_by_mail_values()

    def fill_business_name_and_address_fields(self, name=None, address1="Business_address", zip_code="234567890"):
        name = name if name else f'BusinessName_{datetime.now().strftime("%d%m%Y_%S")}'
        self._general_helper.find_and_click(self.tab_locator("Business"))
        self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.inp_return_by_mail__zip, zip_code)
        self._general_helper.find_and_click(self._pages.CRS.order_entry.inp_return_by_mail__name)
        self._general_helper.wait_for_spinner()
        self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.inp_business__name, name)
        self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.inp_return_by_mail__name, address1)
        return self.get_return_by_mail_values(state_name=True)

    def click_same_as_customer_checkbox(self):
        self._general_helper.find_and_click(self._pages.CRS.order_entry.cbx_same_as_customer)
        self._general_helper.wait_for_spinner()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Parties

    def get_parties_values(self, index=1):
        """Collect values from 'Parties' fields"""
        grantor_fields = \
            [self._pages.CRS.order_entry.inp_parties__first_name(True, index=index),
             self._pages.CRS.order_entry.inp_parties__last_name(index=index),
             self._pages.CRS.order_entry.inp_parties__middle_name(index=index),
             self._pages.CRS.order_entry.inp_parties__suffix(index=index)]
        grantor = [self._general_helper.find(i, get_attribute="value", should_exist=False, timeout=0.3) for i in
                   grantor_fields]
        grantee_fields = \
            [self._pages.CRS.order_entry.inp_parties__first_name(False, index),
             self._pages.CRS.order_entry.inp_parties__last_name(False, index),
             self._pages.CRS.order_entry.inp_parties__middle_name(False, index),
             self._pages.CRS.order_entry.inp_parties__suffix(False, index)]
        grantee = [self._general_helper.find(i, get_attribute="value", should_exist=False, timeout=0.3) for i in
                   grantee_fields]
        return {"Grantor": [i for i in grantor if i], "Grantee": [i for i in grantee if i]}

    def fill_parties_values(self, grantor, grantee, index=1):
        """Grantor and Grantee should be list of values: ['first', 'last',..]"""
        self._general_helper.find_and_click(self.tab_locator("Parties"))
        grantor_fields = \
            [self._pages.CRS.order_entry.inp_parties__first_name(index=index),
             self._pages.CRS.order_entry.inp_parties__last_name(index=index),
             self._pages.CRS.order_entry.inp_parties__middle_name(index=index),
             self._pages.CRS.order_entry.inp_parties__suffix(index=index)]
        [self._general_helper.find_and_send_keys(field, value, timeout=0.5,
                                                 should_exist=False) for field, value in zip(grantor_fields, grantor)]
        grantee_fields = \
            [self._pages.CRS.order_entry.inp_parties__first_name(False, index),
             self._pages.CRS.order_entry.inp_parties__last_name(False, index),
             self._pages.CRS.order_entry.inp_parties__middle_name(False, index),
             self._pages.CRS.order_entry.inp_parties__suffix(False, index)]
        [self._general_helper.find_and_send_keys(field, value, timeout=0.5,
                                                 should_exist=False) for field, value in zip(grantee_fields, grantee)]

    def copy_parties_names(self, year=None, doc_number=None):
        """Copy names from specified document
                or
           Copy From Prior item """
        self._general_helper.find_and_click(self.tab_locator("Parties"))
        self._general_helper.scroll_and_click(self._pages.CRS.order_entry.btn_copy_names)
        if year and doc_number:
            self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.inp_copy_names__recorded_year, year)
            self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.inp_copy_names__doc_number, doc_number)
            self._actions.wait(0.5)
            self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_copy_names__copy)
        else:
            self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_copy_names__copy_from_prior_item)
        self._general_helper.wait_for_spinner()

    def click_parties__add_grantor(self):
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_add_grantor)

    def click_parties__add_grantee(self):
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_add_grantee)

    def click_parties__up_button(self, grantor=True, index=2):
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_parties__up(grantor=grantor, index=index))

    def click_parties__down_button(self, grantor=True, index=1):
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_parties__down(grantor=grantor, index=index))

    def click_parties__delete_button(self, grantor=True, index=2):
        self._general_helper.find_and_click(
            self._pages.CRS.order_entry.btn_parties__delete(grantor=grantor, index=index))

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Properties

    def save_entered_property(self):
        """saves the property data entered by required fields function to test data"""
        data = self._general_helper.get_data()
        prop_fields = []
        if data['config'].test_data(f"{data['current_oit']}.order_summary.save_prop_address"):
            self._general_helper.scroll_and_click(self.tab_locator("Properties"))
            self._general_helper.scroll_into_view(self._pages.CRS.fields.lot_input_by_oi_index_by_property_index())
            prop_fields.append(
                self._actions.get_element_text(self._pages.CRS.fields.lot_input_by_oi_index_by_property_index()))
            prop_fields.append(
                self._actions.get_element_text(self._pages.CRS.fields.block_input_by_oi_index_by_property_index()))
            prop_fields.append(
                self._actions.get_element_text(self._pages.CRS.fields.ncb_input_by_oi_index_by_property_index()))
            prop_fields.append(
                self._actions.get_element_text(
                    self._pages.CRS.fields.subdivision_input_by_oi_index_by_property_index()))
            prop_fields.append(
                self._actions.get_element_text(self._pages.CRS.fields.volume_input_by_oi_index_by_property_index()))
            prop_fields.append(
                self._actions.get_element_text(self._pages.CRS.fields.page_input_by_oi_index_by_property_index()))
            prop_fields.append(
                self._actions.get_element_text(
                    self._pages.CRS.fields.county_block_input_by_oi_index_by_property_index()))
            # prop_fields.append(self._actions.get_element_text(self._pages.CRS.fields.ordinance_input_by_oi_index_by_property_index()))
        data["prop_fields"] = prop_fields

    def get_property_blocks(self):
        """return property blocks dict {position: name}"""
        blocks = self._general_helper.find_elements(self._pages.CRS.order_entry.property_blocks, get_attribute="class")
        names = [str(i).replace('prop-', '').replace(' controlBlock', '') for i in blocks]
        property_blocks = dict(enumerate(names, 1))
        self._actions.step(f":: Property blocks: {property_blocks}")
        return property_blocks

    def get_property_block_index(self, name="newdesc", num=1, should_exist=True, all_blocks=None):
        """return index of [num] 'name' block
            for example: *1-st newdesk property block* position index"""
        all_blocks = self.get_property_blocks() if not all_blocks else all_blocks
        blocks = [k for k, v in all_blocks.items() if v == name]
        if not blocks:
            msg = f"Property block '{name}' not found!: '{all_blocks}'"
            if should_exist:
                raise ValueError(msg)
            else:
                return self._actions.step(msg)
        if len(blocks) >= num:
            return blocks[num - 1]
        else:
            msg = f"Property block '{name}[{num}]' not found!: '{blocks}'"
            if should_exist:
                raise ValueError(msg)
            else:
                self._actions.step(msg)

    def click_properties__add_desc(self, fill=0):
        self._general_helper.scroll_and_click(self._pages.CRS.order_entry.btn_add_new_desc)
        return self.fill_properties_desc(index=fill, return_values=True) if fill else None

    def click_properties__add_subdivision(self, fill=0):
        self._general_helper.scroll_and_click(self._pages.CRS.order_entry.btn_add_new_subdivision)
        return self.fill_properties_subdivision(index=fill, return_values=True) if fill else None

    def click_properties__add_survey(self, fill=0):
        self._general_helper.scroll_and_click(self._pages.CRS.order_entry.btn_add_new_survey)
        return self.fill_properties_survey(index=fill, return_values=True) if fill else None

    def click_properties__add_address(self, fill=0):
        self._general_helper.scroll_and_click(self._pages.CRS.order_entry.btn_add_new_address)
        return self.fill_properties_address(index=fill, return_values=True) if fill else None

    def copy_properties(self, year=None, doc_number=None):
        """Copy properties from specified document
                or
           Copy From Prior Order Item """
        self._general_helper.find_and_click(self.tab_locator("Properties"))
        self._general_helper.scroll_and_click(self._pages.CRS.order_entry.btn_copy_property)
        if not year or not doc_number:
            self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_copy_property__copy_from_prior_item)
        else:
            self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.inp_copy_property__year, year)
            self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.inp_copy_property__doc_num, doc_number)
            self._actions.wait(0.5)
            self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_copy_property__copy)
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_copy_property__new_subdivision_ok,
                                            timeout=2,
                                            should_exist=False)
        self._general_helper.wait_for_spinner()

    # CONTROLS
    #  prop_block should be one of: ["newdesc", "subdivision", "survey", "propaddress"]
    #  if  prop_block=None: click on 'index' element on the page
    def click_properties__up_button(self, index=2, prop_block=None):
        self._general_helper.find_and_click(
            self._pages.CRS.order_entry.btn_properties__up(index=index, prop_block=prop_block))
        self._actions.wait(0.5)

    def click_properties__down_button(self, index=1, prop_block=None):
        self._general_helper.find_and_click(
            self._pages.CRS.order_entry.btn_properties__down(index=index, prop_block=prop_block))
        self._actions.wait(0.5)

    def click_properties__delete_button(self, index=1, prop_block=None):
        self._general_helper.find_and_click(
            self._pages.CRS.order_entry.btn_properties__delete(index=index, prop_block=prop_block))
        self._actions.wait(0.5)

    def fill_properties_desc(self, desc=None, index=1, return_values=False):
        """desc should be list of values: ['descr', 'permit']"""
        desc = desc if desc else [f"description{index}", f"permit{index}"]
        index = self.get_property_block_index("newdesc", index) if index > 1 else index
        fields = [self._pages.CRS.order_entry.inp_properties_desc__description(index=index),
                  self._pages.CRS.order_entry.inp_properties_desc__water_permit(index=index)]
        [self._general_helper.find_and_send_keys(field, value,
                                                 should_exist=False, timeout=0.3) for field, value in zip(fields, desc)]
        return self.get_properties_desc_values(index) if return_values else None

    def get_properties_desc_values(self, index=1):
        fields = [self._pages.CRS.order_entry.inp_properties_desc__description(index=index),
                  self._pages.CRS.order_entry.inp_properties_desc__water_permit(index=index)]
        self._general_helper.find_and_click(fields[0])
        desc = [self._general_helper.find(i, get_attribute="value", should_exist=False, timeout=0.3) for i in fields]
        return desc

    def fill_properties_subdivision(self, subdivision=None, index=1, return_values=False):
        """subdivision should be list of values: ['lot', 'block', 'NCB'...]"""
        subdivision = subdivision if subdivision else \
            [f"{i}{index}" for i in ["lot", "block", "ncb", "sub", "vol", "page", "county", "ordinance"]]
        index = self.get_property_block_index("subdivision", index) if index > 1 else index
        fields = [self._pages.CRS.order_entry.inp_properties_subdivision__lot(index=index),
                  self._pages.CRS.order_entry.inp_properties_subdivision__block(index=index),
                  self._pages.CRS.order_entry.inp_properties_subdivision__ncb(index=index),
                  self._pages.CRS.order_entry.inp_properties_subdivision__subdivision(index=index),
                  self._pages.CRS.order_entry.inp_properties_subdivision__volume(index=index),
                  self._pages.CRS.order_entry.inp_properties_subdivision__page(index=index),
                  self._pages.CRS.order_entry.inp_properties_subdivision__county(index=index),
                  self._pages.CRS.order_entry.inp_properties_subdivision__ordinance(index=index)]
        [self._general_helper.find_and_send_keys(field, value,
                                                 should_exist=False, timeout=0.3) for field, value in
         zip(fields, subdivision)]
        return self.get_properties_subdivision_values(index) if return_values else None

    def get_properties_subdivision_values(self, index=1):
        fields = [self._pages.CRS.order_entry.inp_properties_subdivision__lot(index=index),
                  self._pages.CRS.order_entry.inp_properties_subdivision__block(index=index),
                  self._pages.CRS.order_entry.inp_properties_subdivision__ncb(index=index),
                  self._pages.CRS.order_entry.inp_properties_subdivision__subdivision(index=index),
                  self._pages.CRS.order_entry.inp_properties_subdivision__volume(index=index),
                  self._pages.CRS.order_entry.inp_properties_subdivision__page(index=index),
                  self._pages.CRS.order_entry.inp_properties_subdivision__county(index=index),
                  self._pages.CRS.order_entry.inp_properties_subdivision__ordinance(index=index)]
        self._general_helper.find_and_click(fields[0])
        subdivision = [self._general_helper.find(i, get_attribute="value", should_exist=False, timeout=0.3) for i in
                       fields]
        return subdivision

    def fill_properties_survey(self, survey=None, index=1, return_values=False):
        """survey should be list of values: ['abstract', 'survey', 'acres']"""
        survey = survey if survey else [f"{i}{index}" for i in ["abstract", "survey", "acres"]]
        index = self.get_property_block_index("survey", index) if index > 1 else index
        fields = [self._pages.CRS.order_entry.inp_properties_survey__abstract(index=index),
                  self._pages.CRS.order_entry.inp_properties_survey__survey(index=index),
                  self._pages.CRS.order_entry.inp_properties_survey__acres(index=index)]
        [self._general_helper.find_and_send_keys(field, value,
                                                 should_exist=False, timeout=0.3) for field, value in
         zip(fields, survey)]
        return self.get_properties_survey_values(index) if return_values else None

    def get_properties_survey_values(self, index=1):
        fields = [self._pages.CRS.order_entry.inp_properties_survey__abstract(index=index),
                  self._pages.CRS.order_entry.inp_properties_survey__survey(index=index),
                  self._pages.CRS.order_entry.inp_properties_survey__acres(index=index)]
        self._general_helper.find_and_click(fields[0])
        survey = [self._general_helper.find(i, get_attribute="value", should_exist=False, timeout=0.3) for i in fields]
        return survey

    def fill_properties_address(self, address=None, index=1, return_values=False):
        """address should be list of values: ['address1', 'address2',..]"""
        address = address if address else [f"address1{index}", f"address2{index}", "123456789",
                                           datetime.now().timestamp()]
        zip_code = address.pop(2)
        index = self.get_property_block_index("propaddress", index) if index > 1 else index
        self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.inp_properties_address__zip(index=index),
                                                zip_code)
        self._general_helper.find_and_click(self._pages.CRS.order_entry.inp_properties_address__address2(index=index))
        self._general_helper.wait_for_spinner()
        fields = [self._pages.CRS.order_entry.inp_properties_address__address1(index=index),
                  self._pages.CRS.order_entry.inp_properties_address__address2(index=index),
                  self._pages.CRS.order_entry.inp_properties_address__parcel(index=index)]
        [self._general_helper.find_and_send_keys(field, value,
                                                 should_exist=False, timeout=0.3) for field, value in
         zip(fields, address)]
        return self.get_properties_address_values(index) if return_values else None

    def get_properties_address_values(self, index=1):
        fields = [self._pages.CRS.order_entry.inp_properties_address__address1(index=index),
                  self._pages.CRS.order_entry.inp_properties_address__address2(index=index),
                  self._pages.CRS.order_entry.inp_properties_address__zip(index=index),
                  self._pages.CRS.order_entry.inp_properties_address__city(index=index),
                  self._pages.CRS.order_entry.inp_properties_address__state(index=index),
                  self._pages.CRS.order_entry.inp_properties_address__parcel(index=index)]
        self._general_helper.find_and_click(fields[0])
        address = [self._general_helper.find(i, get_attribute="value", should_exist=False, timeout=0.3) for i in fields]
        return address

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def attach_and_verify_file(self, file_name):
        """Attach file and verify it on page"""
        file = join(self._names.file_path, file_name)
        if isfile(file):
            self._actions.wait_for_element_present(self._pages.CRS.order_entry.attach_file_upload_btn, 120)
            self._actions.wait(3)
            self._actions.send_keys(self._pages.CRS.order_entry.attach_file_upload_input, file)
            expected_file_name = ".".join(file_name.split(".")[:-1] + ["tiff"])
            CRS_functions.verify_file_present(expected_file_name)
        else:
            self._actions.error(message='File is required')

    # ---------------------------------------------------------------------------------------------------------------
    # FEE GRID

    def fee_by_fee_criterion(self, fee_criterion):
        # enters fee criterion and verifies fee amount in fee grid
        data = self._general_helper.get_data()
        no_of = randint(1, 999)
        if fee_criterion == "pages":
            no_of_locator = self._pages.CRS.order_entry.txt_no_of_pages
            non_fee_criterion = int(data['config'].test_data(f"{data['OIT']}.non_fee_pages"))
            per_criterion_fee = float(data['config'].test_data(f"{data['OIT']}.per_page_fee"))
            fee_label = "Plat Copy Fee" if data.OIT == "Plat_Copy" else "Additional Page Fee"
        elif fee_criterion == "names":
            no_of_locator = self._pages.CRS.order_entry.txt_no_of_names
            non_fee_criterion = int(data['config'].test_data(f"{data['OIT']}.non_fee_names"))
            per_criterion_fee = float(data['config'].test_data(f"{data['OIT']}.per_name_fee"))
            fee_label = "Additional Name Fee"
        else:  # fee_criterion == "certifications"
            no_of_locator = self._pages.CRS.order_entry.txt_no_of_certifications
            non_fee_criterion = int(data['config'].test_data(f"{data['OIT']}.non_fee_certifications"))
            per_criterion_fee = float(data['config'].test_data(f"{data['OIT']}.per_certification_fee"))
            fee_label = "Certification Fee"

        self._general_helper.find_and_send_keys(no_of_locator, no_of).send_keys(self._keys.TAB)
        expected_fee_by_criterion = (no_of - non_fee_criterion) * per_criterion_fee if no_of > non_fee_criterion else 0
        locator = self._general_helper.make_locator(self._pages.CRS.order_entry.fee_amount_by_fee_label_, fee_label)
        for _ in range(5):
            try:
                self._actions.wait_for_element_text(locator, "${:,.2f}".format(expected_fee_by_criterion))
                return expected_fee_by_criterion
            except StaleElementReferenceException:
                self._actions.wait(0.5)
        raise StaleElementReferenceException(f"Element {locator[2]} not attached to page")

    def verify_total_fee(self, basic_fee, expected_fees):
        actual_recording_fee = self.fee_amount_by_fee_label(basic_fee) if basic_fee else 0
        expected_total_fee = actual_recording_fee + expected_fees
        actual_total_fee = self.fee_amount_by_fee_label(self.total_text)
        assert actual_total_fee == expected_total_fee, \
            f"Actual Total Fee {actual_total_fee} is NOT equal to expected {expected_total_fee}"
        return actual_total_fee

    def enter_and_verify_fee_amounts_by_fee_criteria(self, basic_fee: str, fee_criteria: list) -> None:
        fees_by_criteria = [self.fee_by_fee_criterion(i) for i in fee_criteria]
        expected_fees_by_criteria = sum(fees_by_criteria)
        actual_total_fee = self.verify_total_fee(basic_fee, expected_fees_by_criteria)
        self.click_add_to_order()
        self._general_helper.wait_for_spinner()
        total_price = float(
            self._general_helper.find(self._pages.CRS.order_summary.price_by_row_index(1), get_text=True).replace('$',
                                                                                                                  ''))
        assert total_price == actual_total_fee, f"Total Price {total_price} is " \
                                                f"NOT equal to Total Fee {actual_total_fee}"

    def enter_and_verify_penalty_fee_amounts(self, fee_type):
        data = self._general_helper.get_data()
        original_total_fee = self.fee_amount_by_fee_label(self.total_text)
        fee_label = "Penalty"
        if fee_type == "Penalty":
            chk_locator = self._pages.CRS.order_entry.chk_penalty
            expected_penalty_fee = original_total_fee
        else:  # fee_type it is Missing_Grantee_Addresses_Fee
            chk_locator = self._pages.CRS.order_entry.chk_missing_grantee_addresses
            expected_penalty_fee = float(data['config'].test_data(f"{data['OIT']}.missing_grantee_addresses_fee"))
        self._general_helper.find_and_click(chk_locator)
        self._general_helper.find_and_click(self._pages.CRS.order_entry.lnk_more, 10, False)
        actual_penalty_fee = self.fee_amount_by_fee_label(fee_label)
        assert actual_penalty_fee == expected_penalty_fee, \
            f"Actual Penalty Fee {actual_penalty_fee} is NOT equal to expected {expected_penalty_fee}"
        expected_new_total_fee = original_total_fee + expected_penalty_fee
        actual_new_total_fee = self.fee_amount_by_fee_label(self.total_text)
        assert actual_new_total_fee == expected_new_total_fee, \
            f"Actual Total fee {actual_new_total_fee} is not equal to expected {expected_new_total_fee}"
        return actual_new_total_fee

    def fee_amount_by_fee_label(self, fee_label):
        self._actions.wait(2)
        return float(self._general_helper.find(self._general_helper.make_locator(
            self._pages.CRS.order_entry.fee_amount_by_fee_label_, fee_label), get_text=True).replace('$', '').replace(
            ',', ''))

    def enter_and_verify_additional_fees(self):
        data = self._general_helper.get_data()
        original_total_fee = self.fee_amount_by_fee_label(self.total_text)
        fee_label = data['config'].test_data(f"{data['OIT']}.additional_fee_labels.additional_fee_1_label")
        self._actions.select_option_by_text(self._pages.CRS.order_entry.ddl_additional_fee, fee_label)
        no_of = randint(1, 99)
        self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.txt_no_of_additional_fees, no_of)
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_add_additional_fee)
        expected_fee_amount = float(
            data['config'].test_data(f"{data['OIT']}.additional_fee_values.additional_fee_1_per_no_fee")) * no_of
        self._general_helper.scroll_and_click(self._pages.CRS.order_entry.lnk_more)
        actual_fee_amount = self.fee_amount_by_fee_label(fee_label)
        assert actual_fee_amount == expected_fee_amount, \
            f"Actual fee amount {actual_fee_amount} is NOT equal to expected {expected_fee_amount}"
        expected_new_total_fee = original_total_fee + expected_fee_amount
        actual_new_total_fee = self.fee_amount_by_fee_label(self.total_text)
        assert actual_new_total_fee == expected_new_total_fee, \
            f"New total fee {actual_new_total_fee} is NOT equal to expected {expected_new_total_fee}"
        self.click_add_to_order()
        total_price = float(self._general_helper.find(
            self._pages.CRS.order_summary.price_by_row_index(1), get_text=True).replace('$', ''))
        assert total_price == expected_new_total_fee, \
            f"New total fee {total_price} is NOT equal to expected {expected_new_total_fee}"

    def enter_all_additional_fees(self, add_btn=True, consideration=False, max_time=300):
        no_of = randint(1, 3)
        t = time.time() + max_time
        # Remove default selected additional fees if exists
        if consideration:
            self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.inp_consideration_amount, randint(1, 5))
        while button := self._general_helper.find(self._pages.CRS.order_entry.btn_remove_addityional_fee,
                                                  should_exist=False, timeout=3):
            button.click()
            if time.time() > t:
                break
        data = self._general_helper.get_data()
        additional_fee_names_by_config = list(data['config'].test_data(f"{data.OIT}.additional_fee_labels").values())
        additional_fee_option_num = len(
            self._general_helper.find_elements(self._pages.CRS.order_entry.ddl_additional_fee_options))

        for i in range(1, additional_fee_option_num):
            additional_fee_ddls = self._general_helper.find_elements(self._pages.CRS.order_entry.ddl_additional_fee)
            self._actions.select_option_by_text(additional_fee_ddls[i - 1], additional_fee_names_by_config[i - 1])
            # self._actions.select_option_by_value(additional_fee_ddls[i+1], str(i))

            if self._general_helper.check_if_element_exists(self._pages.CRS.order_entry.no_of_addittional_fees):
                self._actions.send_keys(self._pages.CRS.order_entry.no_of_addittional_fees, no_of)
            if add_btn:
                self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_add_additional_fee)
        return no_of

    def verify_fund_distribution(self, discount=False, void=False):
        data = self._general_helper.get_data()
        actual_fund_names = []
        actual_fund_values = []
        distributed_amount = 0.0
        if void:
            total_amount = float(
                (self._actions.get_element_text(self._pages.CRS.void_order_summary.pup_fee_desc_lbl_total)))
            actual_fee_fund_names_el = self._general_helper.find_elements(
                self._pages.CRS.void_order_summary.pup_fee_desc_lbl)
            actual_fee_fund_values_el = self._general_helper.find_elements(
                self._pages.CRS.void_order_summary.pup_fee_values_lbl)
            order_fund_number = len(
                self._general_helper.find_elements(self._pages.CRS.void_order_summary.pup_fee_desc_lbl))
        else:
            total_amount = float(
                (self._actions.get_element_text(self._pages.CRS.order_entry.total_fee_fund)).split('$')[1])
            order_fund_number = len(self._general_helper.find_elements(self._pages.CRS.order_entry.lbl_fund_desc))
            actual_fee_fund_names_el = self._general_helper.find_elements(self._pages.CRS.order_entry.lbl_fund_desc)
            actual_fee_fund_values_el = self._general_helper.find_elements(self._pages.CRS.order_entry.lbl_fund_value)

        # get distributed fund names and values
        for actual_fund_name_el in actual_fee_fund_names_el:
            actual_fund_names.append(self._actions.get_element_text(actual_fund_name_el))
        for actual_fund_value_el in actual_fee_fund_values_el:
            actual_fund_values.append(self._actions.get_element_text(actual_fund_value_el))
        fee_funds_by_config = []
        fee_funds_by_config.extend((data['config'].test_data(f"{data.OIT}.fund_distribution")))
        # If Discount is applied remove configured fee_fund
        if discount:
            for fee_fund in fee_funds_by_config:
                if fee_fund['RA']:
                    fee_funds_by_config.remove(fee_fund)
        # check total number of distribution funds
        self._actions.wait(1)
        assert len(fee_funds_by_config) == order_fund_number, "Order Fee Fund number does not match the configuration"
        # check names and values are correct
        for i in range(len(actual_fund_names)):
            assert actual_fund_names[i] == fee_funds_by_config[i]['fund_label'], \
                "Order Fee Fund description does not match the configuration"
            if fee_funds_by_config[i]['value'] != '100%':

                amount_value = fee_funds_by_config[i]['value'].split('$')[1]
                amount = float(amount_value)
                distributed_amount = distributed_amount + amount
                assert actual_fund_values[i] == fee_funds_by_config[i]['value'], "Order Fund value " \
                                                                                 "does not match the configuration"
            else:
                assert float(actual_fund_values[i].split('$')[1]) == (total_amount - distributed_amount), \
                    "Order Fee Fund value does not match the configuration"

    def change_fee_fund_distribution(self, amount=1, increased_fund_index=0, decreased_fund_index=1):
        actual_fund_values = []
        input_fund_elements = self._general_helper.find_elements(self._pages.CRS.order_entry.inp_fund_value)
        actual_fee_fund_values_el = self._general_helper.find_elements(self._pages.CRS.order_entry.lbl_fund_value)
        # Get fee fund values in float format
        for actual_fee_fund_value_el in actual_fee_fund_values_el:
            actual_fund_values.append(float(self._actions.get_element_text(actual_fee_fund_value_el).split('$')[1]))

        # Increase one of fee fund value and decrease for the same amount other fee fund value
        increased_fund_value = actual_fund_values[increased_fund_index] + amount
        decreased_fund_value = actual_fund_values[decreased_fund_index] - amount
        # Replace changed fee fund values in stored list
        actual_fund_values[increased_fund_index] = increased_fund_value
        actual_fund_values[decreased_fund_index] = decreased_fund_value
        # Input Changed fee funds values
        self._actions.clear(input_fund_elements[increased_fund_index])
        self._actions.send_keys(input_fund_elements[increased_fund_index], str(increased_fund_value))
        self._general_helper.reset_focus()
        self._actions.clear(input_fund_elements[decreased_fund_index])
        self._actions.send_keys(input_fund_elements[decreased_fund_index], str(decreased_fund_value))
        self._general_helper.reset_focus()
        return actual_fund_values

    def verify_fund_distribution_with_additional_fees(self, no_of):
        data = self._general_helper.get_data()
        actual_fund_names = []
        actual_fund_values = []
        additional_fee_expected_value = []
        # List for Fee fund names
        actual_additional_fee_names = []
        actual_additional_fee_values = []
        # Get fund names and values
        actual_fund_names_el = self._general_helper.find_elements(
            self._pages.CRS.order_entry.lbl_fund_desc_with_additional_fees)
        actual_fund_values_el = self._general_helper.find_elements(self._pages.CRS.order_entry.lbl_fund_value)
        # Get additional fee names and values
        actual_additional_fee_names_el = self._general_helper.find_elements(
            self._pages.CRS.order_entry.lbl_additional_fees_names)
        actual_additional_fee_values_el = self._general_helper.find_elements(
            self._pages.CRS.order_entry.lbl_additional_fees_values)
        # Get fund and additional fee names from config
        fee_funds_by_config = data['config'].test_data(f"{data.OIT}.fund_distribution")
        additional_fee_names_by_config = list(data['config'].test_data(f"{data.OIT}.additional_fee_labels").values())
        additional_fee_values_by_config = [float(value) for value in
                                           list((data['config'].test_data(
                                               f"{data.OIT}.additional_fee_values").values()))]
        additional_fee_value_names_by_config = list(
            data['config'].test_data(f"{data.OIT}.additional_fee_values").keys())
        distributed_amount = 0.0
        total_amount_of_funds = float(
            (self._actions.get_element_text(self._pages.CRS.order_entry.total_fund_with_additional_fee)).
                split('$')[1])
        order_fund_number = len(
            self._general_helper.find_elements(self._pages.CRS.order_entry.lbl_fund_desc_with_additional_fees))
        # Get distributed fund names and values
        for actual_fund_name_el in actual_fund_names_el:
            actual_fund_names.append(self._actions.get_element_text(actual_fund_name_el))
        for actual_fund_value_el in actual_fund_values_el:
            actual_fund_values.append(self._actions.get_element_text(actual_fund_value_el))
        # Get distributed Additional fees names and values
        for actual_additional_fee_name_el in actual_additional_fee_names_el:
            actual_additional_fee_names.append(self._actions.get_element_text(actual_additional_fee_name_el))
        for actual_additional_fee_value_el in actual_additional_fee_values_el:
            actual_additional_fee_values.append(
                str(float(self._actions.get_element_text(actual_additional_fee_value_el).
                          split('$')[1])))
        # Check total number of distribution funds
        assert len(fee_funds_by_config) == order_fund_number, "Order Fee Fund number does not match the configuration"
        # Compare Fund names from distribution popup and configuration
        for i in range(len(actual_fund_names)):
            assert actual_fund_names[i] == fee_funds_by_config[i]['fund_label'], \
                "Order Fee Fund description does not match the configuration"
            if fee_funds_by_config[i]['value'] != '100%':
                amount_value = fee_funds_by_config[i]['value'].split('$')[1]
                amount = float(amount_value)
                distributed_amount = distributed_amount + amount
                assert actual_fund_values[i] == fee_funds_by_config[i]['value'], "Order Fee Fund value " \
                                                                                 "does not match the configuration"
            else:
                assert float(actual_fund_values[i].split('$')[1]) == (total_amount_of_funds - distributed_amount), \
                    "Order Fee Fund value does not match the configuration"
        # Compare Additional fee values from distribution popup and configuration
        for i in range(len(additional_fee_names_by_config)):
            if additional_fee_values_by_config[i] != 0:
                if 'per_no_fee' in additional_fee_value_names_by_config[i]:
                    additional_fee_expected_value.append(str(additional_fee_values_by_config[i] * no_of))
                else:
                    additional_fee_expected_value.append(str(additional_fee_values_by_config[i]))
        additional_fee_names_and_values_by_config = dict(
            zip(additional_fee_names_by_config, additional_fee_expected_value))
        actual_additional_fee_names_and_values = dict(zip(actual_additional_fee_names, actual_additional_fee_values))
        self._general_helper.scroll_into_view(actual_additional_fee_names_el[1])
        assert sorted(additional_fee_names_and_values_by_config.items()) \
               == sorted(actual_additional_fee_names_and_values.items()), "Additional fee value " \
                                                                          "does not match the configuration"
