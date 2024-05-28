"""Order Header Page Object Model"""

# ---------------------------------------------
# text fields
# ---------------------------------------------
from projects.Kofile.Lib.test_parent import PagesParent


class CRSOrderHeader(PagesParent):
    def __init__(self):
        super(CRSOrderHeader, self).__init__()

    txt_accountname = (
        'id',
        'accountName',
        'Order Header accountname')

    txt_organization_name = (
        'id',
        'organizationFullName',
        'Order Header organization Name')

    organization_balance_field = (
        'id',
        'OrganizationBalance',
        'Organization Balance Field')

    company_account_balance_field = (
        'id',
        'CompanyAccountBalance',
        'Company Account Balance Field')

    company_account_balance_value = (
        'id',
        'accountBalance',
        'Company Account Balance Value')

    ddl_accountname_lookup_by_account_name = (
        'xpath',
        "//*[@id='accounts']/a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '%s')]",
        'Order Header accountname lookup')

    txt_email = (
        'id',
        'AccountEmail',
        'Order Header email')

    ddl_email_lookup_by_email = (
        'xpath',
        "//*[@id='emails']/a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '%s')]",
        'Order Header Email Lookup')

    txt_customername = (
        'id',
        'CustomerName',
        'Order Header customerName')

    ddl_customername_lookup_by_name = (
        'xpath',
        "//*[@id='name-block']//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '%s')]",
        'Order Header Customer Name lookup')

    lbl_address_is_required = (
        "xpath",
        "//div[@id='orderentrypanel']//span[text()='Address is required!']",
        "Address is required error message"
    )

    txt_header_validation_msg = (
        "xpath",
        "//span[contains(@class,'orderHeadervalidationError')]",
        "Header validation message"
    )

    txt_order_number = (
        "xpath",
        "//span[@id='orderNumber']",
        "Order number"
    )

    lbl_recorded_date = (
        "id",
        "recording-date",
        "Recorded date"
    )

    # ---------------------------------------------
    # checkboxes/radiobuttons
    # ---------------------------------------------

    cbx_received_by_email = (
        'xpath',
        '//*[@id="receivedByMail"]',
        'Order Header Recieved By Mail checkbox')

    rbn_auto_print_receipt_yes = (
        'xpath',
        '//*[@id="printReceipt-y"]',
        'AutoPrint Receipt Yes radiobutton')

    rbn_auto_print_receipt_no = (
        'xpath',
        '//*[@id="printReceipt-n"]',
        'AutoPrint Receipt No radiobutton')

    rbn_auto_print_receipt_email = (
        'xpath',
        '//*[@id="emailReceipt"]',
        'AutoPrint Receipt Email radiobutton')

    # ---------------------------------------------
    # TrackingId
    # ---------------------------------------------
    lnk_add_trackingid = (
        'xpath',
        ".//*[@id='addTrackingId']",
        'Add TrackinId')

    pup_txt_trackingid = (
        'xpath',
        ".//*[@name = 'trackingId']",
        'TrackingId input field')

    pup_btn_trackingid_submit = (
        'xpath',
        ".//*[@id='copyOrderItemBtn']",
        'TrackingId Submit button')

    pup_btn_trackingid_cancel = (
        'xpath',
        ".//*[@id='removeTrackingId']",
        'TrackingId Cancel button')

    pup_lbl_trackingID_validation_msg = (
        'xpath',
        ".//*[@id='trakingIdMessage']",
        'TrackingId validation message')

    # ---------------------------------------------
    # More Options
    # ---------------------------------------------
    lnk_more_option = (
        'xpath',
        '//a[contains(@class, "add-control-icon moreOptions")]',
        'More Options link')

    txt_more_option_email = (
        'xpath',
        '//*[@id="CustomerEmail"]',
        'Email field in More Option section')

    txt_more_option_name = (
        'xpath',
        '//*[@id="CustomerFirstName"]',
        'Name field in More Option section')

    txt_more_option_address = (
        'xpath',
        '//*[@id="AddressLine1"]',
        'Address field in More Option section')

    txt_more_option_city = (
        'xpath',
        '//*[@id="City"]',
        'City field in More Option section')

    txt_more_option_state = (
        'xpath',
        '//*[@id="state-block"]/div/select',
        'State field in More Option section')

    txt_more_option_zip = (
        'xpath',
        '//*[@id="ZipCode"]',
        'Zip field in More Option section')

    txt_more_option_phone_number = (
        "id",
        "CustomerPhoneNumber",
        "Customer Phone Number in More Options section"
    )

    txt_more_option_confirmation_success_msg = (
        'xpath',
        '//*[@id="orderentrypanel"]//span[@class ="orderHeadervalidationError text-green"]',
        'Order Header More Option Confirmation Success message'
    )

    txt_more_option_confirmation_fail_msg = (
        'xpath',
        '//*[@id="orderentrypanel"]//span[@class ="orderHeadervalidationError text-red"]',
        'Order Header More Option Confirmation fail message'
    )

    lnk_more_option_new_registration = (
        "xpath",
        "//div[@id='orderHeaderCustomerInfo']/div[contains(@class, 'registration-text')]/a",
        "More Options New Registration action link"
    )
    lbl_refund_to = (
        "xpath",
        '//*[@id="account-section-refund"]/h5',
        "Refun To Section"
    )
