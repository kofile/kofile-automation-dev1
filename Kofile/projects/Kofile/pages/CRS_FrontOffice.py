"""
Front Office Page Object Model
"""
from projects.Kofile.Lib.test_parent import PagesParent


class CRSFrontOffice(PagesParent):
    def __init__(self):
        super(CRSFrontOffice, self).__init__()

    lnk_go_to_orders = (
        "xpath",
        "//li[@id='orders']/a",
        "Go to 'Orders' page")
    front_office_breadcrumb = (
        "xpath",
        "//div[@class='bredcrum']//li[2]",
        "Front Office breadcrumb")
    # ---------------------------------------------
    #  menu items
    # ---------------------------------------------
    lnk_menu_financial = (
        "xpath",
        "//a[text()='Financial']",
        "Financial menu")
    lnk_menu_document = (
        "xpath",
        "//a[text()='Document']",
        "Document menu")
    lnk_menu_system = (
        "xpath",
        "//a[text()='System']",
        "System menu")
    # ---------------------------------------------
    # sub menu items
    # ---------------------------------------------
    # Financial
    lnk_sub_menu_company_accounts = (
        "xpath",
        "//a[text()='Company Accounts']",
        "Company Accounts submenu")
    lnk_sub_menu_nsf_names = (
        "xpath",
        "//a[text()='NSF Names']",
        "NSF Names submenu")
    # ---------------------------------------------
    # Document
    # ---------------------------------------------
    lnk_sub_menu_workflow_dates = (
        "xpath",
        "//a[text()='Workflow Dates']",
        "Workflow Dates submenu")
    # ---------------------------------------------
    # System
    # ---------------------------------------------
    lnk_sub_menu_name_type_ahead = (
        "xpath",
        "//a[text()='Name Type-Ahead']",
        "Name Type-Ahead submenu")
    # ---------------------------------------------
    # _ca_ stands for Company Accounts page
    # ---------------------------------------------
    # ca - search grid
    # ---------------------------------------------
    txt_ca_account_code = (
        "id",
        "AccountCode",
        "Company Accounts, Account Code text field")
    # there is no select element, so only by index option is available
    _ddl_ca_account_code_lookup_by_index = (
        "xpath",
        "//span[@id='resultsAccountCode']/a[%s]",
        "Company Accounts, Account Code lookup by index")
    ddl_ca_account_code_lookup_no_results_found = (
        "id",
        "resultsAccountCode",
        "Company Accounts, Account Code lookup, no results found")
    txt_ca_company_account_name = (
        "id",
        "CompanyAccountName",
        "Company Accounts, Company Account Name text field")
    # there is no select element, so only by index option is available
    _ddl_ca_account_name_lookup_by_index = (
        "xpath",
        "//span[@id='resultsAccountName']/a[%s]",
        "Company Accounts, Account Name lookup by index")
    ddl_ca_account_name_lookup_no_results_found = (
        "id",
        "resultsAccountName",
        "Company Accounts, Account Name lookup, no results found")
    lnk_ca_new_row = (
        "id",
        "newRow",
        "Company Accounts, New Row action link")
    lnk_ca_list_all = (
        "id",
        "listAll",
        "Company Accounts, List All action link")
    lnk_ca_reset_search = (
        "id",
        "resetSearch",
        "Reset Search action link")
    btn_ca_search = (
        "id",
        "searchCmpAccount",
        "Company Accounts, Search button")
    # ---------------------------------------------
    # ca - search results table header
    # ---------------------------------------------
    _lbl_ca_table_header_by_column_index = (
        "xpath",
        "//table[@id='CompanyAccountResultTable']/thead/tr[1]/th[%s+1]",
        "Company Account table header by column index")
    # ---------------------------------------------
    # ca - search results table data
    # ---------------------------------------------
    ca_result_table = (
        "xpath",
        "//table[@id='CompanyAccountResultTable' and not(@style='display: none;')]",
        "Result table"
    )
    ca_found_company_name = (
        "xpath",
        "//td[@class='accountName']/input",
        "Company Account name in result table"
    )
    ca_found_company_code = (
        "xpath",
        "//td[@class='accountCode']/input",
        "Company Account code in result table"
    )
    ca_found_company_edit_btn = (
        "xpath",
        "//td/a[contains(@class,'companyAccounticonedit')]",
        "Company edit button in result table"
    )
    # this locator works for all columns, except Edit column
    _lbl_ca_table_data_by_row_by_column_index = (
        "xpath",
        "//table[@id='CompanyAccountResultTable']/tbody/tr[%s]/td[%s]/input",
        "Company Account table data by row by column index")
    # 'Edit' icon locator
    _btn_ca_table_data_edit_by_row_by_column_index = (
        "xpath",
        "//table[@id='CompanyAccountResultTable']/tbody/tr[%s]/td[%s]/a",
        "Company Account table data 'Edit' icon by row by column index")
    # ---------------------------------------------
    # _cae_ stands for Company Account edit form
    # ---------------------------------------------
    txt_cae_account_code = (
        "xpath",
        "//input[@name='Account.AccountCode']",
        "Company Account Edit, Account Code field")
    cbx_cae_account_active = (
        "xpath",
        "//div[@id='listAccountActive-block']/input",
        "Company Account Edit, Account Active checkbox")
    txt_cae_company_name = (
        "xpath",
        "//input[@name='Account.AccountName']",
        "Company Account Edit, Account Name field")
    txt_cae_company_phone = (
        "xpath",
        "//div[@id='listPhoneNumber-block']/input",
        "Company Account Edit, Account Email field")
    txt_cae_primary_phone_by_index = (
        "xpath",
        "//div[@id='listPhoneNumber-block']/input[%s]",
        "Company Account Edit, Primary Phone by index")
    txt_cae_mailing_address = (
        "xpath",
        "//input[@name='Account.Address.AddressLine1']",
        "Company Account Edit, Mailing Address field")
    txt_cae_city = (
        "xpath",
        "//input[@name='Account.Address.City']",
        "Company Account Edit, City field")
    ddl_cae_state = (
        "xpath",
        "//select[@name='Account.Address.StateCode']",
        "Company Account Edit, State dropdown")
    txt_cae_zip = (
        "xpath",
        "//input[@name='Account.Address.ZipCode']",
        "Company Account Edit, Zip field")
    txt_cae_credit_limit = (
        "xpath",
        "//input[@name='Account.MinimumBalance']",
        "Company Account Edit, Credit Limit field")
    cbx_cae_allow_ordering = (
        "xpath",
        "//input[@name='Account.AllowOrdering']",
        "Company Account Edit, Allow Company Account with Ordering checkbox")
    cbx_cae_allow_erecording = (
        "xpath",
        "//input[@name='Account.AllowERecording']",
        "Company Account Edit, Allow Company Account for E-Recording checkbox")
    cbx_cae_allow_public_search = (
        "xpath",
        "//input[@name='Account.AllowPublicSearch']",
        "Company Account Edit, Allow Company Account with Public Search checkbox")
    radio_cae_ds_per_package = (
        'xpath',
        '//input[@type="radio" and @value="1"]',
        'Company Account Edit, DS Processing Fee - Per Package'
    )
    radio_cae_ds_no_fee = (
        'xpath',
        '//input[@type="radio" and @value="3"]',
        'Company Account Edit, DS Processing Fee - No Fee'
    )
    ddl_cae_nightly_export_billing = (
        'xpath',
        '//select[@name="Account.AccountDetails.OrderItemTypeId"]',
        'Company Account Edit, Nightly Export Billing OIT'
    )
    radio_ds_processing_fee_req_options_first = (
        'xpath',
        '(//*[@class="options-block"]//input[@type="radio" and contains('
        '@data-val-title, "required") or contains(@data-val-title, "required")])[1]',
        "Direct Submission Processing Fee options"
    )
    # ---------------------------------------------
    # Company Account users - table header
    # ---------------------------------------------
    _lbl_cae_users_table_header_by_column_index = (
        "xpath",
        "//div[@data-bind-id='CompanyAccountForm']//table/thead/tr[1]/th[%s]",
        "Company Account Edit, Company Account Users table header by index")
    # ---------------------------------------------
    # Company Account users - table data
    # ---------------------------------------------
    # indexes start from 0
    # ---------------------------------------------
    _txt_cae_users_table_user_by_row = (
        "xpath",
        "//input[@name='Account.UserList[%s].Email']",
        "Company Account Edit, Company Account Users table, User by index")
    _cbx_cae_users_table_enabled_by_row = (
        "xpath",
        "//input[@name='Account.UserList[%s].CompanyUser.IsEnabled']",
        "Company Account Edit, Company Account Users table, Enabled by index")
    _txt_cae_users_table_max_daily_amount_by_row = (
        "xpath",
        "//input[@name='Account.UserList[%s].CompanyUser.DailyLimit']",
        "Company Account Edit, Company Account Users table, Max Daily Amount by index")
    _cbx_cae_users_table_administrator_by_row = (
        "xpath",
        "//input[@name='Account.UserList[%s].CompanyUser.IsAdmin",
        "Company Account Edit, Company Account Users table, Administrator by index")
    _btn_cae_users_table_delete_by_row = (
        "xpath",
        "//div[@data-bind-id='CompanyAccountForm']//table/tbody/tr[%s+1]/td[last()]/a",
        "Company Account Edit, Company Account Users table, delete icon by index")
    lnk_cae_users_table_new_user = (
        "id",
        "newUser",
        "Company Account Edit, Company Account Users table, New User action link")
    txt_new_user_email_field = (
        "id",
        "userEmail",
        "Company Account Edit, Company Account Users table, New User email field")
    found_new_user_email = (
        "xpath",
        "//span[contains(@class, 'autoresultsEmail')]/a",
        "Company Account Edit, Company Account Users table, Found New User email")
    cbx_company_account_user_enable = (
        "xpath",
        "//input[contains(@name,'CompanyUser.IsEnabled')]",
        "Company Account Edit, Company Account Users table, New User 'Enable' checkbox")
    cbx_company_account_user_admin = (
        "xpath",
        "//input[contains(@name,'CompanyUser.IsAdmin')]",
        "Company Account Edit, Company Account Users table, New User 'Administrator' checkbox")
    # ---------------------------------------------
    # Company Accounts entry/edit form buttons
    # ---------------------------------------------
    btn_cae_cancel = (
        "xpath",
        "//div[@data-bind-id='CompanyAccountForm']/div/input[@type='submit' and @value='Cancel']",
        "Company Account Edit, Cancel button")
    btn_cae_save = (
        "id",
        "SaveCompanyAccount",
        "Company Account Edit, Save button")
    btn_cae_save_enabled = (
        "xpath",
        "//input[@id='SaveCompanyAccount' and not(@disabled)]",
        "Company Account Edit, enabled 'Save' button")
    # ---------------------------------------------
    # Name Type ahead page
    # ---------------------------------------------
    # _nta_ stands for Name Type Ahead submenu
    # ---------------------------------------------
    ddl_nta_select_department = (
        "xpath",
        "//div[@id='typeAheadPanel']/div[1]/select",
        "Name Type Ahead, select department dropdown")
    lnk_nta_reset_search = (
        "id",
        "resetSearch",
        "Name Type Ahead, Reset Search action link")
    txt_nta_party_name = (
        "xpath",
        "//div[@id='typeAheadForm']/div[1]/input",
        "Name Type Ahead, Party Name field")
    _ddl_nta_party_name_lbl_by_index = (
        "xpath",
        "//body/ul/li[%s]/a",
        "Name Type Ahead, Party Name dropdown label by index")
    ddl_nta_party_name_no_matches_found = (
        _ddl_nta_party_name_lbl_by_index[0],
        _ddl_nta_party_name_lbl_by_index[1] % 1,
        "Name Type Ahead, Party Name dropdown 'No matches found!'")
    _ddl_nta_party_name_cbx_by_index = (
        "xpath",
        "//body/ul/input[%s]",
        "Name Type Ahead, Party Name dropdown checkbox by index")
    # ---------------------------------------------
    # Name Type Ahead buttons
    # ---------------------------------------------
    btn_nta_search = (
        "id",
        "searchTypeAhead",
        "Name Type Ahead, Search button")
    btn_nta_cancel = (
        "xpath",
        "//div[@id='typeAheadForm']/div[2]/input[@value='Cancel']",
        "Name Type Ahead, Cancel button")
    btn_nta_save = (
        "xpath",
        "//div[@id='typeAheadForm']/div[2]/input[@value='Save']",
        "Name Type Ahead, Save button")
    # ---------------------------------------------
    # Workflow Dates page
    # ---------------------------------------------
    # _wd_ stands for Workflow Dates submenu
    # ---------------------------------------------
    rdb_wd_certification_date_by_department = (
        "id",
        "CertDate",
        "Workflow Dates, Certification Date by department")
    rdb_mail_back_date_by_recorded_date = (
        "id",
        "MailBackDate",
        "Mail Back Date By Recorded Date checkbox")
    lnk_wd_reset_search = lnk_ca_reset_search
    btn_wd_search = (
        "id",
        "searchWorkflowDates",
        "Workflow Dates, Search button")
    # ---------------------------------------------
    # workflow dates table header
    # ---------------------------------------------
    _lbl_wd_table_header_by_column_index = (
        "xpath",
        "//table[@id='WorkflowDatesResultTable']/thead/tr[1]/th[%s]",
        "Workflow Dates, table header by column index")
    # ---------------------------------------------
    # workflow dates table data
    # ---------------------------------------------
    _lbl_wd_department_by_row_by_column_index = (
        "xpath",
        "//table[@id='WorkflowDatesResultTable']/tbody/tr[%s]/td[%s]/span",
        "Workflow Dates, table data, Department by row by column index")
    _lbl_wd_begin_date_by_row_by_column_index = (
        "xpath",
        "//table[@id='WorkflowDatesResultTable']/tbody/tr[%s]/td[%s]/span",
        "Workflow Dates, table data, Begin Date by row by column index")
    _lbl_wd_end_date_by_row_by_column_index = (
        "xpath",
        "//table[@id='WorkflowDatesResultTable']/tbody/tr[%s]/td[%s]/input",
        "Workflow Dates, table data, End Date by row by column index")
    _btn_wd_edit_by_row_by_column_index = (
        "xpath",
        "//table[@id='WorkflowDatesResultTable']/tbody/tr[%s]/td[%s]/a",
        "Workflow Dates, table data, Edit icon by row by column index")
    # ---------------------------------------------
    # workflow dates edit form
    # ---------------------------------------------
    # _wde_ stands for workflow dates edit form
    # ---------------------------------------------
    txt_wde_certified_end_date = (
        "id",
        "certDateEditInput",
        "Workflow Dates, edit row, Certified End Date")
    btn_wde_cancel = (
        "xpath",
        "//div[@id='workflowDatesForm']/div[2]/input[@value='Cancel']",
        "Workflow Dates, edit row, Cancel button")
    btn_wde_save = (
        "xpath",
        "//div[@id='workflowDatesForm']/div[2]/input[@value='Save']",
        "Workflow Dates, edit row, Save button")

    # ---------------------------------------------
    # workflow dates panel
    # ---------------------------------------------
    workflow_dates_panel = (
        "id",
        "workflowDatesPanel",
        "Workflow Dates Panel")
    workflow_dates_panel_start_date = (
        "id",
        "startDate",
        "Recorded Date Range from")
    workflow_dates_panel_end_date = (
        "id",
        "endDate",
        "Recorded Date Range to")
    workflow_dates_panel_search_button = (
        "id",
        "searchWorkflowDates",
        "Recorded Date Range search button")
    workflow_dates_panel_search_result_first_row_edit = (
        "xpath",
        '//*[@id="WorkflowDatesResultTable"]/tbody/tr/td[4]/a',
        "Recorded Date Range first row edit button")
    workflow_dates_panel_search_result_first_row_date = (
        "xpath",
        '//*[@id="WorkflowDatesResultTable"]/tbody/tr/td[3]/input',
        "Recorded Date Range first row date field")
    workflow_dates_panel_search_result_first_row_new_date = (
        "xpath",
        '//*[@id="workflowDatesForm"]/div[1]/div[2]/div/input',
        "Recorded Date Range first row new date input")
    workflow_dates_panel_search_result_first_row_save_new_date = (
        "xpath",
        '//*[@id="workflowDatesForm"]/div[2]/input[2]',
        "Recorded Date Range first row save new date button")
    workflow_dates_panel_search_result_first_row_doc_count = (
        "xpath",
        '//*[@id="WorkflowDatesResultTable"]/tbody/tr/td[2]/span',
        "Recorded Date Range first row doc count field")
    workflow_dates_panel_search_result_first_row_error = (
        "xpath",
        '//*[@id="WorkflowDatesResultTable"]/tbody/tr/td[5]/span',
        "Recorded Date Range first row doc count field")


    @staticmethod
    def get_row_path_workflow_dates_result_table_by_department(dep):
        return (
            "xpath",
            f'//span[text()="{dep}"]/../../td[4]/a',
            "Company edit button in result table"
        )

    @staticmethod
    def ddl_nta_party_name_lbl_by_name(name):
        return "xpath", f"//body/ul/input[translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'," \
                        f"'abcdefghijklmnopqrstuvwxyz')" \
                        f"='{name}']", "Name Type Ahead, Party Name dropdown label by name"
