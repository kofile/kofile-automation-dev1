from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS
    - Navigate to Capture Queue and Click on the "Historical Capture" tab
    - Scan image and click on the document row -> Image is available in image viewer
    - Map document to any historical capture doc group (use DB query to find historical doc groups)
    - Click "Save & Exit" button
    - Navigate to Indexing Queue and search order via doc number 
        -> Order is found. Order status is "Historical Documents". Running man edit button is available
    - Click on the Running man edit button
    - Fill all required fields and click "Save & Advance" button
    - Navigate to Verification Queue and search order via document number
        -> Order is found. Order status is "Historical Documents". Running man edit button is available
    - Click on the Running man edit button
    - Click "Save & Advance" button
    - Click on the "Next Order" button -> Order is moved to Archive
    - Check document in Clerk Search
        """

tags = ["48999_location_2"]


class test(TestParent):                                                                          # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.actions.store("historical", True)
        self.lib.data_helper.reload()

        # Get historical doc groups
        with self.lib.db as db:
            doc_group_id, doc_group, oit_name = db.get_historical_capture_doc_groups()[int(self.data["db_row_index"])]
        self.actions.store("doc_group", doc_group)

        self.atom.CRS.general.go_to_crs(2)
        self.actions.store('doc_types', [self.api.capture(self.data).get_doc_type(doc_group=doc_group)])

        # Scan and map historical document
        self.lib.CRS.order_item_type.scan_and_map()
        self.lib.CRS.order_item_type.save_order_in_capture_step()

        # Index order
        self.lib.CRS.order_item_type.index_order(verify_status_before="Historical")
        self.lib.CRS.order_item_type.save_order_in_index_entry()
        self.lib.CRS.order_item_type.next_order_in_index_summary()

        # Verify order
        self.lib.CRS.order_item_type.index_order(self.lib.CRS.crs.go_to_verification_queue,
                                                 verify_status_before="Historical")
        # self.lib.CRS.order_item_type.re_key_in_verification()
        self.lib.CRS.order_item_type.save_order_in_verification_entry()
        self.lib.general_helper.scroll_and_click(self.pages.CRS.verification_summary.btn_next_order)
        self.lib.general_helper.wait_for_spinner()

        # Update scheduler export job date in DB
        self.lib.db_with_vpn.scheduler_job_update_for_set_export_document(dept_id=self.data["dept_id"])
        self.atom.CS.general.go_to_cs(oit=self.data["CS_OIT"])

        # Search document in CS
        self.cs_api = self.api.clerc_search(self.data)
        cs_doc = self.cs_api.search_by_doc_number(
            doc_number=f"{self.data['doc_year']}-{self.data['doc_number']}")
        assert cs_doc["Filename"], "Document doesn't exist in Clerk Search!"


if __name__ == '__main__':
    run_test(__file__)
