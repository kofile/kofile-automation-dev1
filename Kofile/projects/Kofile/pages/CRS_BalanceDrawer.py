from projects.Kofile.Lib.test_parent import PagesParent


class CRSBalanceDrawer(PagesParent):
    def __init__(self):
        super(CRSBalanceDrawer, self).__init__()

    def __48999__(self):
        self.btn_cash_reconciliation_submit = (
            "xpath",
            ".//*[@id='submitCashReconciliation']",
            "Cash Reconciliation page-Submit button")
        self.btn_cheque_reconciliation_submit = (
            "xpath",
            ".//*[@id='submitCheckReconciliation']",
            "Cheque Reconciliation Submit button")
        self.lnk_post_difference = (
            "id",
            "postDiffreenceSingle",
            "Post Difference link for non admin")
        self.ddl_drawer_sessions = (
            "xpath",
            "//select[contains(@data-bind,'selectedDrawerId')]",
            "Drawer sessions dropdown")

    # ---------------------------------------------
    # Breadcrumb
    # ---------------------------------------------
    lbl_Balance_Drawer_tab = (
        "id",
        "balanceDrawer",
        "Balance Drawer Tab")
    lbl_initialize_Drawer_tab = (
        "id",
        "initializeDrawer",
        "Initialize Drawer Tab")
    lbl_cheque_reconciliation_breadcrumb = (
        "xpath",
        ".//*[@id='wrapper']/div/ul/li[3]",
        "Cheque reconciliation breadcrumb")
    lbl_cheque_reconciliation_breadcrumb_drawer_summary = (
        "xpath",
        ".//*[@id='wrapper']/div/ul/li[2]",
        "Drawer Summary breadcrump")
    # ---------------------------------------------
    # Initialize Drawer
    # ---------------------------------------------
    btn_submit_initialize_Drawer = (
        "xpath",
        "//input[@id='submitInitializeDrawer']",
        "Initialize Drawer 'Submit' button")
    btn_submit_initialize_Drawer_disabled = (
        "xpath",
        "//input[@id='submitInitializeDrawer1']",
        "Initialize Drawer disabled 'Submit' button")
    btn_cancel_initialize_Drawer = (
        "xpath",
        "//input[@id='cancelinitializeDrawer']",
        "Initialize Drawer 'Cancel' button")
    inp_initialize_Drawer__post_date = (
        "xpath",
        "//input[@id='PostDate']",
        "Initialize Drawer 'Post Date' input field")
    btn_initialize_Drawer__search = (
        "xpath",
        "//input[contains(@data-bind, 'searchPostedDates')]",
        "Initialize Drawer 'Search' button")
    btn_initialize_Drawer__submit_posted_date = (
        "xpath",
        "//input[@id='submitPostedDate']",
        "Initialize Drawer 'Submit posted dates' button")
    btn_initialize_Drawer__admin_key = (
        "xpath",
        "//a[@class='icon-admin-key']",
        "Initialize Drawer 'ADMIN key' button")
    inp_recording_date = (
        "id",
        "recordedDate",
        "Recording Date"
    )
    # ---------------------------------------------
    # Drawer data
    # ---------------------------------------------
    ddl_drawer_sessions = (
        "xpath",
        "//select[@data-bind='value:selectedDrawerSessionId']",
        "Drawer sessions dropdown")
    drawer_table_body = (
        "xpath",
        "//div[@class='cashDrawerSummary']//tbody/tr[not(@class='blank_row')]",
        "Drawer table body")
    drawer_table_footer = (
        "xpath",
        "//div[@class='cashDrawerSummary']//tfoot/tr[not(@class='blank_row')]",
        "Drawer table footer")
    btn_reconciliation_icons = (
        "xpath",
        "//a[@class='reconcilCash' and not(@style='display: none;')]",
        "Reconciliation button")
    lbl_payments_with_reconciliation_icons = (
        "xpath",
        "//a[@class='reconcilCash' and not(@style='display: none;')]/../"
        "preceding-sibling::td[contains(@class,'paymentMethodText')]",
        "Payments with Reconciliation button")
    btn_cancel = (
        "xpath",
        "//input[@value='Cancel']",
        "Cancel button")
    btn_submit = (
        "xpath",
        "//input[@value='Submit']",
        "Submit button")

    # ---------------------------------------------
    # Post Difference
    # ---------------------------------------------
    pup_post_difference_btn_cancel = (
        "xpath",
        ".//*[@id='widget-kofileinfobubble-cancelui-id1']",
        "Cancel Post Differerence")
    pup_post_diffenece = (
        "xpath",
        ".//*[@id='postDifferenceBubble']",
        "Post Difference popup")
    pup_post_difference_ddl_payment_method = (
        "xpath",
        ".//*[@id='paymentMethod']",
        "Paymant Method field in Post Difference popup")
    pup_post_difference_btn_Post = (
        "xpath",
        ".//*[@id='postDifference']",
        "Post Post Difference")
    pup_post_difference_fld_comment = (
        "xpath",
        ".//*[@id='comment']",
        "Comment field in Post Difference Popup")
    # ---------------------------------------------
    # Links
    # ---------------------------------------------
    lnk_post_difference = (
        "id",
        "postDiffreenceSessionSingle",
        "Post Difference link for non admin")
    lnk_print_drawer_sumamry = (
        "xpath",
        ".//*[@id='printActionContainer']/div[1]/div/span/a",
        "Print Drawer Summary Link")
    # ---------------------------------------------
    # Buttons
    # ---------------------------------------------
    btn_settle = (
        "xpath",
        ".//*[@id='settleSingle']",
        "Settle button"
    )
    btn_order_queue = (
        "xpath",
        ".//*[@id='cancelsummary']",
        "Order Queue button"
    )
    # ---------------------------------------------
    # Print Drawer Success Popup
    # ---------------------------------------------
    pup_success_print_drawer_summary = (
        "xpath",
        ".//*[@id='dialog-content-holder']/div[1]/div",
        "Print Drawer Summary Success Popup")
    pup_success_btn_close = (
        "xpath",
        ".//*[@id='infobox_Close']",
        "Close button on success popup")
    pup_close_icn_X = (
        "xpath",
        "//a[@title = 'Close']",
        "Close success popup by X icon")
    pup_print_success_text = (
        "xpath",
        "//*[@id='dialog-content-holder']/div[2]/div",
        "Print success popup text")
    pup_print_warning_btn_yes = (
        "id",
        "infobox_Yes",
        "Yes button on warning popup")
    pup_print_warning_btn_no = (
        "id",
        "infobox_No",
        "No button on warning popup")
    pup_drawer_initialization = (
        "id",
        "kofile-CashDrawerInitializationContent",
        "Cash drawer initialization popup"
    )
    pup_drawer_btn_inititialize = (
        "id",
        "cashdrawerinitialize-btn",
        "Cash drawer popup initialization button"
    )
    # ---------------------------------------------
    # Cash Reconciliation page-Cancel btn
    # ---------------------------------------------
    btn_cash_reconciliation_cancel = (
        "xpath",
        ".//*[@id='cancelSessionCashReconciliation']",
        "Cash Reconcilation page-Cancel button")
    btn_cash_reconciliation_submit = (
        "xpath",
        ".//*[@id='submitSessionCashReconciliation']",
        "Cash Reconciliation page-Submit button")
    lnk_cash_reconciliation_clear = (
        "xpath",
        ".//*[@id='clearCashReconciliation']",
        "Cash Reconciliiation page-Clear Link")
    # ---------------------------------------------
    # Cash Reconciliation data
    # ---------------------------------------------
    _lbl_cash_reconciliation_calculated_value_by_row = (
        "xpath",
        ".//*[@id='cashReconciliationBlock']/div['%s']/div[3]/div",
        "Cash reconciliation values by row")
    lbl_cash_reconciliation_expected_fee = (
        "xpath",
        "//span[@id='cashTotal' and contains(@data-bind, 'Expected')]",
        "Cash Reconciliation Expected fee")
    lbl_cash_reconciliation_total_fee = (
        "xpath",
        "//span[@id='cashTotal' and contains(@data-bind, 'Total')]",
        "Cash Reconciliation Total fee")
    btn_cheque_reconciliation_cancel_btn = (
        "xpath",
        ".//*[@id='cancelChequeReconciliation']",
        "Cheque Reconciliation Cancel button")
    # ---------------------------------------------
    # Cheque Reconciliation data
    # ---------------------------------------------
    btn_cheque_reconciliation_cancel = (
        "xpath",
        ".//*[@id='cancelSessionChequeReconciliation']",
        "Cheque Reconciliation Cancel button")
    btn_cheque_reconciliation_submit = (
        "xpath",
        ".//*[@id='submitSessionCheckReconciliation']",
        "Cheque Reconciliation Submit button")
    lnk_check_reconciliation_clear = (
        "xpath",
        ".//*[@id='clearChequeReconciliation']",
        "Cheque Reconciliation Clear link")
    rdb_cheque_reconciliation_deposit = (
        "xpath",
        "//input[@id='balanceDetail_Deposited']",
        "Cheque Reconciliation 'Deposit' radiobutton")
    _rdb_cheque_reconciliation_deposit_by_rdb_number = (
        "xpath",
        "(.//*[@id='balanceDetail_Deposited'])['%s']",
        "Cheque Reconciliation Radiobutton Deposit rdb 1st or second")
    lbl_cheque_reconciliation_deposit = (
        "xpath",
        ".//*[@id='balanceDetail_Deposited']/preceding::tr/th[1]",
        "Cheque Reconciliation-Deposit Lbl")
    lbl_cheque_reconciliation_expected_amount = (
        "xpath",
        ".//*[@id='TotalExpected']",
        "Cheque Reconciliation Expected amount")
    lbl_cheque_reconciliation_actual_amount = (
        "xpath",
        ".//*[@id='TotalActual']",
        "Cheque Reconciliation Actual amount")
    # ---------------------------------------------
    # Message
    # ---------------------------------------------
    lbl_drawer_message = (
        "xpath",
        "//*[@id='drawerMsg']",
        "Balance Drawer message")

    # TODO chek when error is appears and check locator
    # error_bloc= (By.CSS_SELECTOR, 'div[class="dialog-title titleBtnClr radiusTop poptitletxt paddingPanel"]')
