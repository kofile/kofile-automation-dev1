"""
Clerk Search Page Object Model
"""
# --------------------------------
# HEADER AND FOOTER SECTION
# --------------------------------
from projects.Kofile.Lib.general_helpers import GeneralHelpers
from projects.Kofile.Lib.test_parent import PagesParent


class CSMainPage(PagesParent):
    def __init__(self):
        super(CSMainPage, self).__init__()

    lbl_clerk_name = ("xpath", "//*[@id='divLoginButton']/li[1]", "Clerk name including 'Clerk:'")
    img_top_page_logo = ("xpath", "//*[@id='header']/div[1]/div[1]/a/img", "Top page logo")
    img_bottom_page_logo = ("xpath", "//*[@id='footerinner']/div[2]/img", "Bottom page logo")
    lnk_sign_out = ("id", "signOutLink", "Sign out action link")
    lnk_inbox = ("xpath", "//*[@id='cartSummary']/li[2]/a", "Inbox action link")
    lbl_inbox_count = ("id", "InboxItemsCount", "Inbox item count")
    # --------------------------------
    # SEARCH SECTION
    # --------------------------------
    lnk_department_tab_by_dept_id_ = (
        "xpath", "//*[@id='dept-tab-collection']/li/a[@value='%s']", "Department tab by id")
    lnk_department_tab_by_text_ = ("xpath", "//*[@id='dept-tab-collection']/li/a[text()='%s']",
                                   "Department tab by department text")
    btn_department_right = ("id", "slides-nxt-icon", "Department scroll to right")
    btn_department_left = ("id", "slides-prev-icon", "Department scroll to left")
    lbl_current_department = ("xpath", "//*[@id='searchpanel-curDeptText']/h1",
                              "Current department label including word 'Search'")
    certification_date_range = ("id", "searchpanel-recdet-text", "Certification Date Range")
    txt_search_input = ("id", "SearchText", "Search field")
    btn_search = ("xpath", "//*[@id='searchpanel']//ol[@class='searchcontrol']/li[2]/input", "Start search button")
    lnk_option_pane = ("id", "moreoption", "'More/Less Options' action link")
    lnk_reset_search = ("id", "reset-search", "Reset Search link")
    cbx_search_options_ = ("xpath", "//label[contains(text(), '%s')]/../input", "Search By checkbox")
    txt_recorded_date_from = ("id", "RecordedDate.FromDate", "Recorded Date Range, from field")
    txt_recorded_date_to = ("id", "RecordedDate.ToDate", "Recorded Date Range, to field")
    txt_application_date_from = ("id", "ApplicationDate.FromDate", "Application Date Range, from field")
    txt_application_date_to = ("id", "ApplicationDate.ToDate", "Application Date Range, to field")
    txt_marriage_date_from = ("id", "InstrumentDate.FromDate", "Marriage Date Range, from field")
    txt_marriage_date_to = ("id", "InstrumentDate.ToDate", "Marriage Date Range, to field")
    rbns_and_or_ = ("xpath", "//input[@name='UseAnd']", "Radiobuttons AND and OR")
    rbn_advanced_word_search = ("xpath", "//input[@name='IsAdvancedSearch']", "Radiobutton Advanced Word Search")
    txt_name_search = ("id", "nameSearchText", "Name Search field")
    ddl_name_lookup_ = ("xpath", "//a[@class='ui-corner-all' and (contains(text(), '%s') or contains(text(), '%s'))]",
                        "Advanced Search 'Name' lookup")
    rbn_advanced_search_grantor_option_ = ("xpath", "//label[contains(text(), '%s')]/../input", "")
    cbx_search_using_type_ahead = ("id", "useTypeAhead", "Search Using type Ahead checkbox")
    # --------------------------------
    # SEARCH RESULTS SECTION
    # --------------------------------
    lbl_current_page_number = ("id", "spnCurPage", "Current page number")
    lbl_total_pages = ("id", "spnTotalPage", "Total number of pages in search result")
    lbl_mo_matches_found = ("id", "no-matches-message", "'Sorry, no matches found' message")

    result_table = (
        "id",
        "resultTable",
        "Result table"
    )

    column_header_by_column_index_ = (
        "xpath",
        "//*[@id='resultTable']/thead/tr/th[position()=%s]",
        "Search result table header by column index")
    icn_expand_all = ("id", "expandContractButtonId", "Expand/Collapse all rows")
    row_by_index_ = (
        "xpath",
        "//*[@id='resultTable']/tbody/tr[(position() mod 2)=1][%s]",
        "Result table row by index, starting from 1")
    row_by_doc_num_ = (
        "xpath",
        "//td[@data-column='Number' and contains(text(), '%s')]",
        "Result row by doc number")
    column_data_by_doc_num_ = (
        "xpath",
        "//td[@data-column='Number' and contains(text(), '%s')]/../td[@data-column='%s']",
        "Result row column data by doc number")
    column_data_by_row_and_column_index_ = (
        "xpath",
        "//*[@id='resultTable']/tbody/tr[(position() mod 2)=1][%s]/td[position()=%s]",
        "Result row column data by row index, column index, both starting from 1")
    multidoc_btn = (
        "xpath",
        "//div[contains(@class, 'multidoc')]",
        "multidoc button"
    )
    multidoc_images = (
        "xpath",
        "//div[@class='repeater-container']/div/img",
        "multidoc images"
    )
    multidoc_image = (
        "xpath",
        "//div[@class='repeater-container']/div[%s]/img[%s]",
        "multidoc images"
    )
    # --------------------------------

    def column_data_by_row_and_column_index(self, row_index, column_index):
        return GeneralHelpers.find(GeneralHelpers.make_locator(
            self.column_data_by_row_and_column_index_, row_index, column_index), get_text=True)
