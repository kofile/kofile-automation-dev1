# ---------------------------------------------
# Header elements
# ---------------------------------------------
from projects.Kofile.Lib.test_parent import PagesParent


class CRSIndexingEntry(PagesParent):
    def __init__(self):
        super(CRSIndexingEntry, self).__init__()

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
        "//div[text()='Recorded By: ']/span",
        "Recorded By")
    sumbit_block = (
        "id",
        "submit-block",
        "Submit block"
    )

    # ---------------------------------------------
    # Indexing Entry Return Address
    # ---------------------------------------------

    # Todo
    return_address_lnk_Copy_From_Order_Header = (
        "xpath",
        "//*[@id='retAddBlock']//a[contains(text(),'Copy From Order Header')]",
        "Copy From Order Header Link")
    return_address_lnk_Copy_Return_Address = (
        "xpath",
        "//*[@id='retAddBlock']//a[contains(text(),'Copy Return Address')]",
        "Copy Return Address Link")

    # ---------------------------------------------
    # Copy popups items
    # ---------------------------------------------
    pup_copy_property_lnk_copy_from_prior_order_item = (
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
        "id",
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
        "Copy Property checkbox on Copy popup")
    pup_copy_refnames_cbx_copy_grantee = (
        "id",
        "type2",
        "Copy Grantee Checkbox on Copy popup")
    pup_copy_refnames_cbx_copy_grantor = (
        "id",
        "type1",
        "Copy Grantor Checkbox on Copy popup")
    pup_returen_address_warning_popup = (
        "id",
        "dialog-content-holder",
        "Warning Popup in Return address")
    pup_returen_address_warning_btn_yes = (
        "id",
        "infobox_Yes",
        "Yes button on warning popup")
    pup_returen_address_warning_btn_no = (
        "id",
        "infobox_No",
        "No button on warning popup")
    pup_copy_names_lbl_copynames_message = (
        "id",
        "copyNamesMessage",
        "Copy Names Message on Copy Names Popup")

    # ---------------------------------------------
    # Elements after indexing entry form
    # ---------------------------------------------
    lnk_send_order_to_capture_queue = (
        "id",
        "sendToCapture",
        "Send Order to Capture Queue link")
    btn_cancel = (
        "xpath",
        "//input[@id='indexTaskItemCancel']",
        "Cancel button")
    btn_save_and_advance = (
        "id",
        "SaveAdvance",
        "Save and Advance button")

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

    # ---------------------------------------------
    # Indexing Queue New Indexing Task Birth/Death Record
    # ---------------------------------------------
    txt_doc_number = (
        "xpath",
        "//*[@id='Order_OrderItems[0]_Document_InstrumentNumber']",
        "Document Number field")
    txt_recorded_date = (
        "xpath",
        "//*[@id='Order_OrderItems[0]_Document_VitalIndexExtras_DocRecordedDate']",
        "Recorded Date field")
    btn_birth_death_record_save = (
        "id",
        "vitalAccept-Btn",
        "Birth/Death Record, Save button")
    btn_birth_death_record_cancel = (
        "id",
        "vitalCancel-Btn",
        "Birth/Death Record, cancel button")
    icn_birth_death_record_upload = (
        "id",
        "uploadImagePopup",
        "Birth/Death Record, upload button")

    # ---------------------------------------------
    # Search/Upload image screen
    # ---------------------------------------------
    pup_choose_image_btn_search = (
        "xpath",
        "//*[@id='searchDocBtn']",
        "Choose Image, Search button")
    pup_choose_image_txt_search_err = (
        "xpath",
        "//*[@id='search-block']//div[@class = 'notifyjs-bootstrap-base notifyjs-bootstrap-error'] ",
        "Choose Image, Search Validation message")
    pup_choose_image_btn_reset = (
        "xpath",
        "//*[@id='resetBtn']",
        "Choose Image, Reset button")
    pup_choose_image_btn_upload = (
        "xpath",
        "//*[@id='UploadBtn']",
        "Choose Image, Upload button")
    pup_choose_image_btn_cancel = (
        "xpath",
        "//*[@id='closeDialogBtn']",
        "Choose Image, Cancel button")
    pup_choose_image_lnk_return_current_page_to_folder = (
        "xpath",
        "//*[@id='returnPageBtn']",
        "Choose Image, Return Current Page to Folder link")
    _pup_choose_image_folder_by_foldername = (
        "xpath",
        "//*[@id='folderContent']//span[contains(text(), '%s')]",
        "Choose Image, folder selection")
    _pup_choose_image_by_foldername = (
        "xpath",
        "(//*[@id='folderContent']//span[contains(text(), '%s')]/following::div)[1]",
        "Choose Image, image selection")
    # ---------------------------------------------
    # Search section
    # ---------------------------------------------
    pup_choose_image_txt_recorded_year = (
        "xpath",
        "//*[@id='docRecYearInput']",
        "Choose Image, Recorded Year")
    pup_choose_image_txt_doc_number = (
        "xpath",
        "//*[@id='docNumberInput']",
        "Choose Image, Document Number")
    pup_document_lookup_by_doc_number = (
        "xpath",
        "//span[@id='documentNumbersList']//a[contains(text(), '%s')]",
        "Choose Image, Doc lookup")
    pup_choose_image_txt_birth_date = (
        "xpath",
        "//input[@name='birthDate']",
        "Choose Image, Birth Date")
    pup_choose_image_txt_infant_name = (
        "xpath",
        "//input[@id='nameOfApplicant']",
        "Choose Image, Birth Date")
    pup_choose_image_txt_death_date = (
        "xpath",
        "//*[@id='dp1576766511425']",
        "Choose Image, Death Date")
    pup_choose_image_txt_deceased_name = (
        "xpath",
        "//*[@id='nameOfApplicant']",
        "Choose Image, Deceased Name")
    pup_choose_image_txt_recorded_date = (
        "xpath",
        "//*[@id='recordedDate']",
        "Choose Image, Recorded  Date")
    pup_choose_image_txt_mother_name = (
        "xpath",
        "//*[@id='motherName']",
        "Choose Image, Mother Name")
    pup_choose_image_txt_father_name = (
        "xpath",
        "//*[@id='fatherName']",
        "Choose Image, Father Name")
    pup_choose_image_txt_deceased_date = (
        "xpath",
        "//*[@id='deceasedDate']",
        "Choose Image, Father Name")
    # ---------------------------------------------
    # Indexing Entry screen
    # ---------------------------------------------
    type_ahead_checkbox = (
        "id",
        "typeAheadCheckbox",
        "Type Ahead Checkbox"
    )

    grantor_name_input = (
        "xpath",
        "//div[contains(@class, 'grantorPartySection')]//textarea",
        "Grantor Name Input"
    )

    grantee_name_input = (
        "xpath",
        "//div[contains(@class, 'granteePartySection')]//textarea",
        "Grantee Name Input"
    )

    indexing_header = (
        "xpath",
        '//div[@class="indexingTaskEntryHeader"]',
        "Indexing header"
    )

    referer_year = (
        "id",
        "document-year0",
        "First referer year"
    )

    referer_doc_num = (
        "id",
        "document-docNumber0",
        "First referer doc num"
    )

    ref_volpage_block = (
        "xpath",
        "//div[@data-bind='text: ReferenceVolPage']",
        "referer volume and page"
    )

    referer_volume = (
        "id",
        "volume-book0",
        "First referer volume"
    )

    referer_page = (
        "id",
        "volume-page0",
        "First referer page"
    )

    ref_doc_num_res = (
        "xpath",
        "//div[@data-bind='text: ReferenceDocNumDesc']",
        "referer doc number result"
    )

    zoom_btn = (
        "id",
        "ZonalOCR",
        "Zoom btn in image viewer"
    )
    flip_names_first_grantor_cb = (
        "id",
        "zonalOCR-flip_grantor_0",
        "Flip names checkbox for first grantor"
    )
    flip_names_first_grantee_cb = (
        "id",
        "zonalOCR-flip_grantee_0",
        "Flip names checkbox for first grantee"
    )
    split_names_first_grantor_cb = (
        "id",
        "zonalOCR-split_grantor_0",
        "Split names checkbox for first grantor"
    )
    split_names_first_grantee_cb = (
        "id",
        "zonalOCR-split_grantee_0",
        "Split names checkbox for first grantee"
    )
    subdivision_lot = (
        "xpath",
        "//textarea[contains(@id,'subdivision-lot')]",
        "Subdivision lot input"
    )
    subdivision_block = (
        "xpath",
        "//*[contains(@id,'subdivision-block')]",
        "Subdivision book input"
    )
    subdivision_remark = (
        "xpath",
        "//input[contains(@id,'sub-remarks')]|//div[contains(@class,'subdivision')]//"
        "textarea[contains(@id,'subdivision-remarks')]",
        "Subdivision remark input"
    )
    subdivision_township = (
        "xpath",
        "//div[contains(@class,'subdivision')]//textarea[contains(@id,'township-field')]",
        "Subdivision township lookup"
    )
    property_city_block = (
        "id",
        "subdivision-ncb0",
        "Property city block input"
    )
    property_subdivision = (
        "xpath",
        "//textarea[contains(@id,'subdivision-field')]",
        "Property subdivision input"
    )
    property_subdivision_popup = (
        "id",
        "new-subdivision-popup",
        "Property subdivision popup"
    )

    property_new_condominium_popup = (
        "id",
        "kofile-new-condominium-popup",
        "New condominium property popup"
    )

    property_new_prop_popup_yes = (
        "id",
        "infobox_Yes",
        "New property popup yes button"
    )
    property_city = (
        "id",
        "sub-city0",
        "Property city input"
    )
    property_vol = (
        "id",
        "subdivision-volume0",
        "Property volume input"
    )
    property_page = (
        "id",
        "subdivision-page0",
        "Property page input"
    )

    next_doc_link = (
        "id",
        "entryForwardNextDocumentInputLink",
        "Next document"
    )

    preview_content = (
        "id",
        "previewContent",
        "Preview Content contained"
    )

    first_doc_in_search = (
        "xpath",
        "//div[@class='folderGuide']/div[@class='innerFiles']/div[@class='small-icons']",
        "First doc in list"
    )

    subdivision_property_block = (
        "xpath",
        "//div[@class='prop-subdivision controlBlock']",
        "Subdivision's property block"
    )

    add_new_subdivision_btn = (
        "xpath",
        "//a[text() = 'New Subdivision']",
        "The button for adding a new Subdivision property"
    )

    delete_subdivision_btn = (
        "xpath",
        "//div[@class='prop-subdivision controlBlock']//span[@title='Delete']",
        "The button for deleting Subdivision property"
    )

    survey_property_block = (
        "xpath",
        "//div[@class='prop-survey controlBlock']",
        "Survey's property block"
    )

    add_new_survey_btn = (
        "xpath",
        "//a[text() = 'New Survey']",
        "The button for adding a new Survey property"
    )

    delete_survey_btn = (
        "xpath",
        "//div[@class='prop-survey controlBlock']//span[@title='Delete']",
        "The button for deleting Survey property"
    )

    survey_abstract_input = (
        "xpath",
        "//input[contains(@id,'survey-abstract')]",
        "Survey's property Abstract input field"
    )

    survey_block_input = (
        "xpath",
        "//textarea[contains(@id,'survey-block')]",
        "Survey's property Block input field"
    )

    survey_name_input = (
        "xpath",
        "//textarea[contains(@id,'survey-field')]",
        "Survey's property Survey input field"
    )

    survey_township_input = (
        "xpath",
        "//textarea[contains(@id,'survey-townhsip')]",
        "Survey's property Township input field"
    )

    survey_section_input = (
        "xpath",
        "//textarea[contains(@id,'survey-section')]",
        "Survey's property Section input field"
    )

    survey_tract_input = (
        "xpath",
        "//input[contains(@id,'survey-tract')]",
        "Survey's property Tract input field"
    )

    survey_acres_input = (
        "xpath",
        "//input[contains(@id,'survey-acres')]",
        "Survey's property Acres input field"
    )

    description_property_block = (
        "xpath",
        "//div[@class='prop-newdesc controlBlock']",
        "Description's property block"
    )

    add_new_description_btn = (
        "xpath",
        "//a[text() = 'New Desc']",
        "The button in for adding a new Description property"
    )

    delete_description_btn = (
        "xpath",
        "//div[@class='prop-newdesc controlBlock']//span[@title='Delete']",
        "The button for deleting Description property"
    )

    description_property_input = (
        "xpath",
        "//input[contains(@id,'description-legal')]",
        "Description's input field"
    )

    condominium_property_block = (
        "xpath",
        "//div[@class='prop-condominium controlBlock']",
        "Condominium's property block"
    )

    add_new_condominium_btn = (
        "xpath",
        "//a[text() = 'New Condominium']",
        "The button in for adding a new Condominium property"
    )

    delete_condominium_btn = (
        "xpath",
        "//div[@class='prop-condominium controlBlock']//span[@title='Delete']",
        "The button for deleting Condominium property"
    )

    condominium_township = (
        "xpath",
        "//div[contains(@class,'condominium')]//textarea[contains(@id,'township-field')]",
        "Condominium township lookup"
    )

    property_condominium = (
        "xpath",
        "//textarea[contains(@id,'condominium-field')]",
        "Property condominium input"
    )

    condominium_unit_input = (
        "xpath",
        "//textarea[contains(@id,'condominium-unit')]",
        "Condominium unit input"
    )

    condominium_building_input = (
        "xpath",
        "//textarea[contains(@id,'condominium-block')]",
        "Condominium building input"
    )

    condominium_remark = (
        "xpath",
        "//div[contains(@class,'condominium')]//textarea[contains(@id,'subdivision-remarks')]|//"
        "textarea[contains(@id, 'condominium-remarks')]",
        "Condominium remark input"
    )

    unplatted_property_block = (
        "xpath",
        "//div[@class='prop-unplatted controlBlock']",
        "Unplatted's property block"
    )

    add_new_unplatted_btn = (
        "xpath",
        "//a[text() = 'New Unplatted']",
        "The button in for adding a new Unplatted property"
    )

    delete_unplatted_btn = (
        "xpath",
        "//div[@class='prop-unplatted controlBlock']//span[@title='Delete']",
        "The button for deleting Unplatted property"
    )

    unplatted_township_input = (
        "xpath",
        "//div[contains(@class,'unplatted ')]//textarea[contains(@id,'township-field')]",
        "Unplatted township lookup"
    )

    unplatted_section_input = (
        "xpath",
        "//textarea[contains(@id,'unplatted-section')]",
        "Unplatted property Section input field"
    )

    unplatted_half_input = (
        "xpath",
        "//input[contains(@id,'unplatted-half')]",
        "Unplatted property Half input field"
    )

    unplatted_quarter_input = (
        "xpath",
        "//input[contains(@id,'unplatted-quarter')]",
        "Unplatted property Quarter input field"
    )

    unplatted_govlot_input = (
        "xpath",
        "//input[contains(@id,'unplatted-govlot')]",
        "Unplatted property Govlot input field"
    )

    unplatted_corner_input = (
        "xpath",
        "//input[contains(@id,'unplatted-corner')]",
        "Unplatted property Corner input field"
    )

    unplatted_acres_input = (
        "xpath",
        "//textarea[contains(@id,'unplatted-acres')]",
        "Unplatted property Acres input field"
    )

    unplatted_remark = (
        "xpath",
        "//textarea[contains(@id, 'unplatted-remarks')]",
        "Unplatted remark input"
    )

    abstract_prop_block = (
        "xpath",
        "//div[@data-bind-id='PropertyModelControl_Order_OrderItems[0]_Document_Properties']/div/div/div/div",
        "Any properties block on the page"
    )

    doc_type_select = (
        "xpath",
        "//select[contains(@id, 'DocumentTypeId')]",
        "Document type select dropdown"
    )

    liber_input = (
        "xpath",
        "//div[@id='docIdentifires-content']//input[@placeholder='Liber']",
        "Document's Liber input"
    )

    page_input = (
        "xpath",
        "//div[@id='docIdentifires-content']//input[@placeholder='Page']",
        "Document's Page input"
    )

    consideration_input = (
        "xpath",
        "//input[@placeholder='Consideration']",
        "Document's Consideration input"
    )

    property_types_new_links = (
        "xpath",
        "(//div[contains(text(), 'PROPERTY')]//following::div[@class='hideLinkOnCopy action-block'])[1]//"
        "a[not (@style='display: none;')]",
        "Links to add new property types"
    )
    property_types_delete_icon_by_row = (
        "xpath",
        "(//div[contains(text(), 'PROPERTY')]//following::span[@title='Delete'])[%s]",
        "Property types delete icon"
    )

    @staticmethod
    def birth_folder(folder_name: str):
        return "xpath", f"//div[@title='{folder_name}']", "Folder for upload birth cert"

    @staticmethod
    def property_field_locator(property_type, field_name):
        return "xpath", f"//div[contains(@class,'{property_type}')]//*[@placeholder='{field_name}']", \
               "Name of subdivision fields"

    @staticmethod
    def party_name_locator(party_type, field_name):
        return "xpath", f"//input[@data-info-text='{party_type}' and @placeholder = '{field_name}']", \
               "Party section field"
