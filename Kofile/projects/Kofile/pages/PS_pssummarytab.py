"""
Represents properties and methods of Preview/Summary tab
"""
from selenium.webdriver.common.by import By

from projects.Kofile.Lib.test_parent import PagesParent


class PSSummaryTab(PagesParent):
    def __init__(self):
        super(PSSummaryTab, self).__init__()

    def __48999__(self):
        self.doc_num_id_oq = (By.XPATH, ".//*[@id='OrderQueue']/tbody/tr/td[@data-column='Document_DocAndAppNum']",
                              "Doc num ID in summary")
        self.doc_num_id_os = (By.XPATH, ".//*[@id='orderSummary']/tbody/tr/td[@data-column='Document_DocAndAppNum']",
                              "Doc num ID in summary")

    new_order_item = (By.XPATH, "//*[@id='newOrderItem']", "New Order Item link")
    doc_year_oq = (By.XPATH, f"//*[@id='OrderQueue']/tbody/tr[", "Document year in order summary screen.")
    doc_year_os = (By.XPATH, f"//*[@id='orderSummary']/tbody/tr[", "Document year in order summary screen.")
    doc_year_2 = "]/td[@data-column='Document_RecordedYear']"
    doc_num_id_oq = (By.XPATH, ".//*[@id='OrderQueue']/tbody/tr/td[@data-column='Document_InstrumentNumber']",
                     "Doc num ID in summary")
    doc_num_id_os = (By.XPATH, ".//*[@id='orderSummary']/tbody/tr/td[@data-column='Document_InstrumentNumber']",
                     "Doc num ID in summary")
    doc_type_os = (By.XPATH, ".//*/tbody/tr/td[6]", "Document type in order summary screen.")
    fee_desc = (By.XPATH, "//*[@id='NewOrderform']/div[2]/div[4]/span", "Fee Description")
    oit_status = (By.XPATH, ".//*[@id='OrderQueue']/tbody/tr/td[12]", "OIT status string")
    oit_type = (By.XPATH, "//*[@id='OrderQueue']/tbody/tr/td[5]/span[1]", "Order item type in CRS")
    number_of = (By.XPATH, ".//*[@id='OrderQueue']/tbody/tr/td[7]", "Number of pages")
    total_price = (By.XPATH, ".//*/tbody/tr/td[8]", "Order total price")
    amount_field = (By.XPATH, ".//*[@id='paymentMethods']/div[1]/ul/li[4]/input", "Amount")
    balance_field = (By.ID, 'balanceDue', "Balance")
    checkout_field = (By.ID, 'orderPaymentCheckout', "Checkout button")
    tr_id_field = (By.XPATH, "//*[@id='paymentMethods']/div[1]/ul/li[2]/input", "Transaction ID field")
    comment_field = (By.XPATH, ".//*[@id='paymentMethods']/div/ul/li[3]/input", "Enter comment")
    payment_methods_field = (By.XPATH, "//*[@id='paymentMethods']/div[1]/ul/li[1]/select", "Payment methods")
    oit_type_fin = (By.XPATH, "//td[@data-column='OrderItemType_Value']", "'Type' on OIT row")
    order_status = (By.XPATH, f".//*[@id='orderSummary']/tbody/tr", "Order status")
    total_amount = (By.ID, "orderTotalAmt", "Total amount")
    popup_yes_btn = (By.XPATH, "//*[@id='infobox_Yes']", "Popup *YES* button")
    edit_button = (By.XPATH, "//a[@class='orderSummaryiconedit']", "Order Summary edit button")
    save_order_btn = (By.XPATH, "//*[@id='addToOrder']", "Save Order button")
    serial_number_btn = (By.XPATH, "//a[contains(@class, 'serialNumberIcon')]", "Serial number icon")
    serial_number_popup = (By.XPATH, "//div[@id='setSerialNumberBubble']", "Serial number bubble")
    serial_number_start_field = (By.XPATH, "//input[@placeholder='Start Serial Number']", "Serial number field")
    serial_number_end_field = (By.XPATH, "//input[@placeholder='End Serial Number']", "Serial Number end field")
    small_loader = (By.XPATH, "//input[contains(@class, 'iconLoaderSmall')]", "Small loader")
    serial_number_submit_btn = (By.ID, "setSerialNumberBtn", "SerialNumber Submit button")
    checkout_button = (By.ID, "orderSummaryCheckout", "Checkout button")

    doc_type = (By.XPATH, "//div[@class='header']", "Doc type in Summary tab")
    doc_summary_table = (By.XPATH, "//*[@id='documentSummaryArea']/table/tbody/tr[2]/td", "")   # td[1] or td[2]
    doc_sum_inner_table_row = "/table/tbody/tr"                                 # tr[1] ... + column /td[1] or /td[2]
    doc_parties_header = (By.XPATH, "//*[@id='documentSummaryArea']/table/tbody/tr[3]/td/div[1]", "")
    doc_parties_row = (By.XPATH, "//*[@id='documentSummaryArea']/table/tbody/tr[3]/td/div[2]/table/tbody/tr", "")   # tr[1] ...
    doc_sum_last_section = (By.XPATH, "//*[@id='documentSummaryArea']/table/tbody/tr[last()]", "")
    doc_table_row = (By.XPATH, "//*[@id='documentSummaryArea']/table/tbody/tr", "")     # tr[1] ...
    all_summary = (By.XPATH, "//tr[@class='tdspacequal']//tr", "All Summary table fields")
    in_workflow = (By.XPATH, "//span[@data-value='In Workflow']", "in workflow status")
    order_type_list = (By.ID, "orderTypeList", "Order Type List")

    grantor = ("xpath", "//td[@data-value='GRANTOR']/parent::tr/td/a", "Grantor in summary")
    grantee = ("xpath", "//td[@data-value='GRANTEE']/parent::tr/td/a", "Grantee in summary")
    legal_description_link = ("id", "LegalDescription", "Legal description link")
    marginal_ref_link = ("xpath", "//a[@class='marginalRefLink']", "Marginal Ref Link")
    ref_doc_type = ("xpath", "//td[@data-column='Summary.REF_DOC_TYPE']", "Ref doc type")
    ref_record = ("xpath", "//td[@data-column='Summary.REF_RECORDED']", "Ref record")
    doc_remarks = ("id", "Document Remarks", "Document Remarks")
    return_address = ("xpath", "//div[@data-value='Return Address']/parent::td/table", "Return Address")
