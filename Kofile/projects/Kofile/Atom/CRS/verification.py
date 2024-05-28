from projects.Kofile.Lib.test_parent import AtomParent


class Verification(AtomParent):
    def __init__(self):
        super(Verification, self).__init__()

    def check_status_of_order_in_verification(self, status):
        """
           Pre-conditions: Verification Queue page is displayed
           Post-conditions: Verification Queue page is displayed, order status is checked
           """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        self._actions.wait_for_element_displayed(self._pages.CRS.general.lbl_order_count)
        self._lib.CRS.crs.click_all_show_all_action_links()
        self._actions.wait_for_element_displayed(self._pages.CRS.general.lbl_order_count)
        self._lib.CRS.verification_queue.verify_order_status(status)
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def process_review_order(self):
        """
           Pre-conditions: Verification Queue is opened. Order status is 'Review'
           Post-conditions: Verification Summary page is opened
           """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        # Go to Verification Queue
        self._lib.CRS.crs.go_to_verification_queue()
        # Verify that order status is 'Reviewed'
        self.check_status_of_order_in_verification("Review_status")
        # click running man
        self._lib.CRS.crs.click_running_man()
        self._actions.wait_for_element_displayed(self._pages.CRS.indexing_entry.btn_save_and_advance)
        self._lib.CRS.order_item_type.re_key_in_verification()
        self._lib.CRS.order_item_type.save_order_in_verification_entry()
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def return_to_verification_queue(self):
        """
            Pre-conditions: Verification Summary is opened
            Post-conditions: Order is returned to Verification Queue, Verification Queue is opened
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        # Click on the 'Return to Verification Queue' link
        self._lib.general_helper.scroll_and_click(
            self._pages.CRS.verification_summary.lnk_return_to_verification_queue)
        # Verify status in Verification Queue
        self.check_status_of_order_in_verification("In_Process_status")
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def save_order(self):
        """
          Pre-conditions: Verification Summary is opened
          Post-conditions: Order is saved, Verification Queue is opened
          """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        # Click on the 'Save Order' button
        self._lib.general_helper.scroll_and_click(self._pages.CRS.verification_summary.btn_save_order)
        # Fill reason and description
        self._lib.CRS.crs.fill_reason(
            self._pages.CRS.verification_summary.pup_send_order_to_admin_txt_reason)
        # Verify status in Verification Queue
        self.check_status_of_order_in_verification("Save_status")
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def send_back_to_capture(self, reason="test_reason", description="test_description"):
        """
          Pre-conditions: Verification Entry or Verification Summary page is opened
          Post-conditions: 'Send Back to Capture' form is submitted
          """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        # Click on the 'Send Order to Capture Queue' link
        if (self._lib.general_helper.check_if_element_exists(
                self._pages.CRS.verification_entry.lnk_send_order_to_capture_queue)):
            self._lib.general_helper.scroll_and_click(
                self._pages.CRS.verification_entry.lnk_send_order_to_capture_queue, timeout=60)
        else:
            self._lib.general_helper.scroll_and_click(
                self._pages.CRS.verification_summary.lnk_send_order_to_capture_queue, timeout=60)
        self._actions.wait_for_element_displayed(
            self._pages.CRS.verification_entry.pup_send_order_to_capture_txt_reason)
        # Fill reason and descriptions fields
        self._lib.general_helper.find_and_send_keys(
            self._pages.CRS.verification_entry.pup_send_order_to_capture_txt_reason, reason)
        self._lib.general_helper.find_and_send_keys(
            self._pages.CRS.verification_entry.pup_send_order_to_capture_txt_description, description)
        # Click on the 'Submit' button
        self._lib.general_helper.find_and_click(
            self._pages.CRS.verification_entry.pup_send_order_to_capture_lnk_submit)
        self._actions.wait_for_element_displayed(
            self._pages.CRS.verification_queue.btn_administrative)
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def send_to_admin(self):
        """
           Pre-conditions: Verification Summary is opened
           Post-conditions: Order is sent to admin, Verification Queue is opened
           """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        # Click on the 'Send to Administrator' link
        self._lib.general_helper.scroll_and_click(
            self._pages.CRS.verification_summary.lnk_send_to_administrator)
        # Fill Reason and Description fields
        self._lib.CRS.crs.fill_reason(
            self._pages.CRS.verification_summary.pup_send_order_to_admin_txt_reason)
        # Verify status in Verification Queue
        self.check_status_of_order_in_verification("Send_to_Admin_status")
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))
