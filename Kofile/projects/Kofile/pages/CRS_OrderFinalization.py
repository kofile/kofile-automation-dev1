"""
Order Finalization Page Object Model
"""
from projects.Kofile.Lib.test_parent import PagesParent


class CRSOrderFinalization(PagesParent):
    row_name = 'documentNumber'

    def __init__(self):
        super(CRSOrderFinalization, self).__init__()

    def __69999__(self):
        self.txt_table_data_doc_number = (
            "xpath",
            "//table[@id='orderSummary']//td[@data-column='Document_DocAndAppNum']",
            "Order Finalization doc number")

    def __48999__(self):
        self.txt_table_data_doc_number = (
            "xpath",
            "//table[@id='orderSummary']//div[@class='docAndTaxNumberWrap']//span[1]",
            "Order Finalization doc number")
        self.btn_scan_all_doc = (
            "id",
            "scanDocument",
            "Scan all docs button")

        self.row_name = 'instrumentNumber'

    lbl_order_finalize_label = (
        "xpath",
        "//div[@id='left-block']/div[2]/div[1]/span",
        "Order Finalize label")
    # ---------------------------------------------
    # table header
    # ---------------------------------------------
    _lbl_table_header_by_column_index = (
        "xpath",
        "//table[@id='orderSummary']/thead/tr/th[%s-1]",
        "Order Finalization table header by index")
    # ---------------------------------------------
    # table data
    # ---------------------------------------------
    _lbl_table_data_by_row_by_column_index = (
        "xpath",
        "//table[@id='orderSummary']/tbody/tr[%s]/td[%s]",
        "Order Finalization table data by row, by column index")
    _lbl_table_data_row_index_by_row_by_column_index = (
        "xpath",
        # "//table[@id='orderSummary']/tbody/tr[%s]/td[%s]/div/span",
        "//table[@id='orderSummary']/tbody/tr[%s]/td[%s]",
        "Order Finalization table data row index by row, by column index")
    _lbl_table_data_discount_value_by_row_by_column_index = (
        "xpath",
        "//table[@id='orderSummary']/tbody/tr[%s]/td[%s]/div/span",
        "Order Finalization discount value by row, by column index")
    _btn_table_data_discount_icon_by_row_by_column_index = (
        "xpath",
        "//table[@id='orderSummary']/tbody/tr[%s]/td[%s]/div/a",
        "Order Finalization discount icon by row, by column index")
    # all other icons and textboxes, except discount and row index
    _btn_table_data_icon_by_row_by_column_index = (
        "xpath",
        "//table[@id='orderSummary']/tbody/tr[%s]/td[%s]/a",
        "Order Finalization icon by row, by column index")
    _txt_table_data_input_by_row_by_column_index = (
        "xpath",
        "//table[@id='orderSummary']/tbody/tr[%s]/td[%s]/input",
        "Order Finalization input by row, by column index")
    txt_table_data_order_status = (
        "xpath",
        "//table[@id='orderSummary']//td[@data-column='Order_OrderStatus']",
        "Order Finalization order status")
    txt_table_data_doc_year = (
        "xpath",
        "//table[@id='orderSummary']//td[@data-column='Document_RecordedYear']",
        "Order Finalization doc year")
    txt_table_data_doc_number = (
        "xpath",
        "//table[@id='orderSummary']//td[@data-column='Document_InstrumentNumber']",
        "Order Finalization doc number")
    icn_edit_order = (
        'xpath',
        "(//a[contains(@class,'orderSummaryiconedit')])[%s]",
        'Order Finalization Item Edit')
    row_numbers = (
        "xpath",
        "//*[@id='orderSummary']//tbody/tr",
        "OIT's rows in Order Finalization"
    )
    # ---------------------------------------------
    # total
    # ---------------------------------------------
    lbl_total_item_count = (
        "xpath",
        "//div[@id='left-block']/div[2]/div[3]/span[1]",
        "Order Total, item count")
    lbl_total_amount = (
        "id",
        "orderTotalAmt",
        "Order Total, amount")
    lbl_email_address = (
        "id",
        "email-receipt-email",
        "Email Receipt")
    lbl_receipt_message = (
        "id",
        "emaildupreceiptMessageBlock",
        "Email Receipt warning message")
    # ---------------------------------------------
    # action links
    # ---------------------------------------------
    lnk_endorse_check = (
        "id",
        "print-endorse-stamp",
        "Print Endorse Stamp"
    )
    lnk_email_dup_receipt = (
        "id",
        "email-duplicate-receipt",
        "Email Duplicate Receipt action link")
    lnk_print_dup_receipt = (
        "id",
        "print-duplicate-receipt",
        "Print Duplicate Receipt action link")
    lnk_print_all_cover_pages = (
        "id",
        "print-all-labels",
        "Print All Cover Pages action link")
    lnk_scan_all_documents = (
        "id",
        "scanDocument",
        "Scan All Documents action link")
    lnk_edit_order_payments = (
        "id",
        "editOrderPayment",
        "Edit Order Payments action link")
    # ---------------------------------------------
    # buttons
    # ---------------------------------------------
    btn_void_order = (
        "id",
        "VoidOrder",
        "Void Order button")
    btn_get_next = (
        "id",
        "nextOrder",
        "Next Order button")
    btn_order_queue = (
        "id",
        "orderFinalCheckout",
        "Order queue button")
    btn_scan_all_doc = (
        "id",
        "ScanAllDocuments",
        "Scan all docs button")
    btn_cancel = (
        "id",
        "cancel",
        "Cancel button in Edit"
    )
    btn_save_order = (
        "id",
        "addToOrder",
        "Save Order button in Edit"
    )
    btn_send_email_rec = (
        "id",
        "email-rec-send",
        "Email Receipt Send button"
    )
    # ---------------------------------------------
    # Fund Distribution popup
    # ---------------------------------------------
    lnk_view_edit_order_item_funds = (
        "xpath",
        "//a[@id='feeDistribution' or @id='additionalFeeDistribution']",
        "View/Edit Order Item Funds action link")
    _pup_fund_dist_lbl_description_by_row = (
        "xpath",
        "//div[@id='feeDistributionContent']//table/tbody/tr[%s+1]/td[1]",
        "Fund Distribution popup, fund description label by row index")
    _pup_fund_dist_lbl_amount_by_row = (
        "xpath",
        "//div[@id='feeDistributionContent']//table/tbody/tr[%s+1]/td[2]",
        "Fund Distribution popup, fund amount by row index")
    _pup_fund_dist_txt_amount_by_row = (
        "xpath",
        "//div[@id='feeDistributionContent']//table/tbody/tr[%s+1]/td[3]/input",
        "Fund Distribution popup, fund amount in textbox by row index")
    pup_fund_dist_lbl_total_expected = (
        "xpath",
        "//div[@id='additionalfeeDistributionContent']//table/tbody/tr/th[text()='Total']/../th[2]",
        "Fund Distribution popup, fund total expected")
    pup_fund_dist_lbl_total_actual = (
        "xpath",
        "//div[@id='additionalfeeDistributionContent' or @id='feeDistributionContent']"
        "//table/tbody/tr/th[text()='Total']/../th[3]",
        "Fund Distribution popup, fund total calculated")
    pup_fund_dist_btn_close = (
        "id", "widget-kofileinfobubble-closeui-id1",
        "Fund Distribution popup, Close button")
    pup_fund_dist_btn_submit = (
        "id",
        "widget-kofileinfobubble-submitui-id1",
        "Fund Distribution popup, Submit button")
    pup_fund_dist_all_fee_fund_desc = (
        "xpath",
        "//tr/td[contains(@data-bind, 'FeeFund.FeeFundDesc')]",
        "Fund Distribution popup, all Fund descriptions"
    )
    pup_fund_dist_all_fee_fund_value = (
        "xpath",
        "//tr/td[contains(@data-bind, 'FeeFund.Value')]",
        "Fund Distribution popup, all Fund values"
    )
    pup_fund_dist_all_fee_fund_input = (
        "xpath",
        "//tr/td[contains(@data-bind, 'calculatedFeeFundValue')]",
        "Fund Distribution popup, all Fund new values"
    )
    pup_fund_dist_penalty_message = (
        "xpath",
        "//th[contains(text(), 'Please  note:  Order item  contains penalty distributions')]",
        "Fund Distribution popup, penalty message"
    )
    txt_outstanding_balance_due = (
        "xpath",
        "//*[@id='NewOrderform']//ul[@class='feeRow']/li[contains(text(),'Outstanding Balance Due:')]",
        "Outstanding Balance Due label in fee row"
    )
    # -------------------------------------------
    # Outstanding Balance Due popup
    # -------------------------------------------
    pup_outstanding_btn_ok = (
        "id",
        "widget-kofileinfobubble-okui-id1",
        "Outstanding Balance Due popup Ok button"
    )
    pup_outstanding_btn_close = (
        "id",
        "widget-kofileinfobubble-closeui-id1",
        "Outstanding Balance Due popup Close button"
    )
    pup_outstanding_btn_send_to_admin = (
        "id",
        "inSufficientFundssaveAdminBtn",
        "Outstanding Balance Due popup Send To Admin button"
    )
    pup_application_print_success_text = (
        "id",
        "print-document-success",
        "Application print success popup text")
    pup_duplicate_receipt_print_success_text = (
        "id",
        "print-duplicate-receipt-success",
        "Duplicate receipt print success popup text")

    pup_endorse_stamp_printing = (
        "xpath",
        "//*[@id='print-endorse-stamp-success']/ul/li[contains(text(),'Endorse Stamp printing is initiated.')]",
        "Endorse Stamp Printing Success popup"
    )

    def type_by_row_index(self, row_num=1):
        """
        returns OIT type locator by row_index
        """
        return self.__table_data(row_num, "OrderItemType_Value")

    def doc_type_by_row_index(self, row_num=1):
        """
        returns doc_type locator by row_index
        """
        return self.__table_data(row_num, "Document_DocumentType")

    def num_of_by_row_index(self, row_num=1):
        """
        returns number_of locator by row_index
        """
        return self.__table_data(row_num, "NoOfPageOrCopy")

    def price_by_row_index(self, row_num=1):
        """
        returns price locator by row_index
        """
        return self.__table_data(row_num, "Price")

    def year_by_row_index(self, row_num=1):
        """
        returns year locator by row_index
        """
        return self.__table_data(row_num, "Document_RecordedYear")

    def docnum_by_row_index(self, row_num=1):
        """
        returns document number locator by row_index
        """
        return self.__table_data(row_num, self.row_name)

    def status_by_row_index(self, row_num=1):
        """
        returns status locator by row_index
        """
        return self.__table_data(row_num, "Order_OrderStatus")

    def editicon_by_row_index(self, row_num=1):
        """
        returns editicon locator by row_index
        """
        return self.__table_data(row_num, "EditOrderItem")

    def serialnum_by_row_index(self, row_num=1):
        """
        returns serial number locator by row_index
        """
        return self.__table_data(row_num, "SetSerialNumber")

    def print_barcode_by_row_index(self, row_num=1):
        """
        returns print_barcode locator by row_index
        """
        return self.__table_data(row_num, "CanPrintBarcode")

    def print_coverpage_by_row_index(self, row_num=1):
        """
        returns coverpage locator by row_index
        """
        return self.__table_data(row_num, "CanPrintCoverPages")

    def print_doc_label_by_row_index(self, row_num=1):
        """
        returns PrintDocumentLabel locator by row_index
        """
        return self.__table_data(row_num, "CanPrintDocumentLabel")

    def print_doc_image_by_row_index(self, row_num=1):
        """
        returns PrintDocumentImage locator by row_index
        """
        return self.__table_data(row_num, "printDocumentImage")

    def print_application_by_row_index(self, row_num=1):
        """
        returns PrintApplication locator by row_index
        """
        return self.__table_data(row_num, ".PrintApplications")

    def print_cert_form_by_row_index(self, row_num=1):
        """
        returns PrintCertificateForm locator by row_index
        """
        return self.__table_data(row_num, ".PrintCertificateForm")

    def print_address_label_by_row_index(self, row_num=1):
        """
        returns PrintAddressLabel locator by row_index
        """
        return self.__table_data(row_num, "CanPrintAddressLabel")

    def print_cert_front_page_by_row_index(self, row_num=1):
        """
        returns PrintCertificateFrontPage locator by row_index
        """
        return self.__table_data(row_num, "CanPrintCertFrontPage")

    def print_cert_back_page_by_row_index(self, row_num=1):
        """
        returns PrintCertificateBackPage locator by row_index
        """
        return self.__table_data(row_num, "CanPrintCertBackPage")

    def print_cert_by_row_index(self, row_num=1):
        """
        returns PrintCertificate locator by row_index
        """
        return self.__table_data(row_num, "CanPrintCertPages")

    def edit_doc_in_browser_by_row_index(self, row_num=1):
        """
        returns EditDocumentInBrowser locator by row_index
        """
        return self.__table_data(row_num, "CanEditDocInViewer")

    @staticmethod
    def __table_data(row_num, queue_column_name):
        suffix = "a" if queue_column_name in ["EditOrderItem", "SetSerialNumber"] else "*"
        end = "/a" if queue_column_name in ["CanPrintBarcode", "CanPrintCoverPages", "CanPrintDocumentLabel",
                                            "CanPrintAddressLabel", "CanPrintCertFrontPage", "CanPrintCertBackPage",
                                            "CanPrintCertPages", "CanEditDocInViewer"] else ""
        locator = ("xpath", f"//tr[{row_num}]//{suffix}[contains(@data-bind, '{queue_column_name}')]{end}",
                   f"Result table '{queue_column_name}' column")
        return locator

# //td[contains(@data-bind, "documentNumber")]