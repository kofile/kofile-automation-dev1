"""
Order Entry page object model
"""
# ---------------------------------------------
# links
# ---------------------------------------------
from typing import Tuple

from projects.Kofile.Lib.test_parent import PagesParent


class CRSOrderEntry(PagesParent):
    def __init__(self):
        super(CRSOrderEntry, self).__init__()

    lnk_order_entry_tab = ('xpath', '//ul[@id ="orderTypeTabs"]//a[contains(text(), "%s")]', 'Order entry tabs by name')
    no_fee_cb = ("id", "NoFee", "No fee Checkbox")
    image_row = ("xpath", "//tr[@class='rowcolor']", "Image row")
    county_cert_distribution = ("xpath", "//input[@value='CountyCertDistribution']", "County Cert Distribution checkbox")
    state_cert_distribution = ("xpath", "//input[@value='StateCertDistribution']", "State Cert Distribution checkbox")
    birth_verification_letter = ("xpath", "//input[@value='BirthVerificationLetter']", "Birth Verification Letter checkbox")
    birth_certificate = ("xpath", "//input[@value='BirthCertificate']", "Birth Certificate checkbox")
    serial_number_btn = ("xpath", "//a[contains(@class, 'serialNumberIcon')]", "Serial number icon")

    inp_account_code = ('id', 'accountName', 'Account code input')
    inp_account_email = ('id', 'AccountEmail', 'Account email input')
    inp_account_name = ('id', 'CustomerName', 'Account name input')

    recorded_date_fromdate = ('id', 'fromdate', 'Recorded Date Range-FromDate')
    recorded_date_todate = ('id', 'todate', 'Recorded Date Range-ToDate')
    btn_schedule_order = ('xpath', "//input[starts-with(@id, 'scheduleOrder')]", "Schedule Order Button")
    account_search_result = (
        'xpath', '//span[@id="accounts" and not(@style="display: none;")]', 'Account search result')
    recorded_date = ('id', 'recordedDateRange-block', 'Recorded date range')
    # ---------------------------------------------
    # More Options
    # ---------------------------------------------
    lnk_more_options = ('xpath', '//a[text()="More Options"]', 'More Options link')
    lnk_less_options = ('xpath', '//a[text()="Less Options"]', 'Less Options link')
    more_options_block = ('xpath', '//div[@id="orderHeaderCustomerInfo" and not(@style="display: none;")]',
                          'More Options block')
    new_user_email_field = ('id', 'CustomerEmail', 'New user email field')
    new_user_first_name = ('id', 'CustomerFirstName', 'New user first name field')
    new_user_last_name = ('id', 'CustomerLastName', 'New user last name field')
    exp_date = ('id', 'ScheduleCriteria_ExportExpireDate', 'Date Export Expires field')

    lnk_new_registration = ('xpath', '//div[contains(@class, "registration-text")]/a', 'New registration button')
    lbl_success_registration = ("xpath", "//span[@class='orderHeadervalidationError text-green']",
                                "Success registration text")

    _ohc_ = '//div[@id="orderHeaderCustomerInfo"]//input[contains(@name, "{}")]'
    inp_customer__name = ('xpath', _ohc_.format("AddressName"), 'Order header customer name')
    inp_customer__addr1 = ('xpath', _ohc_.format("AddressLine1"), 'Order header customer address1')
    inp_customer__zip = ('xpath', _ohc_.format("ZipCode"), 'Order header customer ZipCode')
    inp_customer__city = ('xpath', _ohc_.format("City"), 'Order header customer City')
    inp_customer__state = ('xpath', _ohc_.format("StateCode"), 'Order header customer State code')
    inp_customer__state_name = ('xpath', '//div[@id="orderHeaderCustomerInfo"]//option[@value="%s"]',
                                'Order header customer State name')
    ddl_customer_state = ('xpath', '//div[@id="orderHeaderCustomerInfo"]//select[contains(@data-bind, "StateCode")]',
                          'Order header State code dropdown')

    # ---------------------------------------------
    # dropdown lists and elements
    # ---------------------------------------------
    ddl_order_type = ('id', 'orderTypeId', 'Order type dropdown')
    _ddl_order_type_item = (
        'xpath', '//select[@id="orderTypeId"]/option[text()="%s"]', 'Order type dropdown item by text')
    _ddl_nsf_lookup_by_order_num = ('xpath', '//*[@id="orderTab"]//div//a[text()="%s"]', 'NFS Order Number lookup')
    txt_order_doc_type = ("id", "autoOrderType", "Order Document Type textbox")
    ddl_order_doc_type_by_ordertype_by_doctype = ("xpath", "(//a[contains(text(),'%s')])[starts-with(text(),'%s(')]",
                                                  "Order Document Type listbox by order type, by document type")
    ddl_order_item_tab_doc_type = ("xpath", "//select[@id='Order_OrderItems[0]_Document_DocumentTypeId']",
                                   "Document Type DDL in Order Item tab")
    btn_gov_fee_distribution_submit = ("id", "widget-kofileinfobubble-submitui-id1",
                                       "Governmentals fee distribution submit button")
    ddl_gov_fee_distribution_copy_from = ("xpath", "//div[@id='feeDistributionContentOIT']//select",
                                          "Governmentals fee distribution popup, Copy From DDL")
    ddl_gov_fee_distribution_copy_options = ("xpath", "//*[@id='feeDistributionContentOIT']//select/option",
                                             "Governmentals fee distribution popup, Copy Options")
    lbl_gov_fee_distribution_fee_fund_name = (
        "xpath",
        "//tbody//th[text()='Fund']//following::td[contains(@data-bind,'FeeFundDesc')]",
        "Governmentals fee distribution popup, FeeFund Name")
    lbl_gov_fee_distribution_fee_total_amount = (
        "xpath",
        "//tbody//th[text()='Fund']//following::span[contains(@data-bind, 'savedTotal')]",
        "Governmentals fee distribution popup, Total amount"
    )
    inp_gov_fee_distribution_fee_value = (
        "xpath",
        "//tbody//th[text()='Fund']//following::input[@class='feeValue']",
        "Governmentals fee distribution popup, input FeeFund value"
    )
    btn_assumed_name_infobox_cancel = ("id", "infobox_Cancel", "Assumed name infobox cancel button")
    pup_nsf = ('id', 'NsfOrderPaymentsBubble', 'NSF popup')

    ddl_additional_fee = ("xpath", "//*[@name='AdditionalFees.DocumentFee']", "Additional Fee Drop-down")
    ddl_additional_fee_options = ("xpath", "(//*[@name='AdditionalFees.DocumentFee'])[1]//option",
                                  "Additional Fee Options")
    ddl_additional_fee_selected_text = ("xpath", "//*[@name='AdditionalFees.DocumentFee']//option[2]",
                                        "Additional Fee Selected text")
    inp_slide_field = ("xpath", "//input[@id='bookpage-page-lookup']", "Slide field")      # noqa
    lkp_slide_lookup_list_options = (
        "xpath",
        "//a[contains(@data-bind, 'AutoResultCompleteKo')]",
        "Slide lookup options"
    )
    # ---------------------------------------------
    # checkboxes
    # ---------------------------------------------
    chk_penalty = ("id", "Penalty", "Penalty checkbox")
    chk_missing_grantee_addresses = ("id", "MissingGranteeAddresses", "Missing Grantee Addresses checkbox")
    chk_duplicate_prior_item = (
        'id', 'duplicatePriorItem', 'Duplicate Prior Order Item to Create Multi-Document checkbox')
    chk_reference_prior_item = ('id', 'chkRefPriorOrderItem', 'Reference Prior Order Item')
    chk_nsf = ('xpath', '//*[@id="NsfOrderPaymentsBubble"]/div//table/tbody/tr/td[5]/input', 'NSF checkbox')
    # ---------------------------------------------
    # buttons
    # ---------------------------------------------
    btn_start_batch_scan = ('xpath', '//button[@id="orderQueueStartBatchScan"]', 'Start Batch Scan button')
    btn_cancel_order = ('xpath', '//li[@id="cancleOuter"]/input', 'Cancel button')
    btn_add_to_order: Tuple[str, str, str] = ('xpath', '//li[@id="addToOrderOuter"]/input', 'Add To Order button')
    btn_nsf_submit = ('id', 'SubmitNsfOrderPaymentBtn', 'NSF Submit button')
    btn_add_additional_fee = ("xpath", "//a[@class='add-control-btn']", "Add additional fee button")
    btn_remove_addityional_fee = ("xpath", "//a[contains(@class, 'remove-control-btn show-additional-btn')]",
                                  "Remove additional fee btn")

    # ---------------------------------------------
    # inputs
    # ---------------------------------------------
    btn_onetimeexport_submit = ("xpath", "//div[@id='kofileBubbleFooter']//a[contains(@id, 'submit')]",
                                "Submit popup One Time Export")
    inp_document_type = ('id', 'autoOrderType', 'Document type input')
    inp_nsf_order_num = ('id', 'nsf-order-number', 'NSF Order Number')
    inp_no_of = ('id', 'NoOf', 'Number Of')
    no_of_addittional_fees = ("xpath", "//div[@class='additional-fee-fields-block']//input[contains(@data-val-title, 'NumberOf')]",
                              "Number of field of additional fees")
    inp_amount = ('id', 'Payment', 'Amount input')
    inp_consideration_amount = ("xpath", "//input[@placeholder='Consideration']", "Consideration field")

    # ---------------------------------------------
    # text fields
    # ---------------------------------------------
    _txt_document_type = ('xpath', '//span[@class="autoresultsDocType autocomplete-block"]/a[text()=%s]',
                          'Document type list item by item name')
    txt_nsf_amount = ('xpath', '//*[@id="NsfOrderPaymentsBubble"]//div/table//tr/td[@data-bind="text: $data.Amount"]',
                      'NSF Amount')
    txt_no_of_pages = ("id", "NoOfPage", "No of Pages")
    txt_no_of_names = ("id", "NoOfNames", "No of Names")
    txt_no_of_certifications = ("id", "NoOfCertifications", "No of Certifications")
    txt_no_of_additional_fees = ("xpath", "//input[@name='AdditionalFees.NumberOf']", "No of additional fees")
    # ---------------------------------------------
    # Return By Mail
    # ---------------------------------------------

    cbx_return_by_mail = ('xpath', '//input[@id="chkReturnByMail-"]', '"Return By Mail" checkbox')

    return_by_mail_block = ('xpath', '//div[@id="retAddBlock"]', '"Return By Mail" block')
    _tab_ = '//div[@class="tabcontent" and @style="display: block;"]'  # current active tab
    # buttons - - - - -
    btn_copy_from_order_header = (
        'xpath', f'{_tab_}//a[@id="copyFromHeaderAddress"]', '"Copy from order header" button')
    btn_copy_from_prior_order_item = ('xpath', f'{_tab_}//a[@id="copyFromPriorOrderAddress"]',
                                      '"Copy from prior order" button')
    btn_copy_mailing_address = ('xpath', f'{_tab_}//a[@id="copyMailingAddress"]', '"Copy Mailing Address" button')
    btn_copy_to_return_by_mail = ('xpath', f'{_tab_}//a[@id="copyToReturnByMail"]', '"Copy To Return by Mail" button')

    # fields - - - - -
    inp_return_by_mail__name = ('xpath', f'{_tab_}//input[contains(@name, "AddressName")]',
                                '"Return By Mail" customer name')
    inp_return_by_mail__owners_name = ('xpath', f'{_tab_}//input[contains(@name, ".Name")]',
                                       '"Owners" name')
    inp_return_by_mail__addr1 = ('xpath', f'{_tab_}//input[contains(@name, "AddressLine1")]',
                                 '"Return By Mail" customer address1')
    inp_return_by_mail__addr2 = ('xpath', f'{_tab_}//input[contains(@name, "AddressLine2")]',
                                 '"Return By Mail" customer address2')
    inp_return_by_mail__zip = ('xpath', f'{_tab_}//input[contains(@name, "ZipCode")]',
                               '"Return By Mail" customer ZipCode')
    inp_return_by_mail__city = ('xpath', f'{_tab_}//input[contains(@name, "City")]',
                                '"Return By Mail" customer City')
    inp_return_by_mail__state = ('xpath', f'{_tab_}//input[contains(@name, "StateName")]',
                                 '"Return By Mail" customer State name')
    inp_return_by_mail__state_code = ('xpath', f'{_tab_}//select[contains(@name, "StateCode")]',
                                      '"Applicant" customer State code')
    inp_business__name = ('xpath', f'{_tab_}//input[contains(@name, "UnIncorporatedBusinessName")]', '"Business" name')
    inp_business__state_name = ('xpath', f'{_tab_}//option[@value="%s"]', 'Business State name')

    inp_applicant__first_name = ('xpath', f'{_tab_}//input[contains(@name, "FirstName")]', '"Applicant" First Name')
    inp_applicant__last_name = ('xpath', f'{_tab_}//input[contains(@name, "LastName")]', '"Applicant" Last Name')

    inp_anticipated_date = ('xpath', '//input[@placeholder="Anticipated Date"]', 'Anticipated Date')
    inp_effective_date = ('xpath', '//input[@placeholder="Effective Date"]', 'Effective Date')
    inp_expiration_date = ('xpath', '//input[@placeholder="Expiration Date"]', 'Expiration Date')
    msg_expiration_date = ('xpath', '//p[@class = "error MlDatesModelErrorText"]', 'Expiration Date validation message')
    # ---------------------------------------------
    cbx_same_as_customer = ('xpath', '//label[@for="Same_as_customer"]/preceding-sibling::input',
                            '"Same as customer" checkbox')

    # Properties
    property_blocks = (
        'xpath', '//div[@class="property-control-block"]//div[contains(@class,"prop-")]', 'Property blocks')
    btn_add_new_desc = ('xpath', '//a[contains(text(),"New Desc")]', 'Properties "New Desc"')
    btn_add_new_subdivision = ('xpath', '//a[contains(text(),"New Subdivision")]', 'Properties "New Subdivision"')
    btn_add_new_survey = ('xpath', '//a[contains(text(),"New Survey")]', 'Properties "New Survey"')
    btn_add_new_address = ('xpath', '//a[contains(text(),"New Property Address")]', 'Properties "New Property Address"')

    btn_copy_property = ('xpath', '//a[@id="copyProperties"]', '"Copy Property" link')
    btn_copy_property__new_subdivision_ok = ('xpath', '//div[@id="new-subdivision-popup"]//input[@id="infobox_Yes"]',
                                             'Copy Property "New Subdivision pop-up" OK button')
    inp_copy_property__year = ('xpath', '//input[@id="recordedYear"]', 'Copy Property "Recorded Year" field')
    inp_copy_property__doc_num = ('xpath', '//input[@id="documentNumber"]', 'Copy Property "Doc number" field')
    btn_copy_property__copy = ('xpath', '//a[@id="copyPropertiesBtn"]', 'Copy Property "Copy" button')
    btn_copy_property__copy_from_prior_item = ('xpath', '//a[@id="copyfromPriorOrderItem"]',
                                               'Copy Property "Copy From Prior Order Item" button')

    # Parties
    btn_add_grantor = ('xpath', '//a[@data-desc="GRANTOR"]', 'Add GRANTOR button')
    btn_add_grantee = ('xpath', '//a[@data-desc="GRANTEE"]', 'Add GRANTEE button')
    btn_copy_names = ('xpath', '//a[contains(@id,"copyNames")]', 'Parties "Copy Names" button')
    btn_reverse_parties = ('xpath', f'//a[@id="reverseParties"]', '"Reverse Parties" button')
    btn_copy_names__copy = ('xpath', '//a[@id="copyNamesBtn"]', 'Parties "Copy Names" Copy button')
    btn_copy_names__copy_from_prior_item = (
        'xpath', '//a[@id="copyFromPriorOrder"]', 'Parties "Copy from prior item" link')
    inp_copy_names__recorded_year = ('xpath', '//input[@id="recordedYear"]', 'Parties "Copy Names Recorded Year" field')
    inp_copy_names__doc_number = ('xpath', '//input[@id="documentNumber"]', 'Parties "Copy Names doc number" field')
    copy_names_popup = ("id", "copyNamesBubble", "copy names popup")
    # ---------------------------------------------
    # Fee block

    _txt_fee_label_less = ('xpath', '//div[@id="lessFeebox"]/ul[%s]/li[@class="fee-label "]',
                           'Fee label in less box (first 3 rows) by index')
    _txt_fee_amount_less = ('xpath', '//div[@id="lessFeebox"]/ul[%s]/li[@class="fee-amount "]',
                            'Fee amount in less box (first 3 rows) by index')
    _txt_fee_label_more = ('xpath', '//div[@id="moreFeebox"]/ul[%s]/li[@class="fee-label "]',
                           'Fee label in more box (first 3 rows) by index')
    _txt_fee_amount_more = ('xpath', '//div[@id="moreFeebox"]/ul[%s]/li[@class="fee-amount "]',
                            'Fee amount in more box (first 3 rows) by index')
    # use find_all() method for these locators
    lbl_all_fee_labels = ("xpath", "//div[@id='moreFeebox' or @id='lessFeebox']//li[@class='fee-label ']",
                          "All fee labels")
    lbl_all_fee_amounts = ("xpath", "//div[@id='moreFeebox' or @id='lessFeebox']//li[@class='fee-amount ']",
                           "All fee amounts")
    lbl_all_outstand_labels = ("xpath", "//div[contains(@class,'feegrid-refund-block')]//li[@class='fee-label']",
                               "All outstanding fee labels")
    lbl_all_outstand_amounts = ("xpath", "//div[contains(@class,'feegrid-refund-block')]//li[@class='fee-amount']",
                                "All outstanding fee amounts")
    txt_total_amount = ('id', 'totalAmount', 'Total amount in fee block')
    lnk_more = ('xpath', '//div[@class="orangeText"]/a[@class="moreFee"]', 'More link in Fee block')
    lnk_less = ('xpath', '//div[@class="orangeText"]/a[@class="lessFee"]',
                'Less link in Fee block')
    lbl_oit_description = ("xpath", "//span[@class='orderItemTypeListDesc']", "Order Item description")
    fee_amount_by_fee_label_ = (
        "xpath",
        "//li[contains(text(), '%s')]/following-sibling::li[@class='fee-amount ' or @class='fee-amount']",
        "Fee amount")
    # ---------------------------------------------
    # admin popup
    # ---------------------------------------------
    pup_orderadmin_bubble = ("id", "orderAdminBubble", "Order Admin Bubble")
    pup_orderadmin_bubble_close = ("id", "widget-kofileinfobubble-closeui-id1", "Close Admin Bubble popup")
    pup_orderadmin_bubble_OK = ("id", "widget-kofileinfobubble-okui-id1", "Ok button on Admin Bubble popup")
    pup_orderadmin_bubble_sendtoadmin = (
        "xpath", "//*[@id='kofileBubbleFooter']/a[@id='inSufficientFundssaveAdminBtn']",
        "Send to admin link on Admin Bubble popup")
    pup_action_reason = ("id", "actionReasonsBubble", "Action reason popup")
    pup_action_reason_field = ("id", "actionReason", "Action Reason field")
    pup_action_reason_description_field = ("id", "actionDescription", "Action description field")
    pup_action_reason_cancel = ("id", "widget-kofileinfobubble-cancelui-id1", "Cancel button on action reason popup")
    pup_action_reason_submit = ("id", "actionReasonsBtn", "Submit button on action reason popup")

    add_note_btn = ("xpath", '//*[@class="addNoteRow"]', "Add note button")
    note_description = ("xpath", '//*[@placeholder="Description"]', "Note Description")
    save_note = ("xpath", '//*[@class="SaveNoteRow"]', "Save note")
    edit_note = ("xpath", '//*[@class="EditNoteRow"]', "Edit note")
    attach_file_upload_input = ("xpath", '//*[@id="attachments-upload-input"]', "Attachments Upload Input")
    attach_file_upload_btn = ("xpath", '//*[@class="attachment-upload-block"]', "Attachments Upload button")
    lbl_fund_desc = (
        "xpath",
        "//div[@class='feeDistTitle']//following::td[contains(@data-bind,'FeeFundDesc')]",
        "Fee Fund name in Fee Distribution popup")

    lbl_fund_desc_with_additional_fees = (
        "xpath",
        "//div[@class='feeDistTitle']//following::span[contains(text(),'Additional')]//\
         preceding::td[contains(@data-bind,'FeeFundDesc')]",
        "Fee Fund name in Fee Distribution popup when additional fees exists"
    )
    lbl_additional_fees_names = (
        "xpath",
        "//div[@class='feeDistTitle']//following::span[contains(text(),'Additional')]"
        "//following::span[contains(@data-bind,'AdditionalFeeName')]",
        "Additional fee names on Fee Distribution popup"
    )
    lbl_additional_fees_values = (
        "xpath",
        "//span[contains(text(),'Additional')]//following::td[contains(@data-bind,'FeeFundDesc')]"
        "//following::td[contains(@data-bind,'Total')]",
        "Additional fee values on Fee Distribution popup"
    )
    lbl_fund_value = (
        "xpath",
        "//div[@class='feeDistTitle']//following::td[contains(@data-bind,'FeeFund.Value')]",
        "Fee Fund value in Fee Distribution popup")
    inp_fund_value = (
        "xpath",
        "//div[@class='feeDistTitle']//following::input[@class='feeValue']",
        "Fee Fund input value in Fee Distribution popup")
    lnk_fund_distribution = (
        "xpath",
        "//a[contains(@id,'Distribution') and (text()='View/Edit Order Item Funds')]",
        "Fund Distribution Link")
    btn_close_distribution_popup = (
        "id",
        "widget-kofileinfobubble-closeui-id1",
        "Close Button on Fee Distribution Popup")
    btn_submit_distribution_popup = (
        "id",
        "widget-kofileinfobubble-submitui-id1",
        "Submit Button on Fee Distribution Popup")
    total_fund_for_distribution = (
        "id",
        "totalFeeForDistributionOIT",
        "Total Fee For Distribution"
    )
    total_fee_fund = (
        "xpath",
        "//div[@class='feeDistTitle']//following::th[@class='calculatedFeeTotal']",
        " Total Fee Fund on FeeFund Popup"
    )
    total_fund_with_additional_fee = (
        "xpath",
        "//div[@class='feeDistTitle']//following::span[contains(text(),'Additional')]"
        "//preceding::th[@class='calculatedFeeTotal']",
        "Total Fee Fund on FeeFund Popup with additional fees"
    )

    required_fields_locator = (
        "xpath",
        "//*[@class='tabcontent' and @style='display: block;']//*[contains(@class,'koValidationError')]",
        "Get all required fields")

    warning_popup = (
        'id',
        'dialog-content-holder',
        'Warning popup')

    yes_button = (
        'id',
        'infobox_Yes',
        'Yes Button')

    required_checkboxes_locator = (
        "xpath",
        "//span[contains(translate(@class,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'validationerror')"
        " and not(@style='display: none;')]/../following-sibling::div/input[@type='checkbox']",
        "Required checkbox")

    required_radiobuttons_locator = (
        "xpath",
        "//*[@class='tabcontent' and @style='display: block;']//input[(contains(@data-val-title, 'Required') or "
        "contains(@data-val-title, 'required')) and @type='radio']",
        "Required radiobutton")

    recorded_date_field = ("xpath", "//span[contains(@class, 'recorded-date')]", "Recorded date")

    applicant_county = (
        "name", 'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].PartyAddress.County', "County")
    applicant_country = (
        "name", 'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].PartyAddress.Country', "Country")
    applicant_ssn = ("name", 'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].MarriageExtras.SSN', "SSN")
    applicant_gender = (
        "name", 'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].Extras.GenderNullable', "Gender")
    applicant_email = (
        "name", 'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].Extras.Contacts[0].Value', "Email")
    applicant_birth_date = (
        "name", 'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].Extras.Birth.BirthDate', "Date of birth")
    prev_marriage = ("name",
                     'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].'
                     'MarriageExtras.PreviousMarriage.NoPreviousMarriages',
                     "Prev marriage count")
    end_date = (
        "name", 'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].MarriageExtras.PreviousMarriage.EndDate',
        "End date")
    reason = (
        "name",
        'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].MarriageExtras.PreviousMarriage.DivorseReason',
        "Reason")
    end_state = (
        "name", 'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].MarriageExtras.PreviousMarriage.EndState',
        "End state")
    end_county = (
        "name", 'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].MarriageExtras.PreviousMarriage.EndCounty',
        "End county")
    end_country = (
        "name", 'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].MarriageExtras.PreviousMarriage.EndCountry',
        "End country")
    years_of_education = (
        "name", 'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].MarriageExtras.EducationYears',
        "Years of education")
    years_of_college = (
        "name", 'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].MarriageExtras.CollegeYears',
        "Years of college")
    occupation = (
        "name", 'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].MarriageExtras.Occupation', "Occupation")
    race = ("name", 'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].MarriageExtras.Etnicity.Race', "Race")
    ancestry = (
        "name", 'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].MarriageExtras.Etnicity.Ancestry',
        "Ancestry")
    applicant_relationship_input = (
        "name", 'Order.OrderItems[0].Document.DocumentExtras.MLApplicantsRelationship', "Applicant relationship input")
    parent_name = (
        "name", 'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].MarriageExtras.Parents[%s].Name',
        "Parent name")
    parent_birth = (
        "name", 'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].MarriageExtras.Parents[%s].Surname',
        "Parent birth")
    parent_city = (
        "name", 'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].MarriageExtras.Parents[%s].City',
        "Parent city")
    parent_state = (
        "name", 'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].MarriageExtras.Parents[%s].StateCode',
        "Parent state")
    parent_county = (
        "name", 'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].MarriageExtras.Parents[%s].Country',
        "Parent county")
    parent_county_of_birth = (
        "name", 'Order.OrderItems[0].Document.DocumentExtras.Applicants[%s].MarriageExtras.Parents[%s].CountryOfBirth',
        "Parent county of birth")
    applicant_relationship_true_checkbox = (
        "xpath", '//input[@type="radio" and @value="True"]', "Applicant relationship true checkbox")
    applicant_relationship_false_checkbox = (
        "xpath", '//input[@type="radio" and @value="False"]', "Applicant relationship false checkbox")
    applicant_age = ("xpath",
                     '//div[@data-bind-id="BirthDateControl_Order_OrderItems[0]_Document_DocumentExtras_Applicants[%s]'
                     '_Extras_Birth_BirthDate"]/div/span[@class="birth-age"]',
                     "Age")
    ml_dob_error_text = ("xpath",
                         "//div[contains(@data-bind-id, 'Applicants[%s]')]//p[@class='error MlDatesModelErrorText']",
                         "error text under the applicants dob")

    anticipated_date_picker = ("css", "input#Order_OrderItems\\[0\\]_Document_MLDetails_AnticipatedDate",
                               "Anticipated date picker")

    expiration_date_picker = (
        "css", "input#Order_OrderItems\\[0\\]_Document_MLDetails_ExpirationDate", "Expiration date picker")

    confirmation_pop_up_text = ("css", "div#dialog-content-holder ul.contactArea>li:first-of-type",
                                "Confirmation pop-up text")

    @staticmethod
    def uploaded_file(expected_file_name):
        return "xpath", "//*[@title='" + expected_file_name + "']", 'Uploaded File'

    # PARTIES TAB - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @staticmethod
    def _parties_constructor(grantor=True, index=1, field="", control=""):
        grantor = "GRANTOR" if grantor else "GRANTEE"
        prefix = f'//label[text()="{grantor}"]/../following-sibling::div//div[{index}][@class="parties-textbox-block"]'
        suffix = f'span[@class="{control}"]' if control else f'input[contains(@name, "{field}")]'
        return 'xpath', f'{prefix}//{suffix}', f'"Parties" {grantor}[{index}] - {field if field else control}'

    def inp_parties__first_name(self, grantor=True, index=1):
        return self._parties_constructor(grantor=grantor, index=index, field="FirstName")

    def inp_parties__last_name(self, grantor=True, index=1):
        return self._parties_constructor(grantor=grantor, index=index, field="LastName")

    def inp_parties__middle_name(self, grantor=True, index=1):
        return self._parties_constructor(grantor=grantor, index=index, field="MiddleName")

    def inp_parties__suffix(self, grantor=True, index=1):
        return self._parties_constructor(grantor=grantor, index=index, field="Suffix")

    def btn_parties__up(self, grantor=True, index=2):
        return self._parties_constructor(grantor=grantor, index=index, control="parties-tools-up")

    def btn_parties__down(self, grantor=True, index=1):
        return self._parties_constructor(grantor=grantor, index=index, control="parties-tools-down")

    def btn_parties__delete(self, grantor=True, index=2):
        return self._parties_constructor(grantor=grantor, index=index, control="parties-tools-delete")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # PROPERTIES TAB - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @staticmethod
    def _properties_constructor(index=1, field="", control="", prop_block=""):
        tag = 'select' if field == 'State' else 'textarea' if field in ['Lot', 'Subdivision', 'Survey'] else 'input'
        prop_block = "property-input-control" if (index > 1 or not prop_block) else f"prop-{prop_block} controlBlock" \
            if prop_block in ["newdesc", "subdivision", "survey", "propaddress"] else prop_block
        prefix = f'div[{index}][contains(@class,"{prop_block}")]'
        suffix = f'span[contains(@class,"{control}")]' if control else f'{tag}[contains(@name, "{field}")]'
        return 'xpath', f'//{prefix}//{suffix}', f'"Properties"[{index}] {field if field else control}'

    def inp_properties_desc__description(self, index=1):
        return self._properties_constructor(index=index, field="UnparsedProperty", prop_block="newdesc")

    def inp_properties_desc__water_permit(self, index=1):
        return self._properties_constructor(index=index, field="Permit", prop_block="newdesc")

    def inp_properties_subdivision__lot(self, index=1):
        return self._properties_constructor(index=index, field="Lot", prop_block="subdivision")

    def inp_properties_subdivision__block(self, index=1):
        return self._properties_constructor(index=index, field="Block", prop_block="subdivision")

    def inp_properties_subdivision__ncb(self, index=1):
        return self._properties_constructor(index=index, field="Block2", prop_block="subdivision")

    def inp_properties_subdivision__subdivision(self, index=1):
        return self._properties_constructor(index=index, field="Subdivision", prop_block="subdivision")

    def inp_properties_subdivision__volume(self, index=1):
        return self._properties_constructor(index=index, field="Volume", prop_block="subdivision")

    def inp_properties_subdivision__page(self, index=1):
        return self._properties_constructor(index=index, field="Page", prop_block="subdivision")

    def inp_properties_subdivision__county(self, index=1):
        return self._properties_constructor(index=index, field="Block3", prop_block="subdivision")

    def inp_properties_subdivision__ordinance(self, index=1):
        return self._properties_constructor(index=index, field="Unit", prop_block="subdivision")

    def inp_properties_survey__abstract(self, index=1):
        return self._properties_constructor(index=index, field="Abstract", prop_block="survey")

    def inp_properties_survey__survey(self, index=1):
        return self._properties_constructor(index=index, field="Survey", prop_block="prop-survey")

    def inp_properties_survey__acres(self, index=1):
        return self._properties_constructor(index=index, field="Acres", prop_block="survey")

    def inp_properties_address__address1(self, index=1):
        return self._properties_constructor(index=index, field="Address1", prop_block="propaddress")

    def inp_properties_address__address2(self, index=1):
        return self._properties_constructor(index=index, field="Address2", prop_block="propaddress")

    def inp_properties_address__zip(self, index=1):
        return self._properties_constructor(index=index, field="ZipCode", prop_block="propaddress")

    def inp_properties_address__city(self, index=1):
        return self._properties_constructor(index=index, field="City", prop_block="propaddress")

    def inp_properties_address__state(self, index=1):
        return self._properties_constructor(index=index, field="State", prop_block="propaddress")

    def inp_properties_address__parcel(self, index=1):
        return self._properties_constructor(index=index, field="ParcelId", prop_block="propaddress")

    def btn_properties__up(self, index=1, prop_block=None):
        """prop_block should be one of: ["newdesc", "subdivision", "survey", "propaddress"]
            if  prop_block=None: return locator of 'index' element on the page"""
        return self._properties_constructor(index=index, control="properties-tools-up", prop_block=prop_block)

    def btn_properties__down(self, index=1, prop_block=None):
        """prop_block should be one of: ["newdesc", "subdivision", "survey", "propaddress"]
            if  prop_block=None: return locator of 'index' element on the page"""
        return self._properties_constructor(index=index, control="properties-tools-down", prop_block=prop_block)

    def btn_properties__delete(self, index=1, prop_block=None):
        """prop_block should be one of: ["newdesc", "subdivision", "survey", "propaddress"]
            if  prop_block=None: return locator of 'index' element on the page"""
        return self._properties_constructor(index=index, control="properties-tools-delete", prop_block=prop_block)
