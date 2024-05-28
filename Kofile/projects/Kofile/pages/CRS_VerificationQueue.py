"""
Verification Queue Page Object Model
"""

# ---------------------------------------------
# Verification Queue table header
# ---------------------------------------------
from projects.Kofile.Lib.test_parent import PagesParent


class CRSVerificationQueue(PagesParent):
    def __init__(self):
        super(CRSVerificationQueue, self).__init__()

    _lbl_table_header_by_column_index = (
        'xpath',
        '//table[@id="VerificationQueue"]/thead/tr/th[%s]',
        'Verification Queue, table header'
    )
    lbl_order_count_value = (
        "xpath",
        "//*[@id='verification']/a/span",
        "Verification queue orders Count")
    # ---------------------------------------------
    # Verification Queue table data
    # ---------------------------------------------
    _lbl_table_data_by_row_by_column_index = (
        'xpath',
        '//table[@id="VerificationQueue"]/tbody/tr/td[%s]/span[text()="%s"]/../../td[%s]',
        'Verification Queue, table data without icon by row by column index'
    )

    _lbl_table_data_value_by_order_number_by_columns = (
        "xpath",
        "//table[@id='VerificationQueue']/tbody/tr/td[%s]/span[text()='%s']/../../td[%s]/span",
        "Verification Queue, table data, value by row by column index"
    )
    _btn_table_data_icon_by_row_by_column_index = (
        "xpath",
        "//table[@id='VerificationQueue']/tbody/tr[%s]/td[%s]/a",
        "Verification Queue, table data, icon by row by column index"
    )

    _lbl_table_data_assigned_by_order_number_by_columns = (
        "xpath",
        "//table[@id='VerificationQueue']/tbody/tr/td[%s]/span[text()='%s']/../../td[%s]/input",
        "Verification Queue, table data, assigned to by row by column index"
    )
    _lnk_show_all_by_department_name = (
        "xpath",
        "//table[@id='VerificationQueue']/tbody/tr/td[contains(text(), 'SHOW ALL')]/preceding-sibling::td[text()='%s']",
        "Verification Queue, table data, SHOW ALL link by department name"
    )
    # first 'td' - order number column index, second 'td' - running man column index
    _btn_table_data_icon_by_order_number_by_columns = (
        "xpath",
        "//table[@id='VerificationQueue']/tbody/tr/td[%s]/span[text()='%s']/../../td[%s]/a",
        "Verification Queue, table data, row icon by order number by column indexes"
    )
    orders_in_queue = (
        "xpath",
        "//*[@data-bind='foreach: verificationTasks']/tr/td[@data-column='Order_OrderHeader_OrderNumber']/span",
        "Rows in Verification Queue"
    )
    # ---------------------------------------------
    # Verification Queue buttons
    # ---------------------------------------------
    btn_administrative = (
        "xpath",
        "//li[@id='icon-key']/a",
        "Verification Queue, Administrative button"
    )
    btn_refresh = (
        "xpath",
        "//li[@id='icon-refresh']/a",
        "Verification Queue, Refresh button"
    )
    btn_process_next_task = (
        "xpath",
        "//li[@id='icon-processnext']/a",
        "Verification Queue, Process Next Task button"
    )
    btn_cancel_verification_entry = (
        "id",
        "verificationTaskItemCancel",
        "Verification Entry Cancel button")
    btn_save_and_advance_verification_entry = (
        "id",
        "SaveAdvance",
        "Verification Entry Save & Advance button"
    )
    # ---------------------------------------------
    # Verification Queue Assign Verification Task popup
    # ---------------------------------------------
    pup_assign_lbl_header = (
        "id",
        "orderNum",
        "Verification Queue Assign Verification Task popup, header message"
    )
    pup_assign_txt_name_lookup = (
        "xpath",
        "//div[@id='assignNames_chosen']/div/div/input",
        "Verification Queue Assign Verification Task popup, name lookup textbox"
    )
    _pup_assign_ddl_select_by_name = (
        "xpath",
        "//div[@id='assignNames_chosen']/div/ul/li[text()='%s']",
        "Verification Queue Assign Verification Task popup, select in ddl by name"
    )
    pup_assign_ddl_value = (
        "xpath",
        "//div[@id='assignNames_chosen']/a/span",
        "Verification Queue Assign Verification Task popup, ddl value"
    )
    pup_assign_ddl_btn_expand = (
        "xpath",
        "//div[@id='assignNames_chosen']/a/div/b",
        "Verification Queue Assign Verification Task popup, expand/collapse button"
    )
    pup_assign_btn_add = (
        "id",
        "addassignedtoBtn",
        "Verification Queue Assign Verification Task popup, Add button"
    )
    pup_assign_btn_cancel = (
        "id",
        "widget-kofileinfobubble-cancel",
        "Verification Queue Assign Verification Task popup, Cancel button"
    )
    # ---------------------------------------------
    # Verification Queue links
    # ---------------------------------------------
    lnk_send_order_to_capture_queue = (
        'id',
        'sendToCapture',
        'Verification entry Send Order to Capture Queue link'
    )
    lnk_show_all_for_all_departments = (
        "xpath",
        "//table[@id='VerificationQueue']/tbody/tr/td[contains(text(), 'SHOW ALL')]",
        "Verification Queue, table data, SHOW ALL link for all departments"
    )

    note_container = (
        "xpath",
        "//div[@class='historyBlock']",
        "Note container"
    )
