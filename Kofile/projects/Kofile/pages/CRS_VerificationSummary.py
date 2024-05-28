"""
Verification Summary Page Object Model
"""

# ---------------------------------------------
# Verification Summary table data
# ---------------------------------------------
from projects.Kofile.Lib.test_parent import PagesParent


class CRSVerificationSummary(PagesParent):
    def __init__(self):
        super(CRSVerificationSummary, self).__init__()

    _lbl_table_data_by_row_by_column_index = ('xpath',
                                              '//table[@id="VerificationTaskSummaryTable"]/tbody/tr[%s]/td[%s]',
                                              'Verification Summary, table data without icon by row by column index')
    _btn_table_data_icon_by_row_by_column_index = ("xpath",
                                                   "//table[@id='VerificationTaskSummaryTable']/tbody/tr[%s]/td[%s]/a",
                                                   "Verification Summary, table icon by row by column index")
    _img_table_data_icon_by_row_index = ('xpath',
                                         '//table[@id="VerificationTaskSummaryTable"]/tbody/tr[%s]/'
                                         'td[@data-column="Image"]/p',
                                         'Verification summary, table image by row index')
    img_table_data = (
        "xpath",
        "//p[@class='verificationSummaryRowImage gridImage']",
        "iamge icon on verification summary row"
    )
    # ---------------------------------------------
    # Verification Summary text
    # ---------------------------------------------
    txt_total_items = ('id',
                       'totalCount',
                       'Verification Summary Total Items')
    # ---------------------------------------------
    # Verification Summary links
    # ---------------------------------------------
    _lnk_bredcrums_by_index = ('xpath',
                               '//div[@class="bredcrum"]/ul/li[%s]',
                               'Verification Summary bredcrums')
    lnk_return_to_verification_queue = ('id',
                                        'orderSummaryCancel',
                                        'Verification Summary Return to Verification Queue link')
    lnk_send_to_administrator = ('id',
                                 'sendToAdministrator',
                                 'Verification Summary Send to Administrator link')
    lnk_send_order_to_capture_queue = ('xpath',
                                       '//a[contains(@class, "sendToCaptureBtn")]',
                                       'Verification Summary Send Order to Capture Queue link')
    lnk_send_order_to_indexing_queue = ('xpath',
                                        "//a[text()='Send Order to Indexing Queue']",
                                        'Verification Summary Send Order to Indexing Queue link')
    # ---------------------------------------------
    # Verification Summary buttons
    # ---------------------------------------------
    btn_save_order = ('id',
                      'orderSummarySaveOrder',
                      'Verification Summary Save Order button')
    btn_next_order = ('id',
                      'orderSummaryNextOrder',
                      'Verification Summary Next Order button')
    # ---------------------------------------------
    # Send Order To Administrator Popup
    # ---------------------------------------------
    pup_send_order_to_admin_txt_reason = (
        "id",
        "actionReason",
        "Send Order to Adninistrator reason field")
    pup_send_order_to_admin_txt_description = (
        "id",
        "actionDescription",
        "Send Order to Administrator Description field")
    pup_send_order_to_admin_lnk_cancel = (
        "id",
        "widget-kofileinfobubble-cancelui-id1",
        "Send Order to Administrator Cancel link")
    pup_send_order_to_admin_lnk_submit = (
        "id",
        "actionReasonsBtn",
        "Send Order to Administrator Submit link")

    def image_by_row(self, row_num=1):
        """
        returns Image locator by row_index
        """
        return self.__table_data(row_num, "verificationSummaryRowImage ")

    def order_type_by_row(self, row_num=1):
        """
        returns OrderType locator by row_index
        """
        return self.__table_data(row_num, "OrderItemType_Value")

    def doc_type_by_row(self, row_num=1):
        """
        returns DocumentType locator by row_index
        """
        return self.__table_data(row_num, "Document_DocumentType")

    def doc_number_by_row(self, row_num=1):
        """
        returns DocumentNumber locator by row_index
        """
        return self.__table_data(row_num, "Document_DocumentId")

    def book_page_by_row(self, row_num=1):
        """
        returns Book/Page locator by row_index
        """
        return self.__table_data(row_num, "Document_Book")

    def pages_by_row(self, row_num=1):
        """
        returns Pages/Copies locator by row_index
        """
        return self.__table_data(row_num, "NoOfPage")

    def status_by_row(self, row_num=1):
        """
        returns Status locator by row_index
        """
        return self.__table_data(row_num, "VerificationTaskStatusGroup")

    def editicon_by_row(self, row_num=1):
        """
        returns EditIcon locator by row_index
        """
        return self.__table_data(row_num, "orderSummaryiconedit ")

    @staticmethod
    def __table_data(row_num, queue_column_name):
        locator = ("xpath", f"//tr[{row_num}]//*[contains(@data-bind, '{queue_column_name}') "
                            f"or contains(@class, '{queue_column_name}')]",
                   f"Result table '{queue_column_name}' column")
        return locator
