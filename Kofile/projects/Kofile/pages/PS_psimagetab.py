"""
Represents properties and methods for Preview/Image tab
"""
from selenium.webdriver.common.by import By

from projects.Kofile.Lib.test_parent import PagesParent


class PSImageTab(PagesParent):
    def __init__(self):
        super(PSImageTab, self).__init__()

    page = (By.XPATH, "//*[@id='image-paging']", "Page")
    pages = (By.XPATH, "//*[@id='total-images']", "Pages")
