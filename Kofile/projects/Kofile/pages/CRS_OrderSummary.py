"""Order Summary Page Object Model"""

# ---------------------------------------------
# breadcrump
# ---------------------------------------------
from projects.Kofile.Lib.test_parent import PagesParent
from projects.Kofile.pages.CRS_General import General as CRS_General


class CRSOrderSummary(PagesParent):
    doc_number = "documentNumber"

    def __init__(self):
        super(CRSOrderSummary, self).__init__()

    def __48999__(self):
        self.doc_number = "Document_DocAndAppNum"

    lbl_ordersummary_breadcrump = (
        'xpath'
        "//*[@class='bredcrum']//child::li[last()]/text()",
        'Order Summary breadcrump')
    # ---------------------------------------------
    lbl_order_number = (
        "id",
        "orderNumber",
        "Order Number"
    )

    print_barcode_btn = (
        'xpath',
        "//a[@title='Print barcode']",
        "Print barcode"
    )

    # ---------------------------------------------
    txt_order_id = (
        "xpath",
        "//input[@id='orderId']",
        "Order ID"
    )
    # ---------------------------------------------
    # Tracking ID
    # ---------------------------------------------
    lbl_add_tracking_id = (
        "xpath",
        "//a[@id='addTrackingId']",
        "Add Tracking ID label"
    )
    # ---------------------------------------------
    txt_add_tracking_id = (
        "xpath",
        "//div[@id='trakingIdBlock-items']//input[@id='trackingId']",
        "Add Tracking ID field"
    )
    btn_submit_tracking_id = (
        "xpath",
        "//a[@id='copyOrderItemBtn']",
        "Submit Tracking ID button"
    )
    # ---------------------------------------------
    lbl_remove_tracking_id = (
        "xpath",
        "//a[@id='removeTrackingId' and text()]",
        "Remove Tracking ID label"
    )
    # ---------------------------------------------
    # table data
    # ---------------------------------------------
    _lbL_table_oit_type_by_row = (
        'xpath',
        "//*[@id='OrderQueue']/tbody/tr[%s]/td[(@data-column= '%s')]/span[1]",
        'Order Summary oit type by row'
    )
    _lbl_table_data_by_row_by_column_index = (
        "xpath",
        "//table[@id='OrderQueue']/tbody/tr[%s]/td[%s]",
        "Order Summary table data row index by row, by column index"
    )
    _lbl_discount_ddl_by_row_by_column_index = (
        "xpath",
        "//table[@id='OrderQueue']/tbody/tr[%s]/td[%s]//span",
        "Order Summary table data row index by row, by column index"
    )
    _lbl_table_data_by_row_by_column_name = (
        'xpath',
        "//*[@id='OrderQueue']/tbody/tr[%s]/td[(@data-column= '%s')]",
        'Order Summary table data  by row by column name')

    _icn_oit_edit = (
        'xpath',
        "//*[@id='OrderQueue']/tbody/tr[%s]//a[@class ='orderSummaryiconedit' ]",
        'Order Item Edit')

    _btn_oit_delete = (
        'xpath',
        ".//*[@id='OrderQueue']/tbody/tr[%s]/td[@class='orderSummaryiconcloseContainer']/a",
        'OrderItem Delet button')
    btn_oit_delete_all = (
        'xpath',
        "//a[contains(@class, 'paymentMethodRowDelete')]",
        'OrderItem Delet button for all rows'
    )
    row_numbers = (
        'xpath',
        "//*[@id='OrderQueue']//tbody/tr/td[last()-1]|td[last()]",
        "OIT's rows in Order Summary"
    )
    _cbx_by_row_by_column_index = (
        "xpath",
        "//table[@id='OrderQueue']/tbody/tr[%s]/td[%s]/a",
        "Checkbox in Order Summary"
    )

    # ---------------------------------------------
    # Copy OIT
    # ---------------------------------------------
    icn_copy_orderitem = (
        'xpath',
        "//*[@id='OrderQueue']/tbody/tr[%s]//a[@class='copyOrderItem']",
        'Copy OrderItem')

    txt_quantity_field = (
        'xpath',
        ".//*[@id='numItems']",
        'Copy Order Item Quantity Field')

    btn_copy_oit_submit = (
        'xpath',
        ".//*[@id='copyOrderItemBtn']",
        'Copy oit submit')

    btn_copy_oit_cancel = (
        'xpath',
        ".//*[@id='widget-kofileinfobubble-cancelui-id1']",
        'Copy oit submit')

    # ---------------------------------------------
    # serial number
    # ---------------------------------------------
    _icn_serial_number_by_row_index = (
        'xpath',
        "//*[@id='OrderQueue']/tbody/tr[%s]/td[@class = 'serialNumberIconContainer']/a ",
        'Order Summary Serial Number')

    txt_start_serial_number = (
        'xpath',
        "//*[@id='setSerialNumbeContent']//input[contains(@class, 'startNumber')]",
        'Start Serial Number field')

    txt_end_serial_number = (
        'xpath',
        "//*[@id='setSerialNumbeContent']//input[contains(@class, 'endNumber')]",
        'Start Serial Number field')

    btn_serial_number_submit = (
        'id',
        "setSerialNumberBtn",
        'Serial Number Submit button')

    btn_serial_number_cancel = (
        'id',
        "cancelSerialNumberBtn",
        'Serial Number Cancel button')

    # ---------------------------------------------
    # discount comment popup
    # ---------------------------------------------
    btn_discount_dropdown = (
        'xpath',
        "//*[@class = 'dropdown-arrow']",
        'Order Summary Discount dropdown')

    lbl_discount_by_value = (
        'xpath',
        "//*[@id='discountField_0']/li[contains(./text(), '%s')]",
        '100 percent discount')

    btn_discount_apply = (
        'xpath',
        ".//*[@class='applyDiscount']",
        'Apply Discount')

    btn_discount_reset = (
        'xpath',
        ".//*[@class='resetDiscount']",
        'Reset Discount')

    pup_discount_txt_comment = (
        "xpath",
        "//div[@id='setOrderSummaryBubbleContent']/div[1]/input",
        "Discount popup comment field")

    pup_discount_btn_cancel = (
        "id",
        "cancelOrderCommentBtn",
        "Discount popup Cancel button")

    pup_discount_btn_submit = (
        "id",
        "submitlOrderCommentBtn",
        "Discount popup Submit button")

    # ---------------------------------------------
    # total
    # ---------------------------------------------
    lbl_total_price = (
        'id',
        "orderTotalAmt",
        'Order Summary Total Amount')

    # ---------------------------------------------
    # action links
    # ---------------------------------------------

    # new order item
    lnk_new_order_item = (
        'xpath',
        ".//*[@id='newOrderItem']/a",
        'New Order Item')

    lnk_return_to_scan_documents = (
        'xpath',
        "//a[contains(@data-bind, 'returnToScanDocumetns')]",
        'Return to scan documents')

    # Cancel Entire Order
    lnk_cancel_entire_order = (
        'xpath',
        ".//*[@id='cancelEntireOrder']",
        'Cancel Entire Order')

    pup_Cancel_entire_order_reason = CRS_General.pup_cancel_txt_reason

    pup_Cancel_Entire_Order_description = CRS_General.pup_cancel_txt_description

    pup_btn_cancel_entire_order_submit = CRS_General.pup_cancel_btn_submit

    pup_btn_cancel_entire_order_cancel = CRS_General.pup_cancel_btn_cancel

    # Reject Entire Order
    lnk_reject_entire_order = (
        'xpath',
        "//a[text()='Reject Entire Order']",
        'Reject Entire Order')

    pup_reject_entire_order_action = (
        'xpath',
        '//*[@id="actionTemplate"]',
        'Action ddl in Reject Entiore Order popup')

    pup_action_reason_filter = (
        'xpath',
        '//*[@id="actionReasonFilter"]',
        'Action Reason filter field'
    )

    first_action_reason = (
        'xpath',
        '//*[@id="actionReason1"]',
        "First Action Reason"
    )

    pup_reject_entire_order_reason = CRS_General.pup_cancel_txt_reason
    pup_reject_entire_order_description = CRS_General.pup_cancel_txt_description

    pup_btn_reject_entire_order_submit = CRS_General.pup_cancel_btn_submit

    pup_btn_reject_entire_order_cancel = CRS_General.pup_cancel_btn_cancel

    # return to order queue
    lnk_return_to_order_queue = (
        'xpath',
        "//*[@id='backtoOrderQueue']",
        'Return to Order Queue')

    # send to administrator
    lnk_send_to_admin = (
        'xpath',
        "//*[@id='sendToAdministrator']",
        'Send to Administrator')

    txt_send_to_admin_description = CRS_General.pup_cancel_txt_description
    pup_btn_send_to_admin_submit = CRS_General.pup_cancel_btn_submit
    pup_btn_send_to_admin_cancel = CRS_General.pup_cancel_btn_cancel

    txt_review_warning = (
        'xpath',
        "//p[@class='warningRev']",
        'Review warning(s)')
    # ---------------------------------------------
    # buttons
    # ---------------------------------------------
    btn_checkout = (
        'id',
        'orderSummaryCheckout',
        'Order Summary Checkout')

    btn_save_order = (
        'id',
        'saveOrderLaterCheckout',
        'Save Order button in OrerSummary')

    div_overlaying_checkout = (
        'xpath',
        '//div[@class="parent-overlay"]',
        'Div overlaying summary page checkout'
    )

    def type_by_row_index(self, row_num=1):
        """
        returns OIT type locator by row_index
        """
        return self.__table_data(row_num, "OrderItemType_Value")

    def doc_type_by_row_index(self, row_num=1):
        """
        returns document type locator by row_index
        """
        return self.__table_data(row_num, "DocumentType")

    def number_of_by_row_index(self, row_num=1):
        """
        returns number of locator by row_index
        """
        return self.__table_data(row_num, "NoOfPageOrCopy")

    def price_by_row_index(self, row_num=1):
        """
        returns price locator by row_index
        """
        return self.__table_data(row_num, "Price")

    def discount_by_row_index(self, row_num=1):
        """
        returns discount locator by row_index
        """
        return self.__table_data(row_num, "OrderItemDiscount")

    def discount_ddl_by_row_index(self, row_num=1):
        """
        returns discount dropdown locator by row_index
        """
        return self.__table_data(row_num, "DiscountDropdown")

    def year_by_row_index(self, row_num=1):
        """
        returns year locator by row_index
        """
        return self.__table_data(row_num, "RecordedYear")

    def docnumber_by_row_index(self, row_num=1):
        """
        returns docnum locator by row_index
        """
        return self.__table_data(row_num, self.doc_number)

    def status_by_row_index(self, row_num=1):
        """
        returns status locator by row_index
        """
        return self.__table_data(row_num, "OrderItemStatus")

    def prioritize_by_row_index(self, row_num=1):
        """
        returns re-prioritize arrow on row by row index
        """
        return self.__table_data(row_num, "PrioritizeOrderItems")

    def editicon_by_row_index(self, row_num=1):
        """
        returns edit icon locator by row_index
        """
        return self.__table_data(row_num, "orderSummaryEdit")

    def copyoit_by_row_index(self, row_num=1):
        """
        returns copy oit locator by row_index
        """
        return self.__table_data(row_num, "copyOrderItem")

    def serial_num_by_row_index(self, row_num=1):
        """
        returns serial_num locator by row_index
        """
        return self.__table_data(row_num, "SerialNumber")

    def printdoc_image_by_row_index(self, row_num=1):
        """
        returns printdoc_image locator by row_index
        """
        return self.__table_data(row_num, "PrintDocumentImage")

    def printapp_image_by_row_index(self, row_num=1):
        """
        returns prin application locator by row_index
        """
        return self.__table_data(row_num, "printDocumentLabel")

    def delete_row_by_row_index(self, row_num=1):
        """
        returns  delete_row locator by row_index
        """
        return self.__table_data(row_num, "deleteOrderItem")

    def checkbox_by_row_index(self, row_num=1):
        """
        returns  checkbox locator by row_index
        """
        return self.__table_data(row_num, "Checkbox")

    @staticmethod
    def __table_data(row_num, queue_column_name):
        locator = ("xpath", f"//tr[{row_num}]//*[contains(@data-bind, '{queue_column_name}')]",
                   f"Result table '{queue_column_name}' column")
        return locator
