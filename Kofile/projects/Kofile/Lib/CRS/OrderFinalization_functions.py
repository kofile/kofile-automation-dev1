from projects.Kofile.Lib.CRS.OrderEntry_functions import OrderEntry
from projects.Kofile.Lib.CRS.OrderHeader_functions import OrderHeader
from projects.Kofile.Lib.test_parent import LibParent
from selenium.common.exceptions import ElementClickInterceptedException
from golem.core.exceptions import ElementNotFound

fee_amount_by_fee_label = OrderEntry().fee_amount_by_fee_label
OrderHeader_functions = OrderHeader()


class OrderFinalization(LibParent):
    def __init__(self):
        super(OrderFinalization, self).__init__()

    def click_edit_order_payments(self):
        # Edit order payments
        self._general_helper.find_and_click(self._pages.CRS.order_finalization.lnk_edit_order_payments)

    def check_not_clickable_edit_order_payments_link(self):
        self._actions.wait_for_element_displayed(self._pages.CRS.order_finalization.lnk_edit_order_payments, 30)
        try:
            self._actions.click(self._pages.CRS.order_finalization.lnk_edit_order_payments)
            raise ElementClickInterceptedException(
                "{} has been clickable".format(self._pages.CRS.order_finalization.lnk_edit_order_payments))
        except (ElementClickInterceptedException, ElementNotFound):
            pass

    def click_edit_order(self, add_pages=0, set_value=False, row=1):
        # Edit order (pencil)

        icn_edit_order = self._general_helper.make_locator(self._pages.CRS.order_finalization.icn_edit_order, row)
        self._general_helper.find_and_click(icn_edit_order)
        if add_pages:
            original_total_fee = fee_amount_by_fee_label("Total:")
            original_pages = int(
                self._general_helper.find(self._pages.CRS.order_entry.txt_no_of_pages, get_attribute="value"))
            if set_value:
                self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.txt_no_of_pages, int(add_pages))
            else:
                self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.txt_no_of_pages,
                                                        int(original_pages) + int(add_pages))
            self._actions.wait(1)
            outstanding_balance = self.close_edit_screen()
            fee_amounts = [original_total_fee, outstanding_balance]
            return fee_amounts

    def close_edit_screen(self):
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_add_to_order)
        if self._general_helper.find(self._pages.CRS.order_entry.pup_orderadmin_bubble, timeout=45, should_exist=False):
            outstanding_balance = fee_amount_by_fee_label("Outstanding Balance Due:")
            self._general_helper.wait_for_element_clickable(self._pages.CRS.order_entry.pup_orderadmin_bubble_OK)
            self._general_helper.scroll_and_click(self._pages.CRS.order_entry.pup_orderadmin_bubble_OK)
            return outstanding_balance

    def get_order_finalization__doc_number(self, get_all=False, with_year=True):
        # Return first doc number with year: '2020-docNumber'
        """
        get_all=True - return list of all document numbers
        get_all=False - return first document number
        with_year=True - return document number with year: '2020-docNumber'
        with_year=False - return document number: 'docNumber'
        """
        doc_num = self._general_helper.find_elements(self._pages.CRS.order_finalization.txt_table_data_doc_number,
                                                     get_text=True)
        if with_year:
            doc_year = self._general_helper.find_elements(self._pages.CRS.order_finalization.txt_table_data_doc_year,
                                                          get_text=True)
            doc_num = [f"{y}-{n}" for y in doc_year for n in doc_num]
        self._actions.step(f"Doc number(s): {doc_num}")
        return doc_num if get_all else doc_num[0]

    def check_order_finalization__order_status(self, expected_status="Finalized"):
        # Check order status
        status = self._general_helper.find_elements(self._pages.CRS.order_finalization.txt_table_data_order_status,
                                                    get_text=True)
        if expected_status:
            expected_status = expected_status if isinstance(expected_status, list) else [expected_status]
            assert expected_status == status, f"Actual 'Order finalization' status(es): {status} " \
                                              f"not equal to expected: {expected_status}"
        return status

    def check_order_finalization__order_total_amount(self, expected_amount=0.00):
        # Check order total amount
        amount = float(
            self._general_helper.find(self._pages.CRS.order_finalization.lbl_total_amount, get_text=True).replace('$',
                                                                                                                  ''))
        if expected_amount is not None:
            assert expected_amount == amount, f"Actual 'Order finalization' TOTAL: {amount} " \
                                              f"not equal to expected: {expected_amount}"
        return amount

    def process_void_order(self, voidable=True, void_oit="ALL", expected_error=None):
        expected_error = "Order cannot be voided. Order contains non-refundable payment method(s)" \
            if not expected_error else expected_error
        self._general_helper.find_and_click(self._pages.CRS.order_finalization.btn_void_order)
        error = self._general_helper.find(("xpath", "//p[@id='VoidOrderError']", "Order cannot be voided error"),
                                          timeout=3, should_exist=False, get_text=True)
        if error or not voidable:
            assert error == expected_error, f"Incorrect void error message! \nExpected: '{expected_error}'" \
                                            f"\nActual: '{error}'"
            return False
        # Fee distribution popup
        self._general_helper.scroll_into_view(self._pages.CRS.void_order_summary.pup_fee_desc_btn_submit)
        # If Void Reports radiobutton exists on Fee Distribution popup
        if self._general_helper.find(self._pages.CRS.void_order_summary.pup_fee_desc_rdb_void_today, timeout=2,
                                     should_exist=False):
            self._general_helper.find_and_click(self._pages.CRS.void_order_summary.pup_fee_desc_rdb_void_today)
        self._general_helper.find_and_click(self._pages.CRS.void_order_summary.pup_fee_desc_btn_submit)
        if void_oit != "ALL":
            # Uncheck OITs for partial void
            void_oit = void_oit if isinstance(void_oit, list) else [void_oit]
            oits = list(range(1, len(self._general_helper.find_elements(                      # noqa
                self._pages.CRS.void_order_summary.void_row_numbers)) + 1))
            uncheck_oit = [i for i in oits if i not in void_oit]
            for i in uncheck_oit:
                self._general_helper.find_and_click(
                    self._general_helper.make_locator(self._pages.CRS.void_order_summary.chk_void_oit_by_row_number,
                                                      i))
        self._general_helper.find_and_click(self._pages.CRS.void_order_summary.btn_void)
        return True

    def void_order_payments__get_all_payment_method_names(self):
        return self._general_helper.find_elements(self._pages.CRS.void_order_payment.col_table_data_payment,
                                                  get_attribute="Value")

    def void_order_payments__get_all_payment_method_amounts(self, check_amounts=False):
        amounts = [float(i) for i in
                   self._general_helper.find_elements(self._pages.CRS.void_order_payment.col_table_data_amount,
                                                      get_attribute="Value")]
        if check_amounts:
            # Sum of negative and positive amounts
            all_amounts = round(sum([i for i in amounts if i < 0]), 2) + round(sum([i for i in amounts if i > 0]), 2)
            assert all_amounts == 0, f"Sum of original and void amounts '{amounts}' not equal to '0'"
        return amounts

    def click_finalize_void_button(self, expected_status="Voided", expected_total=0.00, trigger=None):
        if trigger is None:
            trigger = self._pages.CRS.order_finalization.btn_order_queue
        self._general_helper.scroll_and_click(self._pages.CRS.void_order_payment.btn_finalize_void)
        # Check Comment field if configured
        if self._general_helper.find(self._pages.CRS.void_order_payment.txt_finalize_void_comment, timeout=5,
                                     should_exist=False):
            self._general_helper.find_and_send_keys(self._pages.CRS.void_order_payment.txt_finalize_void_comment,
                                                    "Finalize void comment")
            self._general_helper.find_and_click(self._pages.CRS.void_order_payment.btn_submit_finalize_void_comment)
            self._general_helper.find_and_click(self._pages.CRS.void_order_payment.btn_finalize_void)
        self._general_helper.find(trigger)
        self.check_order_finalization__order_status(expected_status=expected_status)
        self.check_order_finalization__order_total_amount(expected_amount=expected_total)

    def verify_order_status_is_voided(self, row_index=1):
        expected_status = self._general_helper.get_data()['config'].get_status('Order.Void_status.value')
        self.verify_order_status(expected_status, row_index)

    def verify_order_status_is_finalized(self, row_index=1):
        expected_status = self._general_helper.get_data()['config'].get_status('Order.Finalized_status.value')
        self.verify_order_status(expected_status, row_index)

    def verify_order_status(self, expected_status, row_index):
        order_status_el = self._pages.CRS.order_finalization.status_by_row_index(row_index)
        self._actions.verify_element_text(order_status_el, expected_status)

    def click_void_order_button(self):
        self._general_helper.scroll_and_click(self._pages.CRS.order_finalization.btn_void_order)

    def edit_transaction_ids(self):
        rows = self._general_helper.find_elements(self._pages.CRS.void_order_payment.row_numbers)
        self._actions.step(f"{len(rows)} payment rows")
        for row in range(1, len(rows) + 1):
            transaction_id_field = self._pages.CRS.void_order_payment.transaction_id_by_row(row_num=row)
            self._general_helper.find_and_send_keys(transaction_id_field, self._names.ANY_DATA["transaction_id"],
                                                    clear=True)
        self._general_helper.find_and_click(self._pages.CRS.void_order_payment.transaction_id_by_row(row_num=1))

    def get_fund_distribution_total(self):
        self._general_helper.scroll_and_click(self._pages.CRS.order_finalization.lnk_view_edit_order_item_funds)
        self._general_helper.find(self._pages.CRS.order_finalization.pup_fund_dist_btn_submit, wait_displayed=True)
        fund_dist_total = self._general_helper.find(self._pages.CRS.order_finalization.pup_fund_dist_lbl_total_actual,
                                                    get_text=True)[1:]
        return fund_dist_total

    def get_number_of_rows(self):
        # Get rows count
        return len(self._actions.get_browser().find_all(self._pages.CRS.order_finalization.row_numbers))

    def fill_refund_address(self):
        # if refund to address is required, fill it
        if self._general_helper.find(self._pages.CRS.order_header.lbl_address_is_required, timeout=3,
                                     wait_displayed=True,
                                     should_exist=False):
            self._general_helper.scroll_and_click(self._pages.CRS.order_header.lnk_more_option)
            self._general_helper.find(self._pages.CRS.add_payment.txt_refund_to_name, wait_displayed=True)
            OrderHeader_functions.fill_required_fields()
            return True
        return False
        # else:
        # self._actions.step("Refund address is not required")

    def process_through_admin_payment_screen(self):
        from projects.Kofile.Lib.CRS.AdminPayment_functions import AdminPayment
        from projects.Kofile.Lib.CRS.AddPayment_functions import AddPayment

        self._general_helper.scroll_and_click(self._pages.CRS.add_payment.btn_checkout)
        required = self.fill_refund_address()
        if required:
            AddPayment().fill_in_payment_method_comment(row=2, comment=False)
            self._general_helper.scroll_and_click(self._pages.CRS.add_payment.btn_checkout)
            AdminPayment().add_checkout_comment()
        self._general_helper.find(self._pages.CRS.order_finalization.btn_void_order, wait_displayed=True)

    def send_email_receipt_address(self, address):
        self._general_helper.find_and_send_keys(self._pages.CRS.order_finalization.lbl_email_address, str(address))
        self._general_helper.scroll_and_click(self._pages.CRS.order_finalization.btn_send_email_rec)

    def validate_email_receipt_dialog_popup_message(self, message):
        self._actions.wait_for_element_displayed(self._pages.CRS.order_finalization.lbl_receipt_message)
        self._actions.verify_element_text(self._pages.CRS.order_finalization.lbl_receipt_message, message)

    # ---------------------------------------------------------------------------------------------------------------
    # FUND DISTRIBUTIONS

    def get_actual_fund_amounts(self, message=False):
        self.click_edit_order()
        self._general_helper.scroll_and_click(self._pages.CRS.order_entry.lnk_fund_distribution)
        self._actions.wait_for_element_displayed(self._pages.CRS.order_entry.btn_submit_distribution_popup)
        number_of_funds = len(self._general_helper.find_elements(self._pages.CRS.order_entry.lbl_fund_desc))
        actual_fund_values = []
        actual_fund_value_els = self._general_helper.find_elements(self._pages.CRS.order_entry.lbl_fund_value)
        for actual_fund_value_el in actual_fund_value_els:
            actual_fund_values.append(float(self._actions.get_element_text(actual_fund_value_el).split('$')[1]))
        total_amount = float(self._actions.get_element_text(self._pages.CRS.order_entry.total_fee_fund).split('$')[1])
        if message:
            self._general_helper.find(self._pages.CRS.order_finalization.pup_fund_dist_penalty_message)
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_close_distribution_popup)
        return number_of_funds, actual_fund_values, total_amount
    # ---------------------------------------------------------------------------------------------------------------

    def get_price_by_row_index(self, row_num=1):
        return float(self._general_helper.find(
            self._pages.CRS.order_finalization.price_by_row_index(row_num), get_text=True).replace('$', ''))

    def get_order_total(self):
        return float(self._general_helper.find(self._pages.CRS.order_finalization.lbl_total_amount,
                     get_text=True).replace('$', ''))
