from projects.Kofile.Lib.test_parent import PagesParent


# ---------------------------------------------
# Header elements
# ---------------------------------------------
class CRSVerificationEntry(PagesParent):
    def __init__(self):
        super(CRSVerificationEntry, self).__init__()

    def __48999__(self):
        self.pup_ReKey_Verification_rdb_save_rekey_date = (
            "xpath",
            "//input[@id='save-data']",
            "Save ReKey Data rdb on Rekey Verification Options Popup")

        self.txt_property_tab_first_field = (
            "xpath",
            "//div[@id='property-content']//textarea[1]",
            "First field of PROPERTy tab"
        )

    verification_header = (
        "xpath",
        '//div[@class="verificationTaskEntryHeader"]',
        "Verification header")
    lbl_header_order_number = (
        "xpath",
        "//div[@id='left-block']/div/span",
        "Order Number in header")
    lbl_header_document_number = (
        "xpath",
        "//div[text()='Document Number: ']/span",
        "Document number")
    lbl_header_recorded_date = (
        "xpath",
        "//div[text()='Recorded Date: ']/span",
        "Recorded Date")
    lbl_header_doc_type = (
        "xpath",
        "//div[text()='Document Type: ']/span",
        "Document Type")
    lbl_header_book = (
        "xpath",
        "//div[text()='Book: ']/span",
        "Book number")
    lbl_header_volume = (
        "xpath",
        "//div[text()='Volume: ']/span",
        "Volume")
    lbl_header_page = (
        "xpath",
        "//div[text()='Page: ']/span",
        "Page")
    lbl_header_number_of_pages = (
        "xpath",
        "//div[text()='Number of Pages: ']/span",
        "Number of Pages")
    lbl_header_recorded_by = (
        "xpath",
        "//div[text()='Indexed By: ']/span",
        "Indexed By")
    # ---------------------------------------------
    # Return Address
    # ---------------------------------------------
    icn_expand_return_address = (
        "xpath",
        "//div[@id='retAddArrow']",
        "Expand icon of Return address")
    # ---------------------------------------------
    # Copy popups items
    # ---------------------------------------------

    pup_copy_property_address_lnk_copy_from_prior_order_item = (
        "id",
        "copyfromPriorOrderItemIndexing",
        "Copy From Prior Order Item link on Copy Property popup")
    pup_copy_property_names_lnk_cancel = (
        "id",
        "widget-kofileinfobubble-cancelui-id1",
        "Cancel link on Copy popup")
    pup_copy_property_names_lnk_copy = (
        "id",
        "copyPropertiesBtn",
        "Copy link on Copy Property popup")
    pup_copy_names_lnk_copy = (
        "xpath",
        "copyFromPriorIndex",
        "Copy link on Copy Names Popup")
    pup_copy_txt_recorded_year = (
        "id",
        "recordedYear",
        "Recorded Year field on Popup")
    pup_copy_txt_document_number = (
        "id",
        "documentNumber",
        "Document Number field on Popup")
    pup_copy_txt_volume = (
        "id",
        "volume",
        "Volume field on Popup")
    pup_copy_txt_page = (
        "id",
        "page",
        "Page field on Popup")
    pup_copy_refnames_cbx_copy_property = (
        "id",
        "copyPropertyInBubble",
        "Copy Propery checkbox on Copy popup")
    pup_copy_refnames_cbx_copy_grantee = (
        "id",
        "type2",
        "Copy Grantee Checkbox on Copy popup")
    pup_copy_refnames_cbx_copy_grantor = (
        "id",
        "type1",
        "Copy Grantor Checkbox on Copy popup")
    pup_return_address_warning_popup = (
        "id",
        "dialog-content-holder",
        "Warning Popup in Return address")
    pup_return_address_warning_btn_yes = (
        "id",
        "infobox_Yes",
        "Yes button on warning popup")
    pup_return_address_warning_btn_no = (
        "id",
        "infobox_No",
        "No button on warning popup")
    pup_copy_names_lbl_copynames_message = (
        "id",
        "copyNamesMessage",
        "Copy Names Message on Copy Names Popup")

    copy_btn_in_copy_names_popup = (
        "id",
        "copyNamesBtn",
        "Copy button in the Copy Names pop-up"
    )

    copy_names_link = (
        "id",
        "copyNames%s",
        "Copy Names link for Grantor or Grantee section"
    )
    # ---------------------------------------------
    # Parties
    # ---------------------------------------------
    _grantor_name_by_index = (
        "xpath",
        "(//div[contains(@class, 'grantorPartySection')]//following-sibling::textarea)[%s]",
        "Grantor Name"
    )
    _grantee_name_by_index = (
        "xpath",
        "(//div[contains(@class, 'granteePartySection')]//following-sibling::textarea)[%s]",
        "Grantee Name"
    )
    # ---------------------------------------------
    # ReKey Data
    # ---------------------------------------------
    lnk_view_indexing_data = (
        "id",
        "viewIndexingData",
        "View Indexing Data link for property section")
    lnk_view_indexing_grantor_data = (
        "id",
        "viewIndexingGrantorData",
        "View Indexing Data link for grantor section")
    lnk_view_indexing_grantee_data = (
        "id",
        "viewIndexingGranteeData",
        "View Indexing Data link for grantee section")
    lnk_view_indexing_document_data = (
        "id",
        "viewIndexingDocumentData",
        "View Indexing Data link for document section")
    lnk_closed_indexed_property = (
        "xpath",
        "//*[@id='closeViewIndexingPropertyBtn']",
        "Close link on Indexed")
    lbl_property_grid_text = (
        "xpath",
        "//div[@class='indexingPropertyInfoText']",
        "Property grid text")
    pup_ReKey_warning = (
        "id",
        "dialog-content-holder",
        "Rekey Warning Popup")
    pup_ReKey_warning_btn_yes = (
        "xpath",
        "//*[@id='infobox_Yes']",
        "Yes Button on Rekey Warning Popup")
    pup_ReKey_warning_btn_no = (
        "xpath",
        "//*[@id='infobox_No']",
        "No Button on Rekey Warning Popup")
    pup_ReKey_Verification_rdb_save_rekey_date = (
        "xpath",
        "//*[@id='reKeyVerificationOptionsBubble']//input[@id='save-data']",
        "Save ReKey Data rdb on Rekey Verification Options Popup")
    pup_ReKey_Verification_rdb_restore_date = (
        "xpath",
        "//*[@id='reKeyVerificationOptionsBubble']//input[@id='restore-data']",
        "Restore Indexed Data rdb on Rekey Verification Options Popup ")
    pup_ReKey_Verification_lnk_Return_to_Rekey = (
        "xpath",
        "//*[@id='kofileBubbleFooter']//a[@id='ReturnToRekeyBtn']",
        "Return to Rekey link on ReKey Verification Options popup")
    pup_ReKey_Verification_lnk_Save_Changes = (
        "xpath",
        "//*[@id='kofileBubbleFooter']//a[@id='SaveChangesBtn']",
        "Save Changes link on ReKey Verification Options popup")
    txt_property_tab_first_field = (
        "xpath",
        "((//div[@id='property-content'])//following::input[@type='text'])[1]",
        "First field of PROPERTy tab"
    )
    txt_document_tab_first_field = (
        "xpath",
        "((//div[@id='document-content'])//following::input[@type='text'])[1]",
        "First field of Document tab"
    )
    txt_last_field = (
        "xpath",
        "//*[@id='verificationTaskItemCancel']//preceding::input[@type='text'][1]",
        "Last text field of verification entry"
    )
    # ---------------------------------------------
    # Elements after indexing entry form
    # ---------------------------------------------

    lnk_send_order_to_capture_queue = (
        "id",
        "sendToCapture",
        "Send Order to Capture Queue link")
    btn_cancel = (
        "id",
        "verificationTaskItemCancel",
        "Verification Cancel button")
    btn_save_and_advance = (
        "id",
        "saveAdvance",
        "Verification Save and advance")
    # ---------------------------------------------
    # Send Order To Capture Queue Popup
    # ---------------------------------------------
    pup_send_order_to_capture_txt_reason = (
        "id",
        "actionReason",
        "Send Order to Capture Queue reason field")
    pup_send_order_to_capture_txt_description = (
        "id",
        "actionDescription",
        "Send Order to Capture Queue Description field")
    pup_send_order_to_capture_lnk_cancel = (
        "id",
        "widget-kofileinfobubble-cancelui-id1",
        "Send Order to Capture Queue Cancel link")
    pup_send_order_to_capture_lnk_submit = (
        "id",
        "actionReasonsBtn",
        "Send Order to Capture Queue Submit link")
    confirm_popup = (
        "id",
        "dialog-content-holder",
        "Confirm popup"
    )

    send_document_to_index_checkbox = (
        "xpath",
        "//div[@class='sendDocumentToIndexingQueueOverlayblock']",
        "Send Document To Index Checkbox"
    )

    send_document_to_indexing_queue_input = (
        "id",
        "sendDocumentToIndexingQueueInput",
        "Send Document To Index Input"
    )

    send_order_to_indexing_queue_button = (
        "xpath",
        "//a[text()='Send Order to Indexing Queue']",
        "Send order To Index button"
    )
    pup_choose_document = (
        "xpath",
        "//*[@id='dialog-content-holder']//tbody/tr[1]",
        "First document from choose document popup"
    )
    btn_choose_from_pup_choose_doc = (
        "xpath",
        "//*[@id='dialog-content-holder']//a[text()='Choose']",
        "Choose button from Choose document popup"
    )

    abstract_prop_block = (
        "xpath",
        "//div[@data-bind-id='ReKeyPropertyGridControl_Order_OrderItems[0]_Document_Properties']/div/div/div/div",
        "Any properties block on the page"
    )

    doc_type_select = (
        "xpath",
        "//select[contains(@name, 'DocumentTypeId')]",
        "Document type select dropdown"
    )

    book_input = (
        "xpath",
        "//input[@placeholder='Book']",
        "Document's Book input"
    )

    volume_input = (
        "xpath",
        "//input[@placeholder='Volume']",
        "Document's Volume input"
    )

    page_input = (
        "xpath",
        "//input[@placeholder='Page']",
        "Document's Page input"
    )

    consideration_input = (
        "xpath",
        "//input[@placeholder='Consideration Amount']",
        "Document's Consideration Amount input"
    )

    parcel_id_input = (
        "xpath",
        "//input[@placeholder='Parcel Id']",
        "Prop address's Parcel ID input"
    )

    rekey_row_in_view_indexed_data = (
        "xpath",
        "//div[contains(@id,'viewIndexing')]//div[@class='%s controlBlock']",
        "ReKey row in the view indexed data block"
    )

    doc_type_select_in_view_indexed_data = (
        "xpath",
        "//div[@id='viewIndexingDocumentDataContent']//select[@readonly='true' and contains(@data-bind, 'Document Type')]",
        "Document type select in the view indexed data block"
    )

    book_vol_page_input_in_view_indexed_data = (
        "xpath",
        "//div[@class='bookPageBlock bookPageBlockAbsPos']//*[@readonly='true' and @placeholder='%s']",
        "Book or Volume or Page input in the view indexed data block"
    )

    cons_amount_input_in_view_indexed_data = (
        "xpath",
        "//div[@id='viewIndexingDocumentDataContent']//input[@readonly='true' and @placeholder='Consideration Amount']",
        "Consideration Amount input in the view indexed data block"
    )

    view_indexed_section_title = (
        "xpath",
        "//div[@class='section-label indexed-data-title' and text() = 'INDEXED %s']",
        "Title in the view indexed data section"
    )
    instrument_date = (
        "xpath",
        "//input[@placeholder='Instrument Date']",
        "Instrument Date"
    )
