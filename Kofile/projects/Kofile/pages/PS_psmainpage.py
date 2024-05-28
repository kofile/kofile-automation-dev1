from selenium.webdriver.common.by import By

from projects.Kofile.Lib.test_parent import PagesParent

"""
Current tenant PS main page
"""


class PSMainPage(PagesParent):
    def __init__(self):
        super(PSMainPage, self).__init__()

    clerk_name = (By.XPATH, "//*[@id='divLoginButton']/li[1]", "clerk name")
    logo = (By.XPATH, "//a[@class='logo']//img", "Kofile LOGO")
    show_all_search = (By.XPATH, "//td[text()='Search']/following-sibling::td[contains(text(),'SHOW ALL')]", "SHOW ALL")
    show_all_ = (By.XPATH, "//td[contains(text(), 'SHOW ALL')]", "SHOW ALL")
    show_all__recapture = (By.XPATH, "//td[text()='Search']/following::td[contains(text(),'SHOW ALL')]", "SHOW ALL")
    sign_out_link = (By.XPATH, "//*[@id='signOutLink']", "Sign out link")
    inbox_link = (By.XPATH, "//*[@id='cartSummary']/li[2]/a", "Inbox link")
    cart_link = (By.XPATH, "//*[@id='CartDetails']", "Cart link")
    inbox_item_count = (By.XPATH, "//*[@id='InboxItemsCount']", "Inbox item count")
    cart_item_count = (By.XPATH, "//*[@id='CartItemCount']", "Cart item count")
    department_tabs = (By.XPATH, "//*[@id='dept-tab-collection']/li", "Department tabs")
    department_count = (By.XPATH, "//*[@id='dept-tab-collection']/li/a", "Department count")
    dep_next_button = (By.XPATH, "//*[@id='slides-nxt-icon']", "Department Next button")
    dep_prev_button = (By.XPATH, "//*[@id='slides-prev-icon']", "Department Prev button")
    search_title = (By.XPATH, "//*[@id='searchpanel-curDeptText']/h1", "Search title")
    certification_date_range = (By.XPATH, "//*[@id='searchpanel-recdet-text]", "Certification date range")
    search_input = (By.XPATH, "//*[@id='SearchText']", "Search input")
    search_button = (By.XPATH, "//input[@class='searchbutton']", "Search btn")
    result_table = (By.XPATH, "//*[@id='results-table']", "Result table")
    result_table_header = (By.XPATH, "//*[@id='results-table']/table/thead/tr/th", "Result table header")
    result_table_data = (By.XPATH, "//*[@id='results-table']/table/tbody/tr", "Result table data")
    result_table_doc_numbers = (By.XPATH, "//tr[contains(@class,'document-row')]/td[@data-column='Number']",
                                "Document number in result table")
    current_page_number = (By.XPATH, "//*[@id='spnCurPage']", "Current page number")
    current_pages_count = (By.XPATH, "//*[@id='spnTotalPage']", "Current pages count")
    div_pagescount = (By.XPATH, "//*[@id='pagesCount']", "Pages count")
    data_row = (By.XPATH, "//*[@id='results-table']/table/tbody/tr", "Data row")
    load_spiner = (By.XPATH, "html/body/div[3]/div", "load spinner")
    sorry_message = (By.XPATH, "//*[@id='no-matches-message']", "Sorry message")
    recorded_date_from = (By.XPATH, "//*[@id='RecordedDate.FromDate']", "Recorded date from")
    recorded_date_to = (
    By.XPATH, "//*[contains(translate(@id,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
              "'recordeddate.todate')]", "Recorded date to")
    option_pane_button = (By.XPATH, "//*[@id='moreoption']", "Option pane button")
    next_page = (By.XPATH, "//*[@id='paging']/ul/li[last()]/a", "Next page")
    prev_page = (By.XPATH, "//*[@id='paging']/ul/li[1]/a", "Prev page")
    last_row = (By.XPATH, "//*[@id='tabs-template']", "Last row")
    instrument_date_from = (By.XPATH, "//*[@id='InstrumentDate.FromDate']", "Instrument date from")
    instrument_date_to = (By.XPATH, "//*[@id='InstrumentDate.ToDate']", "Instrument date to")
    search_more_panel = (By.XPATH, "//*[@id='searchmorepanel']", "Search more panel")
    expand_btn = (By.XPATH, "//table/tbody/tr[1]/td[@class='expand-document-tabs']", "Expand button")
    doc_rows = (By.XPATH, "//table/tbody/tr[@class='document-row']", "Doc rows")

    """
    option search
    """
    checkboxes = (By.XPATH, "//*[@id='searchfields']/div/ul/li", "Checkboxes")
    pp_checkboxes = (By.XPATH, "//*[@id='partytypes']/div/ul/li", "PartyType Checkboxes")
    dg_checkboxes = (By.XPATH, "//*[@id='documentgroups']/div/ul/li", "DocGroups Checkboxes")
    rb_text_search = (By.XPATH, "//*[@id='searchpanel']/ul/li/ol[4]/li[1]/div/div/label", "RB text search")
    rb_image_search = (By.XPATH, "//*[@id='searchpanel']/ul/li/ol[4]/li[1]/div/div/span/label", "RB image search")
    doc_num_checkbox = (By.XPATH, "//input[@value='DOC#']", "document number checkbox")

    """
    search result
    """
    print_icon = (By.XPATH, "//a[@title='QuickDoc']", "print icon")  # Quick Doc
    print_icon_confirm = (By.XPATH, "//a[@class='widget-kofileinfobubble-download']", "Quick Doc confirm link")
    print_button = (By.XPATH, "//a[@title='Print']", "print button")  # Quick Doc
    add_to_inbox_button = (By.XPATH, "//a[@title='Add to Inbox']", "Add to Inbox")
    company_acc_purchase = (By.XPATH, "//input[@id='companyAccPurchase']", "company acc purchase button")
    inbox_result_number_of_page = (
    By.XPATH, '//*[@id="viewInboxTable"]/tbody/tr[{}]/td[6]', "Inbox first row number of page")
    ms_popup_window = (By.ID, "messageBoxPopup", "Message popup")
    ms_popup_ms = (By.XPATH, "//ul[@class='contactArea']/li", "Message popup ms")
    apply_print = (By.XPATH, "//a[@class='widget-kofileinfobubble-print']", "Apply print link")
    locator_spinner = ("xpath", "//div[contains(@class,'loader')]", "spinner")
    close_popup_btn = (By.ID, "infobox_Close", "Close popup")
    export_result_btn = (By.ID, "exportResultLink", "Export result link")
    export_manager_form = (By.ID, "exportManagerForm", "Export manager form")
    export_manager_exel = (By.ID, "exportmanagerExcel", "Export manager exel")
    export_manager_pdf = (By.ID, "exportmanagerPdf", "Export manager pdf")
    export_manager_csv = (By.ID, "exportmanagerCsv", "Export manager csv")
    export_manager_files = {"exel": export_manager_exel, "pdf": export_manager_pdf, "csv": export_manager_csv}
    is_expand = (By.ID, "isexpand", "is expand")
    apply_export = (By.XPATH, "//a[@class='widget-kofileinfobubble-export']", "Apply export link")
    date_in_result = (By.XPATH, "//td[@data-column='RecordedDateText']", "Recorded date in search result")
    date_in_result_filter = (By.XPATH, "//th[@data-index='RecordedDateText']", "Recorded date in search result filter")
    doc_num_in_result_filter = (By.XPATH, "//th[@data-index='Number']", "Document number in search result filter")
    doc_num_in_result = (By.XPATH, "//td[@data-column='Number']", "Document number in search result")
    grantor_in_result_filter = (By.XPATH, "//th[@data-index='BestMatchGrantor']", "Grantor in search result filter")
    grantor_in_result = (By.XPATH, "//td[@data-column='BestMatchGrantor']", "Grantor in search result")
    grantee_in_result_filter = (By.XPATH, "//th[@data-index='BestMatchGrantee']", "Grantee in search result filter")
    grantee_in_result = (By.XPATH, "//td[@data-column='BestMatchGrantee']", "Grantee in search result")
    doc_type_in_result_filter = (By.XPATH, "//th[@data-index='DocType']", "Doc type in search result filter")
    doc_type_in_result = (By.XPATH, "//td[@data-column='DocType']", "Doc type in search result")
    legal_dept_in_result_filter = (
    By.XPATH, "//th[@data-index='BestMatchLegalDesc']", "Legal dept in search result filter")
    legal_dept_in_result = (By.XPATH, "//td[@data-column='BestMatchLegalDesc']", "Legal dept in search result")
    instrument_date_in_result_filter = (
    By.XPATH, "//th[@data-index='InstrumentDateText']", "Instrument Date in search result filter")
    instrument_date_in_result = (
    By.XPATH, "//td[@data-column='InstrumentDateText']", "Instrument Date in search result")
    book_vol_page_in_result_filter = (By.XPATH, "//th[@data-index='BookPage']", "Book Vol Page in search result filter")
    book_vol_page_in_result = (By.XPATH, "//td[@data-column='BookPage']", "Book Vol Page in search result")
    expand_all_btn = (By.ID, "expandContractButtonId", "Expand all rows button")
    grantor_tab_view = (By.XPATH, "//ul[@data-bind='limit: 5, foreach: Grantor']", "Grantor view")
    grantee_tab_view = (By.XPATH, "//ul[@data-bind='limit: 5, foreach: Grantee']", "Grantee view")
    legal_desc = (By.XPATH, "//ul[@data-bind='limit: 5, foreach: LegalDesc']", "Legal Desc view")
    legal_description_tab = (By.XPATH, "//div[contains(text(), 'Legal Description')]", "Legal Description tab")
    marginal_references_tab = (By.XPATH, "//div[contains(text(), 'Marginal References')]", "Marginal References tab")
    ref_book = (By.XPATH, "//td[@data-column='REF.REF_BOOKPAGE']", "Ref book and page")
    ref_type = (By.XPATH, "//td[@data-column='REF.REF_DOC_TYPE']", "Ref type")
    ref_record = (By.XPATH, "//td[@data-column='REF.REF_RECORDED']", "Ref record")
    document_remarks_tab = (By.XPATH, "//div[contains(text(), 'Document Remarks')]", "Document Remarks tab")
    document_remarks = (By.XPATH, "//ul[@data-bind='limit: 5, foreach: DocumentRemarks']", "Document Remarks view")
    return_address_tab = (By.XPATH, "//div[contains(text(), 'Return Address')]", "Return Address tab")
    return_address = (By.XPATH, "//div[@data-bind='html: ReturnAddress']", "Return Address view")
