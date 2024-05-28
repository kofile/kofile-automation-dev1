"""Cart page object"""
from selenium.webdriver.common.by import By

from projects.Kofile.Lib.test_parent import PagesParent


class PSPpCart(PagesParent):
    def __init__(self):
        super(PSPpCart, self).__init__()

    cart_item_count = (By.XPATH, "//*[@id='CartItemCount']", "Cart item count")
    clear_cart = (By.XPATH, "//*[@id='clearShoppingCartLink']", "Clear cart")
    file_format = (By.XPATH, "//*[@id='FileFormatList']", "File format")
    cart_row1 = (By.XPATH, "//*[@id='shoppingCart']/tbody/tr[", "Cart row 1")           # row number goes here
    cart_row2 = "]/td//*[@id='cartItemGenericDetails']/tbody/tr/td["                    # column number goes here
    cart_row2_email = "]/td//*[@id='cartItemUserDetails']//*[@id='txtDeliveryEmailId']"
    cart_row2_phone = "]/td//*[@id='cartItemUserDetails']//*[@id='txtDeliveryTelephone']"
    cart_row2_name = "]/td//*[@id='cartItemUserDetails']//*[@id='txtDeliveryName']"
    cart_row2_addr = "]/td//*[@id='cartItemUserDetails']//*[@id='txtDeliveryAddress']"
    cart_row2_city = "]/td//*[@id='cartItemUserDetails']//*[@id='txtDeliveryCity']"
    cart_row2_zip = "]/td//*[@id='cartItemUserDetails']//*[@id='txtDeliveryZip']"
    cart_row2_state = "]/td//*[@id='cartItemUserDetails']//*[@id='cmbDeliveryState']"
    cart_row3 = "]"
    cart_row4 = "/select"                                                               # for delivery method only
    subtotal = (By.XPATH, "//*[@id='priceText']", "Subtotal")
    checkout_btn = (By.XPATH, "//*[@id='shoppinCartCheckoutBtn']", "Checkout button")
    go_home = (By.XPATH, "//*[@id='profileNav']/li[1]/a/img", "Go home")
    cart_rows = (By.XPATH, "//*[@id='shoppingCart']/tbody/tr/td", "Cart rows")
    co_text = (By.XPATH, "//*[@id='convenienceFeeDialog']/ul/li[1]", "CO text")
    co_cancel_btn = (By.XPATH, "//*[@id='infobox_Cancel']", "CO cancel button")
    co_continue_btn = (By.XPATH, "//*[@id='infobox_Continue']", "CO continue button")
    cart_breadcrumb = (By.XPATH, "//*[@id='profileNav']/li[3]/a", "Cart breadcrumb")
    kiosk_submit = (By.XPATH, "//*[@id='btnSubmit']", "Kiosk submit")
    kiosk_name_field = (By.XPATH, "//*[@id='txtUserName']", "Kiosk name field")
    kiosk_email_field = (By.XPATH, "//*[@id='txtUserEmail']", "Kiosk email field")
    kiosk_close = (By.XPATH, "//*[@id='btnClose']", "Kiosk close")
    kiosk_order_number = (By.XPATH, "//*[@id='spnOrderNumber']", "Kiosk order number")
