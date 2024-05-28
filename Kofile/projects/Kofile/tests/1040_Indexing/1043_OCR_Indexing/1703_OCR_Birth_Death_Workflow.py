"""Test - OCR Birth Workflow"""
from projects.Kofile.Lib.test_parent import TestParent
from datetime import datetime
from runner import run_test

description = """Create OCR orders, find the last submitted OCR order, process to Archive and find in Clerk Search"""

tags = ["48999_location_2"]


class test(TestParent):                                                                                 # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: OCR order is created, processed and found in Clerk Search
        """
        oit = str(self.data["OIT"]).lower()
        test_config = self.lib.data_helper.test_config(oit=self.data.get("OIT"))
        dept_id = test_config.get("dept_id")
        doc_number = str(datetime.now().timestamp())[:-7]  # unique number
        # create a Birth/Death OCR order
        self.atom.CRS.indexing.OCR_Image_Upload(birth_count=1 if "birth" in oit else 0,
                                                death_count=1 if "death" in oit else 0)
        # wait for OCR service to create the order and get the last submitted OCR order number from DB
        self.actions.wait(20)
        self.data["order_number"] = self.lib.db_with_vpn.get_last_ocr_number_by_host_ip()
        self.actions.step(f"OCR order number is {self.data['order_number']}")
        # find the OCR order in Indexing and process
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.crs.go_to_indexing_queue()
        self.atom.CRS.order_queue.assign_order()
        self.lib.CRS.crs.click_running_man()
        self.lib.required_fields.crs_fill_required_fields()
        self.lib.CRS.indexing_entry.fill_doc_number(doc_number)
        self.lib.CRS.indexing_entry.fill_recorded_date()
        self.lib.CRS.indexing_entry.click_birth_death_record_save_button()
        self.lib.CRS.indexing_summary.click_next_order_button()
        # if death order, process through Verification
        if self.data['config'].test_data(f"{self.data.OIT}.verification.step"):
            self.lib.CRS.crs.go_to_verification_queue()
            self.atom.CRS.order_queue.assign_order()
            self.lib.CRS.crs.click_running_man()
            self.lib.required_fields.crs_fill_required_fields()
            self.lib.CRS.verification_entry.click_save_and_advance_button()
            self.lib.CRS.verification_summary.click_next_order_button()
        # convert the doc number for CS
        now = datetime.now()
        doc_number_full = f"{now.year}-{doc_number}"
        # export docs to CS and search the OCR doc by doc number
        self.lib.db_with_vpn.scheduler_job_update_for_set_export_document(dept_id=dept_id)
        self.atom.CS.general.go_to_cs()
        self.api.clerc_search(self.data).search_by_doc_number(doc_number=doc_number_full)


if __name__ == '__main__':
    run_test(__file__)
