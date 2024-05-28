from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test
from random import choice, random as r

description = """Test steps:
                 1. Navigate to CRS, add new order with 2 Plat OITs and finalize
                 2. Navigate to Capture Queue
                 3. Search order via order number
                 4. Click on the Upload button
                 5. Click on Document group - Document number DDL
                 6. Select one of the OITs
                 7. Fill only one of 'Recorded Year' or 'Document Number' fields and click Search
                 8. Enter invalid data both in 'Recorded Year' and 'Document Number' fields and click search
                 9. Enter valid data both in Recorded Year' and 'Document Number' fields and click search
                 10. Click on Reset action link
                 11. Enter again valid data both in Recorded Year' and 'Document Number' fields and click search
                 12. Click on Return Current Page To Folder action link
                 13. Enter again valid data both in Recorded Year' and 'Document Number' fields and click search
                 14. Click on Next Page, First Page, Prior Page, Last Page navigation buttons
                 15. Click on Undo Upload Image icon
                 16. Enter again valid data both in Recorded Year' and 'Document Number' fields and click search
                 17. Click on Upload button
                 18. Click on the Upload button again, and open Document group - Document number DDL
                 19. Enter again valid data both in Recorded Year' and 'Document Number' fields and click search
                 20. Click on Upload button
              """

tags = []                                  # tag is removed to skip the test until 93496 bug is fixed


