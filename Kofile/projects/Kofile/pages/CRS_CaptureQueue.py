"""
Capture Queue Page Object Model
"""
from projects.Kofile.Lib.test_parent import PagesParent
from projects.Kofile.pages.CRS_General import General


class CRSCaptureQueue(PagesParent):
    def __init__(self):
        super(CRSCaptureQueue, self).__init__()

    lnk_go_to_capture = (
        "xpath",
        "//li[@id='capture']/a",
        "Go to 'Capture' page"
    )
    lbl_order_count_value = (
        "xpath",
        "//*[@id='capture']/a/span",
        "Capture queue orders Count")
    # ---------------------------------------------
    # Capture Queue table header
    # ---------------------------------------------
    _lbl_table_header_by_column_index = (
        "xpath",
        "//table[@id='OrderQueue']/thead/tr/th[%s]",
        "Capture Queue, table header")
    # ---------------------------------------------
    # Capture Queue table data
    # ---------------------------------------------

    _cell_ordernumber_with_icon = (
        "xpath",
        "//table[@id='OrderQueue']/tbody/tr/td[%s]/span[text()='%s']/../../td[%s]",
        "Capture Queue, table data, column data by order number, by column indexes"
    )

    _cell_ordernumber_w_o_icon = (
        "xpath",
        "//table[@id='OrderQueue']/tbody/tr/td[%s][text()='%s']/../td[%s]",
        "Capture Queue, table data, column data by order number, by column indexes"
    )

    lnk_show_all_for_all_departments = (
        "xpath",
        "//table[@id='OrderQueue']/tbody/tr/td[contains(text(), 'SHOW ALL')]",
        "Capture Queue, table data, SHOW ALL link for all departments"
    )

    _cell_checkbox = "/input"
    _cell_row_icon = "/a"

    _lnk_show_all_by_department_name = (
        "xpath",
        "//table[@id='OrderQueue']/tbody/tr/td[contains(text(), 'SHOW ALL')]/preceding-sibling::td[text()='%s']",
        "Capture Queue, table data, SHOW ALL link by department name")

    orders_in_queue = (
        "xpath",
        "//table[@id='OrderQueue']/tbody/tr/td[@data-column='OrderNumber']",
        "Rows in Capture Queue"
    )
    # ---------------------------------------------
    # Capture Queue buttons
    # ---------------------------------------------
    btn_admin_key = (
        "xpath",
        "//*[@id='icon-key']/a/span",
        "Capture Queue, Administrative button")
    btn_start_batch_scan = (
        "xpath",
        "//*[@id='icon-batchscan']/a/span",
        "Capture Queue, Start Batch Scan button")
    btn_refresh = (
        "xpath",
        "//*[@id='icon-refresh']/a/span",
        "Capture Queue, Refresh button")
    # ---------------------------------------------
    # Capture Queue miscellaneous
    # ---------------------------------------------
    lnk_queue_count = (
        "xpath",
        "//h3/span",
        "Queue, order count")
    pup_order_cancel_lbl_order_number = (
        "id",
        "order",
        "Cancel popup order number")
    pup_order_cancel_txt_reason = (
        "id",
        "actionReason",
        "Cancel popup reason textbox")
    pup_order_cancel_txt_description = (
        "id",
        "actionDescription",
        "Cancel popup description textbox")
    pup_order_cancel_btn_cancel = (
        "id",
        "widget-kofileinfobubble-cancelui-id1",
        "Cancel popup Cancel button")
    pup_order_cancel_btn_submit = (
        "id",
        "actionReasonsBtn",
        "Cancel popup Submit button")
    # ---------------------------------------------
    # Capture Queue Upload Image popup
    # ---------------------------------------------
    pup_upload_lbl_rootfolder = (
        "xpath",
        "//div[@id='folderContent']/div[@class='innerFolders']/div/span",
        "Capture Queue, Upload Image popup, root folder")
    pup_upload_lbl_rootfolder_file_by_index = (
        "xpath",
        "//div[@id='folderContent']/div[@class='folderGuide']/div[@class='innerFiles']/div[%s]/span",
        "Capture Queue, Upload Image popup, root folder file by index")
    pup_upload_lbl_subfolder_by_index = (
        "xpath",
        "//div[@id='folderContent']/div[@class='folderGuide']/div[contains(@class,'innerFolders')]/div[%s]/span",
        "Capture Queue, Upload Image popup, root folder, sub_folder by index")
    pup_upload_lbl_subfolder_by_name = (
        "xpath",
        "//div[@id='folderContent']/div[@class='folderGuide']/div[contains(@class,'innerFolders')]/div/span[text()='%s']",
        "Capture Queue, Upload Image popup, root folder, sub_folder by name")
    pup_upload_lbl_file_by_subfolder_index_by_index = (
        "xpath",
        "//div[@id='folderContent']/div[@class='folderGuide']/div[contains(@class,'innerFolders')]/div[%s]/following-sibling::div[@class='folderGuide']/div[@class='innerFiles']/div[%s]/span",
        "Capture Queue, Upload Image popup, sub_folder file by sub_folder index, by index")
    pup_upload_lbl_file_by_subfolder_name_by_index = (
        "xpath",
        "//div[@id='folderContent']/div[@class='folderGuide']/div[contains(@class,'innerFolders')]/div/span[text()='%s']/../following-sibling::div[@class='folderGuide']/div[@class='innerFiles']/div[%s]/span",
        "Capture Queue, Upload Image popup, sub_folder file by sub_folder name, by file index")
    pup_upload_lbl_order_item_id = (
        "xpath",
        "//div[@id='orderItemIds_chosen']/a/span",
        "Capture Queue, Upload Image popup, order item ID")
    pup_upload_ddl_order_item_value = (
        "xpath",
        "//div[@id='orderItemIds_chosen']//ul[@class='chosen-results']/li",
        "Capture Queue, Upload Image popup, order item DDL values")
    pup_upload_txt_recorded_year = (
        "id",
        "docRecYearInput",
        "Capture Queue, Upload Image popup, recorded year")
    pup_ddl_doc_group_doc_number = (
        "xpath",
        "//*[@id='orderItemIds_chosen']/a/span[text() = 'Plats - %s']",
        "Doc_Group_Doc_Number_DDL"
    )
    pup_upload_txt_document_number = (
        "id",
        "docNumberInput",
        "Capture Queue, Upload Image popup, document number")
    pup_upload_btn_search = (
        "id",
        "searchDocBtn",
        "Capture Queue, Upload Image popup, search document button")
    pup_upload_lbl_no_matches_found = (
        "xpath",
        "//*[@id='searchDocBtn']/preceding-sibling::div[contains(@class,'notifyjs-wrapper')]//span",
        "Capture Queue, Upload Image popup, 'No matches found' error popup")
    pup_upload_lnk_reset = (
        "id",
        "resetBtn",
        "Capture Queue, Upload Image popup, Reset button action link")
    pup_upload_lnk_return_current_page_to_folder = (
        "id",
        "returnPageBtn",
        "Capture Queue, Upload Image popup, Return Current Page To Folder action link")
    pup_upload_btn_cancel = (
        "id",
        "closeDialogBtn",
        "Capture Queue, Upload Image popup, Cancel button")
    pup_upload_btn_upload = (
        "id",
        "UploadBtn",
        "Capture Queue, Upload Image popup, Upload button")
    pup_upload_btn_first_page = (
        "id",
        "moveFirst",
        "Capture Queue, Upload Image popup, First Page button")
    pup_upload_btn_previous_page = (
        "id",
        "prevImage",
        "Capture Queue, Upload Image popup, Previous Page button")
    pup_upload_btn_next_page = (
        "id",
        "nextImage",
        "Capture Queue, Upload Image popup, Next Page button")
    pup_upload_btn_last_page = (
        "id",
        "moveLast",
        "Capture Queue, Upload Image popup, Last Page button")
    pup_upload_btn_undo_upload = (
        "id",
        "undoUploadImagePopup",
        "Capture Queue, Upload Image popup, Indo Upload button")
    pup_upload_txt_current_page_number = (
        "id",
        "imagePaging",
        "Capture Queue, Upload Image popup, current page number")
    pup_upload_txt_page_count = (
        "xpath",
        "//div[@id='totalImages']/span",
        "Capture Queue, Upload Image popup, total page count")
    pup_upload_spinner = (
        "xpath",
        "//div[@class='ajax-overlay']",
        "Upload spinner"
    )
    rotate_left_button = (
        "id",
        "rotateLeft",
        "Capture Queue, rotate to left button")

    rotate_right_button = (
        "id",
        "rotateRight",
        "Capture Queue, rotate to right button")
    pup_upload_img = (
        "xpath",
        "//div[@id = 'previewContent']/img",
        "Capture Queue, Upload Image popup, image in image viewer")

    @staticmethod
    def upload_image_icon_by_order_number(order_number):
        """
        returns upload image icon locator by order number
        """
        return General()._queue_xpath_constructor(order_number, "uploadimage")
