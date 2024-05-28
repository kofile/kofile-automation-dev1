"""Clerk Search, Public Search or Kiosk Search main page,
including Option, Party, Document Groups and Search Type panels"""
import logging

from projects.Kofile.Lib.PS_CS.PS_inbox import PSInbox
from projects.Kofile.Lib.test_parent import LibParent
from selenium.webdriver.common.by import By
import time

ps_inbox = PSInbox()


class PSMainPage(LibParent):
    def __init__(self):
        super(PSMainPage, self).__init__()

    def clear_inbox_(self):
        if int(self.inbox_item_count()) > 0:
            self.click_inbox()
            # wait until all inbox rows are loaded
            ps_inbox.table_row_count(self.inbox_item_count())
            ps_inbox.click_clear_inbox()
            ps_inbox.click_cancel()

    def result_table_header_list(self):
        """
        Returns a list of strings containing non-empty column names
        """
        # to verify presence of table header
        self._general_helper.find(self._pages.PS.main_page.result_table)
        t_header_list = self._general_helper.find_elements(self._pages.PS.main_page.result_table_header, get_text=True)
        return t_header_list

    def result_table_data_row_count(self):
        """
        Returns number of data rows as integer after clicking Search button.
        """
        # wait for table header to be loaded
        self._general_helper.find(self._pages.PS.main_page.result_table)
        self._general_helper.find(self._pages.PS.main_page.next_page)
        # verify 'expand row' button for the first row
        self._general_helper.find(self._pages.PS.main_page.expand_btn)
        data_rows = self._general_helper.find_elements(self._pages.PS.main_page.doc_rows)
        last_row = self._general_helper.find(
            self._general_helper.remake_locator(self._pages.PS.main_page.doc_rows, f"[{len(data_rows)}]"))
        # fucking EPAM
        if last_row.get_attribute("id") == "tabs-template":
            return len(data_rows) - 1  # last row is not informative
        else:
            return len(data_rows)

    def result_table_data(self, pspp=False):
        """
        Returns a list of lists. Inner lists contain data strings. 'Print', 'QuickDoc',
        'Add to Inbox' and 'Document in Workflow' icons are saved as '1' (str) in case if icon is visible, and
        '0' (str) - if not.
        This method takes approximatelly 15-20 sec to be executed if there are about 100 rows.
        """
        res_data = []  # result list
        temp_res_list = []  # temp list, vertical
        tab_header = []  # non empty column numbers of table header
        col_tag = self._general_helper.remake_locator(self._pages.PS.main_page.doc_rows, "/td")
        # get numbers of columns where table header is not empty, first column - 1
        self._general_helper.find(
            self._general_helper.remake_locator(self._pages.PS.main_page.result_table_header, "[last()]"))
        t_header = self._general_helper.find_elements(self._pages.PS.main_page.result_table_header)
        if len(t_header) > 0:
            for i in range(len(t_header)):
                # add only non empty column numbers
                if t_header[i].text != "":
                    tab_header.append(i + 1)
            # get current search result row count
            data_rows = self.result_table_data_row_count()
            if data_rows > 0:
                # iterate through columns and add data to temp_res_list
                for s_col in tab_header:
                    # read single column
                    res = self._general_helper.find_elements(self._general_helper.remake_locator(
                        col_tag, f"[{s_col}]", f"Doc column: {s_col}"))
                    if len(res) > data_rows:
                        # remove last row
                        res1 = res[0:data_rows]
                    else:
                        res1 = res
                    # add current column to temp vertical list
                    temp_res_list.append([x.text for x in res1])
                # read the rest of columns Print, QuickDoc, Add to Inbox
                for k in range(tab_header[-1] + 1, len(t_header) + 1):
                    if self._general_helper.find(
                            self._general_helper.remake_locator(self._pages.PS.main_page.result_table_data,
                                                                f"[1]/td[{k}]")):
                        continue
                    elem = self._general_helper.find(
                        self._general_helper.remake_locator(self._pages.PS.main_page.result_table_data,
                                                            f"[1]/td[{k}]/a"))
                    elem_attr = elem.get_attribute("title")
                    if pspp is False:
                        if elem_attr == "Print" or elem_attr == "QuickDoc" or \
                                elem_attr == "Add to Inbox" or elem_attr == "Document in workflow":
                            res = self._general_helper.find_elements(
                                self._general_helper.remake_locator(col_tag, f"[{k}]/a"))
                            if len(res) > data_rows:
                                # remove last row
                                res1 = res[0:data_rows]
                            else:
                                res1 = res
                            # add current column to temp vertical list
                            cur_lst = []
                            if len(res1) > 0:
                                for x in res1:
                                    if x.get_attribute("style") == "":
                                        cur_lst.append(elem_attr + "|0")
                                    else:
                                        cur_lst.append(elem_attr + "|1")
                                    # print(f"cur_lst: {cur_lst}")
                            temp_res_list.append(cur_lst)
                    else:
                        if elem_attr == "Add to KDrive" or elem_attr == "QuickDoc" or elem_attr == "Add to Cart":
                            res = self._general_helper.find_elements(
                                self._general_helper.remake_locator(col_tag, f"[{k}]/a"))
                            if len(res) > data_rows:
                                # remove last row
                                res1 = res[0:data_rows]
                            else:
                                res1 = res
                            # add current column to temp vertical list
                            cur_lst = []
                            if len(res1) > 0:
                                for x in res1:
                                    if x.get_attribute("style") == "":
                                        cur_lst.append(elem_attr + "|0")
                                    else:
                                        cur_lst.append(elem_attr + "|1")
                            temp_res_list.append(cur_lst)
                # convert vertical list to horizontal
                for c_row in range(data_rows):
                    lst_temp = []
                    for c_col in range(len(temp_res_list)):
                        # print(lst_temp)
                        lst_temp.append(temp_res_list[c_col][c_row])
                    # add table row to result
                    res_data.append(lst_temp)
                #  result is returned
                return res_data
            else:
                return res_data
        else:
            # empty list
            return res_data

    def click_search_button(self):
        """
        Starts search on currently opened department tab
        """
        self._general_helper.find_and_click(self._pages.PS.main_page.search_button)
        return self.__wait_for_search_result()

    def __wait_for_search_result(self):
        tm = time.time() + 30
        display_none = "display: none;"
        search_is_running = True
        while search_is_running is True and tm > time.time():
            time.sleep(1)
            self._actions.step("Wait until search is finished")
            p_count = self._general_helper.find(self._pages.PS.main_page.div_pagescount).get_attribute("style")
            no_match = self._general_helper.find(self._pages.PS.main_page.sorry_message).get_attribute("style")
            if (p_count == display_none and no_match != display_none) or \
                    (p_count != display_none and no_match == display_none):
                search_is_running = False
        # check if there is no timeout
        if search_is_running is True:
            self._actions.step("Time is out for search to be started")
            return False
        else:
            time.sleep(1)
            return True

    def next_department(self, click=True):
        """
        Locates Next '>' button and return True if button active
        click=True: clicks on it
        """
        next_btn = self._general_helper.find(self._pages.PS.main_page.dep_next_button)
        if next_btn.get_attribute("class") != "disabled-slide-nav":
            if not click:
                return True
            self._actions.step("-> Click 'Next department' button")
            next_btn.click()
            self._actions.wait(0.5)
            return True
        else:
            return False

    def prev_department(self, click=True):
        """
        Locates Prev '<' button and return True if button active
        click=True: clicks on it
        """
        prev_btn = self._general_helper.find(self._pages.PS.main_page.dep_prev_button)
        if prev_btn.get_attribute("class") != "disabled-slide-nav":
            if not click:
                return True
            self._actions.step("-> Click 'Prev department' button")
            prev_btn.click()
            self._actions.wait(0.5)
            return True
        else:
            return False

    def department_list(self, return_names=False, return_all=False):
        """
        Returns department tab elements
        return_names=True: return visible tab names
        return_all=True: return all tab names
        """
        all_departments_loc = (By.XPATH, "//a[contains(@id, 'Department_')]", "All department tabs")
        department_tabs = self._general_helper.find_elements(all_departments_loc, get_text=return_names)
        if return_names and return_all:
            # Scroll to last department
            tabs = []
            while self.next_department():
                tabs.extend(self._general_helper.find_elements(all_departments_loc, get_text=True))
            # add hidden tabs
            for i in tabs:
                if i not in department_tabs:
                    department_tabs.append(i)
            # remove empty strings
            department_tabs = [i for i in department_tabs if i]
            self._actions.step(str(department_tabs))
        return department_tabs

    def __wait_for_clicked_tab_is_loaded(self, dep_name):
        """Waits until page is loaded after clicking department tab. Returns
        True if current department is equal to dep_name
        dep_name    - clicked tab name

        """
        is_loaded = False
        tm = time.time() + 30
        while is_loaded is False and tm > time.time():
            if self.current_search_page_name() == dep_name:
                return True
            else:
                time.sleep(1)
        return False

    def click_on_department_tab(self, dep_name):
        departments = self.department_list(True)
        found = False
        limit = 3000
        if dep_name not in departments:
            if self.prev_department(click=False) and not self.next_department(click=False):
                # Scroll to first department
                while self.prev_department() and limit > 0:
                    limit -= 1
            else:
                # Scroll to last department
                while not found and self.next_department():
                    if dep_name in self.department_list(True):
                        found = True
            departments = self.department_list(True)
            if dep_name not in departments:
                raise ValueError(f"Expected department *{dep_name}* not found in: {departments}")
        department_tabs = self.department_list()
        for i in department_tabs:
            if i.text == dep_name:
                self._actions.step(f'-> Click on *{dep_name}* tab')
                i.click()
                return

    def click_department_tab(self, dep_name, dep_list):
        """
        Clicks department tab. Before using this method, use department_list() method to create a list of available tabs
        and get department tab count.
        Returns True if click was successfull, False - otherwise
        dep_name - department name (tab name)
        """
        # if tab is visible, click it
        dli = dep_list.index(dep_name) + 1
        dep_elem = self._general_helper.find(
            self._general_helper.remake_locator(self._pages.PS.main_page.department_tabs, f"[{dli}]/a"))
        if dep_elem.text != "":
            self._general_helper.find_and_click(
                self._general_helper.remake_locator(self._pages.PS.main_page.department_tabs, f"[{dli}]/a"))
            # odo - add here waiting for department page to be loaded after tab clicking
            self.__wait_for_clicked_tab_is_loaded(dep_name)
            return True
        # ---------------------------
        if len(dep_list) > 0:
            # search for dep_name in tabs
            for i in range(1, len(dep_list) + 1):
                # read tab text
                dep_elem = self._general_helper.find(
                    self._general_helper.remake_locator(self._pages.PS.main_page.department_tabs, f"[{i}]/a"))
                clickcount = 0
                while dep_elem.text == "" and clickcount < 20:
                    if clickcount < 10:
                        # click previous button
                        if self._general_helper.find(self._pages.PS.main_page.dep_prev_button).get_attribute(
                                "class") == "disabled-slide-nav":
                            clickcount += 1
                            continue
                        self._general_helper.find_and_click(self._pages.PS.main_page.dep_prev_button)
                        self._actions.wait(2)
                        clickcount += 1
                        dep_elem = self._general_helper.find(
                            self._general_helper.remake_locator(self._pages.PS.main_page.department_tabs, f"[{i}]/a"))
                    else:
                        # click next button
                        self._general_helper.find_and_click(self._pages.PS.main_page.dep_next_button)
                        self._actions.wait(2)
                        clickcount += 1
                        dep_elem = self._general_helper.find(
                            self._general_helper.remake_locator(self._pages.PS.main_page.department_tabs, f"[{i}]/a"))
                if dep_name == dep_elem.text:
                    self._general_helper.find_and_click(
                        self._general_helper.remake_locator(self._pages.PS.main_page.department_tabs, f"[{i}]/a"))
                    self.__wait_for_clicked_tab_is_loaded(dep_name)
                    return True

    def click_inbox(self, pspp=False):
        """
        Clicks Inbox or Cart link
        """
        self._general_helper.find_and_click(
            self._pages.PS.main_page.cart_link if pspp else self._pages.PS.main_page.inbox_link)
        return True

    def current_search_page_name(self):
        """
        Returns string containing current department search page name. Empty string otherwise
        """
        cur_page = self._general_helper.find(self._pages.PS.main_page.search_title, get_text=True)
        if len(cur_page) > 7:
            return cur_page[0:len(cur_page) - 7]
        else:
            return ""

    def clerk_name(self):
        """
        Returns current clerk name without 'Clerk:' word. If user is in public mode -
        returns string 'public'. In case of error or exception - returns empty string.
        """
        try:
            res = self._general_helper.find((By.XPATH, "//*[@id='registerUser']", "Clerk name"))
            if res is not None:
                return "public"
        except Exception as e:
            logging.error(type(e).__name__)
        res = self._general_helper.find(self._pages.PS.main_page.clerk_name, get_text=True)
        if len(res) > 6:
            return res[7:len(res)]
        else:
            return ""

    def current_page_number(self):
        """
        Returns current search page number as string. "0" - otherwise. Before using this method use
        click_search_button() method.
        """
        tm = time.time()
        res = self._general_helper.find(self._pages.PS.main_page.current_page_number)
        while res.text == "" and (tm + 5) > time.time():
            time.sleep(1)
            res = self._general_helper.find(self._pages.PS.main_page.current_page_number)
        if res.text != "":
            return res.text
        else:
            return "0"

    def current_pages_number(self):
        """
        Returns current search pages count as string. "0" - otherwise. Before using this method use
        click_search_button() method.
        """
        tm = time.time()
        res = self._general_helper.find(self._pages.PS.main_page.current_pages_count)
        while res.text == "" and (tm + 5) > time.time():
            time.sleep(1)
            res = self._general_helper.find(self._pages.PS.main_page.current_pages_count)
        if res.text != "":
            return res.text
        else:
            return "0"

    def is_search_successful(self):
        """
        Returns True if any search result is appear.
        False otherwise.
        In case of exception, returns False.
        Before calling this method, call click_search_button()
        """
        # Wait spinner
        self._general_helper.wait_for_spinner()
        # Wait result table
        self._general_helper.find(self._pages.PS.main_page.result_table)
        # Check "Sorry, no matches found." message
        if self._general_helper.find(self._pages.PS.main_page.result_table).get_attribute(
                "style") == 'display: none;' and self._general_helper.find(
                self._pages.PS.main_page.sorry_message).get_attribute("style") == "display: inline;":
            self._actions.step("--> Sorry, no matches found. <--")
            return False
        elif not self._general_helper.find(self._pages.PS.main_page.result_table).get_attribute(
                "style") == 'display: inline-block;':
            self._actions.error("--> CS API respond with 500 <--")
            return False
        return True

    def search_field(self, key_send, clear=False, timeout=30):
        """
        action, keysend - the same as for wait_for_element_to_be_present_and_log() method
        returns webelement, if any, None otherwise
        """
        el = self._general_helper.find_and_send_keys(self._pages.PS.main_page.search_input, key_send, clear=clear,
                                                     timeout=timeout)
        return el

    def inbox_item_count(self, pspp=False):
        """
        Returns Inbox or Cart item count as string.

        pspp - bool, if False return value for Inbox,
         if True - for Cart
        """
        res = self._general_helper.find(
            self._pages.PS.main_page.cart_item_count if pspp else self._pages.PS.main_page.inbox_item_count,
            get_text=True)
        return int(res)

    def click_more_options_button(self):
        btn = self._general_helper.find(self._pages.PS.main_page.option_pane_button)
        if btn.text == "More Options":
            self._actions.step(f'-> CLICK on *{self._pages.PS.main_page.option_pane_button}*')
            btn.click()

    def recorded_date_from_get(self):
        """
        Before calling this method, call option_pane_button() method to be sure that option
        pane is visible.
        Returns the string representing recorded date from field value. In case of exception - string 'None'
        """
        res = self._general_helper.find(self._pages.PS.main_page.recorded_date_from)
        return res.get_attribute("value")

    def instrument_date_from_get(self):
        """
        Before calling this method, call option_pane_button() method to be sure that option
        pane is visible.
        Returns the string representing instrument date from field value for the following tabs:
        Marriage Licenses       - Marriage Date Range From
        Birth Records           - Birth Date Range From
        Death Records           - Deceased Date Range From
        Commissioners Court     - Meeting Date Range From
        Foreclosures            - Sale Date Range From

        In case of exception - string 'None'
        """
        res = self._general_helper.find(self._pages.PS.main_page.instrument_date_from)
        return res.get_attribute("value")

    def recorded_date_from_set(self, newdate):
        """
        Sets Recorded date field value.
        Before calling this method, call option_pane_button() method to be sure that option
        pane is visible.
        newdate - new date, string
        """
        self._general_helper.find_and_send_keys(self._pages.PS.main_page.recorded_date_from, newdate)

    def instrument_date_from_set(self, newdate):
        """
        Sets Instrument date from field value.
        Before calling this method, call option_pane_button() method to be sure that option
        pane is visible.
        Applicable to the following tabs:
        Marriage Licenses       - Marriage Date Range From
        Birth Records           - Birth Date Range From
        Death Records           - Deceased Date Range From
        Commissioners Court     - Meeting Date Range From
        Foreclosures            - Sale Date Range From

        newdate - new date, string
        """
        self._general_helper.find_and_send_keys(self._pages.PS.main_page.instrument_date_from, newdate)

    def recorded_date_to_get(self):
        """
        Before calling this method, call option_pane_button() method to be sure that option
        pane is visible.
        Returns the string representing recorded date from field value. In case of exception - string 'None'
        """
        res = self._general_helper.find(self._pages.PS.main_page.recorded_date_to)
        return res.get_attribute("value")

    def instrument_date_to_get(self):
        """
        Before calling this method, call option_pane_button() method to be sure that option
        pane is visible.
        Returns the string representing instrument date to field value for the following tabs:
        Marriage Licenses       - Marriage Date Range From
        Birth Records           - Birth Date Range From
        Death Records           - Deceased Date Range From
        Commissioners Court     - Meeting Date Range From
        Foreclosures            - Sale Date Range From

        In case of exception - string 'None'
        """
        res = self._general_helper.find(self._pages.PS.main_page.instrument_date_to)
        return res.get_attribute("value")

    def date_to_set(self, req_dept_tab):
        newdate = r"{:%m/%d/%Y}".format(self._general_helper.get_current_date())
        if req_dept_tab != "Commissioners Court":
            self.recorded_date_to_set(newdate)
        else:
            self.instrument_date_to_set(newdate)

    def recorded_date_to_set(self, newdate):
        """
        Sets Recorded date field value.
        Before calling this method, call option_pane_button() method to be sure that option
        pane is visible.
        newdate - new date, string
        """
        self._general_helper.find_and_send_keys(self._pages.PS.main_page.recorded_date_to, newdate)

    def instrument_date_to_set(self, newdate):
        """
        Sets Instrument date to field value.
        Before calling this method, call option_pane_button() method to be sure that option
        pane is visible.
        Applicable to the following tabs:
        Marriage Licenses       - Marriage Date Range From
        Birth Records           - Birth Date Range From
        Death Records           - Deceased Date Range From
        Commissioners Court     - Meeting Date Range From
        Foreclosures            - Sale Date Range From

        newdate - new date, string
        """
        self._general_helper.find_and_send_keys(self._pages.PS.main_page.instrument_date_to, newdate)

    def click_row_icon(self, index, button):
        """
        Clicks Print, QuickDoc or Add to Inbox icon in a given row. Row is specified by index (integer).
        Before calling this method use result_table_data() method to get a list of
        search data and check whether this row has Print or another icons.

        index - integer, row index to be clicked, starts from 1;

        button for clerk search - integer: 1 - Print, 2 - QuickDoc, 3 - Add to Inbox;
        button for public search - integer: 1 - Add to KDrive, 2 - QuickDoc, 3 - Add to Cart
        """
        elems = self._general_helper.find_elements(
            self._general_helper.remake_locator(self._pages.PS.main_page.result_table_data, f"[{index}]//a"))
        if len(elems) > 0:
            for elem in elems:
                if (elem.get_attribute("title") == "Print" and button == 1) or \
                        (elem.get_attribute("title") == "QuickDoc" and button == 2) or \
                        (elem.get_attribute("title") == "Add to Inbox" and button == 3) or \
                        (elem.get_attribute("title") == "Add to KDrive" and button == 1) or \
                        (elem.get_attribute("title") == "Add to Cart" and button == 3):
                    # click it
                    elem.click()
                    self._actions.wait(2)
                    return True
        else:
            return False

    def click_next_page_button(self):
        """
        Clicks Next button at the bottom of the search result page.
        Before using this method use click_search_button() method.
        """
        self._general_helper.find_and_click(self._pages.PS.main_page.next_page)
        return self.__wait_for_search_result()

    def click_prev_page_button(self):
        """
        Clicks Next button at the bottom of the search result page.
        Before using this method use click_search_button() method.
        """
        self._general_helper.find_and_click(self._pages.PS.main_page.prev_page)
        return self.__wait_for_search_result()

    def get_found_document_numbers(self, return_numbers=False, not_in_workflow=False):
        """
        Return document number elements/text from result table
        """
        suffix = "/td/a[contains(@class, 'iconInWorkflow') and " \
                 "not(contains(@title, 'Document in workflow') and @style)]/../.."
        locator = ("xpath", f"//tr[contains(@class,'document-row')]"
                            f"{suffix if not_in_workflow else ''}/td[@data-column='Number']",
                   "Document number in result table")
        return self._general_helper.find_elements(locator, get_text=return_numbers)

    def click_row_with_doc_number(self, doc_number, not_in_workflow=False):
        doc_rows = self.get_found_document_numbers(not_in_workflow=not_in_workflow)
        result = []
        for i in doc_rows:
            result.append(i.text)
            if i.text == doc_number:
                self._actions.step(f"Click on row with *{doc_number}* in result table")
                i.click()
                return self.__wait_preview_update()
        raise ValueError(f"Document {doc_number} not found in result table: {result}")

    def click_row(self, index):
        """
        Clicks a row. Row is defined by index (integer). Before using this method
        call result_table_data_row_count() method to get maximum rows available.
        index starts from 1
        Returns True if Preview popup is visible, False - otherwise
        """
        preview_is_visible = False
        self._general_helper.scroll_and_click(
            self._general_helper.remake_locator(self._pages.PS.main_page.doc_rows, f"[{index}]"))
        # preview is opened
        tm = time.time() + 60
        # timeout for Preview opening is increased from 15s to 30s, increased again from 30s to 60s
        while preview_is_visible is False and tm > time.time():
            time.sleep(1)
            preview_visibility = self._general_helper.find((By.XPATH, "/html/body", "Page body")).get_attribute("class")
            preview_is_visible = True if ("no-scrollable" in preview_visibility) else False
        preview_is_visible = False
        tm = time.time() + 30
        while (preview_is_visible is False) and (tm > time.time()):
            time.sleep(1)
            dwn = self._general_helper.find((By.XPATH, "//*[@id='preview-dialog']", "Preview dialog")). \
                get_attribute("class").lower()
            preview_is_visible = False if ("loadindicator" in dwn) else True
        return preview_is_visible

    def __wait_preview_update(self):
        preview_is_visible = False
        # preview is opened
        tm = time.time() + 10
        while not preview_is_visible and (tm > time.time()):
            preview_visibility = self._general_helper.find((By.XPATH, "/html/body", "Page body")).get_attribute("class")
            if "no-scrollable" in preview_visibility:
                preview_is_visible = True
            else:
                self._actions.wait(1)
        # wait until preview data is loaded
        preview_is_visible = False
        tm = time.time() + 30
        while not preview_is_visible and (tm > time.time()):
            dwn = self._general_helper.find((By.XPATH, "//*[@id='preview-dialog']", "Preview dialog")). \
                get_attribute("class").lower()
            if "loadindicator" in dwn:
                preview_is_visible = True
            else:
                self._actions.wait(1)
        return preview_is_visible

    def wait_until_inbox_updated(self, init_value, pspp=False):
        """init_value - integer, inbox/cart item count before update"""
        now_value = int(self.inbox_item_count(pspp))
        tm = time.time()
        while now_value == init_value and (tm + 30) > time.time():
            time.sleep(0.5)
            now_value = int(self.inbox_item_count(pspp))
        if now_value == init_value:
            raise ValueError

    def wait_for_icon(self, pspp=False):
        """Waits for add to inbox/cart icon in first row to be visible.
        if pspp is False, clerk search must be opened.
        """
        # wait for add to cart icon to be visible
        ind = 14 if pspp else 15
        self._general_helper.find((By.XPATH, f"//*[@id='resultTable']/tbody/tr[1]/td[{ind}]/a", "Result table"))

    def c_names(self, checkbox_type="search"):
        """
        Before calling this method, call option_pane_button() method to be sure that option
        pane is visible.
        """
        # read checkbox names
        locator = self._pages.PS.main_page.checkboxes if checkbox_type == "search" else \
            self._pages.PS.main_page.pp_checkboxes if checkbox_type == "party" \
                else self._pages.PS.main_page.dg_checkboxes

        all_cb = self._general_helper.find_elements(locator, get_text=True)
        return all_cb

    def get_checkbox_names(self, checkbox_type="search"):
        """
        Returns a list of strings representing available checkbox names.
        In case of error returns empty list.
        """
        return self.c_names(checkbox_type)

    def get_checkbox_state(self, c_name, checkbox_type="search"):
        """
        Returns an integer representing a state of checkbox specified
        by c_name (checkbox name as string). 1 - checked, 0 - unchecked, -1 - error
        """
        locator = self._pages.PS.main_page.checkboxes if checkbox_type == "search" else \
            self._pages.PS.main_page.pp_checkboxes if checkbox_type == "party" else self._pages.PS.main_page.dg_checkboxes
        giv_c_box = self._general_helper.find(self._general_helper.remake_locator(
            locator, f"[{self.c_names(checkbox_type).index(c_name) + 1}]/input"))
        if giv_c_box.is_selected() is True:
            return 1
        else:
            return 0

    def click_checkbox(self, c_name, checkbox_type="search", should_exist=True):
        """
        Clicks the checkbox specified by c_name (checkbox name as string). Returns
        True if click is successful, False - otherwise
        """
        locator = self._pages.PS.main_page.checkboxes if checkbox_type == "search" else \
            self._pages.PS.main_page.pp_checkboxes if checkbox_type == "party" else self._pages.PS.main_page.dg_checkboxes
        self._general_helper.find_and_click(self._general_helper.remake_locator(
            locator, f"[{self.c_names(checkbox_type).index(c_name) + 1}]/input"), should_exist=should_exist)

    def get_checkbox_avail(self, c_name, checkbox_type="search"):
        """Verifies whether checkbox specified by c_name is available
        for clicking or not. Returns integer 1 - if available, 0 - if not

        """
        locator = self._pages.PS.main_page.checkboxes if checkbox_type == "search" else \
            self._pages.PS.main_page.pp_checkboxes if checkbox_type == "party" else self._pages.PS.main_page.dg_checkboxes
        res = self._general_helper.find(self._general_helper.remake_locator(
            locator, f"[{self.c_names(checkbox_type).index(c_name) + 1}]/input"))
        if res.get_attribute("disabled") == "disabled":
            return 0
        else:
            return 1

    def select_document_group(self, doc_group=None):
        doc_group = doc_group if doc_group else self._general_helper.get_data().get("test_config", {}).get("doc_group")
        if not doc_group:
            return
        try:
            self._general_helper.scroll_and_click(
                (By.XPATH, f"//*[@id='documentgroups']//li/label[text()='{doc_group}']",
                 f"'{doc_group}' Document Group Checkbox"), 2)
        except Exception as e:
            logging.info(e)

    def p_names(self):
        panel_names = []
        time.sleep(1)
        panels = self._general_helper.find_elements(self._pages.PS.main_page.rb_text_search)
        for elem in panels:
            if elem.text != "":
                panel_names.append(elem.text)
        panels2 = self._general_helper.find_elements(self._pages.PS.main_page.rb_image_search)
        for elem in panels2:
            if elem.text != "":
                panel_names.append(elem.text)
        return panel_names

    def get_rb_names(self):
        """Returns a list of strings representing available search panel
        radio button names

        """
        return self.p_names()

    def click_radio_button(self, o_name):
        """Clicks the radio button specified by o_name (radio button name as string)

        """
        pos = self.p_names().index(o_name)
        if pos <= 1:
            self._general_helper.find_and_click(
                self._general_helper.remake_locator(self._pages.PS.main_page.rb_text_search, f"[{pos + 1}]/input"))
        else:
            self._general_helper.find_and_click(
                self._general_helper.remake_locator(self._pages.PS.main_page.rb_image_search, f"[{pos - 1}]/input"))

    def get_rb_state(self, o_name):
        """Returns an integer representing a state of radio button
        specified by o_name (radio button name as string). 1 - checked, 0 - unchecked

        """
        pos = self.p_names().index(o_name)
        if pos <= 1:
            res = self._general_helper.find(
                self._general_helper.remake_locator(self._pages.PS.main_page.rb_text_search, f"[{pos + 1}]/input"))
            if res.is_selected() is True:
                return 1
            else:
                return 0
        else:
            res = self._general_helper.find(
                self._general_helper.remake_locator(self._pages.PS.main_page.rb_image_search, f"[{pos - 1}]/input"))
            if res.is_selected() is True:
                return 1
            else:
                return 0

    def verify_number_of_page(self, value, row=1):
        by, loc, desc = self._pages.PS.main_page.inbox_result_number_of_page
        path = (by, loc.format(row), desc)
        self._actions.wait_for_element_present(path)
        self._actions.wait_for_element_text(path, value)
