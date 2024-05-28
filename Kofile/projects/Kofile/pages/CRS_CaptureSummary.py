"""
Capture Summary Page Object Model
"""
from projects.Kofile.Lib.test_parent import PagesParent


class CRSCaptureSummary(PagesParent):
    def __init__(self):
        super(CRSCaptureSummary, self).__init__()

    # ---------------------------------------------
    # Capture Summary
    # ---------------------------------------------
    lnk__capture_tab = (
        "xpath",
        "//div[@class='capture-tabs']//li[contains(@data-bind, 'capture')]",
        "Capture Summary, Capture tab")
    lnk__historical_capture_tab = (
        "xpath",
        "//div[@class='capture-tabs']//li[contains(@data-bind, 'historical')]",
        "Capture Summary, 'Historical' Capture tab")
    lnk__prep_ml_tab = (
        "xpath",
        "//div[@class='capture-tabs']//li[contains(@data-bind, 'prepMl')]",
        "Capture Summary, 'Prep ML' Capture tab")
    # ---------------------------------------------
    # Capture Summary buttons
    # ---------------------------------------------
    btn_start_scan = (
        "xpath",
        "//div[@class='captureActionsBar']//span[text()='Start Scan']/../a",
        "Capture Summary, Start Scan button")
    btn_stop_scan = (
        "xpath",
        "//div[@class='captureActionsBar']//span[text()='Stop Scan']/../a",
        "Capture Summary, Stop Scan button")
    btn_open_capture_setup = (
        "xpath",
        "//div[@class='captureActionsBar']/a[1]",
        "Capture Summary, Capture Setup button")
    btn_cancel = (
        "id",
        "cancel",
        "Capture Summary, Cancel button")
    btn_cancel_order = (
        "id",
        "cancleOuter",
        "Capture Summary, Cancel button")
    btn_save_and_exit = (
        "id",
        "save",
        "Capture Summary, Save & Exit button")

    btn_collapse = (
        "xpath",
        "//*[@id='batchScanForm']//div[@class='capture-batch']/div[%s]//a[contains(@class,'capture-collapse')]",
        "Collapse document row button"
    )
    # ---------------------------------------------
    # Capture Summary action links
    # ---------------------------------------------
    lnk_scan_documents__apply_all = (
        "id",
        "scanDocumentsApplyAll",
        "Apply All link")
    lnk_save_batch_for_later_processing = (
        "id",
        "saveForProcessing",
        "Capture Summary, Save Batch for Later Processing")
    inp_reason_popup__reason = (
        "xpath",
        "//input[@id='actionReason']",
        "Reason pop-up *reason* field")
    inp_reason_popup__description = (
        "xpath",
        "//textarea[@id='actionDescription']",
        "Reason pop-up *description* field")
    btn_reason_popup__submit = (
        "xpath",
        "//a[@id='actionReasonsBtn']",
        "Reason pop-up *Submit* button")
    inp_doc_type_attachment = (
        "xpath",
        "//input[@placeholder='Doc Type']",
        "Doc Type input field"
    )
    edit_icon_attachment = (
        "xpath",
        "//a[@title='Edit']",
        "Edit Icon for attachment in capture summary"
    )
    lnk_send_to_administrator = (
        "id",
        "sendToAdmin",
        "Capture Summary, Send to Administrator")
    floating_field = (
        "xpath",
        "//div[@class='floating-label']",
        "Scan Attachment Doc Type Field")
    # ---------------------------------------------
    # Capture Summary table data headers
    # ---------------------------------------------
    # NOT MAPPED
    # ---------------------------------------------
    _lbl_not_mapped_table_header_by_column_index = (
        "xpath",
        "//div[@class='capture-batch']//span[text()='NOT MAPPED']/../../following-sibling::div/table/thead/tr/th[%s]",
        "Capture Summary, not mapped table header, by column index")
    # ---------------------------------------------
    # MAPPED
    # ---------------------------------------------
    _lbl_mapped_table_header_by_ordernumber_by_column_index = (
        "xpath",
        "//div[@class='capture-batch']//span[text()='%s']/../../following-sibling::div/table/thead/tr/th[%s]",
        "Capture Summary, mapped table header, by order number, by column index")
    # ---------------------------------------------
    # Capture Summary table data
    # ---------------------------------------------
    # NOT MAPPED
    # ---------------------------------------------
    # row labels
    _lbl_not_mapped_table_data_by_row_by_column_index = (
        "xpath",
        "//div[@class='capture-batch']//span[text()='NOT MAPPED']/../../../div[2]/table/tbody/tr[position() mod 2 = 1][%s]/td[%s]/div/span",
        "Capture Summary, not mapped table data, row data by row by column index")
    # row icons
    _btn_not_mapped_table_data_by_row_by_column_index = (
        "xpath",
        "//div[@class='capture-batch']//span[text()='NOT MAPPED']/../../../div[2]/table/tbody/tr[position() mod 2 = 1][%s]/td[%s]/a",
        "Capture Summary, not mapped table data, row icons by row by column index")
    # row textboxes
    _txt_not_mapped_table_data_by_row_by_column_index = (
        "xpath",
        "//div[@class='capture-batch']//span[text()='NOT MAPPED']/../../../div[2]/table/tbody/tr[position() mod 2 = 1][%s]/td[%s]/div/div/input",
        "Capture Summary, not mapped table data, row textbox by row by column index")
    # ---------------------------------------------
    # MAPPED
    # ---------------------------------------------
    img_capture_summary = (
        "xpath",
        "//img[@class='gridItemImage']",
        "Image on capture summary row"
    )
    # row labels
    _lbl_mapped_table_data_by_ordernumber_by_row_by_column_index = (
        "xpath",
        "//div[@class='capture-batch']//span[text()='%s']/../../../div[2]/table/tbody/tr[position() mod 2 = 1][%s]/td[%s]/div/span",
        "Capture Summary, mapped table data, row data by order number by row by column index")
    # row icons
    _btn_mapped_table_data_by_ordernumber_by_row_by_column_index = (
        "xpath",
        "//div[@class='capture-batch']//span[text()='%s']/../../../div[2]/table/tbody/tr[position() mod 2 = 1][%s]/td[%s]/a",
        "Capture Summary, mapped table data, row icons by order number by row by column index")
    # row textboxes
    _txt_mapped_table_data_by_ordernumber_by_row_by_column_index = (
        "xpath",
        "//div[@class='capture-batch']//span[text()='%s']/../../../div[2]/table/tbody/tr[position() mod 2 = 1][%s]/td[%s]/div/div/input",
        "Capture Summary, mapped table data, row textbox by order number by row by column index")
    # ---------------------------------------------
    # Capture Summary table data mapped orders (for load testing)
    # ---------------------------------------------
    aux_mapped_table_order_count = (
        "xpath",
        "//div[@class='capture-batch']/div//table",
        "Mapped order row count"
    )
    _aux_mapped_table_doc_count_by_order_row_index = (
        "xpath",
        "//div[@class='capture-batch']/div[%s]//table/tbody/tr[position() mod 2 = 1]",
        "Mapped order order item count by order row index"
    )
    aux_mapped_table_order_numbers = (
        "xpath",
        "//div[@class='capture-batch']/div/div/div/span[not(contains(text(),'NOT MAPPED'))]",
        "Mapped orders, order numbers"
    )
    aux_mapped_table_document_count = (
        "xpath",
        "//div[@class='capture-batch']/div/div/div/span[not(contains(text(),'NOT MAPPED'))]/../../..//table/tbody/tr[position() mod 2 = 1]",
        "Mapped orders, mapped document count"
    )
    _lbl_mapped_table_documents_field_by_column_index = (
        "xpath",
        "//div[@class='capture-batch']/div/div/div/span[not(contains(text(),'NOT MAPPED'))]/../../..//table/tbody/tr[position() mod 2 = 1]/td[%s]/div/span[not(contains(text(),'Original Not Found'))]",
        "Mapped orders, all mapped documents, column by index"
    )
    _aux_lbl_mapped_table_by_order_row_index_by_column_index = (
        "xpath",
        "//div[@class='capture-batch']/div[%s]//table/tbody/tr[position() mod 2 = 1][%s]/td[%s]/div/span",
        "Mapped order item field by order row index, by column index"
    )
    capture_table_row = (
        "xpath",
        "//table[contains(@class,'capture-table')]/tbody/tr[%s]",
        "Capture row by number"
    )
    capture_table_row_before = (
        "xpath",
        "//table[contains(@class,'capture-table')]/tbody//*[text()='Pending']",
        "Capture row (Pending)"
    )
    capture_table_row_after = (
        "xpath",
        "//table[contains(@class,'capture-table')]/tbody//*[text()='Reviewed']",
        "Capture row (Reviewed)"
    )
    # ---------------------------------------------
    # Capture Summary table data doc group / doc type dropdowns
    # ---------------------------------------------
    ddl_doc_group_doc_type_by_text = (
        "xpath",
        "//body/ul[not(contains(@style,'display: none'))]/li/a[text()='%s']",
        "Capture Summary, doc group / doc type dropdown by text")
    # ---------------------------------------------
    # _cs_ stands for Capture Setup popup
    # ---------------------------------------------
    # todo: not finished yet
    pup_cs_tab_scanner_lbl_default_profile = (
        "xpath",
        "//div[@id='CaptureSetupDialog']//div[@data-tab-content='1']//span[contains(@data-bind,'DefaultProfile')]",
        "Capture Summary, Capture Setup, Scanner tab, current profile")
    # ---------------------------------------------
    # Capture Summary Miscellaneous
    # ---------------------------------------------
    lbl_scan_progress_bar = (
        "xpath",
        "//div[contains(@class, 'progressBox')]",
        "Capture Summary, scan progress bar")
    # ---------------------------------------------
    # Capture Summary Confirm popup
    # ---------------------------------------------
    pup_confirm_lbl_message = (
        "xpath",
        "//div[@id='confirm']//span[@class='userMessage']",
        "Popup, message")
    pup_confirm_btn_cancel = (
        "id",
        "CancelButtonId",
        "Popup, Cancel button")
    pup_confirm_btn_ok = (
        "id",
        "YesButtonId",
        "Popup, Ok button")
    # ---------------------------------------------
    # Capture Summary Expanded Indexing div
    # ---------------------------------------------
    div_expanded_indexing = (
        "xpath",
        "//div[@class='indexingFormContainer']",
        "Expanded Indexing div"
    )
    expanded_indexing_fields = (
        "xpath",
        "//div[contains(@data-bind, 'IndexingData')]//*[@placeholder]",
        "Expanded indexing fields")
    txt_ml_recorded_date = ("xpath", "//input[@name='RecordedDate']", "ML expanded indexing Recorded Date")
    # ---------------------------------------------
    # Capture Summary 'No connection' popup
    # ---------------------------------------------
    pup_no_connection_lbl_message = pup_confirm_lbl_message
    pup_no_connection_btn_ok = pup_confirm_btn_ok
    # ---------------------------------------------
    # Capture Summary generated thumbnails
    # ---------------------------------------------
    img_thumbnails = (
        "xpath",
        "//div[@id='thumbnailImageContainer']//div[@id='imageContainer']/ul/li",
        "Generated thumbnails"
    )
    REQ_LOCATOR_FIELD = (
        "xpath",
        "//*[contains(@class,'koValidationError')]",
        "Required field locator"
    )
    img__image_viewer = (
        "xpath",
        "//div[contains(@class,'previewViewerContainer') and not(@style='display: none;')]",
        "Image Viewer visible"
    )
    img__document_image = (
        "xpath",
        "//div[@id='singleImageContainer']/img[@src]",
        "Document image in Image Viewer"
    )

    tab_pre_ml = ("xpath", "//a[text()='Prep ML Recording']", "Ad pre ml tab")
    add_pre_ml = ("xpath", "//a[@class='addPrepMlBtn clickable']", "Ad pre ml button")
    print_app = ("xpath", "//a[@class='prepMlPrintApplication']", "Print application button")
    print_certificate = ("xpath", "//a[@class='prepMlPrintLicense']", "Print certificate button")
    print_app_dialog_text = ("xpath", "//div[@id='print-document-success']/ul", "Print application dialog text")
    print_app_dialog_close_btn = ("id", "infobox_Close", "Print application dialog close button")
    scan_ml_progressbar = ("xpath", "//div[@class='bar']", "scan progressbar")
    scan_ml_btn_start = ("xpath", "//a[@class='prepMlStartScan']", "scan button start")
    scan_ml_btn_stop = ("xpath", "//a[@title='Stop Scan']", "scan button stop")
    scanned_files_ms_count = ("xpath", "//span[@data-bind='text: Scanned']", "Files count")
    first_doc = ("xpath", "//tbody[@data-bind='foreach: documents']/tr", "First document row")
    image_viewer_container = ("xpath", "//div[@class='cropper-container']", "Image viewer container")

    parent_OrderItemTypes = 'parent.OrderItemTypes'

    upload_tab = ("xpath", "//a[@href='#' and text()='Upload']", "Upload tab")
    drop_zone = ("xpath", "//div[@class='uploadDropZone']", "Drop zone")
    edit_button = ("xpath", "//a[@class='orderAdminiconedit']", "Edit button")

    # - - - - - - - - - - Not mapped - - - - - - - - - -
    def doc_group_not_mapped_by_row_index(self, row_num=1):
        """
        returns DocGroup locator by row_index
        """
        return self.__table_data(row_num, "DocumentGroup")

    def doc_type_not_mapped_by_row_index(self, row_num=1):
        """
        returns DocType locator by row_index
        """
        return self.__table_data(row_num, "DocumentType")

    def order_type_ddl_not_mapped_by_row_index(self, row_num=1):
        """
        returns DocType drop-down list locator by row_index
        """
        return self.__table_data(row_num, self.parent_OrderItemTypes if row_num == 0 else "scannedDocumetsTypeList")

    def recorded_year_not_mapped_by_row_index(self, row_num=1):
        """
        returns RecordedYear locator by row_index
        """
        return self.__table_data(row_num, "Year")

    def doc_number_not_mapped_by_row_index(self, row_num=1):
        """
        returns DocNumber locator by row_index
        """
        return self.__table_data(row_num, "Number")

    def pages_not_mapped_by_row_index(self, row_num=1):
        """
        returns pages locator by row_index
        """
        return self.__table_data(row_num, "Pages")

    def status_not_mapped_by_row_index(self, row_num=1):
        """
        returns Status  locator by row_index
        """
        return self.__table_data(row_num, "Status")

    def edit_button_not_mapped_by_row_index(self, row_num=1):
        """
        returns Edit button locator by row_index
        """
        return self.__table_data(row_num, "editDocument")

    def images_not_mapped_by_row_index(self, row_num=1):
        """
        returns Images locator by row_index
        """
        return self.__table_data(row_num, "Scanned")

    # - - - - - - - - - - Mapped - - - - - - - - - -
    def doc_group_mapped_by_row_index(self, order_num, row_num=1):
        """
        returns doc_number  locator by row_index
        """
        return self.__table_dat_mapped(order_num, row_num, "DocumentGroup")

    def doc_type_mapped_by_row_index(self, order_num, row_num=1):
        """
        returns doc_type locator by row_index
        """
        return self.__table_dat_mapped(order_num, row_num, "DocumentType")

    def order_type_ddl_mapped_by_row_index(self, order_num, row_num=1):
        """
        returns DocType drop-down list locator by row_index
        """
        return self.__table_dat_mapped(order_num, row_num, "scannedDocumetsTypeList")

    def recorded_year_mapped_by_row_index(self, order_num, row_num=1):
        """
        returns RecordedYear  locator by row_index
        """
        return self.__table_dat_mapped(order_num, row_num, "Year")

    def doc_number_mapped_by_row_index(self, order_num, row_num=1):
        """
        returns DocNumber  locator by row_index
        """
        return self.__table_dat_mapped(order_num, row_num, "Number")

    def bookpage_mapped_by_row_index(self, order_num, row_num=1):
        """
        returns BookPage  locator by row_index
        """
        return self.__table_dat_mapped(order_num, row_num, "Book")

    def pages_mapped_by_row_index(self, order_num, row_num=1):
        """
        returns Pages  locator by row_index
        """
        return self.__table_dat_mapped(order_num, row_num, "Pages")

    def images_mapped_by_row_index(self, order_num, row_num=1):
        """
        returns Images  locator by row_index
        """
        return self.__table_dat_mapped(order_num, row_num, "Scanned")

    def status_mapped_by_row_index(self, order_num, row_num=1):
        """
        returns Status  locator by row_index
        """
        return self.__table_dat_mapped(order_num, row_num, "Status")

    def edit_mapped_by_row_index(self, order_num, row_num=1):
        """
        returns Edit button  locator by row_index
        """
        return self.__table_dat_mapped(order_num, row_num, "editDocument")

    def expand_index_mapped_by_row_index(self, order_num, row_num=1):
        """
        returns Expand Index button  locator by row_index
        """
        return self.__table_dat_mapped(order_num, row_num, "Expand")

    def deleteicon_mapped_by_row_index(self, order_num, row_num=1):
        """
        returns Delete icon locator by row_index
        """
        return self.__table_dat_mapped(order_num, row_num, "deleteDocument")

    # - - - - - - - - - - Edit Mapped - - - - - - - - - -

    def pages_edit_mapped_by_row_index(self, order_num, row_num=1):
        """
        returns Pages  locator by row_index
        """
        return self.__table_dat_edit_mapped(order_num, row_num, "Pages")

    def __table_data(self, row_num, queue_column_name):
        prefix = "" if (row_num == "all" or queue_column_name == self.parent_OrderItemTypes) else \
            f"//span[@class='tableresult' and text()='NOT MAPPED']/../../..//" \
            f"tr[not(contains(@class,'indexingForm'))][{row_num}]"
        suffix = "input" if queue_column_name in ["DocumentGroup", "DocumentType", "Year", "Number", "Pages"] \
            else "a" if queue_column_name in ["editDocument", "deleteDocument"] \
            else "select" if queue_column_name in ["scannedDocumetsTypeList", self.parent_OrderItemTypes] else "span"
        locator = ("xpath", f"{prefix}//{suffix}[contains(@data-bind, '{queue_column_name}')]",
                   f"Result table '{queue_column_name}' column, '{row_num}' row")
        "//span[@class='tableresult' and text()='NOT MAPPED']/../../..//tr[1]//*[contains(@data-bind, 'DocumentGroup')]"
        "//tr[1]//input[contains(@data-bind, 'DocumentGroup')]"
        return locator

    @staticmethod
    def __table_dat_mapped(order_num, row_num, queue_column_name):
        prefix = f"text()='{order_num}'" if order_num else f"not(text()='NOT MAPPED')"
        suffix = "a" if queue_column_name in ["editDocument", "Expand", "deleteDocument"] \
            else "select" if queue_column_name in ["scannedDocumetsTypeList"] else "span"
        locator = ("xpath", f"//span[{prefix}]/../../..//tr[not(contains(@class, 'indexingForm'))][{row_num}]"
                            f"//{suffix}[contains(@data-bind, '{queue_column_name}')]",
                   f"Result table '{queue_column_name}' column, '{row_num}' row")
        return locator

    @staticmethod
    def __table_dat_edit_mapped(order_num, row_num, queue_column_name):
        prefix = f"text()='{order_num}'" if order_num else f"not(text()='NOT MAPPED')"
        suffix = "a" if queue_column_name in ["editDocument", "Expand", "deleteDocument"] \
            else "select" if queue_column_name in ["scannedDocumetsTypeList"] else "input"
        locator = ("xpath", f"//span[{prefix}]/../../..//tr[not(contains(@class, 'indexingForm'))][{row_num}]"
                            f"//{suffix}[contains(@data-bind, '{queue_column_name}')]",
                   f"Result table '{queue_column_name}' column, '{row_num}' row")
        return locator
