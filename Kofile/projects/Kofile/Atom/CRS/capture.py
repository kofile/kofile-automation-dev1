from projects.Kofile.Lib.test_parent import AtomParent


class Capture(AtomParent):
    def __init__(self):
        super(Capture, self).__init__()

    def capture_and_map(self, row_num=1, oit_num=1, exp_indexing=True, scan=True, click_edit=True, scan_count=1,
                        to_row=1):
        """
            Pre-conditions: Capture Summary is displayed
            Post-conditions: Image is scanned and mapped to the order, expanded indexing if enabled,
                            Capture Summary is displayed
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        # Start scan
        for i in range(scan_count):
            if i == 1:
                self._lib.general_helper.find_and_click(
                    self._lib.general_helper.make_locator(self._pages.CRS.capture_summary.capture_table_row, to_row))
            self._lib.CRS.capture.start_scan() if scan else None
        # Map the doc
        self._lib.CRS.capture.click_edit_icon(row_num) if click_edit else None
        self._lib.CRS.capture.add_doc_group_and_doc_type(row_num, oit_num)
        self._lib.CRS.capture.add_doc_number(row_num, oit_num)
        self._lib.CRS.capture.add_pages_count(row_num)
        self._lib.CRS.capture.click_edit_icon(row_num)
        self._lib.CRS.capture.expanded_indexing() if exp_indexing else None

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def capture_and_map_pre_ml(self, row_num=1, oit_num=1):
        """
            Pre-conditions: Capture Summary is displayed
            Post-conditions: Image is scanned and mapped to the order, expanded indexing if enabled,
                            Capture Summary is displayed
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        # Start scan
        self._lib.CRS.capture.add_pre_ml()
        # Map the doc
        self._lib.CRS.capture.click_edit_icon(row_num)
        self._lib.CRS.capture.add_doc_group_and_doc_type(row_num, oit_num)
        self._lib.CRS.capture.add_doc_number(row_num, oit_num)
        self._lib.CRS.capture.click_edit_icon(row_num)
        self._lib.CRS.capture.expanded_indexing(False)

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def check_status_of_order_in_capture(self, status):
        """
        Pre-conditions: Capture Queue page is displayed
        Post-conditions: Capture Queue page is displayed, order status is checked
        """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        self._actions.wait_for_element_displayed(self._pages.CRS.general.lbl_order_count)
        self._lib.CRS.crs.click_all_show_all_action_links()
        self._actions.wait_for_element_displayed(self._pages.CRS.general.lbl_order_count)
        self._lib.CRS.capture.verify_order_status(status)
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def process_recapture_order(self):
        """
            Pre-conditions: Document sent to Re-Capture, order number saved to data['order_num']
            Post-conditions: Re-Capture order processed and sent to archive
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        # Go to Capture Queue
        self._lib.CRS.crs.go_to_capture_queue()
        # Process order
        self._lib.CRS.crs.click_running_man()
        # Wait loading page
        self._lib.general_helper.find(self._pages.CRS.capture_summary.btn_cancel_order)
        self._lib.general_helper.wait_for_spinner()
        # Click on Capture table row
        self._lib.general_helper.find_and_click(self._pages.CRS.capture_summary.capture_table_row_before)
        # Check status. Must be changed from 'Pending' to 'Reviewed'
        self._lib.general_helper.find(self._pages.CRS.capture_summary.capture_table_row_after)
        # Fill required fields if needed
        self._lib.required_fields.crs_required_fields(self._pages.CRS.capture_summary.REQ_LOCATOR_FIELD)
        # Click 'Save and exit'
        self._lib.general_helper.scroll_and_click(self._pages.CRS.capture_summary.btn_save_and_exit)
        self._lib.general_helper.wait_for_spinner()
        # Wait loading page
        self._lib.general_helper.find(self._pages.CRS.capture_queue.btn_start_batch_scan, 90)
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def process_reprocess_order(self):
        """
            Pre-conditions: Document is sent back to Capture Queue. Order status is 'Reprocess'
            Post-conditions: 'Reprocess' order is processed to the next step
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        # Go to Capture Queue
        self._lib.CRS.crs.go_to_capture_queue()
        # Verify that order status is 'Reprocess'
        self.check_status_of_order_in_capture("Reprocess_status")
        # Process order
        self._lib.CRS.crs.click_running_man()
        # Wait loading page
        self._lib.general_helper.find(self._pages.CRS.capture_summary.btn_cancel_order)
        self._lib.general_helper.wait_for_spinner()
        # Click 'Save and exit'
        self._lib.general_helper.scroll_and_click(self._pages.CRS.capture_summary.btn_save_and_exit)
        self._actions.wait_for_element_displayed(self._pages.CRS.capture_summary.pup_confirm_btn_ok)
        # Click 'Ok' button in popup
        self._actions.click(self._pages.CRS.capture_summary.pup_confirm_btn_ok)
        self._lib.general_helper.wait_for_spinner()
        # Wait loading page
        self._lib.general_helper.find(self._pages.CRS.capture_queue.btn_start_batch_scan, 90)
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def upload_image(self):
        """
            Pre-conditions: Capture Queue is opened
            Post-conditions: Image is uploaded from Auto_Plats folder, Capture Queue is displayed
            """
        data = self._lib.general_helper.get_data()
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        upload_folder = data['config'].test_data(f"{data.OIT}.capture.upload_image.folder")
        # show all orders
        self._lib.CRS.crs.click_all_show_all_action_links()
        # click upload button
        btn_upload = self._pages.CRS.capture_queue.upload_image_icon_by_order_number(data["order_number"])
        self._lib.general_helper.wait_for_element_clickable(btn_upload)
        self._lib.general_helper.scroll_and_click(btn_upload)
        # wait until Choose image popup is displayed
        self._lib.general_helper.find(self._pages.CRS.capture_queue.pup_upload_btn_upload, wait_displayed=True)
        # verify that doc_group_doc_number ddl exists
        self._actions.verify_element_displayed(
            self._lib.general_helper.make_locator(
                self._pages.CRS.capture_queue.pup_ddl_doc_group_doc_number, data.get("doc_number")))
        # upload folder locator
        self._lib.general_helper.scroll_and_click(
            self._lib.general_helper.make_locator(self._pages.CRS.capture_queue.pup_upload_lbl_subfolder_by_name,
                                                  upload_folder))
        self._actions.wait(0.5)
        # first file in sub folder
        first_file = self._lib.general_helper.make_locator(
            self._pages.CRS.capture_queue.pup_upload_lbl_file_by_subfolder_name_by_index, upload_folder, 1)
        is_file_count_more_then_one = self._lib.general_helper.find(self._lib.general_helper.make_locator(
            self._pages.CRS.capture_queue.pup_upload_lbl_file_by_subfolder_name_by_index, upload_folder, 2),
                                                                    should_exist=False, timeout=3)
        self._actions.mouse_over(first_file)
        self._lib.general_helper.scroll_and_click(first_file)
        self._lib.general_helper.wait_for_spinner()
        self._lib.general_helper.wait_for_element_clickable(self._pages.CRS.capture_queue.pup_upload_lnk_reset)
        # Click on the 'Reset' action link
        self._lib.general_helper.find_and_click(self._pages.CRS.capture_queue.pup_upload_lnk_reset)
        self._lib.general_helper.wait_for_spinner()
        self._actions.wait_for_element_present(
            self._lib.general_helper.make_locator(self._pages.CRS.capture_queue.pup_upload_lbl_subfolder_by_name,
                                                  upload_folder))
        if not is_file_count_more_then_one:
            self._lib.general_helper.scroll_and_click(
                self._lib.general_helper.make_locator(self._pages.CRS.capture_queue.pup_upload_lbl_subfolder_by_name,
                                                      upload_folder))
            self._actions.wait(0.5)
        # first file in sub folder
        self._actions.mouse_over(first_file)
        self._lib.general_helper.scroll_and_click(first_file)
        self._lib.general_helper.wait_for_spinner()
        # Click on the 'Return Current Page To Folder action link' action link
        self._lib.general_helper.find_and_click(
            self._pages.CRS.capture_queue.pup_upload_lnk_return_current_page_to_folder)
        self._lib.general_helper.wait_for_spinner()
        if not is_file_count_more_then_one:
            self._lib.general_helper.scroll_and_click(
                self._lib.general_helper.make_locator(self._pages.CRS.capture_queue.pup_upload_lbl_subfolder_by_name,
                                                      upload_folder))
            self._actions.wait(0.5)
        # first file in sub folder
        self._actions.mouse_over(first_file)
        self._lib.general_helper.scroll_and_click(first_file)
        self._lib.general_helper.wait_for_spinner()
        # wait for upload button to be displayed
        self._lib.general_helper.wait_for_element_clickable(self._pages.CRS.capture_queue.pup_upload_btn_upload)
        self._lib.general_helper.scroll_and_click(self._pages.CRS.capture_queue.pup_upload_btn_upload)
        # wait for upload button to be deleted from dom
        self._lib.general_helper.wait_for_spinner(spinner_out=30)
        self._actions.wait_for_element_not_present(self._pages.CRS.capture_queue.pup_upload_btn_upload, timeout=45)
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))
