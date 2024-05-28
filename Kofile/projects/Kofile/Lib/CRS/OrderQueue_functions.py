from projects.Kofile.Lib.CRS.CRS_functions import CRS
from projects.Kofile.Lib.test_parent import LibParent
from projects.Kofile.Atom.CRS.order_queue import OrderQueue as OrderQueueAtom
from projects.Kofile.Atom.CRS.order_summary import OrderSummary

CRS_functions = CRS()


class OrderQueue(LibParent):
    def __init__(self):
        super(OrderQueue, self).__init__()

    def add_new_order(self, warning_popup=False, init_popup=False, init=True):
        # click on "Add new Order" button and check pop-ups
        self._general_helper.find_and_click(self._pages.CRS.order_queue.btn_add_new_order)
        warn_popup = self.check_popup(warning_popup, init_popup, init)
        if init and not warn_popup:
            # Wait 'New order' page loaded
            self._general_helper.find(self._pages.CRS.order_entry.ddl_order_type)

    def next_order(self, warning_popup=False, init_popup=False, init=True):
        # click "Next order" button and check pop-ups
        self._general_helper.find_and_click(self._pages.CRS.order_queue.btn_next_order)
        self.check_popup(warning_popup, init_popup, init)

    def check_popup(self, warning_popup=False, init_popup=False, init=True):
        if init:
            # Click on 'Initialize' button in Drawer initialization pop-up if it displays
            self._general_helper.find_and_click(self._pages.CRS.order_queue.pup_drawer_initialize_btn_initialize,
                                                timeout=3,
                                                should_exist=init_popup)
        else:  # Wait 'Initialize' button and click 'Close(X)'
            if self._general_helper.find(self._pages.CRS.order_queue.pup_drawer_initialize_btn_initialize, timeout=3,
                                         should_exist=init_popup):
                self._general_helper.find_and_click(self._pages.CRS.order_queue.pup_drawer_initialize__btn_close)
                return
        # Wait 'new drawer session for the same day' pop-up
        popup = self._general_helper.find(self._pages.CRS.order_queue.pup_drawer_new_session_for_the_same_day,
                                          timeout=3,
                                          should_exist=warning_popup)
        exp_msg = "System is trying to initialize a new drawer session for the same day . " \
                  "Please ask an Administrator to help correct this error"
        # Check warning pop-up if it should exist
        if warning_popup and popup:
            assert popup.text == exp_msg, f"Actual warning message '{popup.text}' is not equal to expected '{exp_msg}'"
            self._general_helper.find_and_click(
                self._pages.CRS.order_queue.pup_drawer_new_session_for_the_same_day__ok_btn)
            return popup
        elif warning_popup and not popup:
            assert popup, f"Warning popup '{exp_msg}' is not displayed"

    def wait_for_order_queue_is_displayed(self):
        self._actions.wait_for_element_displayed(self._pages.CRS.general.btn_add_new_order)
        CRS_functions.click_all_show_all_action_links()
        self._actions.wait_for_element_displayed(self._pages.CRS.general.lbl_order_count)

    def check_order_after_switching_between_queues(self):
        self.wait_for_order_queue_is_displayed()
        run_man = self._pages.CRS.general.running_man_by_order_number(self._general_helper.get_data()["order_number"])
        self._general_helper.scroll_and_click(run_man)
        self._actions.wait_for_element_displayed(self._pages.CRS.order_summary.lbl_order_number)
        # edit OIT
        OrderSummary().edit_oit(edit_all=True)
        # go to any queue and the return to order queue
        self._actions.wait(1)
        self._actions.wait_for_element_present(self._pages.CRS.general.lnk_go_to_indexing)
        CRS_functions.go_to_indexing_queue()
        self._actions.wait(0.5)
        self._actions.wait_for_element_displayed(self._pages.CRS.indexing_queue.btn_add_new_indexing_task)
        CRS_functions.go_to_order_queue()
        # atom
        OrderQueueAtom().check_status_of_order(status='In_Process')
        CRS_functions.check_assignment()

    def click_running_man(self):
        self._actions.wait_for_element_displayed(self._pages.CRS.general.lbl_order_count)
        CRS_functions.click_all_show_all_action_links()
        self._actions.wait_for_element_displayed(self._pages.CRS.general.lbl_order_count)
        run_man = self._pages.CRS.general.running_man_by_order_number(self._general_helper.get_data()["order_number"])
        self._general_helper.scroll_and_click(run_man)
        self._actions.wait_for_element_displayed(self._pages.CRS.order_summary.lbl_order_number)

    def get_order_info_in_queue(self, order):
        order_status_ = self._general_helper.find(self._pages.CRS.general.status_by_order_number(order), get_text=True)
        assigned_clerk_el_ = self._pages.CRS.general.assigned_to_by_order_number_text(order)
        assigned_clerk_ = self._general_helper.find(assigned_clerk_el_, get_attribute='value')
        origin_ = self._general_helper.find(self._pages.CRS.general.origin_by_order_number(order), get_text=True)
        run_man_ = self._pages.CRS.general.running_man_by_order_number(order)
        return order_status_, assigned_clerk_el_, assigned_clerk_, origin_, run_man_

    def run_man_existence(self, run_man_el, order_num, should_exist=True):
        self._actions.assert_element_attribute_is_not(run_man_el, 'style', 'display: none;') if should_exist \
            else self._actions.assert_element_attribute(run_man_el, 'style', 'display: none;')
        self._actions.step(f"{order_num} running man {'' if should_exist else 'not '}exist")

    def check_note_description(self, note_desc):
        self._actions.wait_for_element_displayed(self._pages.CRS.order_entry.note_description)
        self._actions.wait(1)
        desc_in_page = self._actions.get_element_value(self._pages.CRS.order_entry.note_description)
        if note_desc not in desc_in_page:
            self._actions.error(f"Note description is: '{desc_in_page}' not contains to actual: '{note_desc}'")

    def check_note_pop_up_text(self, note):
        self._actions.wait_for_element_displayed(self._pages.CRS.order_queue.tip_status_comment)
        self._actions.verify_element_text_contains(self._pages.CRS.order_queue.tip_status_comment, note)

    def find_order_in_order_queue(self, order_number):
        CRS_functions.click_all_show_all_action_links()
        if self._general_helper.find(
                self._general_helper.make_locator(self._pages.CRS.order_queue.order_number_by_order_number_,
                                                  order_number)):
            self._logging.info("Order is found in Order Queue")
