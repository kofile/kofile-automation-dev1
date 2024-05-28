"""Clerk Search, Public Search or Kiosk Search Preview popup
 when a row is clicked"""
from projects.Kofile.Lib.test_parent import LibParent
import time


class PSPreview(LibParent):
    def __init__(self):
        super(PSPreview, self).__init__()

    def preview_loading(self):
        preview_loading_ = True
        tm = time.time() + 30
        while preview_loading_ and (tm > time.time()):
            time.sleep(1)
            if "loadindicator" not in self._general_helper.find(self._pages.PS.preview.preview_dialog).get_attribute(
                    "class").lower():
                preview_loading_ = False

    def visible_tabs(self):
        """
        Returns a list of strings containing visible tab names.
        """
        res_list = []
        self._general_helper.find(self._pages.PS.preview.is_preview_loaded)
        lst = self._general_helper.find_elements(self._pages.PS.preview.visible_tabs)
        if len(lst) > 0:
            res_list = [x.text for x in lst if x.text != "" and "ng-hide" not in x.get_attribute("class")]
            return res_list
        else:
            return res_list

    @staticmethod
    def __is_attribute_present(welement, attribute, attribute_value, timeout=5):
        """
        This method waits until given attribute value is equal to given value within timeout. Returns
        True if attribute value is equal to attribute_value, False - otherwise.
        This method doesn't verifies whether 'welement' is present or not.
        welement        - webelement, as webelement
        attribute       - attribute name as string
        attribute_value - expected attribute value as string
        timeout         - timeout in seconds as integer, default value is 5 seconds
        """
        ret = True
        cur_time = time.time()
        while (cur_time + timeout) > time.time():
            res = welement.get_attribute(attribute)
            if attribute_value not in res:
                ret = False
            else:
                return True
        return ret

    @staticmethod
    def __is_attribute_not_present(welement, attribute, attribute_value, timeout=5):
        """
        This method waits until given attribute value is not equal to given value within timeout. Returns
        True if attribute value is not equal to attribute_value, False - otherwise.
        This method doesn't verifies whether 'welement' is present or not.
        welement        - webelement, as webelement
        attribute       - attribute name as string
        attribute_value - expected attribute value as string
        timeout         - timeout in seconds as integer, default value is 5 seconds
        """
        ret = True
        cur_time = time.time()
        while (cur_time + timeout) > time.time():
            res = welement.get_attribute(attribute)
            if attribute_value in res:
                ret = False
            else:
                return True
        return ret

    def click_add_to_inbox(self, pages, count="1", pspp=False):
        """
        Adds current document to Inbox.
        pages - what to add, integer: 1 - All, 2 - Current, 3 - Custom
        count - page count for custom option, string
        """
        if "Image" in self.visible_tabs():
            # use method parameters, add to Inbox image
            if self.active_tab() != "Image":
                # go to Image tab
                self.click_tab("Image")
            if not pspp:
                self._general_helper.find_and_click(self._pages.PS.preview.add_to_inbox_button)
            else:
                self._general_helper.find_and_click(self._pages.PS.preview.add_to_cart_btn)
            if pages == 1:  # All
                self._general_helper.find_and_click(self._pages.PS.preview.addtoinbox_all)
            elif pages == 2:  # Current
                self._general_helper.find_and_click(self._pages.PS.preview.addtoinbox_current)
            elif pages == 3:  # Custom
                self._general_helper.find_and_click(self._pages.PS.preview.addtoinbox_custom)
                self._general_helper.find_and_send_keys(self._pages.PS.preview.addtoinbox_custom_text, count)
            self._general_helper.find_and_click(self._pages.PS.preview.addtoinbox_continue)
            res = self._general_helper.find(self._pages.PS.preview.addtoinbox_hidden)
            if pspp is False:
                attr_value = "ng-scope addToInboxWithImage ng-hide"
            else:
                attr_value = "ng-scope ng-hide"
            if self.__is_attribute_present(res, "class", attr_value, 30) is False:
                return False
            return True
        else:
            # don't use method parameters, add to Inbox document only
            self._general_helper.find_and_click(self._pages.PS.preview.add_to_inbox_button)
            res = self._general_helper.find(self._pages.PS.preview.addtoinbox_hidden)
            if self.__is_attribute_not_present(res, "class", "ng-hide", 30) is False:
                print("Time is out for Add to Inbox popup to be opened")
            res = self._general_helper.find(self._pages.PS.preview.addtoinbox_hidden)
            if self.__is_attribute_present(res, "class", "ng-hide", 30) is False:
                return False
            return True

    def active_tab(self):
        """
        Returns the name of active tab as string. Empty string otherwise
        """
        res = self._general_helper.find_elements(self._pages.PS.preview.visible_tabs)
        for i in res:
            if "active" in i.get_attribute("class"):
                return i.text

    def click_cancel(self):
        """
        Clicks Cancel button and closes Preview window
        """
        self._general_helper.find(self._pages.PS.preview.html_body)
        self._general_helper.find_and_click(self._pages.PS.preview.cancel_button)
        preview_is_visible = True
        tm = time.time()
        while preview_is_visible is True and (tm + 5) > time.time():
            time.sleep(1)
            preview_visibility = self._general_helper.find(self._pages.PS.preview.html_body).get_attribute("class")
            preview_is_visible = True if "no-scrollable" in preview_visibility else False
        return not preview_is_visible

    def click_close(self):
        """
        Clicks close button and closes Preview window
        """
        # preview is visible
        self._general_helper.find(self._pages.PS.preview.html_body)
        self._general_helper.find_and_click(self._pages.PS.preview.cancel_button)
        # preview is closed
        preview_is_visible = True
        tm = time.time() + 5
        while preview_is_visible and tm > time.time():
            time.sleep(1)
            preview_visibility = self._general_helper.find(self._pages.PS.preview.html_body).get_attribute("class")
            preview_is_visible = True if "no-scrollable" in preview_visibility else False
        return not preview_is_visible

    def click_tab(self, tab_name):
        """
        Clicks specified tab. For a list of available tabs call visible_tabs()
        tab_name - string, tab name to be clicked
        """
        self._general_helper.wait_disappear_element(self._pages.PS.preview.preview_spinner, 30)
        tab_locator = self._general_helper.remake_locator(
            self._pages.PS.preview.visible_tabs, f"[text()='{tab_name}']", f"'{tab_name}' tab")
        self._actions.wait_for_element_displayed(tab_locator)
        self._general_helper.find_and_click(tab_locator)

    def click_prev_doc_button(self):
        """
        Clicks Prev Doc button if button is enabled
        """
        p_but = self._general_helper.find(self._pages.PS.preview.prev_doc)
        if "previewNavDisabled" not in p_but.get_attribute("class"):
            self._general_helper.find_and_click(
                self._general_helper.remake_locator(self._pages.PS.preview.prev_doc, "/span"))
            time.sleep(1)
            # wait until preview data is loaded
            self.preview_loading()

    def click_next_doc_button(self):
        """
        Clicks Next Doc button if button is enabled
        """
        p_but = self._general_helper.find(self._pages.PS.preview.next_doc)
        if "previewNavDisabled" not in p_but.get_attribute("class"):
            self._general_helper.find_and_click(
                self._general_helper.remake_locator(self._pages.PS.preview.prev_doc, "/span"))
            time.sleep(1)
            # wait until preview data is loaded
            self.preview_loading()