class test(TestParent):                                                                               # noqa
    def __init__(self, data):
        self.docs = []
        super(test, self).__init__(data, __name__, precondition=self._precondition)

    def __test__(self):
        # Navigate to CRS, add new order with 2 Plat OITs and finalize
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order, oi_count=2)
        # Get the Document and Order Numbers
        doc_num = self.data["doc_numbers"]
        order_num = self.data["order_number"]
        # Navigate to Capture Queue
        self.lib.CRS.crs.go_to_capture_queue()
        self.lib.CRS.crs.click_all_show_all_action_links()
        # Check order status
        self.lib.CRS.capture.verify_order_status('Pending_status')
        # Click on the Upload button
        self.lib.general_helper.find_and_click(
            self.pages.CRS.capture_queue.upload_image_icon_by_order_number(self.data["order_number"]))
        # Click on Document group - Document number DDL
        self.actions.click(self.pages.CRS.capture_queue.pup_upload_lbl_order_item_id)
        doc_in_ddl = self.lib.general_helper.find_elements(
            self.pages.CRS.capture_queue.pup_upload_ddl_order_item_value, get_text=True)
        for actual in doc_in_ddl:
            expected = f"Plats - {doc_num[doc_in_ddl.index(actual)]}"
            assert expected == actual, f"Expected str: {expected} is NOT equal to actual: {actual}"
        # Select one of the OITs
        self.actions.click(
            self.lib.general_helper.find_elements(self.pages.CRS.capture_queue.pup_upload_ddl_order_item_value)[-1])
        act_selected_oi = self.actions.get_element_text(self.pages.CRS.capture_queue.pup_upload_lbl_order_item_id)
        exp_selected_oi = f"Plats - {doc_num[-1]}"
        assert exp_selected_oi == act_selected_oi, f"Expected OI in the DDL: {exp_selected_oi} " \
                                                   f"is NOT equal to actual: {act_selected_oi}"
        # Fill only one of the 'Recorded Year' or 'Document Number' fields and click Search
        current_doc = choice(self.docs)
        self.docs.remove(current_doc)
        self._search_img_by_rec_year_and_doc_num(rec_year=current_doc.get('RecordedDate').split('/')[-1])
        self._check_warning_msg('Recorded Year and Document Number are required fields')
        # Enter invalid data both in 'Recorded Year' and 'Document Number' fields and click search
        self._search_img_by_rec_year_and_doc_num(current_doc.get('RecordedDate').split('/')[-1], int(r() * 1000))
        self._check_warning_msg('No matches found')
        # Enter valid data both in Recorded Year' and 'Document Number' fields and click search
        self._search_img_by_rec_year_and_doc_num(current_doc.get('RecordedDate').split('/')[-1],
                                                 current_doc.get('Number').split('-')[-1])
        self.actions.wait_for_element_displayed(self.pages.CRS.capture_queue.pup_upload_img)
        # Click on Reset action link
        self.actions.click(self.pages.CRS.capture_queue.pup_upload_lnk_reset)
        self.lib.general_helper.wait_for_spinner()
        self.actions.assert_element_not_present(self.pages.CRS.capture_queue.pup_upload_img)
        self.actions.assert_element_value(self.pages.CRS.capture_queue.pup_upload_txt_recorded_year, "")
        self.actions.assert_element_value(self.pages.CRS.capture_queue.pup_upload_txt_document_number, "")
        # Enter again valid data both in Recorded Year' and 'Document Number' fields and click search
        self._search_img_by_rec_year_and_doc_num(current_doc.get('RecordedDate').split('/')[-1],
                                                 current_doc.get('Number').split('-')[-1])
        self.actions.wait_for_element_displayed(self.pages.CRS.capture_queue.pup_upload_img)
        # Click on Return Current Page To Folder action link
        self.actions.click(self.pages.CRS.capture_queue.pup_upload_lnk_return_current_page_to_folder)
        self.lib.general_helper.wait_for_spinner()
        self.actions.assert_element_not_present(self.pages.CRS.capture_queue.pup_upload_img)
        # Enter again valid data both in Recorded Year' and 'Document Number' fields and click search
        self._search_img_by_rec_year_and_doc_num(current_doc.get('RecordedDate').split('/')[-1],
                                                 current_doc.get('Number').split('-')[-1])
        self.actions.wait_for_element_displayed(self.pages.CRS.capture_queue.pup_upload_img)
        # Click on Next Page, First Page, Prior Page, Last Page navigation buttons
        self._check_image_viewer_page_navigation(self.pages.CRS.capture_queue.pup_upload_btn_next_page)
        self._check_image_viewer_page_navigation(self.pages.CRS.capture_queue.pup_upload_btn_previous_page)
        self._check_image_viewer_page_navigation(self.pages.CRS.capture_queue.pup_upload_btn_last_page)
        self._check_image_viewer_page_navigation(self.pages.CRS.capture_queue.pup_upload_btn_first_page)
        # Click on Undo Upload Image icon
        self.actions.click(self.pages.CRS.capture_queue.pup_upload_btn_undo_upload)
        self.lib.general_helper.wait_for_spinner()
        self.actions.assert_element_not_present(self.pages.CRS.capture_queue.pup_upload_img)
        # Enter again valid data both in Recorded Year' and 'Document Number' fields and click search
        self._search_img_by_rec_year_and_doc_num(current_doc.get('RecordedDate').split('/')[-1],
                                                 current_doc.get('Number').split('-')[-1])
        self.actions.wait_for_element_displayed(self.pages.CRS.capture_queue.pup_upload_img)
        # Click on Upload button
        self.actions.click(self.pages.CRS.capture_queue.pup_upload_btn_upload)
        self.lib.general_helper.wait_for_spinner()
        assert self.lib.general_helper.wait_until(
            self._check_wf_step_and_dmc_path, 30, 2, act_selected_oi
        ), f"The current OI {act_selected_oi} is still in the 2nd workflow step or has no image path."
        # Again click on the Upload button, and open Document group - Document number DDL
        self.lib.general_helper.wait_for_spinner()
        self.lib.general_helper.find_and_click(
            self.pages.CRS.capture_queue.upload_image_icon_by_order_number(self.data["order_number"]))
        act_selected_oi = self.actions.get_element_text(self.pages.CRS.capture_queue.pup_upload_lbl_order_item_id)
        exp_selected_oi = f"Plats - {doc_num[0]}"
        assert exp_selected_oi == act_selected_oi, f"Expected OI in the DDL: {exp_selected_oi} " \
                                                   f"is NOT equal to actual: {act_selected_oi}"
        # Enter again valid data both in Recorded Year' and 'Document Number' fields and click search
        current_doc = choice(self.docs)
        self.docs.remove(current_doc)
        self._search_img_by_rec_year_and_doc_num(current_doc.get('RecordedDate').split('/')[-1],
                                                 current_doc.get('Number').split('-')[-1])
        self.actions.wait_for_element_displayed(self.pages.CRS.capture_queue.pup_upload_img)
        # Click on Upload button
        self.actions.click(self.pages.CRS.capture_queue.pup_upload_btn_upload)
        self.lib.general_helper.wait_for_spinner()
        assert self.lib.general_helper.wait_until(
            self._check_wf_step_and_dmc_path, 30, 2, act_selected_oi
        ), f"The current OI {act_selected_oi} is still in the 2nd workflow step or has no image path."
        with self.lib.db as db:
            assert db.get_order_workflow_step(
                order_num) > 2, f"The current order {order_num} is still in the capture workflow step."

    def _precondition(self):
        self.cs_api = self.api.clerc_search(self.data)
        page_num = 1
        while len(self.docs) < 2:
            docs_data = self.cs_api.document_search(page_num=page_num, search_text='2023')[
                'ResultSet']
            not_in_workflow_docs = self.cs_api.get_documents_extra_info(
                {i['Number']: {i['Id']: i['Filename']} for i in docs_data})
            docs = [{"Number": i['Number'], 'RecordedDate': i['RecordedDateText']} for i in docs_data if
                    i['Number'] in not_in_workflow_docs
                    and i['DocType'] == self.cs_api.test_config.get('doc_type_in_cs')
                    and i['NumOfPages'] and int(i['NumOfPages']) > 1]
            self.docs = self.docs + docs
            page_num += 1
            if page_num > 20:
                raise Exception(
                    f"No documents were found using "
                    f"{self.cs_api.test_config.get('dept')} department "
                    f"and {self.cs_api.test_config.get('doc_group')} document group")

    def _check_warning_msg(self, exp_warning):
        self.actions.wait_for_element_displayed(self.pages.CRS.capture_queue.pup_upload_lbl_no_matches_found)
        act_warning = self.actions.get_element_text(self.pages.CRS.capture_queue.pup_upload_lbl_no_matches_found)
        assert exp_warning == act_warning, f"Expected warning msg: {exp_warning} is NOT equal to actual: {act_warning}"
        self.actions.wait_for_element_not_displayed(self.pages.CRS.capture_queue.pup_upload_lbl_no_matches_found)

    def _check_image_viewer_page_navigation(self, button_locator):
        prev_img_lnk = self.actions.get_element_attribute(self.pages.CRS.capture_queue.pup_upload_img, "src")
        self.actions.click(button_locator)
        self.lib.general_helper.wait_for_spinner()
        self.actions.wait(2)
        act_img_lnk = self.actions.get_element_attribute(self.pages.CRS.capture_queue.pup_upload_img, "src")
        assert act_img_lnk != prev_img_lnk, f"Actual image link: {act_img_lnk} is equal to previous: {prev_img_lnk}"

    def _search_img_by_rec_year_and_doc_num(self, rec_year=None, doc_num=None):
        if rec_year:
            self.actions.clear(self.pages.CRS.capture_queue.pup_upload_txt_recorded_year)
            self.actions.send_keys(self.pages.CRS.capture_queue.pup_upload_txt_recorded_year, rec_year)
        if doc_num:
            self.actions.clear(self.pages.CRS.capture_queue.pup_upload_txt_document_number)
            self.actions.send_keys(self.pages.CRS.capture_queue.pup_upload_txt_document_number, doc_num)
        self.actions.click(self.pages.CRS.capture_queue.pup_upload_btn_search)
        self.lib.general_helper.wait_for_spinner()

    def _check_wf_step_and_dmc_path(self, act_selected_oi):
        with self.lib.db as db:
            step_id, path = db.get_oi_workflow_step_and_dmc_path(act_selected_oi.split('- ')[-1])
        return step_id > 2 and path


if __name__ == '__main__':
    run_test(__file__)
