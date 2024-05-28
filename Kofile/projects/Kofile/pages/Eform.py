"""
Eform Page Object Model
"""
from projects.Kofile.Lib.test_parent import PagesParent


class EForm(PagesParent):
    def __init__(self):
        super(EForm, self).__init__()

    lnk_eform_order_type = (
        "xpath",
        "//*[@id='kioskGrid']//div/a[(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz')='%s')]",
        "Order type link on eform page")

    btn_cancel_eform = (
        "id",
        "cancel-eform",
        "Cancel button"
    )
    btn_submit_eform = (
        "id",
        "submit-eform",
        "Submit button"
    )
    pup_submission = (
        "id",
        "dialog-content-holder",
        "Eform submission popup"
    )
    pup_submission_txt_email = (
        "id",
        "conf-mail",
        "Emain field on Eform submission popup"
    )
    pup_submission_btn_continue = (
        "id",
        "succes-continue",
        "Continue button on Eform submission popup"
    )
    pup_submission_txt_order = (
        "id",
        "OrderNumber",
        "Order Number on submission popup"
    )
    pup_information_dialog_close = (
        "xpath",
        "//*[@ID='dialog-content-holder']//following::a[@title='Close']",
        "Close Icon on Information popup"
    )

    rbt_death_certificate = (
        "id",
        "VitalCertificate_ApplicationType1",
        "Death Certificate Radiobutton"
    )

    txt_customer_name = (
        "xpath",
        "//*[@id='cartItemsBlock']//tr//input[@placeholder='Customer Name']",
        "Customer Name"
    )
    btn_checkout = (
        "xpath",
        "//*[@id='cartItemsBlock']//tr//input[@value='Check Out']",
        "Check Out"
    )
    btn_return_to_eform_menu = (
        "xpath",
        "//*[@id='cartItemsBlock']//tr//input[@value='Return To eForm Menu']",
        "Return To eForm Menu"
    )
    btn_remove_eform = (
        "xpath",
        "//*[@id='cartItemsBlock']//tr[%s]//a/img",
        "Remove eForm from Cart"
    )
    txt_total_eforms = (
        "xpath",
        "//*[@id='cartItemsBlock']//tbody/tr/td[@class='text-bold text-center']",
        "Total eforms in Cart"
    )

    # Passport Request eForm

    btn_next = (
        "xpath",
        "//*[@id='PassportApplicationPage1']//a[contains(text(),'NEXT')]",
        "NEXT button"
    )
    btn_yes = (
        "xpath",
        "//*[@id='PassportApplicationPage%s']//a[contains(text(),'Yes')]",
        "Yes button"
    )
    inp_last_name = (
        "id",
        "PassportRequest_Order_OrderItems_0__OrderItemApplicantLastName",
        "Last Name"
    )
    inp_first_name = (
        "id",
        "PassportRequest_Order_OrderItems_0__OrderItemApplicantFirstName",
        "First Name"
    )
    inp_number = (
        "id",
        "PassportRequest_Order_OrderItems_0__OrderItemApplicant.PartyId",
        "Number"
    )
    btn_submit = (
        "xpath",
        "//*[@id='PassportApplicationPage9']//a[contains(text(),'Submit')]",
        "Submit button"
    )

    eform_required_fields_locator = (
        "xpath",
        "//*[contains(@class,'koValidationError')]",
        "Get all required fields for eform")

    eform_required_checkboxes_locator = (
        "xpath",
        "//span[@class='customValidationError']//following::input[@type='checkbox']",
        "Get all required checkboxes")

    required_radiobuttons_locator = (
        "xpath",
        "//input[(@type='radio') and (@class='koValidationError')]",
        "Get all required radiobuttons in eform")

    applicant_email = (
        "id",
        "mlformal_Order_OrderItems_0__Document_Parties_%s__Extras_Contacts_0_Email",
        "applicant email"
    )

    applicant_phone = (
        "id",
        "mlformal_Order_OrderItems_0__Document_Parties_%s__Extras_Contacts_1_Phone",
        "applicant phone"
    )

    applicant_county = (
        "id",
        "mlformal_Order_OrderItems_0__Document_Parties_%s__PartyAddress.County",
        "applicant county"
    )
    applicant_country = (
        "id",
        "mlformal_Order_OrderItems_0__Document_Parties_%s__PartyAddress.Country",
        "applicant country"
    )

    applicant_gender = (
        "id",
        "mlformal_Order_OrderItems[0]_Document_Parties[%s]_Extras_GenderNullable",
        "gender select"
    )
    applicant_age_field = (
        "name",
        "Order.OrderItems[0].Document.Parties[%s].Extras.Birth.BirthDate",
        "age field"
    )
    applicant_age_number = (
        "xpath",
        '//div[@data-bind-id="BirthDateControl_Order_OrderItems[0]_Document'
        '_Parties[%s]_Extras_Birth_BirthDate"]/div/span[@class="birth-age"]',
        "age number"
    )

    anticipated_date_of_ceremony = (
        "name",
        'Order.OrderItems[0].Document.MLDetails.AnticipatedDate',
        "Anticipated Date"
    )

    city_of_marriage = (
        "name",
        'Order.OrderItems[0].Document.CityOfMarriage',
        "City Of Marriage"
    )
    applicant_first_name = (
        "id",
        'mlformal_Order_OrderItems_0__Document_Parties_%s_.FirstName',
        "applicant first name"
    )
    applicant_last_name = (
        "id",
        'mlformal_Order_OrderItems_0__Document_Parties_%s_.LastName',
        "applicant last name"
    )

    ssn = (
        "name",
        'Order.OrderItems[0].Document.Parties[%s].MarriageExtras.SSN',
        "ssn"
    )
    previous_marriages = (
        "name",
        'Order.OrderItems[0].Document.Parties[%s].MarriageExtras.PreviousMarriage.NoPreviousMarriages',
        "No of Previous Marriages"
    )

    previous_marriages_reason = (
        "name",
        'Order.OrderItems[0].Document.Parties[%s].MarriageExtras.PreviousMarriage.DivorseReason',
        "Previous Marriages reason"
    )

    previous_marriages_date = (
        "name",
        'Order.OrderItems[0].Document.Parties[%s].MarriageExtras.PreviousMarriage.EndDate',
        "Previous Marriages date"
    )
    previous_marriages_state = (
        "name",
        'Order.OrderItems[0].Document.Parties[%s].MarriageExtras.PreviousMarriage.EndState',
        "Previous Marriages state"
    )
    previous_marriages_country = (
        "name",
        'Order.OrderItems[0].Document.Parties[%s].MarriageExtras.PreviousMarriage.EndCountry',
        "Previous Marriages country"
    )
    previous_marriages_county = (
        "name",
        'Order.OrderItems[0].Document.Parties[%s].MarriageExtras.PreviousMarriage.EndCounty',
        "Previous Marriages county"
    )
    data_list = (
        "id",
        'selectReasonBox',
        "Data list"
    )
    reason_input = (
        "xpath",
        '//input[@list="selectReasonBox"]',
        "Reason input"
    )
    prev_marriage_reason_box = (
        "xpath",
        '//div[@data-bind-id="PreviousMarriageControl_Order_OrderItems[0]_Document_Parties[%s]'
        '_MarriageExtras_PreviousMarriage"]/div[@id="selectReason"]',
        "Previous Marriage reason box"
    )
    education_years = (
        "name",
        'Order.OrderItems[0].Document.Parties[%s].MarriageExtras.EducationYears',
        "Education Years"
    )

    college_years = (
        "name",
        'Order.OrderItems[0].Document.Parties[%s].MarriageExtras.CollegeYears',
        "College Years"
    )

    occupation = (
        "name",
        'Order.OrderItems[0].Document.Parties[%s].MarriageExtras.Occupation',
        "Select Occupation"
    )

    occupation_box = (
        "xpath",
        '//div[@data-bind-id="AdvancedComboBoxModelControl_Order_OrderItems[0]_'
        'Document_Parties[%s]_MarriageExtras_Occupation"]',
        "occupation box"
    )

    occupation_input = (
        "xpath",
        '//input[@list="advancedComboBoxList"]',
        "occupation input"
    )

    occupation_data_list = (
        "id",
        'advancedComboBoxList',
        "occupation Data list"
    )

    race_select = (
        "name",
        "Order.OrderItems[0].Document.Parties[%s].MarriageExtras.Etnicity.Race",
        "Race select"
    )

    ancestry_select = (
        "name",
        "Order.OrderItems[0].Document.Parties[%s].MarriageExtras.Etnicity.Ancestry",
        "Ancestry select"
    )

    ancestry_select_data_list = (
        "id",
        "Ancestry_%s",
        "Ancestry select data list"
    )

    parent_name = (
        "name",
        "Order.OrderItems[0].Document.Parties[%s].MarriageExtras.Parents[%s].Name",
        "Parent name"
    )
    parent_city = (
        "name",
        "Order.OrderItems[0].Document.Parties[%s].MarriageExtras.Parents[%s].City",
        "Parent city"
    )
    parent_state = (
        "name",
        "Order.OrderItems[0].Document.Parties[%s].MarriageExtras.Parents[%s].StateCode",
        "Parent state"
    )
    surname_at_birth = (
        "name",
        "Order.OrderItems[0].Document.Parties[%s].MarriageExtras.Parents[%s].Surname",
        "Surname at Birth"
    )
    parent_county = (
        "name",
        "Order.OrderItems[0].Document.Parties[%s].MarriageExtras.Parents[%s].Country",
        "parent county"
    )
    county_of_birth = (
        "name",
        "Order.OrderItems[0].Document.Parties[%s].MarriageExtras.Parents[%s].CountryOfBirth",
        "county of birth"
    )
    parent_state_code = (
        "name",
        "Order.OrderItems[0].Document.Parties[%s].MarriageExtras.Parents[%s].StateCode",
        "Parent state code"
    )
    applicant_relationship_true_radiobutton = (
        "id",
        "mlformal_Order.OrderItems[0].Document.DocumentExtras.AreApplicantsRelatedToEachOther0",
        "Applicant relationship true radiobutton"
    )
    applicant_relationship_input = (
        "id",
        "mlformal_Order_OrderItems_0__Document_DocumentExtras_MLApplicantsRelationship",
        "Applicant relationship input"
    )
    applicant_relationship_false_radiobutton = (
        "id",
        "mlformal_Order.OrderItems[0].Document.DocumentExtras.AreApplicantsRelatedToEachOther1",
        "Applicant relationship false radiobutton"
    )
    parent_deceased = (
        "xpath",
        "//div[@data-bind-id='ParentModelControl_Order_OrderItems[0]_Document_Parties[%s]"
        "_MarriageExtras_Parents[%s]']/div[@class='parent-checkbox-block']/input[@type='checkbox']",
        "Parent Deceased"
    )
