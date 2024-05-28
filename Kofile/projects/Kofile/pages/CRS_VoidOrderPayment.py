"""
Void Order Payment Page Object Model
"""

# ---------------------------------------------
# Void Grid
# ---------------------------------------------
from projects.Kofile.Lib.test_parent import PagesParent


class CRSVoidOrderPayment(PagesParent):
    def __init__(self):
        super(CRSVoidOrderPayment, self).__init__()

    lbl_voidgrid_balance_paid_label = (
        "xpath",
        "//div[@id='voidBalanceTotal']/ul/li[1]",
        "Void Grid, Balance Paid label")
    lbl_voidgrid_balance_paid_amount = (
        "id",
        "balancePaid",
        "Void Grid, Balance Paid amount")
    _lbl_voidgrid_pay_method_label_by_row = (
        "xpath",
        "//div[@id='voidPaymentMethodsList']/ul[%s]/li[1]/span[1]",
        "Void Grid, payment method by row index")
    _lbl_voidgrid_pay_method_count_by_row = (
        "xpath",
        "//div[@id='voidPaymentMethodsList']/ul[%s]/li[1]/span[2]",
        "Void Grid, payment count by row index")
    _lbl_voidgrid_pay_method_amount_by_row = (
        "xpath",
        "//div[@id='voidPaymentMethodsList']/ul[%s]/li[2]/span[1]",
        "Void Grid, payment amount by row index")
    lbl_voidgrid_total_voids_label = (
        "xpath",
        "//div[@id='voidPaymentTotal']/ul[1]/li[1]",
        "Void Grid, total voids label")
    lbl_voidgrid_total_voids_count = (
        "xpath",
        "//div[@id='voidPaymentTotal']/ul[1]/li[1]/span",
        "Void Grid, total voids count")
    lbl_voidgrid_total_voids_amount = (
        "xpath",
        "//div[@id='voidPaymentTotal']/ul[1]/li[2]/span",
        "Void Grid, total voids label")
    # ---------------------------------------------
    # table header
    # ---------------------------------------------
    _lbl_table_header_by_column_index = (
        "xpath",
        "//div[@id='paymentMethodLabel']/ul/li[%s]/label",
        "Void Order Payment table header by column index")
    # ---------------------------------------------
    # table data
    # ---------------------------------------------
    _lbl_table_data_by_row_by_column_index = (
        "xpath",
        "//div[@id='paymentMethods']/div[%s]/ul/li[%s]/input[@type='text']",
        "Void Order Payment table data by row by column index")
    # it looks like this locator is applicable to payment method column only
    _ddl_table_data_by_row_by_column_index = (
        "xpath",
        "//div[@id='paymentMethods']/div[%s]/ul/li[%s]/select",
        "Void Order Payment table data select element by row by column index")
    row_numbers = (
        "xpath",
        "//*[@id='paymentMethods']//ul[@class='horizantal']",
        "Row numbers on Void Order Payment Screen"
    )
    col_table_data_payment = (
        "xpath",
        "//div[@class='paymentMethodType']//li[1]/input[last()]",
        "Payments table 'payment' column")
    col_table_data_amount = (
        "xpath",
        "//div[@class='paymentMethodType']//li[4]/following-sibling::input",
        "Payments table 'amount' column")
    # ---------------------------------------------
    # buttons
    # ---------------------------------------------
    btn_cancel_void = (
        "id",
        "orderPaymentHistoryBack",
        "Void Order Payment Cancel button")
    btn_finalize_void = (
        "id",
        "voidOrderPaymentCheckout",
        "Void Order Payment Finalize Void button")

    # ---------------------------------------------
    # comment popup
    # ---------------------------------------------

    txt_finalize_void_comment = (
        "xpath",
        "//*[@id='OrderPaymentCommentContent']//input",
        "Void Order Payment Comment field")

    btn_submit_finalize_void_comment = (
        "id",
        "SubmitOrderPaymentCommentBtn",
        "Finalize Void Comment Submit")

    btn_cancel_finalize_void_comment = (
        "id",
        "CancelOrderPaymentCommentBtn",
        "Finalize Void Comment Cancel")

    def payment_method_by_row(self, row_num=2):
        """
        returns payment method ddl locator by row_index, default row_index is 2
        """
        return self.__table_data(row_num, "PaymentMethodId")

    def transaction_id_by_row(self, row_num=2):
        """
        returns TransactionId method ddl locator by row_index, default row_index is 2
        """
        return self.__table_data(row_num, "TransactionId")

    def comment_field_by_row(self, row_num=2):
        """
        returns Comment locator by row_index, default row_index is 2
        """
        return self.__table_data(row_num, "Comment")

    def amount_field_by_row(self, row_num=2):
        """
        returns Amount locator by row_index, default row_index is 2
        """
        return self.__table_data(row_num, "Amount")

    @staticmethod
    def __table_data(row_num, queue_column_name):
        suffix = "select" if queue_column_name == "PaymentMethodId" else "input"
        locator = ("xpath", f"//div[@id='paymentMethods']/div[{row_num}]"
                            f"//{suffix}[contains(@data-bind, '{queue_column_name}')]",
                   f"Result table '{queue_column_name}' column")
        return locator
