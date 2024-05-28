"""
Kiosk Search Page Object Model
"""
from selenium.webdriver.common.by import By
# --------------------------------
# HEADER SECTION
# --------------------------------
from projects.Kofile.Lib.test_parent import PagesParent


class KSHomepage(PagesParent):
    def __init__(self):
        super(KSHomepage, self).__init__()

    lnk_sign_in = (By.XPATH, "//a[contains(text(), 'Sign In')]", "Sign In link")
    lnk_sign_out = (By.XPATH, "//a[@id='signOutLink']", "Sign Out link")
    txt_email_pup_sign_in = (By.XPATH, "//*[@id='loginusername']", "User Email")
    txt_password_pup_sign_in = (By.XPATH, "//*[@id='loginpassword']", "User Password")
    btn_sign_in_pup_sign_in = (By.XPATH, "//button[contains(text(), 'Sign In')]", "Sign In button")
    lnk_cart = (By.XPATH, "//a[@id='CartDetails']", "Cart icon")
    # --------------------------------
    # SEARCH SECTION
    # --------------------------------
    txt_search = (By.ID, "SearchText", "Search textfield")
    btn_search = (By.XPATH, "//input[@class='searchbutton']", "Search button")
    # --------------------------------
    # SEARCH RESULTS SECTION
    # --------------------------------
    all_rows_with_add_to_cart = (By.XPATH, "//a[@title='Add to Cart' and @style='visibility: visible;']/../..",
                                 "All rows with cart icon")
    icn_k_drive_by_row_num_ = (By.XPATH, "//tr[@data-value='%s']/td/a[@title='Add to KDrive']", "Icon kDrive")
    icn_quick_doc_by_row_num_ = (By.XPATH, "//tr[@data-value='%s']/td/a[@title='QuickDoc']", "Icon QuickDoc")
    icn_add_to_cart_by_row_num_ = (By.XPATH, "//tr[@data-value='%s']/td/a[@title='Add to Cart']", "Icon Add to Cart")
    # --------------------------------
    # QUICK DOC POPUP
    # --------------------------------
    pup_order_confirmation = (By.XPATH, "//div[@id='dialog-content-holder']", "Order Confirmation popup")
    lbl_total_due = (By.XPATH, "//span[@id = 'spnTotalDue']", "Total Due")
    lbl_available_balance = (By.XPATH, "//label[@for='rbtnCompAcctUserChoice_CompAcct']", "CA Available Balance")
    rbn_company_account = (By.XPATH, "//input[@id='rbtnCompAcctUserChoice_CompAcct']", "Company Account option")
    rbn_credit_card = (By.XPATH, "//input[@id='rbtnCompAcctUserChoice_CreditCard']", "Credit Card option")
    rbn_pay_at_counter = (By.XPATH, "//input[@id='rbtnCompAcctUserChoice_Pickup']", "Pay at Counter option")
    btn_submit_pup = (By.XPATH, "//input[@id='btnQuickDocSubmit']", "Button Submit")
    btn_submit_pay_at_counter = (By.XPATH, "//input[@id='btnSubmit']", "Button Submit Pay at Counter")
    btn_close_pup = (By.XPATH, "//a[@title='Close']", "Button Close popup")
    lbl_total_price = (By.XPATH, "//ul[@id='itnet-ec-ordcon-receipt-total-amt']/li", "Order Price for CA payment")
    btn_new_search = (By.XPATH, "//input[@id='newSearch']", "Button New Search")
    lbl_order_number = (By.XPATH, "//span[@id='spnOrderNumber']", "Pay at Counter Order Number")
    # --------------------------------
    # CART
    # --------------------------------
    lbl_cart = (By.XPATH, "//div[@id='cartHearderBlock-left']", "Cart label")
    delivery_method_by_text_ = (
    By.XPATH, "//select[@id='delieveryMethod']/option[contains(text(), %s)]", "Delivery Method")
    btn_checkout = (By.ID, "companyUserCheckOut", "Cart Checkout")
    pup_cart_payments = (By.ID, "divOrderPreConfirmationKioskCompAcctSubmit", "Cart payments popup")
    btn_purchase_pup = (By.XPATH, "//a[contains(text(), 'Purchase')]", "Button Purchase in Cart payments")
    lnk_clear_cart = (By.ID, "clearShoppingCartLink", "Clear Cart link")
    lbl_no_items_in_cart = (By.ID, "noItemsText", "No items in cart message")
    icn_home = (By.XPATH, "//li[@class='homeIcon']", "Back to Homepage")
