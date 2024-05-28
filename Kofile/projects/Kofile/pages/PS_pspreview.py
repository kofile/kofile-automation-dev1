"""
Current document Preview popup window methods and properties
"""
from selenium.webdriver.common.by import By

from projects.Kofile.Lib.test_parent import PagesParent


class PSPreview(PagesParent):
    def __init__(self):
        super(PSPreview, self).__init__()

    visible_tabs = (By.XPATH, "//*[@id='previewHeaderTabs']/ul/li", "Visible tabs")
    html_body = (By.XPATH, "/html/body", "Page body")
    # //*[@id="previewHeaderTabs"]/ul/li[2]
    window_title = (By.XPATH, "//*[@id='preview-dialog']/div[1]/div[1]", "Window title")
    preview_dialog = (By.XPATH, "//*[@id='preview-dialog']", "Preview dialog")
    preview_spinner = (By.XPATH, "//div[contains(@class,'loadIndicator')]", "Preview Spinner")
    add_to_inbox_button = (By.XPATH, "//*[@id='preview-footer-buttons']/ul/li[3]/input", "Add to inbox button")
    cancel_button = (By.XPATH, "//*[@id='cancel']", "Cancel button")
    is_preview_loaded = (By.XPATH, "//*[@id='previewContentRow']/div[1]", "Is preview loaded")
    parties_section = (By.XPATH, "//*[@id='documentSummaryArea']/table/tbody/tr[3]/td/div[1]", "Parties section")
    addtoinbox_all = (By.XPATH, "//*[@id='addToCartBubbleAllpages']", "Add to inbox ALL")
    addtoinbox_current = (By.XPATH, "//*[@id='addToCartBubbleCurrentpage']", "Add to inbox CURRENT")
    addtoinbox_custom = (By.XPATH, "//*[@id='addToCartBubbleCustompage']", "Add to inbox CUSTOM")
    addtoinbox_custom_text = (By.XPATH, "//*[@id='addToCartBubbleCustomPageNo']", "Add to inbox CUSTOM text")
    addtoinbox_continue = (By.XPATH, "//*[@id='bubbleContent']/div[3]/a[2]", "Add to inbox CONTINUE")
    addtoinbox_cancel = (By.XPATH, "//*[@id='bubbleContent']/div[3]/a[1]", "Add to inbox CANCEL")
    addtoinbox_hidden = (By.XPATH, "//*[@id='image_preview_sub']", "Add to inbox HIDDEN")
    addtoinbox_success = (By.XPATH, "//*[@id='addToInboxMessage']", "Add to inbox SUCCESS")  # span text should be empty
    close_button = (By.XPATH, "//*[@id='dialog-content-holder-close']", "Add to inbox CLOSE")
    prev_doc = (By.XPATH, "//*[@id='previewHeaderNav']/a[1]", "Prev doc")  # for click add /span
    next_doc = (By.XPATH, "//*[@id='previewHeaderNav']/a[2]", "Next doc")
    add_to_cart_btn = (By.XPATH, "//*[@id='addToCartBtn']", "ADD to cart button")
