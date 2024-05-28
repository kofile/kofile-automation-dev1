from datetime import datetime
from golem.core.exceptions import ElementNotFound

from projects.Kofile.Lib.general_helpers import DATE_PATTERN
from projects.Kofile.Lib.test_parent import LibParent
from projects.Kofile.pages.CRS_OrderSearch import CRSOrderSearch
from selenium.common.exceptions import ElementClickInterceptedException

result_table_all_rows = CRSOrderSearch().result_table_all_rows


class OrderSearch(LibParent):
    def __init__(self):
        super(OrderSearch, self).__init__()

    def verify_order_status(self, expected_status):
        data = self._general_helper.get_data()
        if 'ShowIndexQueue' in self._actions.get_current_url():
            expected_status_localized = expected_status
            order_status_el = self._pages.CRS.indexing_queue.get_order_status_by_number(data["order_number"])
        else:
            expected_status_localized = data['config'].get_status(f'Order_Search.{expected_status}.value')
            order_status_el = self._pages.CRS.order_search.queue_by_order_number(data["order_number"])
        self._actions.verify_element_text(order_status_el, expected_status_localized)

    def verify_order_status_archive(self):
        self.verify_order_status("archive_status")

    def verify_order_status_capture(self):
        self.verify_order_status("capture_status")

    def verify_order_status_voided(self):
        self.verify_order_status("Void_status")

    def verify_order_status_indexing(self):
        self.verify_order_status("indexing_status")

    def verify_order_status_verification(self):
        self.verify_order_status("verification_status")

    def get_ordered_on_string_by_order_number(self, order_number):
        # gets Ordered On as a string
        loc_ordered_on = self._pages.CRS.order_search.ordered_on_by_order_number(order_number)
        ordered_on_string = self._actions.get_element_attribute(loc_ordered_on, 'data-value')
        return ordered_on_string

    def get_ordered_on_date_string_by_order_number(self, order_number):
        # removes the time from Ordered On string
        ordered_on_string = self.get_ordered_on_string_by_order_number(order_number)
        return ordered_on_string.rsplit(' ')[0]

    def get_ordered_on_date_by_order_number(self, order_number):
        # gets Ordered On as a date object for date comparison
        ordered_on_date_string = self.get_ordered_on_date_string_by_order_number(order_number)
        ordered_on_date = datetime.strptime(ordered_on_date_string, DATE_PATTERN).date()
        return ordered_on_date

    def get_order_number_by_row_index(self, row_index):
        loc_order_number = self._pages.CRS.order_search.order_number_by_row_index(row_index)
        order_number = self._actions.get_element_text(loc_order_number)
        return order_number

    def click_pup_in_workflow_btn_yes(self):
        self._general_helper.find_and_click(self._pages.CRS.order_search.pup_in_workflow_btn_yes, timeout=3,
                                            should_exist=False, retries=1)

    def click_edit_icon(self, order_number):
        edit_icon_locator = self._pages.CRS.order_search.edit_order_icon_by_order_number(order_number)
        self._general_helper.wait_and_click(edit_icon_locator)

    def click_email_duplicate_receipt(self):
        self._general_helper.find_and_click(self._pages.CRS.order_search.lnk_email_duplicate_receipt)

    def fill_email_field(self, email):
        self._general_helper.find_and_send_keys(self._pages.CRS.order_search.txt_email_field, email)

    def verify_receipt_message(self, message):
        self._actions.wait_for_element_displayed(self._pages.CRS.order_search.lbl_receipt_message)
        self._actions.verify_element_text(self._pages.CRS.order_search.lbl_receipt_message, message)

    def click_print_duplicate_receipt(self):
        self._general_helper.wait_and_click(self._pages.CRS.order_search.lnk_print_duplicate_receipt)

    def verify_receipt_preview_order_number(self, order_number):
        self._actions.focus_element(self._pages.CRS.order_search.pup_receipt_preview)
        self._actions.verify_element_text(self._pages.CRS.order_search.lbl_receipt_preview_order_number,
                                          f"Order # {order_number}")

    def click_reprint_receipt_icon(self, order_number):
        reprint_receipt_icon_locator = self._pages.CRS.order_search.reprint_receipt_icon_by_order_number(order_number)
        self._general_helper.wait_and_click(reprint_receipt_icon_locator)

    def get_result_table_all_rows(self):
        result_rows = self._general_helper.find_elements(self._pages.CRS.order_search.result_table_all_rows)
        self._actions.store("result_rows", result_rows)
        return result_rows

    def verify_to_date(self, date: str):
        self._actions.verify_element_value(self._pages.CRS.order_search.txt_to_date, date)

    def verify_from_date(self, date: str):
        self._actions.verify_element_value(self._pages.CRS.order_search.txt_from_date, date)

    def click_reset_search(self):
        self._general_helper.scroll_and_click(self._pages.CRS.order_search.lnk_reset_search)

    def fill_date_and_search(self, from_date, to_date):
        self._general_helper.find_and_send_keys(self._pages.CRS.order_search.txt_from_date, from_date)
        self._general_helper.find_and_send_keys(self._pages.CRS.order_search.txt_to_date, to_date)
        self._general_helper.wait_and_click(self._pages.CRS.order_search.btn_search)

    def verify_date_range_validation_text(self, text):
        self._actions.wait_for_element_displayed(self._pages.CRS.order_search.lbl_date_range_validation)
        self._actions.verify_element_text(self._pages.CRS.order_search.lbl_date_range_validation, text)

    def verify_count_of_oits_by_order_number(self, order_number, count_of_oits):
        oit_value_locator = self._pages.CRS.order_search.number_of_order_items_by_order_number(order_number)
        self._actions.verify_element_text(oit_value_locator, str(count_of_oits))

    def verify_doc_number_by_order_number(self, order_number, doc_number):
        doc_number = doc_number if isinstance(doc_number, list) else [doc_number]
        search_doc_number = self._general_helper.find(
            self._pages.CRS.order_search.doc_number_by_order_number(order_number),
            get_text=True)
        assert all(i in search_doc_number for i in doc_number), f"Incorrect document number!\n" \
                                                                f"Expected: {doc_number}\nActual: {search_doc_number}"

    def verify_customer_by_order_number(self, order_number, customer):
        if self.check_order_present_in_result(order_number):
            if self._general_helper.check_if_element_exists(
                    self._pages.CRS.order_search.customer_by_order_number(order_number)):
                customer_locator = self._pages.CRS.order_search.customer_by_order_number(order_number)
            else:
                customer_locator = self._pages.CRS.order_search.customer_by_order_number(order_number,
                                                                                         loc="ErCustomerName")
            self._actions.verify_element_text(customer_locator, customer)
        else:
            self._actions.error(f"Order was not found by order number {order_number}")

    def verify_order_present_in_result(self, order_number):
        if not self.check_order_present_in_result(order_number):
            self._actions.error(f"Order was not found by order number {order_number}")

    def verify_no_matches_found(self):
        self._actions.verify_element_text(self._pages.CRS.order_search.lbl_no_matches_found, "No match found")

    def check_no_matches_found(self):
        no_matches_found = self._general_helper.find(self._pages.CRS.order_search.lbl_no_matches_found,
                                                     should_exist=False)
        if no_matches_found and no_matches_found.text == "No match found":
            return True

    def verify_not_empty_result_or_no_matches_found(self):
        if not self.get_result_table_all_rows():
            self.verify_no_matches_found()

    def check_order_present_in_result(self, order_number):
        order_elements = self._actions.get_browser().find_all(self._pages.CRS.order_search.results_order_column)
        for order_element in order_elements:
            if order_number == order_element.text:
                return True
        return False

    def search_by_more_options(self, field_locator, dropdown, search_data):
        # clicks on More Options, fills the field and clicks on search
        self._actions.wait_for_element_displayed(self._pages.CRS.order_search.lnk_option_pane)
        if self._actions.get_element_text(self._pages.CRS.order_search.lnk_option_pane).lower() == "more options":
            self._actions.click(self._pages.CRS.order_search.lnk_option_pane)
        self._actions.wait_for_element_displayed(field_locator)
        if dropdown:
            self._actions.select_option_by_text(field_locator, search_data)
        else:
            self._actions.send_keys(field_locator, search_data)
        self._general_helper.scroll_and_click(self._pages.CRS.order_search.btn_search)

    def search_by_date_range_and_payment_method(self, from_date, to_date, option_text="Cash"):
        self._actions.wait_for_element_displayed(self._pages.CRS.order_search.lnk_option_pane)
        if self._actions.get_element_text(self._pages.CRS.order_search.lnk_option_pane).lower() == "more options":
            self._actions.click(self._pages.CRS.order_search.lnk_option_pane)
        self._actions.wait_for_element_displayed(self._pages.CRS.order_search.ddl_payment_type)
        self._actions.select_option_by_text(self._pages.CRS.order_search.ddl_payment_type, option_text)
        self.fill_date_and_search(from_date, to_date)

    def search_by_order_number(self, order_number):
        # fills order number and clicks search
        self._general_helper.find_and_send_keys(self._pages.CRS.order_search.txt_order_number, order_number)
        self._general_helper.wait_and_click(self._pages.CRS.order_search.btn_search)

    def search_by_account_code(self, account_code):
        self._general_helper.find_and_send_keys(self._pages.CRS.order_search.txt_account_code, account_code)
        self._general_helper.wait_and_click(self._pages.CRS.order_search.btn_search)

    def search_by_email(self, email_user):
        self._general_helper.find_and_send_keys(self._pages.CRS.order_search.txt_email, email_user)
        self._general_helper.wait_and_click(self._pages.CRS.order_search.btn_search)

    def click_resend_rejection(self, email_user):
        self._general_helper.find_and_send_keys(self._pages.CRS.order_search.txt_resend_rejection, email_user)
        self._general_helper.wait_and_click(self._pages.CRS.order_search.btn_resend_rejection)

    def find_by_params_in_result(self, **kwargs):
        """
        all params optional!
            order_number: str,
            location: str,
            department: str,
            origin: str,
            customer: str,
            ordered_on: str,
            recorded_on: str,
            recorded_by: str,
            order_item_count: str,
            price: str,
            docs_count: str,
            gr_number: str,
            doc_number: str,
            status: str
            }
            """
        all_results = self._general_helper.find_elements(result_table_all_rows)
        assert all_results, f"No search result with locator {result_table_all_rows}"
        data_keys = ("order_number", "location", "department", "origin", "customer", "ordered_on", "recorded_on",
                     "recorded_by", "order_item_count", "price", "docs_count", "gr_number", "doc_number", "status")
        for a, row in enumerate(all_results):
            data = [i.text.strip().lower() for i in row.find_all("td")][3:-8]
            y = dict(zip(data_keys, data))
            shared_items = {k: kwargs[k] for k in kwargs if k in y and kwargs[k] and str(kwargs[k]).lower() == y[k]}
            if len(shared_items) == len(kwargs):
                shared_items["row"] = a
                return shared_items

    def click_on_order_for_edit_payment(self):
        all_results = self._general_helper.find_elements(result_table_all_rows)
        assert all_results, f"No search result with locator {result_table_all_rows}"
        for a, row in enumerate(all_results):
            data = [i.text.strip().lower() for i in row.find_all("td")][3:-8]
            num, loc, dep, orig, customer, od, rd, rec_by, item_count, price, doc_count, gfn, doc_num, status = data
            if price != self._names.zero_price and status in ("archive", "indexing", "capture"):
                try:
                    by, path, desk = self._pages.CRS.order_search.results_edit_column
                    row.find((by, path), timeout=0).click()
                    return status
                except (ElementClickInterceptedException, ElementNotFound):
                    pass

    def click_on_endorse_check_icon(self, order_number):
        icon_locator = self._general_helper.make_locator(
            self._pages.CRS.order_search.icn_endorse_check_by_order_number_,
            order_number)
        self._general_helper.find_and_click(icon_locator)
