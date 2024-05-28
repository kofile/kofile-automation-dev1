"""
CRS main menu items
"""
from golem import actions
import logging

from projects.Kofile.Lib.test_parent import PagesParent


class General(PagesParent):
    def __init__(self):
        super(General, self).__init__()

    # ---------------------------------------------
    # Header elements
    # ---------------------------------------------
    _lnk_Queue_menu_by_name = (
        "xpath",
        "//li[@id='%s']/a",
        "Go to menu page"
    )
    lnk_go_to_orders = ("xpath", "//li[@id='orders']/a", "Go to 'Orders' page")
    lnk_go_to_capture = ("xpath", "//li[@id='capture']/a", "Go to 'Capture' page")
    lnk_go_to_indexing = ("xpath", "//li[@id='indexing']/a", "Go to 'Indexing' page")
    lnk_go_to_verification = ("xpath", "//li[@id='verification']/a", "Go to 'Verification' page")
    lnk_go_to_search = ("xpath", "//li[@id='searching']/a", "Go to 'Search' page")
    lnk_go_to_package_search = ("xpath", "//li[@id='packageSearch']/a", "Go to 'Package Search' page")
    lnk_go_to_reports = ("xpath", "//li[@id='report']/a", "Go to 'Report' page")
    lnk_go_to_front_office = ("xpath", "//li[@id='frontoffice']/a", "Go to 'Front Office' page")

    lbl_order_count = (
        "xpath",
        "//h3[contains(@class,'Count')]/span",
        "Orders Count in Queue")
    orders_in_queue = (
        "xpath",
        "//td[contains(@data-column,'OrderNumber') and (@data-bind or @data-value)]",
        "Rows in Order Queue"
    )
    lnk_submenu_Documents_Search = (
        "xpath",
        "//li/a[contains(text(),'Documents')]",
        "Documents Submenu under Search menu"
    )
    logo = (
        'xpath',
        '//*[@id="wrapper"]/header/div[1]/a/img',
        'logo'
    )
    lbl_user_name = (
        "xpath",
        ".//*[@id='loggedInUser']",
        "Clerk name"
    )
    lbl_bredcrum = (
        "xpath",
        "//*[@id='wrapper']/div[@class='bredcrum']/ul[1]/li[last()]",
        "Last Breadcrumb of the page"
    )
    lbl_front_office = (
        "xpath",
        "//li[@id='frontoffice']/a",
        "Front Office lbl on top of the each page"
    )
    thumbnails = (
        'xpath',
        "//div[@class='thumbnailSelection']",
        "Generated thumbails"
    )
    document_image = (
        "id",
        "documentImage",
        "Document image in imageviewer"
    )
    btn_last_page = (
        "id",
        "moveLast",
        "Last page button of image viewer"
    )
    total_images = (
        "xpath",
        "//div[@id='totalImages' and contains(@data-bind,'documentViewModel')]",
        "Total images of document"
    )
    # ---------------------------------------------
    # Buttons
    # ---------------------------------------------
    btn_add_new_order = (
        "xpath",
        "//a[@class='icon-plus-custom']",
        "Add new Order icon")
    btn_admin_key = (
        "id",
        "icon-key",
        "Admin key icon")
    btn_next_order = (
        "xpath",
        "//a[@class='icon-running-man-custom']",
        "Next Order icon")
    btn_refresh = (
        "xpath",
        "//*[contains(@class,'icon-refresh')]",
        'Refresh button')
    # ---------------------------------------------
    show_all_link = ("xpath", "//td[contains(text(), 'SHOW ALL')]", "SHOW ALL link for all departments")
    # ---------------------------------------------
    # Footer elements
    # ---------------------------------------------
    lbl_footer = (
        "xpath",
        ".//*[@id='footerinner']",
        "footer")
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
        "First name for assign")
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

    pup_assign_ddl_select_by_name = ("xpath",
                                     "//div[@id='assignNames_chosen']/div/ul/li[text()='%s']",
                                     "Order Queue Assign Order Task popup, select in ddl by name")

    # cancel icon popup elements
    pup_cancel_txt_reason = (
        'xpath',
        '//*[@id="actionReason"]',
        'Reason in Cancel popup')

    pup_cancel_txt_description = (
        'xpath',
        '//*[@id="actionDescription"]',
        'Description in Cancel popup')

    pup_cancel_btn_submit = (
        'xpath',
        '//*[@id="actionReasonsBtn"]',
        'Submit button in Cancel popup')

    pup_cancel_btn_cancel = (
        'xpath',
        '//*[@id="widget-kofileinfobubble-cancelui-id1"]',
        'Cancel button in Cancel popup')

    greyed_overlay = (
        'xpath',
        '//div[@class="parent-overlay"]',
        'Div gray overlaying during spinner work'
    )

    @staticmethod
    def _queue_xpath_constructor(order_number, column):
        capture = True if "/Capture/" in actions.get_browser().current_url else False
        column = "IndexingTaskStatusGroup" if column == "StatusDesc" and "ShowIndexQueue" in actions.get_browser().current_url else column
        class_ = ['iconredirectorder', 'iconbatchscan', 'iconassign', 'iconclose',
                  'uploadimage']  # use @class instead of @data-column
        if "running_man" in column:
            column = "iconbatchscan" if capture else "iconredirectorder"  # class names of running man
        elif "FirstName" in column:
            column = "Customer" if capture else column  # 'Customer' column name for queue
        _pref = f"{' and ' if capture else ']/span['}"  # prefix for queue
        prefix = f"//td[contains(@data-column,'OrderNumber'){_pref}contains(text(),'{order_number}')]"
        _suf_1 = f"{'/..' if capture else '/../..'}"  # suffix1 for queue
        _suf_2 = f"{'/a' if column in class_ else ''}"  # suffix2 for some columns
        _suf_3 = f"{'class' if column in class_ else 'data-column'}"  # suffix3 for some columns
        suffix = f"{_suf_1}/td{_suf_2}[contains(@{_suf_3}, '{column}')]"
        end = "/span" if (column == "Status") else "/input" if column == "AssignedTo" else ""
        locator = ("xpath", f"{prefix}{suffix}{end}", f"'{column}' column of '{order_number}' order")
        logging.debug(f"|--- {locator[2]} = '{locator[1]}' ---|")
        return locator

    def running_man_by_order_number(self, order_number):
        """
        returns running man locator by order number,
        """
        return self._queue_xpath_constructor(order_number, "running_man")

    def assign_icon_by_order_number(self, order_number):
        """
        returns assign icon locator by order number,
        """
        return self._queue_xpath_constructor(order_number, "iconassign")

    @staticmethod
    def notes_by_order_number(order_number):
        """
        returns Notes locator by order number,
        """
        return "xpath", f"//span[text()='{order_number}']/following::a", f"Note button for order {order_number}"

    def location_by_order_number(self, order_number):
        """
        returns location locator by order number,
        """
        return self._queue_xpath_constructor(order_number, "Location")

    def origin_by_order_number(self, order_number):
        """
        returns origin locator by order number,
        """
        return self._queue_xpath_constructor(order_number, "Origin")

    def customer_by_order_number(self, order_number):
        """
        returns customer locator by order number,
        """
        return self._queue_xpath_constructor(order_number, "FirstName")

    def department_by_order_number(self, order_number):
        """
        returns department locator by order number,
        """
        return self._queue_xpath_constructor(order_number, "Department")

    def recorded_date_by_order_number(self, order_number):
        """
        returns recorded date locator by order number,
        """
        return self._queue_xpath_constructor(order_number, "Date")

    def status_by_order_number(self, order_number):
        """
        returns status locator by order number,
        """
        return self._queue_xpath_constructor(order_number, "Status")

    def status_desc_by_order_number(self, order_number):
        """
        returns status locator by order number,
        """
        return self._queue_xpath_constructor(order_number, "StatusDesc")

    def assigned_to_by_order_number_text(self, order_number):
        """
        returns assigned to locator by order number,
        """
        return self._queue_xpath_constructor(order_number, "AssignedTo")

    def assigned_to_by_order_number_text_in_indexing(self, order_number):
        """
        returns assigned to locator by order number,
        """
        return self._queue_xpath_constructor(order_number, "AssignedTo_UserName")

    def cancel_by_order_number_text(self, order_number):
        """
        returns cancel icon locator by order number,
        """
        return self._queue_xpath_constructor(order_number, "iconclose")

    @staticmethod
    def order_number_by_doc_number(doc_number, capture_queue=False):
        """
        returns order number locator by document number
        """
        return ("xpath", f"//td[text()='{doc_number}']/preceding-sibling::td[contains(@data-column,'OrderNumber')]"
                         f"{'' if capture_queue else '/span'}", f"Order number by '{doc_number}' Doc number")
