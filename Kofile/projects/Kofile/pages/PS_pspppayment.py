"""Payment Details and Success screens"""
from selenium.webdriver.common.by import By

from projects.Kofile.Lib.test_parent import PagesParent


class PSPayment(PagesParent):
    def __init__(self):
        super(PSPayment, self).__init__()

    amount = (By.XPATH, "//*[@id='payment-gateway-body-content']/table/tbody/tr[2]/td[2]/span", "Amount")
    name_on_CC = (By.XPATH, "//*[@id='ccname']", "Name on CC")
    ccnumber = (By.XPATH, "//*[@id='ccnum']", "CC number")
    exp_mon = (By.XPATH, "//*[@id='ExpiryMonth']", "Expire month")
    exp_year = (By.XPATH, "//*[@id='ExpiryYear']", "Expire year")
    cvv = (By.XPATH, "//*[@id='cvv']", "CVV")
    process_btn = (By.XPATH, "//*[@id='PaymentSubmit']", "Process button")
    cancel_btn = (By.XPATH, "//*[@id='PaymentCancel']", "Cancel button")
    s_order_num = (By.XPATH, "//*[@id='order-detail-block']/ul/li[1]/span[2]", "Order num")
    # receipt row goes here
    s_receipt1 = (By.XPATH, "//*[@id='itnet-ec-ordcon-receipt-block-content-body-block']/ul[", "Receipt")
    s_receipt2 = "]/li["  # receipt column goes here
    s_receipt3 = "]"
    s_recept_total = (By.XPATH, "//*[@id='itnet-ec-ordcon-receipt-total-amt']/li", "Receipt total")
    breadcrumb = (By.XPATH, "//*[@id='profileNav']/li[3]/a", "Breadcrumb")
    payment_status_block = (By.XPATH, "//div[@id='PaymentStatus']", "payment status block")
    wrapper_page_content = (By.XPATH, "//div[@id='itnet-ec-ordcon']", "wrapper page content block")
