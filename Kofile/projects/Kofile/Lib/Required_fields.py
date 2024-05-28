"""fill required fields"""
import random
from selenium.webdriver.common.keys import Keys

from projects.Kofile.Lib.test_parent import LibParent
from golem.webdriver.extended_webelement import Select
from time import time
from selenium.webdriver.support.ui import Select


class RequiredFields(LibParent):
    def __init__(self):
        super(RequiredFields, self).__init__()

    def crs_fill_required_fields(self, fields=True, radiobutton=True, checkbox=True, tabs_locator=None):
        """
        Main function for fill CRS required fields
        """

        def fill_all(required_fields_locator=None):
            if radiobutton:
                self.crs_required_radio_buttons_input()
            if checkbox:
                self.crs_required_checkboxes_input()
            if fields:
                self.crs_required_fields(required_fields_locator)

        tabs_locator = tabs_locator if tabs_locator else ('xpath', '//a[@class="error"]', 'Required Tabs')
        required_tabs = self._general_helper.find_elements(tabs_locator, get_text=True)
        if not required_tabs:
            tabs = self._general_helper.find(("xpath", "//*[@class='tabcontent']", "Tabs"), should_exist=False,
                                             timeout=1)
            suffix = " and @style='display: block;'" if tabs else ""  # in case of "invisible" fields
            self._actions.step(f"- - - - - Fill all REQUIRED fields - - - - -")
            fill_all(("xpath", f"//*[contains(@class,'koValidationError'){suffix}]", "Get all required fields"))
            return
        for tab in required_tabs:
            self._actions.step(f"- - - - - *{tab}* tab --> fill all REQUIRED fields - - - - -")
            _tabs_locator = ('xpath', f'//a[@class="error" and contains(text(),"{tab}")]', f'"{tab}" Required Tab')
            self._general_helper.find_and_click(_tabs_locator)
            fill_all()

    def click_all(self, locator):
        max_time = time() + 300
        while time() < max_time:
            try:
                el = self._general_helper.find(locator, timeout=2)
                el.send_keys(Keys.TAB)
                el.wait_displayed(1)
                el.click()
                self._actions.step(
                    f"-- click {locator[2]} -- *{el.get_attribute('name') if el.has_attribute('name') else ''}*")
            except Exception as e:
                self._logging.warning(f"-- no more {locator[2]}:\n\t{e}")
                break

    def crs_required_radio_buttons_input(self, required_radiobuttons_locator=None):
        """
        Fill crs all required radiobuttons
        """
        if not required_radiobuttons_locator:
            required_radiobuttons_locator = self._pages.CRS.order_entry.required_radiobuttons_locator
        self.click_all(required_radiobuttons_locator)

    def crs_required_checkboxes_input(self, required_checkboxes_locator=None):
        """click all required checkboxes"""
        if not required_checkboxes_locator:
            required_checkboxes_locator = self._pages.CRS.order_entry.required_checkboxes_locator
        self.click_all(required_checkboxes_locator)

    def crs_required_fields(self, required_fields_locator=None):
        """
        Function get all crs required fields and input data per tab
        """
        self._general_helper.wait_for_spinner()

        if required_fields_locator is None:
            required_fields_locator = self._pages.CRS.order_entry.required_fields_locator
        numbers = self._names.FIELDS_VALUE["Numbers"]
        max_time = time() + 300
        while time() < max_time:
            try:
                field = self._general_helper.find(required_fields_locator, timeout=3)
            except Exception as e:
                self._logging.warning(f"-- no more required fields --:\n\t{e}")
                break
            self._actions.get_browser().execute_script(self._names.scroll_js, field)
            field_name_attribute = field.get_attribute("name")
            field_name = field.get_attribute('placeholder') if not field_name_attribute \
                else field_name_attribute.split('.')[-1]
            if field.tag_name in ("input", "textarea"):
                if field_name in numbers.keys():
                    value = random.randrange(numbers[field_name][0], numbers[field_name][1])
                else:
                    value = random.choice(self._names.FIELDS_VALUE["Strings"][field_name])
                if field_name == 'ParcelId':
                    data = self._general_helper.get_data()
                    parcel_id = data['config'].test_data(f"{data.OIT}.parcel_id")
                    value = parcel_id if parcel_id else value

                # Fill correct EventDate in Re-Index
                if field_name == "EventDate":
                    rec_date = self._general_helper.find(self._pages.CRS.order_entry.recorded_date_field,
                                                         should_exist=False, timeout=1, get_text=True)
                    if rec_date:
                        m, d, y = rec_date.split('/')
                        m = f"0{m}" if int(m) < 10 else m
                        d = f"0{d}" if int(d) < 10 else d
                        value = f"{m}{d}{y}"

                self._actions.step(f"--> Fill '{field_name}' with '{value}' --")
                field.wait_displayed(1)
                field.clear()
                if field_name in ['AnticipatedDate']:
                    field.send_keys(value)
                    self._general_helper.reset_focus()
                else:
                    field.send_keys(value, Keys.TAB)
                if field_name in ["ZipCode", "Zip Code", "BirthDate", "Date of Birth"]:
                    self._general_helper.wait_for_spinner()
                if field_name in ["BirthDate"]:
                    try:
                        field_name.send_keys(Keys.ENTER)
                    except Exception as e:
                        print(e)
                field.wait_has_not_attribute('data-orig-title', 10)
                try:
                    if field_name in ('DocNumber', 'ParcelId'):
                        self._general_helper.find(self._pages.CRS.order_entry.warning_popup, 5)
                        self._general_helper.find_and_click(self._pages.CRS.order_entry.yes_button)
                        self._general_helper.wait_disappear_element(self._pages.CRS.order_entry.warning_popup)
                except Exception as e:
                    self._logging.warning(e)
                try:
                    if field_name == 'UnIncorporatedBusinessName':
                        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_assumed_name_infobox_cancel,
                                                            5)
                        self._general_helper.wait_disappear_element(
                            self._pages.CRS.order_entry.btn_assumed_name_infobox_cancel, 5)
                except Exception as e:
                    self._logging.warning(e)
            elif field.tag_name == 'select':
                Select(field).select_by_index(1)
                field.send_keys(Keys.TAB)
                self._actions.step(f"--> Select '{field.value}' option from *{field_name}* dropdown list")
            else:
                raise Exception(f"Unexpected field name {field.tag_name}")

    def eform_fill_required_fields(self, fields=True, radiobutton=True, checkbox=True):
        """
        Main function for eForm required fields
        """
        if radiobutton:
            self.eform_required_radio_buttons_input()
        if checkbox:
            self.eform_required_checkboxes_input()
        if fields:
            self.eform_required_fields()
        self._actions.wait(2)

    def eform_required_radio_buttons_input(self):
        """Fill all required radiobuttons in Eform"""

        max_time = time() + 300
        while time() < max_time:
            try:
                required_radiobuttons = self._actions.get_browser().find_all(
                    self._pages.eform.required_radiobuttons_locator)

                self._actions.wait_for_element_displayed(required_radiobuttons[0])
                self._actions.execute_javascript(
                    self._names.scroll_js, required_radiobuttons[0])
                self._actions.wait(0.5)
                self._actions.click(required_radiobuttons[0])
                self._actions.step("-- click radio --")

            except Exception as e:
                print(e)
                self._actions.step("-- no more required radiobuttons")
                break

    def eform_required_checkboxes_input(self):
        """fill eForm all required checboxes and radiobuttons"""

        required_checkbox = self._actions.get_browser().find_all(
            self._pages.eform.eform_required_checkboxes_locator)
        for checkbox in required_checkbox:
            if checkbox.is_displayed():
                self._actions.wait_for_element_displayed(checkbox)
                self._actions.execute_javascript(
                    self._names.scroll_js, checkbox)
                self._actions.wait(0.5)
                self._actions.click(checkbox)
                self._actions.step("-- click radio --")

    def eform_required_fields(self):
        """This function get all eform required fields and input data"""

        eform_required_fields = self._actions.get_browser().find_all(
            self._pages.eform.eform_required_fields_locator)

        for field in eform_required_fields:
            if field.is_displayed():

                self._actions.wait_for_element_enabled(field, timeout=3)
                self._actions.execute_javascript(
                    self._names.scroll_js, field)
                self._actions.wait(0.5)
                if field.tag_name == "input":
                    field_name_attribute = self._actions.get_element_attribute(
                        field, 'name')
                    field_placeholder_attribute = self._actions.get_element_attribute(
                        field, 'placeholder')
                    if field_name_attribute != '':
                        field_name = (field_name_attribute.split('.'))[-1]
                    else:
                        field_name = field_placeholder_attribute

                    # note: 'self._names.fields_value[field_name]' returns a list
                    # and this list is then sent to field. now the list has only one
                    # value, but if there are few values?

                    if field_name in self._names.FIELDS_VALUE["Numbers"].keys():
                        value = random.randrange((self._names.FIELDS_VALUE["Numbers"][field_name][0]),
                                                 (self._names.FIELDS_VALUE["Numbers"][field_name][1]))

                    else:
                        if field_name == 'Value' and 'Email' in str(
                                self._actions.get_element_attribute(field, 'data-val-title')):
                            value = self._names.FIELDS_VALUE["Strings"]['Email'][0]
                        else:
                            value = random.choice(
                                self._names.FIELDS_VALUE["Strings"][field_name]).split('_')[0]

                    self._actions.send_keys(field, value)
                    field.send_keys(Keys.TAB)
                    self._actions.wait_for_element_has_not_attribute(
                        field, 'data-orig-title', 30)
                    if 'ExpectedMarriageDate' in field_name:
                        self._general_helper.wait_for_spinner(spinner_in=30, spinner_out=30)
                    if field_name == 'BirthDate':
                        self._actions.wait(2)

                    try:
                        if field_name in ('UnIncorporatedBusinessName',):
                            self._actions.wait_for_element_displayed(self._pages.eform.pup_information_dialog_close, 5)
                            self._actions.click(self._pages.eform.pup_information_dialog_close)
                            self._actions.wait_for_element_not_displayed(self._pages.eform.pup_information_dialog_close)
                    except Exception as e:
                        print(e)

                elif field.tag_name == 'select':
                    Select(field).select_by_index(1)