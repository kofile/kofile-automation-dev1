# ---------------------------------------------
# Header elements
# ---------------------------------------------
from projects.Kofile.Lib.test_parent import PagesParent
from projects.Kofile.pages.CRS_General import General


class CRSOrderQueue(PagesParent):
    def __init__(self):
        super(CRSOrderQueue, self).__init__()

    lbl_order_count = (
        "xpath",
        "//*[@id='orderqueue']/preceding::h3[@class='orderCount']",
        "Order Count")
    lbl_order_count_value = (
        "xpath",
        "//*[@id='orders']/a/span",
        "Order queue orders Count")
    lbl_login_user = (
        "id",
        "loggedInUser",
        "Login user name"
    )
    # ---------------------------------------------
    # Buttons
    # ---------------------------------------------
    btn_add_new_order = (
        "id",
        "addNewOrder",
        "Add new Order icon")
    btn_admin_key = (
        "id",
        "icon-key",
        "Admin key icon")
    btn_next_order = (
        "id",
        "nextOrder",
        "Next Order icon")
    btn_refresh = (
        "xpath",
        "//*[@id='icon-nextorder']/following::li/a",
        'Refresh button')
    # ---------------------------------------------
    # Order Queue Table data
    # ---------------------------------------------
    _lbl_table_data_by_row_by_column_index = (
        "xpath",
        "//table[@id='OrderQueue']/tbody/tr/td[%s]/span[text()='%s']/../../td[%s]",
        "Order Queue table data without icon by row, by column index")

    _lbl_table_data_assigned_by_order_number_by_columns = (
        "xpath",
        "//table[@id='OrderQueue']/tbody/tr/td[%s]/span[text()='%s']/../../td[%s]/input",
        "Order Queue, table data, assigned to by row by column index"
    )
    _lbl_table_data_value_by_order_number_by_columns = (
        "xpath",
        "//table[@id='OrderQueue']/tbody/tr/td[%s]/span[text()='%s']/../../td[%s]/span",
        "Order Queue, table data, value by row by column index"
    )

    _btn_table_data_icon_by_order_number_by_columns = (
        "xpath",
        "//table[@id='OrderQueue']/tbody/tr/td[%s]/span[text()='%s']/../../td[%s]/a",
        "Order Queue, table data, row icon by order number by column indexes"
    )

    lnk_show_all_for_all_departments = (
        "xpath",
        "//table[@id='OrderQueue']/tbody/tr/td[contains(text(), 'SHOW ALL')]",
        "Order Queue, table data, SHOW ALL link for all departments"
    )
    tip_status_comment = (
        "id",
        "mCSB_1_container",
        "Order Queue Status Comment"
    )
    note_success_icon = (
        "xpath",
        "//*[@data-column='OrderItemType_Value']/span[2]",
        "Note tool tip"
    )
    pup_drawer_initialization = (
        "xpath",
        ".//*[@id='dialog-content-holder']//div[@class='dialog-title-left']",
        "Drawer Initialization popup")
    pup_drawer_initialize_btn_initialize = (
        "id",
        "cashdrawerinitialize-btn",
        "Drawer Initialize popup, Initialize button"
    )
    pup_drawer_initialize__btn_close = (
        "xpath",
        "//a[contains(@class,'fancybox-close')]",
        "Drawer Initialize popup, 'Close(X)' button"
    )
    orders_in_queue = (
        "xpath",
        "//td[contains(@data-column,'OrderNumber')]",
        "Rows in Order Queue"
    )
    pup_drawer_new_session_for_the_same_day = (
        "xpath",
        "//div[@id='kofile-validation-fix']//li[1]",
        "Drawer 'new session for the same day' popup")
    pup_drawer_new_session_for_the_same_day__ok_btn = (
        "xpath",
        "//input[@id='infobox_Ok']",
        "Drawer 'new session for the same day' popup OK button")
    # ---------------------------------------------
    # Assign Order Popup
    # ---------------------------------------------
    pup_ddl_assign_name = (
        "xpath",
        ".//*[@id='assignNames_chosen']/a",
        "Assign Name DDL")
    txt_assignedName_search = (
        "xpath",
        ".//*[@id='assignNames_chosen']//following::input",
        "Input assigned name")
    _ddl_assign_name_by_selection = (
        "xpath",
        ".//*[@class='chosen-results']//li[text()='%s']",
        "First name for assign")  # ToDo change
    pup_lbl_assign_order_num = (
        "xpath",
        ".//*[@id='orderNum']",
        "Assigning Order Number")

    pup_assign_btn_add = ("id",
                          "addassignedtoBtn",
                          "Order Queue Assign Order Task popup, Add button")
    pup_btn_assignorder_cancel = (
        "id",
        "widget-kofileinfobubble-cancelui-id1",
        "Cancel btn on popup ")
    pup_assign_ddl_btn_expand = ("xpath",
                                 "//div[@id='assignNames_chosen']/a/div/b",
                                 "Order Queue Assign Order Task popup, expand/collapse button")

    _pup_assign_ddl_select_by_name = ("xpath",
                                      "//div[@id='assignNames_chosen']/div/ul/li[text()='%s']",
                                      "Order Queue Assign Order Task popup, select in ddl by name")

    # pup_initialize_same_drawer   = ("xpath","//*[contains(@class, 'fancybox-outer')]","initialize_same_drawer")
    # cancel icon popup elements
    pup_cancel_txt_reason = General.pup_cancel_txt_reason

    pup_cancel_txt_description = General.pup_cancel_txt_description

    pup_cancel_btn_submit = General.pup_cancel_btn_submit

    pup_cancel_btn_cancel = General.pup_cancel_btn_cancel

    order_number_by_order_number_ = ("xpath", "// span[contains(text(), '%s')]", "Order Number")

    @staticmethod
    def get_admin_assign_path(order):
        return "xpath", f"//td[contains(@data-column,'OrderNumber')]/span[contains(text(),'{order}')]", f"'{order}'"
