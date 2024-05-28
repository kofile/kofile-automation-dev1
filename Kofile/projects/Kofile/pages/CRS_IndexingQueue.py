"""
Indexing Queue Page Object Model
"""
from projects.Kofile.Lib.test_parent import PagesParent


class CRSIndexingQueue(PagesParent):
    def __init__(self):
        super(CRSIndexingQueue, self).__init__()

    lnk_go_to_indexing = (
        "xpath",
        "//li[@id='indexing']/a",
        "Go to 'Indexing' page"
    )
    lbl_order_count_value = (
        "xpath",
        "//*[@id='indexing']/a/span",
        "Indexing queue orders Count")
    # ---------------------------------------------
    # Indexing Queue table header
    # ---------------------------------------------
    _lbl_table_header_by_column_index = (
        "xpath",
        "//table[@id='IndexQueue']/thead/tr/th[%s]",
        "Indexing Queue, table header")
    # ---------------------------------------------
    # Indexing Queue table data
    # ---------------------------------------------

    _lbl_table_data_by_row_by_column_index = (
        'xpath',
        '//table[@id="IndexQueue"]/tbody/tr/td[%s]/span[text()="%s"]/../../td[%s]',
        'Indexing Queue, table data without icon by row by column index')

    _lnk_show_all_by_department_name = (
        "xpath",
        "//table[@id='IndexQueue']/tbody/tr/td[contains(text(), 'SHOW ALL')]/preceding-sibling::td[text()='%s']",
        "Indexing Queue, table data, SHOW ALL link by department name")

    # ---------------------------------------------
    # Indexing Queue buttons
    # ---------------------------------------------
    btn_administrative = (
        "xpath",
        "//li[@id='icon-key']/a",
        "Indexing Queue, Administrative button")
    btn_refresh = (
        "xpath",
        "//li[@id='icon-refresh']/a",
        "Indexing Queue, Refresh button")
    btn_process_next_task = (
        "xpath",
        "//li[@id='icon-processnext']/a",
        "Indexing Queue, Process Next Task button")
    btn_add_new_indexing_task = (
        "xpath",
        "//li[@id='icon-plus']/a",
        "Indexing Queue, Add New Indexing Task button")
    # ---------------------------------------------
    # Indexing Queue miscellaneous
    # ---------------------------------------------
    # imported from Capture Queue POM, see import section of this file
    ddl_administrative_user_group = (
        "xpath",
        "//li[@id='icon-plus']/select",
        "Indexing Queue, Administrative is active, user group dropdown")
    # ---------------------------------------------
    # Indexing Queue Assign Indexing Task popup
    # ---------------------------------------------
    pup_assign_lbl_header = (
        "id",
        "orderNum",
        "Indexing Queue Assign Indexing Task popup, header message")
    pup_assign_txt_name_lookup = (
        "xpath",
        "//div[@id='assignNames_chosen']/div/div/input",
        "Indexing Queue Assign Indexing Task popup, name lookup textbox")
    _pup_assign_ddl_select_by_name = (
        "xpath",
        "//div[@id='assignNames_chosen']/div/ul/li[text()='%s']",
        "Indexing Queue Assign Indexing Task popup, select in ddl by name")
    pup_assign_ddl_value = (
        "xpath",
        "//div[@id='assignNames_chosen']/a/span",
        "Indexing Queue Assign Indexing Task popup, ddl value")
    pup_assign_ddl_btn_expand = (
        "xpath",
        "//div[@id='assignNames_chosen']/a/div/b",
        "Indexing Queue Assign Indexing Task popup, expand/collapse button")
    pup_assign_btn_add = (
        "id",
        "addassignedtoBtn",
        "Indexing Queue Assign Indexing Task popup, Add button")
    pup_assign_btn_cancel = (
        "id",
        "widget-kofileinfobubble-cancel",
        "Indexing Queue Assign Indexing Task popup, Cancel button")
    # ---------------------------------------------
    # Indexing Queue New Indexing Task popup
    # ---------------------------------------------
    # _nit_ stands for New Indexing Task popup
    # ---------------------------------------------
    pup_nit_ddl_doc_group = (
        "id",
        "certificateType",
        "Indexing Queue, New Indexing Task, select doc group dropdown")
    pup_nit_ddl_select_doc_group = (
        "xpath",
        ".//*[@id='certificateType']/option[contains(text(), '%s')]",
        "select Doc group")
    pup_nit_btn_cancel = (
        "id",
        "widget-kofileinfobubble-cancel",
        "Indexing Queue, New Indexing Task, Cancel button")
    pup_nit_btn_submit = (
        "id",
        "addNewCertificateSubmit",
        "Indexing Queue, New Indexing Task, Submit button")

    lnk_show_all_for_all_departments = (
        "xpath",
        "//table[@id='IndexQueue']/tbody/tr/td[contains(text(), 'SHOW ALL')]",
        "Indexing Queue, table data, SHOW ALL link for all departments"
    )

    orders_in_queue = (
        "xpath",
        "//*[@data-bind='foreach: indexTasks']/tr/td[@data-column='Order_OrderHeader_OrderNumber']/span",
        "Rows in Indexing Queue"
    )

    add_new_order_btn = (
        "id",
        "addNewIndexingTask",
        "Add new order button"
    )

    @staticmethod
    def get_order_status_by_number(order_numb):
        """returns Order's status locator by order number"""
        return "xpath", f"//span[text()='{order_numb}']/../following-sibling::td[contains(@data-bind, " \
                        f"'StatusTemplate')]/span", f"Order status for order '{order_numb}' "
