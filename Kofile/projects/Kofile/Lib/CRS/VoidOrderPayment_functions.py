from projects.Kofile.Lib.CRS.OrderHeader_functions import OrderHeader
from projects.Kofile.Lib.test_parent import LibParent

OrderHeader_functions = OrderHeader()


class VoidOrderPayment(LibParent):
    def __init__(self):
        super(VoidOrderPayment, self).__init__()

    def clear_transaction_id_fields_and_fill_again(self):
        rows_number = len(self._actions.get_browser().find_all(self._pages.CRS.void_order_payment.row_numbers))
        self._actions.step(f"Rows number: {rows_number}")
        for row in range(1, rows_number + 1):
            transaction_id_field = self._pages.CRS.void_order_payment.transaction_id_by_row(row_num=row)
            self._actions.clear(transaction_id_field)
            self._actions.send_keys(transaction_id_field, self._names.ANY_DATA["transaction_id"])
        self._actions.click(self._pages.CRS.void_order_payment.transaction_id_by_row(row_num=1))

    def fill_and_submit_finalize_void_comment_if_exists(self):
        try:
            self._general_helper.find_and_send_keys(self._pages.CRS.void_order_payment.txt_finalize_void_comment,
                                                    self._names.ANY_DATA["void_comment_popup"])
        except Exception as e:
            print(e)
            self._actions.step("Comment is not displayed")
        else:
            self._actions.click(self._pages.CRS.void_order_payment.btn_submit_finalize_void_comment)
            self.click_finalize_void_button()

    def click_finalize_void_button(self):
        self._actions.wait_for_element_enabled(self._pages.CRS.void_order_payment.btn_finalize_void)
        self._general_helper.scroll_and_click(self._pages.CRS.void_order_payment.btn_finalize_void)

    def fill_refund_to_fields_if_exist(self):
        attribute_style = str(
            self._actions.get_browser().find(self._pages.CRS.order_header.lbl_address_is_required).get_attribute(
                'style'))
        if "display: none" not in attribute_style:
            self._logging.info(f"{self._pages.CRS.order_header.lbl_address_is_required[2]} is displayed")
            self._actions.click(self._pages.CRS.order_header.lnk_more_option)
            self._actions.wait_for_element_visible(self._pages.CRS.order_header.lbl_refund_to)
            OrderHeader_functions.fill_required_fields()
