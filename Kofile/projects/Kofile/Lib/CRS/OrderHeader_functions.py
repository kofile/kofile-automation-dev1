from random import randint
from projects.Kofile.Lib.test_parent import LibParent


class OrderHeader(LibParent):
    def __init__(self):
        super(OrderHeader, self).__init__()

    def fill_required_fields(self, required_field_locator=None):
        """
        fills in required fields in order header
        """
        _LOC_REQUIRED_FIELDS = (
            "xpath",
            "//*[@style='display: block;']//*[contains(@class,'koValidationError')]",
            "Order header required field locator"
        )
        if required_field_locator is None:
            LOC_REQUIRED_FIELDS = _LOC_REQUIRED_FIELDS                                  # noqa
        else:
            LOC_REQUIRED_FIELDS = required_field_locator                                 # noqa
        located = True
        while located:
            try:
                required_field = self._actions.get_browser().find(
                    LOC_REQUIRED_FIELDS,
                    timeout=2,
                    wait_displayed=True
                )
                self._general_helper.scroll_into_view(required_field)
                if required_field.tag_name == "input":
                    req_field_placeholder = self._actions.get_element_attribute(
                        required_field, "placeholder")
                    if req_field_placeholder == "":
                        req_field_name_attribute = self._actions.get_element_attribute(
                            required_field, "name")
                        req_field_name = req_field_name_attribute.split(".")[-1]
                    else:
                        req_field_name = req_field_placeholder
                    if req_field_name.lower() == "email":
                        field_value = self._general_helper.random_string(
                            randint(3, 15)) + "@kofiletest.com"                                 # noqa
                    elif req_field_name.lower() in \
                            ["firstname", "lastname", "address", "addressline1", "city"]:       # noqa
                        field_value = self._general_helper.random_string(randint(3, 15))
                    elif req_field_name.lower() in ["zip", "zipcode", "zip code"]:
                        field_value = self._names.default_zip
                    elif req_field_name.lower() == "phone":
                        field_value = self._general_helper.random_string(10, 1)
                    else:
                        field_value = self._general_helper.random_string(randint(3, 15))
                    self._actions.step(f"Field name or placeholder '{req_field_name}'")
                    self._actions.send_keys(required_field, field_value)
                    required_field.send_keys(self._keys.TAB)
                    if req_field_name.lower() in ["zip", "zipcode", "zip code"]:
                        self._general_helper.wait_for_spinner()
                    self._actions.wait_for_element_has_not_attribute(
                        required_field, "data-orig-title", 5)
                    if req_field_name.lower() in ["zip", "zipcode"]:
                        self._actions.wait(5)
                elif required_field.tag_name == "select":
                    required_field.click()
                    required_field.send_keys(self._keys.ARROW_DOWN)
                    required_field.send_keys(self._keys.ENTER)
                    required_field.send_keys(self._keys.TAB)
            except Exception as e:
                print(e)
                located = False

    def get_order_number(self):
        return self._general_helper.find(self._pages.CRS.order_header.txt_order_number, get_text=True)

    def fill_order_header_customer(self, customer_type, customer_name):
        if customer_type == "account":
            customer_field_locator = self._pages.CRS.order_header.txt_accountname
            name_lookup = self._general_helper.make_locator(
                self._pages.CRS.order_header.ddl_accountname_lookup_by_account_name,
                customer_name)
        elif customer_type == "email":
            customer_field_locator = self._pages.CRS.order_header.txt_email
            name_lookup = self._general_helper.make_locator(self._pages.CRS.order_header.ddl_email_lookup_by_email,
                                                            customer_name)
        else:  # customer_type == "guest":
            customer_field_locator = self._pages.CRS.order_header.txt_customername
            name_lookup = self._general_helper.make_locator(
                self._pages.CRS.order_header.ddl_customername_lookup_by_name,
                customer_name)

        self._general_helper.find_and_send_keys(customer_field_locator, customer_name)
        # wait for lookup list to appear and click on name option
        self._general_helper.wait_and_click(name_lookup)

    def check_account_balance(self, value):
        self._actions.wait_for_element_present(self._pages.CRS.order_header.company_account_balance_field)
        self._actions.wait_for_element_displayed(self._pages.CRS.order_header.company_account_balance_field)
        for _ in range(30):
            text = self._actions.get_element_value(self._pages.CRS.order_header.company_account_balance_field)
            if text.strip():
                break
            self._actions.wait(1)
        self._actions.verify_element_value(self._pages.CRS.order_header.company_account_balance_field, f"($ {value})")

    def select_auto_print_option(self, option_name="yes"):
        if option_name == "email":
            rbn_locator = self._pages.CRS.order_header.rbn_auto_print_receipt_email
        elif option_name == "no":
            rbn_locator = self._pages.CRS.order_header.rbn_auto_print_receipt_no
        else:
            rbn_locator = self._pages.CRS.order_header.rbn_auto_print_receipt_yes

        self._general_helper.find_and_click(rbn_locator)
        self._actions.wait(3)

    def check_header_validation_error(self, expected_error="Please Enter Account OR Email OR Name"):
        error = self._general_helper.find(self._pages.CRS.order_header.txt_header_validation_msg, wait_displayed=True,
                                          get_text=True)
        assert error == expected_error, f"Actual error message: '{error}' is not equal to expected: '{expected_error}'"

    def return_state_of_field_is_selected_or_no(self, radio_btn):
        return self._actions.get_browser().find_element_by_xpath(radio_btn).is_selected()

    def get_account_balance(self):
        """returns string value of CA balance"""
        self._actions.wait_for_element_present(self._pages.CRS.order_header.company_account_balance_field)
        self._actions.wait_for_element_displayed(self._pages.CRS.order_header.company_account_balance_field)
        return self._actions.get_element_value(self._pages.CRS.order_header.company_account_balance_field)

    def get_ca_balance_numeric(self):
        """returns float value of ca balance"""
        ca_balance_string = self.get_account_balance()
        numeric_chars = ""
        for char in ca_balance_string:
            if char.isdigit() or char in ('-', '.'):
                numeric_chars += char
        return float(numeric_chars)
