"""Sign in/Sign out to pspp"""
from selenium.webdriver.common.by import By

from projects.Kofile.Lib.test_parent import PagesParent


class PSPrint(PagesParent):
    def __init__(self):
        super(PSPrint, self).__init__()

    si_lnk = (By.XPATH, "//*[@id='divLoginButton']/li[3]/a", "Si link")
    login_button = (By.XPATH, "//a[@class='button-login']", "login button")
    marriage_license_tab = (By.XPATH, "//a[@id='Department_6']", "marriage license tab")
    marriage_date_range = (By.XPATH, "//div[@id='InstrumentDate']", "marriage date range")
    logout_button = (By.XPATH, "//a[@id='signOutLink']", "login button")
    si_popup_header = (By.XPATH, "//*[@id='dialog-content-holder']/div[1]/div[1]", "Si popup header")
    si_email = (By.XPATH, "//*[@id='loginusername']", "Si email")
    si_pass = (By.XPATH, "//*[@id='loginpassword']", "Si pass")
    si_cancel_btn = (By.XPATH, "//*[@id='user-signin-cancel']", "Si cancel button")
    si_signin_btn = (By.XPATH, "//*[@id='userSignIn']/ul/li[5]/ol/li[1]/button", "Si signin button")
    so_popup_header = (By.XPATH, "//*[@id='dialog-content-holder']/div[1]/div", "So popup header")
    so_cancel_btn = (By.XPATH, "//*[@id='logoutCancel']", "So cancel button")
    so_yes_btn = (By.XPATH, "//*[@id='logoutOk']", "So Yes button")
