"""Properties and methods of Inbox popup"""
from golem.webdriver.extended_webelement import Select

from projects.Kofile.Lib.test_parent import LibParent
import time


class PSInbox(LibParent):
    def __init__(self):
        super(PSInbox, self).__init__()

    def comment(self, set_value=""):
        """
        If set_value - empty string, returns field's value as string.
        If set_value - not empty string, sets new value for the field.
        """
        if not set_value:
            el = self._general_helper.find(self._pages.PS.inbox.comment)
            # return field value
            return el.get_attribute("value")
        else:
            # set field value
            self._general_helper.find_and_send_keys(self._pages.PS.inbox.comment, set_value)

    def customer_name(self, set_value=""):
        """
        If set_value - empty string, returns field's value as string.
        If set_value - not empty string, sets new value for the field.
        """
        if not set_value:
            el = self._general_helper.find(self._pages.PS.inbox.customer)
            # return field value
            return el.get_attribute("value")
        else:
            # set field value
            self._general_helper.find_and_send_keys(self._pages.PS.inbox.customer, set_value)

    def order_type_options(self):
        """
        Returns a list of strings of available options
        In case of exception returns empty list
        """
        self._general_helper.find(
            self._general_helper.remake_locator(self._pages.PS.inbox.order_type_options, "[last()]"))
        res = self._general_helper.find_elements(self._pages.PS.inbox.order_type_options, get_text=True)
        return res

    def select_order_type(self, option):
        """
        Selects Order Type from dropdown list. Returns True if Ok, False - otherwise
        option - string, representing one of the dropdown list options
        """
        self._general_helper.find(self._pages.PS.inbox.order_type)
        all_options = self._general_helper.find_elements(self._general_helper.remake_locator(
            self._pages.PS.inbox.order_type, "/option"), get_text=True)
        assert option in all_options, f"Expected option '{option}' not found in options list: {all_options}"
        self._actions.step(f"-> Select '{option}'")
        Select(self._general_helper.find(self._pages.PS.inbox.order_type)).select_by_visible_text(option)
        return True

    def label(self):
        """
        Returns label value as string
        """
        el = self._general_helper.find(self._pages.PS.inbox.label, get_text=True)
        return el.text

    def click_clear_inbox(self):
        """
        Clicks Clear Inbox link
        """
        self._general_helper.find_and_click(self._pages.PS.inbox.clear_inbox)
        return True

    def click_cancel(self):
        """
        Clicks Cancel link
        """
        self._general_helper.find_and_click(self._pages.PS.inbox.cancel)

    def click_submit(self):
        """
        Clicks Submit button
        """
        self._actions.wait(0.5)
        self._general_helper.find_and_click(self._pages.PS.inbox.submit)

    def table_row_count(self, should_be):
        """
        Returns an integer representing table row count in Inbox, when
        table rows are fully loaded
        should_be - number of items that should be in Inbox as string,
        use psmainpage.inbox_item_count() method to get this value
        """
        tm = time.time() + 30
        res = self._general_helper.find_elements(self._pages.PS.inbox.table_rows)
        # waiting for the first row
        while res is None and tm > time.time():
            time.sleep(1)
            res = self._general_helper.find_elements(self._pages.PS.inbox.table_rows)
        if res is None:
            return -1
        # waiting for another rows
        tm = time.time() + 30
        res = self._general_helper.find_elements(self._pages.PS.inbox.table_rows)
        while len(res) != int(should_be) and tm > time.time():
            time.sleep(1)
            res = self._general_helper.find_elements(self._pages.PS.inbox.table_rows)
        if len(res) != int(should_be):
            return -1
        else:
            time.sleep(1.5)
            return len(res)

    def table_row(self, index):
        """
        Returns a list of strings of row data in a format: [DocType, Doc#, RecDate, #ofPages]
        index - integer, row index, starting from 1
        """
        locators = [self._general_helper.remake_locator(self._pages.PS.inbox.table_rows, i)
                    for i in [f"[{index}]/td[2]", f"[{index}]/td[3]", f"[{index}]/td[4]/span", f"[{index}]/td[5]"]]
        res_lst = [self._general_helper.find(locator).text for locator in locators]
        return res_lst

    def delete_table_row(self, index):
        """
        Deletes data row. Data row is specified by index (integer).
        index - integer, starts from 1
        """
        self._general_helper.find_and_click(
            self._general_helper.remake_locator(self._pages.PS.inbox.table_rows, f"[{index}]/td[6]/a"))

    def confirmation_order_number(self):
        """
        Returns Order Number as string from Order Confirmation popup
        """
        # Wait until 'Order Confirmation' pop-up appears
        self._general_helper.find(self._pages.PS.inbox.order_confirmation_pop_up, 60)
        return self._general_helper.find(self._pages.PS.inbox.conf_order_number, get_text=True)

    def confirmation_order_number_multi(self, row):
        """Returns Order Number as string from Order Confirmation popup
         for appropriate row.
         Make sure there are more than one rows in Confirmation popup.

         row - integer, confirmation popup row, starting from 1"""
        self._general_helper.find(self._pages.PS.inbox.conf_close)
        res = self._general_helper.find(self._general_helper.remake_locator(
            self._pages.PS.inbox.conf_order_number_multi_1,
            f"{row + 1}{self._pages.PS.inbox.conf_order_number_multi_2}"),
            get_text=True)
        return res

    def confirmation_number_of_docs(self):
        """
        Returns Number of Documents as string from Order Confirmation popup
        """
        self._general_helper.find(self._pages.PS.inbox.conf_close)
        res = self._general_helper.find(self._pages.PS.inbox.conf_number_of_docs, get_text=True)
        return res

    def confirmation_close(self):
        """
        Closes Order Confirmation popup
        """
        self._general_helper.find_and_click(self._pages.PS.inbox.conf_close)
