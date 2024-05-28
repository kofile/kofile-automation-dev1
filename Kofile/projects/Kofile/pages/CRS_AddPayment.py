"""
Add Payment Page Object Model
"""
from projects.Kofile.Lib.test_parent import PagesParent


class AddPayment(PagesParent):
    def __init__(self):
        super(AddPayment, self).__init__()

    # ---------------------------------------------
    # payment grid
    # ---------------------------------------------
    lbl_paygrid_balance_due_label = (
        "xpath",
        "//div[@data-bind-id='PaymentGridTotal']/ul[1]/li[1]",
        "Balance Due label")
    lbl_paygrid_balance_due_amount = (
        "xpath",
        "//div[@data-bind-id='PaymentGridTotal']/ul[1]/li[2]",
        "Balance Due value with $ symbol")
    lbl_processing_fee_amount = (
        "id",
        "ProcessingFee",
        "Processing fee amount"
    )
    # ---------------------------------------------
    _lbl_paygrid_pay_method_label_by_row = (
        "xpath",
        "//div[@data-bind-id='PaymentGridTotal']/div[2]/ul[%s]/li[1]/span[1]",
        "Payment grid, payment method by index")
    _lbl_paygrid_pay_method_count_by_row = (
        "xpath",
        "//div[@data-bind-id='PaymentGridTotal']/div[2]/ul[%s]/li[1]/span[2]",
        "Payment grid, payment count by index")
    _lbl_paygrid_pay_method_amount_by_row = (
        "xpath",
        "//div[@data-bind-id='PaymentGridTotal']/div[2]/ul[%s]/li[2]",
        "Payment grid, payment amount by index")
    # ---------------------------------------------
    lbl_paygrid_subtotal_label = (
        "xpath", "//div[@id='paymentSummary']/ul[1]/li[1]",
        "Payment grid, payment summary, subtotal label")
    lbl_paygrid_subtotal_amount = (
        "xpath", "//div[@id='paymentSummary']/ul[1]/li[2]",
        "Payment grid, payment summary, subtotal amount")
    # ---------------------------------------------
    lbl_paygrid_balance_owed_label = (
        "xpath", "//div[@id='paymentSummary']/ul[2]/li[1]",
        "Payment grid, payment summary, balance owed label")
    lbl_paygrid_balance_owed_amount = (
        "xpath", "//div[@id='paymentSummary']/ul[2]/li[2]",
        "Payment grid, payment summary, balance owed amount")
    # ---------------------------------------------
    lbl_paygrid_change_due_label = (
        "xpath", "//div[@id='paymentSummary']/ul[3]/li[1]",
        "Payment grid, payment summary, change due label")
    lbl_paygrid_change_due_amount = (
        "xpath", "//div[@id='paymentSummary']/ul[3]/li[2]",
        "Payment grid, payment summary, change due amount")
    # ---------------------------------------------
    # payment methods
    # ---------------------------------------------
    ddl_paymethod_payment_method_by_row = (
        "xpath",
        "//div[@id='paymentMethods']/div[@class='paymentMethodType'][%s]/ul/li[1]/select",
        "Payment method by row index")
    txt_paymethod_transaction_id_by_row = (
        "xpath",
        "//div[@id='paymentMethods']/div[@class='paymentMethodType'][%s]/ul/li[2]/input",
        "Transaction ID by row index")
    txt_paymethod_comment_by_row = (
        "xpath",
        "//div[@id='paymentMethods']/div[@class='paymentMethodType'][%s]/ul/li[3]/input",
        "Comment by row index")
    payment_comment_by_row = (
        "xpath",
        "//input[@name='OrderPayment[%s].Comment']",
        "Comment by row index")
    txt_paymethod_amount_by_row = (
        "xpath",
        "//div[@id='paymentMethods']/div[@class='paymentMethodType'][%s]/ul/li[4]/input",
        "Amount by row index")
    txt_cash_change_due_amount = (
        "xpath",
        "//div[@id='cashChangeDue']//input[contains(@name,'Amount')]",
        "CashChangeDue Amount")
    btn_paymethod_delete_by_row = (
        "xpath",
        "//div[@id='paymentMethods']/div[@class='paymentMethodType'][%s]/ul/li[4]/a[2]",
        "Delete button by row index")
    ddl_all_payment_methods = (
        "xpath",
        "//select[contains(@class,'paymentMethodSelect')]/option[not(text()='Select')]",
        "All payment methods drop-down list")
    # ---------------------------------------------
    # buttons
    # ---------------------------------------------
    btn_new_payment_method = (
        "xpath",
        "//form[@id='orderPaymentForm']/div[@data-bind-id='NewPaymentMethodHolder']/a[1]",
        "Payment Method button")
    lnk_cancel_entire_order = (
        "xpath",
        "//form[@id='orderPaymentForm']/div[@data-bind-id='PaymentGridBtns']/div[2]/span/a",
        "Cancel Entire Order action link")
    lnk_send_to_admin = (
        "xpath",
        "//form[@id='orderPaymentForm']/div[@data-bind-id='PaymentGridBtns']/div[3]/span/a",
        "Send to Administrator action link")
    btn_save_order = (
        "id",
        "saveOrderLaterCheckout",
        "Save Order button")
    btn_checkout = (
        "id",
        "orderPaymentCheckout",
        "Checkout button")
    # ---------------------------------------------
    # popup
    # ---------------------------------------------
    pup_txt_reason = (
        "xpath",
        "//*[@id='actionReason']",
        "Popup Reason field"
    )
    pup_txt_description = (
        "xpath",
        "//*[@id='actionDescription']",
        "Popup Description field"
    )
    pup_btn_submit = (
        "xpath",
        "//*[@id='actionReasonsBtn']",
        "Popup Submit button"
    )
    pup_btn_cancel = (
        "xpath",
        "//*[@id='widget-kofileinfobubble-cancelui-id1']",
        "Popup Cancel button"
    )

    # -------------------------------------------
    # checkout comment popup
    # -------------------------------------------
    pup_checkout_txt_comment = (
        "xpath",
        "//div[@id='OrderPaymentCommentContent']//input",
        "Checkout comment popup, text field"
    )
    pup_checkout_btn_cancel = (
        "id",
        "CancelOrderPaymentCommentBtn",
        "Checkout comment popup, Cancel button"
    )
    pup_checkout_btn_submit = (
        "id",
        "SubmitOrderPaymentCommentBtn",
        "Checkout comment popup, Submit button"
    )

    # -------------------------------------------
    # Save order header popup
    # -------------------------------------------
    pup_save_header_btn_yes = (
        "id",
        "saveHeaderYes",
        "Save Order Header popup, Yes button"
    )
    pup_save_header_btn_no = (
        "id",
        "saveHeaderNo",
        "Save Order Header popup, No button"
    )
    # -------------------------------------------
    txt_refund_to_name = ("id", "CustomerFirstName", "Refund to customer name")
