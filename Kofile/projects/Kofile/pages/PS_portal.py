"""Kiosk navigation buttons to search and eforms"""
from projects.Kofile.Lib.test_parent import PagesParent


class PSPortal(PagesParent):
    def __init__(self):
        super(PSPortal, self).__init__()

    __kiosk_home_navs = "//div[@id='kioskGrid']//a[contains(@class, 'kiosk-home-nav kiosk-caption')]"
    __kiosk_home_nav = "//div[@id='kioskGrid']//a[contains(@class, 'kiosk-home-nav kiosk-caption') and ./text()='%s']"

    """Kiosk menu: Cart count indicator, go to Cart icon and error message"""
    __cart_counter = "//*[@id='cart-items-count']"
    __go_to_cart = "//*[@id='cartLink']"
    __error_message = "//*[@id='cartLimitExceedMessage']/p"

    """Kiosk Cart"""
    __cart_customer_name = "//*[@id='cartItemsBlock']//input[@placeholder='Customer Name']"
    __cart_table_rows = "//*[@id='cartItemsBlock']/div[2]/table/tbody/tr"
    __cart_table_row = __cart_table_rows + "[%s]/td[%s]"
    __delete_the_row = __cart_table_rows + "[%s]/td[4]/a"
    __form_button = "//*[@id='cartItemsBlock']//input[@type='button' and @value='%s']"

    """Submit and Cancel buttons for all forms"""
    __form_submit_button = "//*[@id='submit-eform']"
    __form_cancel_button = "//*[@id='cancel-eform']"
