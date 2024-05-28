"""
module doc string
"""
from projects.Kofile.Lib.test_parent import LibParent

class CRS(LibParent):
    def __init__(self):
        super(CRS, self).__init__()

    def verify_order_status(self, status):
        """Verify status of order in order queue"""
        data = self._general_helper.get_data()
        if not data.get("order_number") and data.get("doc_number"):
            self._actions.store("order_number",
                                self._general_helper.find(
                                    self._pages.CRS.general.order_number_by_doc_number(data["doc_number"]),
                                    get_text=True))
        self._actions.verify_element_text(self._pages.CRS.general.status_by_order_number(data["order_number"]),
                                          data['config'].get_status(f'Order.{status}.value'))

    def verify_file_present(self, expected_file_name):
        """verify if field have expected text"""
        self._actions.wait_for_element_present(self._pages.CRS.order_entry.uploaded_file(expected_file_name), 120)
        self._actions.assert_element_text(self._pages.CRS.order_entry.uploaded_file(expected_file_name),
                                          expected_file_name)

    def check_assignment(self):
        """check that order assigned to logged in clerk"""
        assigned_to_loc = self._pages.CRS.general.assigned_to_by_order_number_text(
            self._general_helper.get_data()['order_number'])
        self.click_all_show_all_action_links()
        self._general_helper.scroll_into_view(assigned_to_loc)
        self._actions.verify_element_attribute(assigned_to_loc, 'value', self.assign_user_name())

    def assign_order_by_user_name(self, order_number, ind=0, add=True):
        """
        assign order, specified by order_number.
        user name is taken from environment json file.
        order must be already visible in queue and Administrative button is already clicked
        """
        # assign button in queue row
        if self._general_helper.check_if_element_exists(self._pages.CRS.indexing_queue.ddl_administrative_user_group):
            self._actions.select_option_by_value(self._pages.CRS.indexing_queue.ddl_administrative_user_group, '0')
            self._general_helper.wait_for_spinner(spinner_in=10)
            self._actions.wait_for_element_not_exist(self._pages.CRS.general.greyed_overlay)
        assign_path = self._pages.CRS.general.assign_icon_by_order_number(order_number)
        for attempt in range(2, -1, -1):
            try:
                self._general_helper.scroll_and_click(assign_path, timeout=10)
            except ValueError as e:
                self._logging.info(e)
                if not attempt:
                    raise e
            if self._general_helper.check_if_element_exists(self._pages.CRS.general.pup_assign_ddl_btn_expand,
                                                            timeout=10):
                break
            self.refresh_queue()
        # expand dropdown
        self._general_helper.find_and_click(self._pages.CRS.general.pup_assign_ddl_btn_expand)
        assign_name = self._general_helper.make_locator(self._pages.CRS.general.pup_assign_ddl_select_by_name,
                                                        self.assign_user_name(ind))
        self._general_helper.scroll_and_click(assign_name)
        self._general_helper.find_and_click(
            self._pages.CRS.general.pup_assign_btn_add if add else
            self._pages.CRS.general.pup_btn_assignorder_cancel)
        self._actions.wait_for_element_not_present(self._pages.CRS.general.pup_assign_btn_add)
        self._general_helper.wait_for_spinner()

    def assign_user_name(self, ind=0):
        """
        return login user name
        """
        env = self._general_helper.get_data().env
        return f"{env.user_first[ind]} {env.user_last[ind]}"

    def click_all_show_all_action_links(self, wait_between_clicks=1):
        """
        Locates 'SHOW ALL' links and clicks it
        """
        self._general_helper.find(self._pages.CRS.general.logo)
        try:
            all_ = self._general_helper.find_elements(self._pages.CRS.general.show_all_link)
            for _ in all_:
                self._general_helper.scroll_and_click(self._pages.CRS.general.show_all_link)
                self._actions.wait(wait_between_clicks)
            return True
        except Exception as e:
            self._logging.info(e)
            return False

    def get_list_of_orders(self):
        """
        Return list of orders
        """
        self.click_all_show_all_action_links()
        self._general_helper.wait_for_spinner()
        self._actions.wait(2)
        orders_list = self._general_helper.find_elements(self._pages.CRS.general.orders_in_queue, get_text=True)
        return orders_list

    def click_running_man(self):
        """Click running man of given order in given page (for example page=CRS_OrderQueue)"""
        run_man = self._pages.CRS.general.running_man_by_order_number(self._general_helper.get_data()["order_number"])
        self._general_helper.wait_for_page_load()
        try:
            self._general_helper.scroll_and_click(run_man, 2)
        except Exception as e:
            self._logging.warning(e)
            self.click_all_show_all_action_links()
            if not self._general_helper.scroll_and_click(run_man, 5):
                raise e
        # Click on 'Initialize' button in Drawer initialization pop-up if it displays
        self._general_helper.find_and_click(self._pages.CRS.order_queue.pup_drawer_initialize_btn_initialize, timeout=1,
                                            should_exist=False)

    def count_orders_in_queue(self):
        """
        Pre-conditions: Order Queue is opened
        Post-conditions: Order queue is opened, order number count is checked
        """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        lbl_total = self._general_helper.find(self._pages.CRS.general.lbl_order_count, get_text=True)
        return lbl_total

    def go_to_order_queue(self):
        """
        go to Order Queue
        """
        self._actions.step("- - - - - Go to ORDER QUEUE - - - - -")
        self._general_helper.find_and_click(self._pages.CRS.general.lnk_go_to_orders)
        self._general_helper.wait_for_spinner()
        self._actions.wait_for_window_present_by_partial_url("/ShowOrderQueue")
        self._actions.wait_for_element_displayed(self._pages.CRS.order_queue.btn_refresh, timeout=60)

    def go_to_capture_queue(self):
        """
        go to Capture Queue
        """
        self._actions.step("- - - - - Go to CAPTURE QUEUE - - - - -")
        self._general_helper.find_and_click(self._pages.CRS.general.lnk_go_to_capture)
        self._general_helper.wait_for_spinner()
        self._actions.wait_for_window_present_by_partial_url("/ShowCaptureQueue")
        # Wait loading page
        self._general_helper.find(self._pages.CRS.capture_queue.btn_start_batch_scan)

    def go_to_indexing_queue(self):
        """
        go to Indexing Queue
        """
        self._actions.step("- - - - - Go to INDEXING QUEUE - - - - -")
        self._actions.wait_for_element_present(self._pages.CRS.general.lnk_go_to_indexing)
        self._general_helper.find_and_click(self._pages.CRS.general.lnk_go_to_indexing)
        self._general_helper.wait_for_spinner()
        self._actions.wait_for_window_present_by_partial_url("/ShowIndexQueue")

    def go_to_verification_queue(self):
        """
        go to Verification Queue
        """
        self._actions.step("- - - - - Go to VERIFICATION QUEUE - - - - -")
        self._general_helper.find_and_click(self._pages.CRS.general.lnk_go_to_verification)
        self._general_helper.wait_for_spinner()
        self._actions.wait_for_window_present_by_partial_url("/ShowVerificationQueue")

    def go_to_order_search(self, retries=2):
        """
        go to Main Menu-Search
        """
        self._actions.step("- - - - - Go to ORDER SEARCH - - - - -")
        self._general_helper.find_and_click(self._pages.CRS.general.lnk_go_to_search)
        retries -= 1
        self._general_helper.wait_for_spinner()
        try:
            self._actions.wait_for_window_present_by_partial_url("/OrderSearch", 15)
        except Exception as e:
            if retries:
                self._logging.warning(e)
                return self.go_to_order_search(retries)
            else:
                raise ValueError(e)

    def go_to_package_search(self):
        """
        go to Search Submenu -> Package Search
        """
        self._actions.step("- - - - - Go to PACKAGE SEARCH - - - - -")
        self.go_to_order_search()
        self._general_helper.find_and_click(self._pages.CRS.general.lnk_go_to_package_search)
        self._general_helper.wait_for_spinner()
        self._actions.wait_for_window_present_by_partial_url("/PackageSearch")

    def go_to_reports(self):
        """
        go to Reports
        """
        self._actions.step("- - - - - Go to REPORTS - - - - -")
        self._general_helper.find_and_click(self._pages.CRS.general.lnk_go_to_reports)
        self._general_helper.wait_for_spinner()
        self._actions.wait_for_window_present_by_partial_url("/reports")

    def go_to_front_office(self):
        """
        go to Front Office menu
        """
        self._actions.step("- - - - - Go to FRONT OFFICE - - - - -")
        self._general_helper.find_and_click(self._pages.CRS.general.lnk_go_to_front_office)
        self._general_helper.wait_for_spinner()
        self._actions.wait_for_window_present_by_partial_url("/CompanyAccounts")

    def check_count_orders(self):
        self.click_all_show_all_action_links()
        self._actions.wait(1)
        lbl_total = self.count_orders_in_queue().split('/')[0]
        if lbl_total == '0':
            self._actions.step('Queue is empty')
        else:
            orders_count = len(self._actions.get_browser().find_all(self._pages.CRS.general.orders_in_queue))
            self._general_helper.scroll_into_view(self._pages.CRS.general.lbl_order_count)
            self._actions.assert_equals(lbl_total, str(orders_count))

    def refresh_queue(self):
        self._general_helper.wait_for_element_clickable(self._pages.CRS.general.btn_refresh)
        self._general_helper.scroll_and_click(self._pages.CRS.general.btn_refresh)
        self._general_helper.wait_for_spinner()

    def click_admin_key(self):
        self._general_helper.find_and_click(self._pages.CRS.general.btn_admin_key)
        self._general_helper.wait_for_spinner()

    def fill_reason(self, popup_locator, submit=True):
        self._actions.wait_for_element_displayed(popup_locator)
        if self._general_helper.find(self._pages.CRS.order_summary.pup_reject_entire_order_action, should_exist=False, timeout=2):
            if self._general_helper.find(
                self._pages.CRS.order_summary.pup_reject_entire_order_action, should_exist=False, get_attribute='Style') != 'display: none;':
                self._actions.wait_for_element_text_is_not(self._pages.CRS.order_summary.pup_reject_entire_order_action, "")
            self._actions.send_keys_with_delay(self._pages.CRS.order_entry.pup_action_reason_field, self._names.ANY_DATA['any_text'])
            self._actions.send_keys(self._pages.CRS.order_entry.pup_action_reason_description_field,
                                self._names.ANY_DATA['any_text'])
        else:
                self._actions.send_keys_with_delay(self._pages.CRS.order_entry.pup_action_reason_field, self._names.ANY_DATA['any_text'])
                self._general_helper.find(self._pages.CRS.order_entry.pup_action_reason_field).send_keys(self._keys.TAB)
        self._actions.click(
            self._pages.CRS.order_entry.pup_action_reason_submit if
            submit else self._pages.CRS.order_entry.pup_action_reason_cancel)

    def reject_erproxy_order(self, submit=True):
        self._general_helper.wait_and_click(self._pages.CRS.order_summary.pup_action_reason_filter)
        self._general_helper.wait_and_click(self._pages.CRS.order_summary.first_action_reason)
        self._actions.click(
            self._pages.CRS.order_entry.pup_action_reason_submit if
            submit else self._pages.CRS.order_entry.pup_action_reason_cancel)



    def verify_order_notes(self, text):
        data = self._general_helper.get_data()
        self._general_helper.find_and_click(self._pages.CRS.general.notes_by_order_number(data["order_number"]))
        self._actions.wait_for_element_present(self._pages.CRS.verification_queue.note_container)
        self._actions.wait_for_element_text_contains(self._pages.CRS.verification_queue.note_container, text)
        self._actions.wait_for_element_text_contains(self._pages.CRS.verification_queue.note_container,
                                                     data["env"]["user"][data["user_index"]])
