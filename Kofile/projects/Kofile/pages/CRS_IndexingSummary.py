# ---------------------------------------------
# Indexing Queue table information
# ---------------------------------------------
from projects.Kofile.Lib.test_parent import PagesParent


class CRSIndexingSummary(PagesParent):
    def __init__(self):
        super(CRSIndexingSummary, self).__init__()

    _indexing_table_information_by_column_index = (
        "xpath",
        ".//*[@id='IndexingTaskSummaryTable']//tbody//td[%s]",
        "IndexingTaskSummary value by column_index")

    _edit_icon = (
        "xpath",
        ".//*[@id='IndexingTaskSummaryTable']//tbody//td[%s]/a",
        "IndexingTaskSummary value by column_index")

    # ---------------------------------------------
    # Links
    # ---------------------------------------------
    lnk_Return_to_indexing_queue = (
        "xpath",
        ".//*[@id='indexingSummaryReturn']",
        "Return to Indexing Queue link")
    lnk_Send_to_administrator = (
        "xpath",
        ".//*[@id='indexingSummaryReturn']//following::a[text()='Send to Administrator']",
        "Send To Administrator Link")
    lnk_Send_order_to_capture_queue = (
        "xpath",
        ".//*[@id='left-block']//following::a[text()='Send Order to Capture Queue']",
        "Send Order to Caprture Queue")

    # ---------------------------------------------
    # Links
    # ---------------------------------------------
    btn_save_order = (
        "xpath",
        ".//*[@id='orderSummarySaveOrder']",
        "Save Order Button")
    btn_next_order = (
        "xpath",
        ".//*[@id='orderSummaryNextOrder']",
        "Next Order Button")

    remark_link = ("xpath", "//a[contains(text(), 'New REMARK')]", "Remark link")
    remark_input = ("xpath", "//input[@placeholder='Remarks']", "Remark input")
    new_desk_link = ("xpath", "//a[contains(text(), 'New Desc')]", "New Desc link")
    new_desk_input = ("xpath", "//input[@placeholder='Legal Description / Remarks']", "New Desc input")

    def image(self):
        """
        returns  Image locator by row_index
        """
        return self.__table_data("Image")

    def order_type(self):
        """
        returns  OrderType locator by row_index
        """
        return self.__table_data("OrderItemType_Value")

    def doc_type(self):
        """
        returns  DocumentType locator by row_index
        """
        return self.__table_data("DocumentType")

    def doc_number(self):
        """
        returns  DocumentNumber locator by row_index
        """
        return self.__table_data("DocumentId")

    def book_page(self):
        """
        returns  Book/Page locator by row_index
        """
        return self.__table_data("Book")

    def pages(self):
        """
        returns  Pages/Copies locator by row_index
        """
        return self.__table_data("NoOfPage")

    def status(self):
        """
        returns  Status locator by row_index
        """
        return self.__table_data("Status")

    def edit_icon(self):
        """
        returns  EditIcon locator by row_index
        """
        return self.__table_data("CanEdit")

    @staticmethod
    def __table_data(queue_column_name):
        suffix = "a" if queue_column_name in ["CanEdit"] else "p" if queue_column_name in ["Image"] else "td"
        locator = ("xpath", f"//{suffix}[contains(@data-bind, '{queue_column_name}')]",
                   f"Result table '{queue_column_name}' column")
        return locator
