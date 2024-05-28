"""
Void Order Summary Page Object Model
"""

# ---------------------------------------------
# Fee Distribution popup
# ---------------------------------------------
from projects.Kofile.Lib.test_parent import PagesParent


class CRSVoidOrderSummary(PagesParent):
    def __init__(self):
        super(CRSVoidOrderSummary, self).__init__()

    _pup_fee_dist_lbl_description_by_row = (
        "xpath",
        "//div[@id='voidFeeDistributionContent']//table/tbody/tr[%s]/td[1]",
        "Fee Distribution popup, fee description label by row index")
    _pup_fee_dist_lbl_amount_by_row = (
        "xpath",
        "//div[@id='voidFeeDistributionContent']//table/tbody/tr[%s]/td[2]",
        "Fee Distribution popup, fee amount by row index")
    _pup_fee_dist_txt_amount_by_row = (
        "xpath",
        "//div[@id='voidFeeDistributionContent']//table/tbody/tr[%s]/td[3]/input",
        "Fee Distribution popup, fee amount in textbox by row index")
    pup_fee_desc_lbl_total = (
        "xpath",
        "//div[@id='voidAddFeeDistributionContent']//table/tbody/tr[last()]/th[2]",
        "Fee Distribution popup, fee total")
    pup_fee_values_lbl = (
        "xpath",
        "//div[@id='voidAddFeeDistributionContent']//table/tbody//td[2]",
        "Fee values on fee distribution popup on void summary"
    )
    pup_fee_desc_lbl = (
        "xpath",
        "//div[@id='voidAddFeeDistributionContent']//table/tbody//td[2]/preceding-sibling::td",
        "Fee description on fee distribution popup on void summary"
    )
    pup_fee_desc_lbl_total_in_red = (
        "xpath",
        "//div[@id='voidFeeDistributionContent']//table/tbody/tr[last()]/th[3]",
        "Fee Distribution popup, fee total in red")
    pup_fee_desc_rdb_void_prior_date = (
        "xpath",
        "//div[@id='voidDate-options']/input[@value='1']",
        "Fee Distribution popup, void prior date report radio button")
    pup_fee_desc_rdb_void_today = (
        "xpath",
        "//div[@id='voidDate-options']/input[@value='2']",
        "Fee Distribution popup, void today report radio button")
    pup_fee_desc_btn_close = (
        "id", "widget-kofileinfobubble-closeui-id1",
        "Fee Distribution popup, Close button")
    pup_fee_desc_btn_submit = (
        "id",
        "widget-kofileinfobubble-submitui-id1",
        "Fee Distribution popup, Submit button")
    # ---------------------------------------------
    # Fee Grid
    # ---------------------------------------------
    lbl_feegrid_balance_paid_label = (
        "xpath",
        "//div[@id='voidBalanceTotal']/ul/li[1]",
        "Fee Grid, Balance Paid label")
    lbl_feegrid_balance_paid_amount = (
        "id",
        "balancePaid",
        "Fee Grid, Balance Paid label")
    _lbl_feegrid_pay_method_label_by_row = (
        "xpath",
        "//div[@id='voidPaymentMethodsList']/ul[%s]/li[1]/span[1]",
        "Fee Grid, payment method by row index")
    _lbl_feegrid_pay_method_count_by_row = (
        "xpath",
        "//div[@id='voidPaymentMethodsList']/ul[%s]/li[1]/span[2]",
        "Fee Grid, payment count by row index")
    _lbl_feegrid_pay_method_amount_by_row = (
        "xpath",
        "//div[@id='voidPaymentMethodsList']/ul[%s]/li[2]/span[1]",
        "Fee Grid, payment amount by row index")
    lbl_feegrid_total_voids_label = (
        "xpath",
        "//div[@id='voidPaymentTotal']/ul[1]/li[1]",
        "Fee Grid, total voids label")
    lbl_feegrid_total_voids_count = (
        "xpath",
        "//div[@id='voidPaymentTotal']/ul[1]/li[1]/span",
        "Fee Grid, total voids count")
    lbl_feegrid_total_voids_amount = (
        "xpath",
        "//div[@id='voidPaymentTotal']/ul[1]/li[2]/span",
        "Fee Grid, total voids label")
    # ---------------------------------------------
    # select/deselect all
    # ---------------------------------------------
    lnk_select_all = (
        "id",
        "selectAllVoid",
        "Select All action link")
    lnk_deselect_all = (
        "id",
        "deSelectAllVoid",
        "DeSelect All action link")
    # ---------------------------------------------
    # table header
    # ---------------------------------------------
    _lbl_table_header_by_column_index = (
        "xpath",
        "//table[@id='VoidOrder']/thead/tr[1]/th[%s]",
        "Void Order Summary table header by column index")
    # ---------------------------------------------
    # table data
    # ---------------------------------------------
    _lbl_table_data_by_row_by_column_index = (
        "xpath",
        "//table[@id='VoidOrder']/tbody/tr[%s]/td[%s]",
        "Void Order Summary table data by row by column index")
    chk_void_oit_by_row_number = (
        "xpath",
        "//tr[%s]//input[@class='iconfeeDistribution']",
        "Void OIT Checkbox on Void Order Summary table by row"
    )
    void_row_numbers = (
        "xpath",
        "//*[@id='VoidOrder']//tbody/tr",
        "OIT's rows in void screen"
    )
    _chk_by_row_by_column_index = (
        "xpath",
        "//table[@id='VoidOrder']/tbody/tr[%s]/td[%s]/input",
        "Checkbox on Void Order Summary table by row"
    )
    # ---------------------------------------------
    # total
    # ---------------------------------------------
    lbl_total_amount = (
        "id",
        "orderTotalAmt",
        "Void Total, amount")
    # ---------------------------------------------
    # buttons
    # ---------------------------------------------
    btn_void = (
        "xpath",
        "//div[@data-bind-id='voidOrderSummaryBottomLinks']/input[@value='Void']",
        "Void Order Summary button")
    btn_cancel_void = (
        "id",
        "voidOrderSummaryCancel",
        "Void Order Summary Cancel button")
    # ---------------------------------------------
    # Prior Date Void warning popup
    # ---------------------------------------------
    pup_prior_date_warn_lbl_message = (
        "xpath",
        "//div[@id='validation-fix']/ul/li[1]",
        "Prior Date Void warning popup, message text")
    pup_prior_date_warn_btn_yes = (
        "id",
        "infobox_Yes",
        "Prior Date Void warning popup, Yes button")
    pup_prior_date_warn_btn_no = (
        "id",
        "infobox_No",
        "Prior Date Void warning popup, No button")

    def order_type_by_row_index(self, row_num=1):
        """
        returns OrderType locator by row_index
        """
        return self.__table_data(row_num, "OrderItemType_Value")

    def document_type_by_row_index(self, row_num=1):
        """
        returns DocumentType locator by row_index
        """
        return self.__table_data(row_num, "Document_DocumentType")

    def number_of_by_row_index(self, row_num=1):
        """
        returns NumberOf locator by row_index
        """
        return self.__table_data(row_num, "FeeParameterCriteria_NoOfPageOrCopy")

    def price_by_row_index(self, row_num=1):
        """
        returns Price locator by row_index
        """
        return self.__table_data(row_num, "Price")

    def doc_number_by_row_index(self, row_num=1):
        """
        returns DocNumber locator by row_index
        """
        return self.__table_data(row_num, "Document_InstrumentNumber")

    def status_by_row_index(self, row_num=1):
        """
        returns Status locator by row_index
        """
        return self.__table_data(row_num, "OrderItemStatus")

    def fee_distribution_popup_by_row_index(self, row_num=1):
        """
        returns FeeDistributionPopup locator by row_index
        """
        return self.__table_data(row_num, "voidAddFeeDistribution")

    def checkbox_by_row_index(self, row_num=1):
        """
        returns SelectCheckbox locator by row_index
        """
        return self.__table_data(row_num, "iconfeeDistribution")

    def state_by_row_index(self, row_num=1):
        """
        returns State locator by row_index
        """
        return self.__table_data(row_num, "statusInfo")

    @staticmethod
    def __table_data(row_num, queue_column_name):
        end = "/preceding-sibling::a" if queue_column_name == "statusInfo" else ""
        locator = ("xpath", f"//tr[{row_num}]//*[contains(@data-bind, '{queue_column_name}') "
                            f"or contains(@class, '{queue_column_name}')]{end}",
                   f"Result table '{queue_column_name}' column")
        return locator
