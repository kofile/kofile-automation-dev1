"""
Order Search Page Object Model
"""
from projects.Kofile.Lib.test_parent import PagesParent


class CRSOrderSearch(PagesParent):
    def __init__(self):
        super(CRSOrderSearch, self).__init__()

    lnk_go_to_order_search = ("xpath", "//li[@id='searching']/a", "Go to 'Order Search' page")
    lnk_go_to_packages = ("xpath", "//li[@id='packageSearch']/a", "Go to 'Packages' page")
    txt_order_number = ("id", "OrderNumber", "Order Number field")
    txt_account_code = ("id", "AccountCode", "Account Code field")
    txt_email = ("id", "EmailId", "Email field")
    rdb_order_date_range = ("id", "orderDateRadio", "Order Date Range")
    rdb_recorded_date_range = ("id", "recordedDateRadio", "Recorded Date Range")
    txt_from_date = ("id", "FromDate", "From Date field")
    btn_from_date_picker = ("xpath", "//div[@id='daterange-block']/img[1]", "From Date date picker")
    txt_to_date = ("id", "ToDate", "To Date field")
    btn_to_date_picker = ("xpath", "//div[@id='daterange-block']/img[2]", "To Date date picker")
    lbl_date_range_validation = ("id", "birtherror", "Date range validation message")
    btn_search = ("id", "search", "Search button")
    lnk_last_search = ("xpath", "//div[@id='criteriaSearchBlock']/a[1]", "Last search criteria action link")
    lnk_reset_search = ("id", "resetOrderSearch", "Reset Search action link")
    # MORE OPTIONS SECION-----------------------------------------------------------------------------------------------
    lnk_option_pane = ("xpath", "//div[@id='links-block']/span[1]/a[1]", "More / Less Options action link")
    lnk_more_options = ("xpath", "//a[@class='moreOption']", "More options button")
    txt_name = ("id", "Name", "Name field in option pane")
    txt_more_options_phone_number = ("id", "PhoneNumber", "More Options, Phone Number field")
    txt_tracking_id = ("id", "TrackingId", "Tracking ID in option pane")
    ddl_location = ("id", "LocationId", "Location dropdown in option pane")
    ddl_department = ("id", "DepartmentId", "Department dropdown in option pane")
    ddl_origin = ("id", "OriginId", "Origin dropdown in option pane")
    ddl_assigned_to = ("id", "AssignedTo", "AssignedTo dropdown in option pane")
    ddl_payment_type = ("id", "OrderPaymentTypeId", "Payment Type dropdown in option pane")
    txt_transaction_id = ("id", "OrderPaymentId", "Transaction Id field in option pane")
    txt_serial_number = ("id", "SerialNumber", "Serial Number field in option pane")
    txt_gf_number = ("id", "GFNumber", "GF Number field in option pane")
    txt_doc_number_from = ("id", "docNumberStart", "Document Number from field")
    txt_doc_number_to = ("id", "docNumberEnd", "Document Number to field")
    cbx_nsf = ('id', 'NSF', 'NSF checkbox')
    # SEARCH RESULTS GRID-----------------------------------------------------------------------------------------------
    lbl_no_matches_found = ("xpath", "//div[@class='orderSearchResultBlock']//em", "No match found label")
    order_search_results = ("xpath", "//div[@class='orderSearchResultBlock']", "Search results")
    results_order_column = ("xpath", "//td[@data-column='OrderHeader.OrderNumber']", "Order Numbers")
    results_status_column = ("xpath", "//td[@data-column='OrderSearchStatus']", "Order search status")
    results_edit_column = ("xpath", "//a[@class='iconEditOrder']", "Order edit icons")
    results_edit_column2 = ("xpath", "//a[contains(@class,'orderSummaryiconedit')]", "Order edit icons")
    result_table_all_rows = ("xpath", "//table[@id='orderSearchBlock']/tbody/tr", "Result table data all rows")
    pup_in_workflow_lbl_message = (
        "xpath", "//div[@id='kofile-null']/div[@id='null']/ul/li[1]", "Order is in workflow popup message text")
    pup_in_workflow_btn_yes = ("id", "infobox_Yes", "Order is in workflow popup Yes button")
    pup_in_workflow_btn_no = ("id", "infobox_No", "Order is in workflow popup No button")
    pup_send_to_admin = ("id", "assignContent", "Send to Admin popup")
    pup_send_to_admin_txt_actionreason = ("id", "actionReason", "Send to Admin popup action reason field")
    pup_send_to_admin_txt_description = ("id", "actionDescription", "Send to Admin popup description field")
    pup_send_to_admin_lnk_cancel = ("id", "widget-kofileinfobubble-cancelui-id1", "Send to Admin popup Cancel")
    pup_send_to_admin_lnk_submit = ("id", "actionReasonsBtn", "Send to Admin popup Submit")
    pup_receipt_preview = ("id", "receiptPreviewBlock", "Receipt Preview popup")
    lbl_receipt_preview_order_number = (
        "xpath", "//*[@id='receiptPreviewBlock']//span[@class='receiptPreviewOrdernumber']",
        "Reprint Receipt Order Number")
    lnk_print_duplicate_receipt = (
        "xpath", "//div[@id='receiptPreviewBlock']//a[@id='printDuplicateCopy']", "Print Duplicate Copy link")
    lbl_receipt_message = (
        "xpath", "//div[@id='receiptPreviewBlock']//li[@id='orderReceiptMessage']", "Print Receipt message")
    txt_email_field = ("xpath", "//div[@id='receiptPreviewBlock']//input[@id='email']", "Email")
    lnk_email_duplicate_receipt = (
        "xpath", "//div[@id='receiptPreviewBlock']//a[@id='emailDuplicateCopy']", "Email Duplicate Copy link")

    _lbl_result_table_header_by_column_index = (
        "xpath", "//table[@id='orderSearchBlock']/thead/tr/th[%s]", "Result table header by column index")
    _lbl_result_table_data_by_row_index_by_column_index = (
        "xpath", "//table[@id='orderSearchBlock']/tbody/tr[%s]/td[%s]",
        "Result table data by row index and by column index")
    _lbl_result_table_data_by_order_number_by_column_index = (
        "xpath", "//table[@id='orderSearchBlock']/tbody/tr/td[@data-value='%s']/../td[%s]",
        "Result table data by order number and by column index label")
    _btn_row_actions_by_order_number_by_column_index = (
        "xpath", "//table[@id='orderSearchBlock']/tbody/tr/td[contains(text(), '%s')]/../td[%s]/a",
        "Result row actions by order number and by column index")

    _btn_result_table_data_by_order_number_by_column_index = (
        "xpath", "//table[@id='orderSearchBlock']/tbody/tr/td[@data-value='%s']//following::td[%s]/a",
        "Result table data by order number and by column index button")

    icn_endorse_check_by_order_number_ = (
        "xpath",
        "//td[@data-value='%s']/..//td/a[@class='iconEndorseStamp']",
        "Endorse Check icon by order number"
    )

    btn_resend_rejection = ("id", "email-rec-send", "Send")
    txt_resend_rejection = ("id", "resend-receipt-email", "Email address")

    # HELPER FUNCTIONS-------------------------------------------------------------------------------------------------
    @staticmethod
    def order_number_by_row_index(row_index=1):
        """returns Order# locator by row index"""
        loc = (
            "xpath", f"//tr[{row_index}]/td[contains(@data-column, 'OrderNumber')]", f"Order Number in {row_index} row")
        return loc

    @staticmethod
    def order_number_by_(text):
        """returns Order# locator by row index"""
        loc = ("xpath", f"//td[contains(@data-column, 'OrderNumber')]", f"Order Number by {text}")
        return loc

    def location_by_order_number(self, order_number):
        """returns Location locator by order number"""
        return self.__table_data(order_number, "Location")

    def department_by_order_number(self, order_number):
        """returns Department locator by order number"""
        return self.__table_data(order_number, "Department")

    def origin_by_order_number(self, order_number):
        """returns Origin locator by order number"""
        return self.__table_data(order_number, "Origin")

    def customer_by_order_number(self, order_number, loc="OrderUser"):
        """returns Customer locator by order number"""
        return self.__table_data(order_number, loc)

    def ordered_on_by_order_number(self, order_number):
        """returns Ordered On locator by order number"""
        return self.__table_data(order_number, "OrderDate")

    def recorded_on_by_order_number(self, order_number):
        """returns Recorded On locator by order number"""
        return self.__table_data(order_number, "RecordedDate")

    def recorded_by_by_order_number(self, order_number):
        """returns Recorded By locator by order number"""
        return self.__table_data(order_number, "FinalizeAgentName")

    def number_of_order_items_by_order_number(self, order_number):
        """returns Number Of Order Items locator by order number"""
        return self.__table_data(order_number, "NoOfItems")

    def order_total_by_order_number(self, order_number):
        """returns Order Total locator by order number"""
        return self.__table_data(order_number, "OrderTotal")

    def number_of_docs_by_order_number(self, order_number):
        """returns Number Of Docs locator by order number"""
        return self.__table_data(order_number, "NoOfDocuments")

    def gf_number_by_order_number(self, order_number):
        """returns GF Number locator by order number"""
        return self.__table_data(order_number, "GFNumber")

    def doc_number_by_order_number(self, order_number):
        """returns Doc Number locator by order number"""
        return self.__table_data(order_number, "DocumentNumber")

    def queue_by_order_number(self, order_number):
        """returns Queue locator by order number"""
        return self.__table_data(order_number, "OrderSearchStatus")

    def edit_order_icon_by_order_number(self, order_number):
        """returns Edit Order locator by order number"""
        return self.__table_data(order_number, "iconEditOrder")

    def send_to_admin_icon_by_order_number(self, order_number):
        """returns Send To Administrator locator by order number"""
        return self.__table_data(order_number, "iconSendAdmin")

    def reprint_receipt_icon_by_order_number(self, order_number):
        """returns Reprint Receipt locator by order number"""
        return self.__table_data(order_number, "iconDuplicateRecipt")

    def print_rejection_letter_icon_by_order_number(self, order_number):
        """returns Print Rejection Letter locator by order number"""
        return self.__table_data(order_number, "iconPrintRejectionLetter")

    def send_back_to_order_queue_icon_by_order_number(self, order_number):
        """returns Send Back To Order Queue locator by order number"""
        return self.__table_data(order_number, "sendRejectedOrderBack")

    def send_back_cancelled_order_by_order_number(self, order_number):
        """returns Send Back To Order Queue locator by order number"""
        return self.__table_data(order_number, "sendCancelledOrderBack")

    def resend_rejection_icon(self, order_number):
        return self.__table_data(order_number, "resendRejectEmail")

    @staticmethod
    def __table_data(order_number, queue_column_name):
        locator = ("xpath", f"//td[@data-value='{order_number}']/..//*[contains(@data-column, '{queue_column_name}') "
                            f"or contains(@class, '{queue_column_name}')]",
                   f"Search result table '{queue_column_name}' column for order '{order_number}'")
        return locator
