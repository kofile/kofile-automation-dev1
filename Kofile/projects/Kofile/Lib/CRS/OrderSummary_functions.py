from datetime import datetime
from projects.Kofile.Lib.CRS.OrderEntry_functions import OrderEntry
from projects.Kofile.Lib.test_parent import LibParent

OrderEntry_functions = OrderEntry()


class OrderSummary(LibParent):
    def __init__(self):
        self.process_attachment = self.process_attachment_from_capture_summary_48000
        super(OrderSummary, self).__init__()

    def __48999__(self):
        self.process_attachment = self.process_attachment_from_capture_summary_48999

    # ---------------------------------------------
    # Tracking ID
    def click_add_tracking_id_button(self):
        self._general_helper.find_and_click(self._pages.CRS.order_summary.lbl_add_tracking_id)
        self._general_helper.find(self._pages.CRS.order_summary.txt_add_tracking_id)

    def fill_in_tracking_id(self, t_id=None):
        t_id = t_id if t_id else datetime.now().strftime("%Y%m%d%H%M%S")
        self._general_helper.find_and_send_keys(self._pages.CRS.order_summary.txt_add_tracking_id, t_id)
        return t_id

    def submit_tracking_id(self):
        self._general_helper.find_and_click(self._pages.CRS.order_summary.btn_submit_tracking_id)
        self._general_helper.wait_for_element_clickable(self._pages.CRS.order_summary.lbl_remove_tracking_id)
        self._general_helper.wait_disappear_element(self._pages.CRS.order_summary.btn_submit_tracking_id)
      
    def click_remove_tracking_id_button(self):
        self._general_helper.find_and_click(self._pages.CRS.order_summary.lbl_remove_tracking_id)
        self._general_helper.wait_disappear_element(self._pages.CRS.order_summary.lbl_remove_tracking_id, 3)

    # ---------------------------------------------

    def click_order_summary_checkout_button(self, should_be_enabled=True):
        # Check 'Order Summary' Checkout button enabled/disabled
        checkout = self._general_helper.find(self._pages.CRS.order_summary.btn_checkout, 60, get_attribute="disabled")
        if should_be_enabled and checkout:
            raise ValueError("Order summary 'Checkout' button unexpectedly disabled")
        if not should_be_enabled and not checkout:
            raise ValueError("Order summary 'Checkout' button unexpectedly enabled")
        # Click 'Order Summary' Checkout button
        if self._general_helper.find(self._pages.CRS.order_summary.div_overlaying_checkout, 30, should_exist=False):
            self._actions.wait_for_element_not_present(self._pages.CRS.order_summary.div_overlaying_checkout)
        self._general_helper.scroll_and_click(self._pages.CRS.order_summary.btn_checkout)

    def click_edit_icon_by_row_index(self, row):
        self._general_helper.wait_and_click(self._pages.CRS.order_summary.editicon_by_row_index(row))
        self._actions.wait_for_element_displayed(self._pages.CRS.order_entry.btn_add_to_order)

    def click_delete_icon_by_row_index(self, row):
        self._general_helper.find_and_click(self._pages.CRS.order_summary.delete_row_by_row_index(row))
        self._general_helper.wait_for_spinner()

    def get_number_of_rows(self):
        # Get rows count
        return len(self._actions.get_browser().find_all(self._pages.CRS.order_summary.row_numbers))

    def enter_serial_number(self, row=1):
        self._general_helper.scroll_and_click(self._pages.CRS.order_summary.serial_num_by_row_index(row))
        self._actions.wait_for_element_present(self._pages.CRS.order_summary.btn_serial_number_submit)
        self._actions.mouse_over(self._pages.CRS.order_summary.btn_serial_number_cancel)
        # input serial number until accepted
        retries = 5
        while retries:
            try:
                random_sn = self._general_helper.random_string(5, 1)
                self._general_helper.find_and_send_keys(self._pages.CRS.order_summary.txt_start_serial_number,
                                                        random_sn)
                self._general_helper.find_and_click(self._pages.CRS.order_summary.btn_serial_number_submit)
                self._actions.store("serial_number", random_sn)
                return
            except Exception as e:
                retries -= 1
                self._actions.execution.logger.info(f"Serial Number already exists: \n{e}")

    def copy_oit(self, order_item_quantity=None, row_index=1):
        copy_icon_el = self._general_helper.make_locator(self._pages.CRS.order_summary.icn_copy_orderitem, row_index)
        self._general_helper.scroll_and_click(copy_icon_el)
        order_item_quantity = order_item_quantity if order_item_quantity else self._names.ANY_DATA[
            'order_item_quantity']
        self._general_helper.find_and_send_keys(self._pages.CRS.order_summary.txt_quantity_field, order_item_quantity)
        self._general_helper.wait_and_click(self._pages.CRS.order_summary.btn_copy_oit_submit, enabled=True,
                                            scroll=True)
        self._general_helper.wait_for_spinner()
        return order_item_quantity

    def click_cancel_entire_order(self):
        self._general_helper.scroll_and_click(self._pages.CRS.order_summary.lnk_cancel_entire_order)

    def get_status_by_row_index(self, row):
        return self._general_helper.find(self._pages.CRS.order_summary.status_by_row_index(row), wait_displayed=True,
                                         get_text=True)

    def verify_status_by_row_index(self, status, row=1):
        status_summary = self.get_status_by_row_index(row)
        assert status_summary == status, f"Expected status: {status} is not equal to actual: '{status_summary}'"

    def get_type_by_row_index(self, row):
        return self._general_helper.find(self._pages.CRS.order_summary.type_by_row_index(row), wait_displayed=True,
                                         get_text=True)

    def verify_type_by_row_index(self, order_type, row=1):
        ot_summary = self.get_type_by_row_index(row)
        assert order_type == ot_summary, f"Expected order type: {order_type} is not equal to actual: '{ot_summary}'"

    def click_new_order_item_icon(self):
        self._general_helper.find_and_click(self._pages.CRS.order_summary.lnk_new_order_item)

    def click_return_to_scan_documents_link(self):
        self._general_helper.find_and_click(self._pages.CRS.order_summary.lnk_return_to_scan_documents)
        self._actions.wait_for_window_present_by_partial_url("/Order/ScanDocuments")

    def apply_discount(self, discount_type="100%", comment="test-comment"):
        self._actions.click(self._pages.CRS.order_summary.btn_discount_dropdown)
        self._actions.click(
            self._general_helper.make_locator(self._pages.CRS.order_summary.lbl_discount_by_value, discount_type))
        self._actions.wait_for_element_enabled(self._pages.CRS.order_summary.btn_discount_apply)
        self._actions.click(self._pages.CRS.order_summary.btn_discount_apply)
        self._actions.wait_for_element_displayed(self._pages.CRS.order_summary.pup_discount_txt_comment)
        self._actions.send_keys(self._pages.CRS.order_summary.pup_discount_txt_comment, comment)
        self._actions.wait_for_element_enabled(self._pages.CRS.order_summary.pup_discount_btn_submit)
        self._actions.click(self._pages.CRS.order_summary.pup_discount_btn_submit)
        self._actions.wait_for_element_not_present(self._pages.CRS.order_summary.pup_discount_txt_comment)
        price = self._actions.get_element_text(self._pages.CRS.order_summary.price_by_row_index())
        return price

    def process_attachment_from_capture_summary_48999(self):
        self._general_helper.wait_for_element_clickable(self._pages.CRS.capture_summary.edit_icon_attachment)
        self._general_helper.find_and_click(
            self._pages.CRS.capture_summary.edit_icon_attachment)
        data = self._general_helper.get_data()
        self._general_helper.find_and_send_keys(
            self._pages.CRS.capture_summary.inp_doc_type_attachment, data.doc_type)
        self._general_helper.wait_for_spinner()
        self._general_helper.find_and_click(
            self._pages.CRS.capture_summary.edit_icon_attachment)

    def process_attachment_from_capture_summary_48000(self, row_num=1):
        pass

    def scan_attachment(self):
        self.click_edit_icon_by_row_index(row=1)
        self._general_helper.find_and_click(OrderEntry_functions.tab_locator('Attachments'))
        self._general_helper.find_and_click(self._pages.CRS.edit_order_item.lnk_start_capture_to_scan_attachments)
        self._general_helper.wait_for_spinner()
        self._general_helper.find_and_click(self._pages.CRS.capture_summary.btn_start_scan)
        self._general_helper.wait_for_spinner()
        self._actions.wait_for_element_displayed(self._pages.CRS.capture_summary.lbl_scan_progress_bar)
        self._actions.wait_for_element_not_displayed(self._pages.CRS.capture_summary.lbl_scan_progress_bar, 60)
        self.process_attachment()
        self._actions.wait_for_element_enabled(self._pages.CRS.capture_summary.btn_save_and_exit)
        self._general_helper.find_and_click(self._pages.CRS.capture_summary.btn_save_and_exit)
        self._general_helper.wait_for_spinner()
        filename = self._general_helper.find(self._pages.CRS.edit_order_item.lbl_attached_filename, get_text=True)
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_add_to_order)
        self._general_helper.wait_for_spinner()
        return filename

    def get_order_item_price(self, row_num=1):
        return float(self._general_helper.find(
            self._pages.CRS.order_summary.price_by_row_index(row_num), get_text=True).replace('$', ''))

    def get_order_total(self):
        return float(self._general_helper.find(self._pages.CRS.order_summary.lbl_total_price,
                     get_text=True).replace('$', ''))
