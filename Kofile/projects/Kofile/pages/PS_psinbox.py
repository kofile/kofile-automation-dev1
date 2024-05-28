"""
Represents properties and methods for Inbox popup
"""
# probably I should add an attribute that indicates that inbox
# popup is opened
from selenium.webdriver.common.by import By

from projects.Kofile.Lib.test_parent import PagesParent


class PSInbox(PagesParent):
    def __init__(self):
        super(PSInbox, self).__init__()

    inbox_pop_up = (By.ID, "viewInboxItemsBubble", "Inbox pop-up window")
    submit_button = (By.XPATH, "//*[@id='submitInboxBtn']", "Submit button")
    comment = (By.XPATH, "//*[@id='comment']", "Comment")
    customer = (By.XPATH, "//*[@id='CustomerName']", "Customer")
    order_type_options = (By.XPATH, "//*[@id='orderTypeList']/option", "Order type options")
    order_type = (By.XPATH, "//*[@id='orderTypeList']", "Order type")
    order_type_multi_1 = (By.XPATH, "//table[@id='viewInboxTable']/tbody/tr[", "Order type multi")
    order_type_multi_2 = "]/td[6]/div/div/div[1]/select[@id='orderTypeList']"
    label = (By.XPATH, "//*[@id='orderTypeDesc']", "Label")
    clear_inbox = (By.XPATH, "//*[@id='clearInboxBtn']", "Clear inbox")
    cancel = (By.XPATH, "//*[@id='widget-kofileinfobubble-cancelui-id1']", "Cancel")
    submit = (By.XPATH, "//*[@id='submitInboxBtn']", "Submit")
    table_rows = (By.XPATH, "//*[@id='viewInboxTable']/tbody/tr", "Table rows")
    order_confirmation_pop_up = (By.ID, "kofile-orderConfirmation", "Order confirmation pop-up")
    conf_close = (By.XPATH, "//*[@id='closeInboxSubmitOderConfirm']", "Conf close")
    conf_order_number = (By.XPATH, "//*[@id='orderConfirmationBlock']/div/div[2]/div[1]", "Conf order number")
    conf_order_number_multi_1 = (By.XPATH, "//div[@id='orderConfirmation']/div/div/div[", "Conf order number multi")
    conf_order_number_multi_2 = "]/div[1]"
    conf_number_of_docs = (By.XPATH, "//*[@id='orderConfirmationBlock']/div/div[2]/div[2]", "Conf number of docs")
    conf_doc_numbers = (
    By.XPATH, "//*[@id='orderConfirmationBlock']/div/div[2]/div[3]/div", "Conf doc numbers")  # add [number]
    conf_status = (By.XPATH, "//*[@id='orderConfirmationBlock']/div/div[2]/div[4]", "Conf status")
