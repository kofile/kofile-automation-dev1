"""
Represents properties and methods for Preview/Attachments tab
"""
from selenium.webdriver.common.by import By

from projects.Kofile.Lib.test_parent import PagesParent


class PSAttachmentsTab(PagesParent):
    def __init__(self):
        super(PSAttachmentsTab, self).__init__()

    type_section = (By.XPATH, "//*[@id='attachmentsBlock']/ul/li", "Type section")
