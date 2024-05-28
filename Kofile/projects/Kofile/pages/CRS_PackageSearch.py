"""
Package Search Page Object Model
Created by Anna Adamyan
"""
from projects.Kofile.Lib.test_parent import PagesParent


class CRSPackageSearch(PagesParent):
    def __init__(self):
        super(CRSPackageSearch, self).__init__()

    # LOCATORS---------------------------------------------------------------------------------------------------------
    lnk_go_to_order_search = ("xpath", "//li[@id='searching']/a", "Go to 'Order Search' page")
    lnk_go_to_packages = ("xpath", "//li[@id='packageSearch']/a", "Go to 'Packages' page")
    txt_package_id = ("id", "PackageId", "ERecording Package ID")
    txt_customer_name = ("id", "CustomerName", "Customer Name field")
    txt_organization = ("id", "SubmitterName", "Organization field")
    txt_from_date = ("id", "FromDate", "From Date field")
    btn_from_date_picker = ("xpath", "//div[@id='daterange-block']/img[1]", "From Date date picker")
    txt_to_date = ("id", "ToDate", "To Date field")
    btn_to_date_picker = ("xpath", "//div[@id='daterange-block']/img[2]", "To Date date picker")
    btn_search = ("id", "search", "Search button")
    lnk_reset_search = ("id", "resetPackageSearch", "Reset Search action link")
    lbl_no_matches_found = ("xpath", "//div[@class='packageSearchResultBlock']//em", "No match found label")
    result_table_all_rows = ("xpath", "//table[@id='OrderQueue']/tbody/tr", "Result table data all rows")
    ddl_package_id_lookup = ("xpath", "//span[@id='packageIdList' and @style='display: inline;']/a[text()='%s']",
                             "ERecording Package ID search lookup")

    _lbl_result_table_header_by_column_index = (
        "xpath", "//table[@id='OrderQueue']/thead/tr/th[%s]", "Result table header by column index")
    _lbl_result_table_data_by_row_index_by_column_index = (
        "xpath", "//table[@id='orderSearchBlock']/tbody/tr[%s]/td[%s]",
        "Result table data by row index and by column index")
    _lbl_order_number_by_row_index_by_column_index = (
        "xpath", "//table[@id='OrderQueue']/tbody/tr[%s]/td[%s]/a",
        "Result table data by row index and by column index")
    _lbl_result_table_data_by_order_number_by_column_index = (
        "xpath", "//table[@id='OrderQueue']/tbody/tr/td[contains(text(), '%s')]/../td[%s]",
        "Result table data by package id and by column index")

    # HELPER FUNCTIONS------------------------------------------------------------------------------------------------
    @staticmethod
    def order_number_by_row_index(row_index):
        """returns Order# locator by row index"""
        loc = ("xpath", f"//tr[{row_index}]//td[contains(@data-column, 'OrderNumber')]",
               f"Order number in {row_index} row")
        return loc

    def order_number(self, order_number):
        """ returns PackageID locator by order number"""
        return self.__table_data(order_number, "OrderNumber")

    def package_id_by_order_number(self, order_number):
        """ returns PackageID locator by order number"""
        return self.__table_data(order_number, "PackageId")

    def department_by_order_number(self, order_number):
        """returns Department locator by order number"""
        return self.__table_data(order_number, "DepartmentDesc")

    def origin_by_order_number(self, order_number):
        """returns Origin locator by order number"""
        return self.__table_data(order_number, "Origin")

    def organization_by_order_number(self, order_number):
        """returns Organization locator by order number"""
        return self.__table_data(order_number, "SubmitterName")

    def customer_by_order_number(self, order_number):
        """returns Customer locator by order number"""
        return self.__table_data(order_number, "CustomerName")

    def received_on_by_order_number(self, order_number):
        """returns Received On locator by order number"""
        return self.__table_data(order_number, "OrderReceivedOn")

    def recorded_on_by_order_number(self, order_number):
        """returns Recorded On locator by order number"""
        return self.__table_data(order_number, "OrderRecordedOn")

    def recorded_by_by_order_number(self, order_number):
        """returns Recorded By locator by order number"""
        return self.__table_data(order_number, "RecordedBy")

    def number_of_docs_by_order_number(self, order_number):
        """returns Number Of Docs locator by order number"""
        return self.__table_data(order_number, "AdUserName")

    def doc_number_by_order_number(self, order_number):
        """returns Doc Number locator by order number"""
        return self.__table_data(order_number, "DocumentNo")

    @staticmethod
    def __table_data(order_number, queue_column_name):
        locator = ("xpath", f"//td[@data-value='{order_number}']/..//*[contains(@data-column, '{queue_column_name}') "
                            f"or contains(@class, '{queue_column_name}')]",
                   f"Package search result table '{queue_column_name}' column for order '{order_number}'")
        return locator
