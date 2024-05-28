from datetime import datetime
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS, create new order -> process and finalize order, remember doc number
    -> Connect to DB und update SCHEDULE_JOB table to run document export scheduler for OIT within 1 second
    -> check document in CS
    -> back to CRS -> search document -> edit and VOID order
    -> Connect to DB und update SCHEDULE_JOB table to run document export scheduler for OIT within 1 second
    -> check document in CS (Document type should be changed to voided)
        """

tags = ['48999_location_2']


class test(TestParent):                                                                                    # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__, precondition=self._precondition)

    def __test__(self):
        start_from_capture = self.data["config"].test_data(f"{self.data.OIT}.capture.start_from_capture.value")
        verification_step = self.data["config"].test_data(f"{self.data.OIT}.verification.step")
        self.lib.data_helper.test_config()
        dept_id = self.data["test_config"]["dept_id"]

        def verify_order():
            # Verify order
            self.lib.CRS.crs.go_to_verification_queue()
            self.lib.CRS.crs.click_all_show_all_action_links()
            if not self.data.get("order_number"):
                self.data["order_number"] = self.lib.general_helper.find(
                    self.pages.CRS.general.order_number_by_doc_number(
                        self.data['doc_number']), get_text=True)
            # Assign the order
            self.atom.CRS.order_queue.assign_order()
            # Click running man
            self.lib.CRS.crs.click_running_man()
            # Fill required fields
            self.lib.general_helper.find(self.pages.CRS.verification_entry.btn_save_and_advance)
            self.lib.required_fields.crs_fill_required_fields()
            # Save
            self.lib.general_helper.scroll_and_click(self.pages.CRS.verification_entry.btn_save_and_advance)
            # Next order
            self.lib.general_helper.scroll_and_click(self.pages.CRS.verification_summary.btn_next_order)
            # Back to Queue
            self.lib.CRS.crs.go_to_verification_queue()

        # Go to CRS
        if start_from_capture:
            now = datetime.now()
            # Generate doc number
            self.data["doc_number"] = now.strftime("%m%d%H%M%S")
            doc_number = f"{now.year}-{self.data['doc_number']}"
            self.atom.CRS.general.go_to_crs()
            self.lib.CRS.order_item_type.scan_and_map()
            self.lib.CRS.order_item_type.save_order_in_capture_step()
            if verification_step:
                verify_order()
        else:
            # Add new order and process it
            self.atom.CS.api_helper.create_order()
            self.data["doc_number"] = self.data["doc_num"]
            doc_number = f"{datetime.now().year}-{self.data['doc_number']}"
        # Finalize in Capture
        if self.data["OIT"] == "Marriage_License":
            self.atom.CS.api_helper.capture_document()

        # Update scheduler export job date in DB
        self.lib.db_with_vpn.scheduler_job_update_for_set_export_document(dept_id=dept_id)

        cs_api = self.api.clerc_search(self.data)
        # Search document in CS
        cs_api.search_by_doc_number(doc_number=doc_number, retries=5, wait=5)

        if start_from_capture:
            # Finish test if OIT created from the Capture step
            return

        # Go to CRS
        self.atom.CRS.general.go_to_crs()
        # Search order
        self.atom.CRS.order_search.search_order_by_doc_number()
        if self.data["order_number"]:
            self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
        else:
            self.logging.warning('data["order_number"] is empty')
        # Edit found order
        if not self.lib.general_helper.find_and_click(self.pages.CRS.order_search.results_edit_column,
                                                      should_exist=False):
            self.lib.general_helper.find_and_click(self.pages.CRS.order_search.results_edit_column2,
                                                   timeout=5)  # Redaction Request OIT
        try:
            # Confirm edit order if confirmation pop-up appears
            self.lib.general_helper.find_and_click(self.pages.CRS.order_search.pup_in_workflow_btn_yes,
                                                   should_exist=False, timeout=3)
        except Exception as err:
            self.logging.warning(err)
        # Void order
        self.atom.CRS.order_finalization.void_order()
        # Update scheduler export job date in DB
        self.lib.db_with_vpn.scheduler_job_update_for_set_export_document(dept_id=dept_id)
        # Search document in CS and check doc type
        self.actions.step(f"* * * Wait until document type will be updated to 'VOID' * * *")
        cs_api.search_by_doc_number(doc_number=doc_number, retries=5, wait=5, check_doctype="VOID")


    def _precondition(self):
        self.atom.CS.api_helper.initialize_drawer()


if __name__ == '__main__':
    run_test(__file__)
