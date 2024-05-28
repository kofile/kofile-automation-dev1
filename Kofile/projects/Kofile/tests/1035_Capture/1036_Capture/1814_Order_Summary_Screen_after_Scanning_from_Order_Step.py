"""Scan-first (e-file) flow"""

from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS, click on Add New Order button and fill order header
    Click the "Start Batch Scan" button
    Scan 2 rows and select 2 different order types 
    Save scanned documents and check Order Summary screen
    Click 'New Order Item' link and click new 'Start Batch Scan' icon -> Scan Documents screen is opened 
                            Scanned rows are displayed with selected OITs and with the ability change OIT
    Scan new row, select OIT and save -> Order summary screen is opened new OIT is added with pending status
    Click checkout button -> "OITs must be reviewed before proceeding" Warning message is shown for each 
                              not reviewed OIT
    Edit and save first oit, delete 2-nd and 3-rd oit
    Add a non e-file OIT with capture step (e.g. Default) and finalize order
    Navigate to Order Search -> order in Capture Queue
    From Capture scan image, map to non e-file doc and save
    Navigate to Order Search -> order in Indexing Queue"""

tags = ["48999_location_2"]


class test(TestParent):                                                                           # noqa

    def __init__(self, data):
        self.order_types = [data["OT_1"], data["OT_2"]]
        super(test, self).__init__(data, __name__)

    def __test__(self):

        # Add 'Scan First' OITs
        self.atom.CRS.order_queue.add_order_with_scan_first_flow(order_types=self.order_types)

        # Check OrderSummary page
        for i, ot in enumerate(self.order_types, 1):
            self.lib.CRS.order_summary.verify_type_by_row_index(ot, i)
            self.lib.CRS.order_summary.verify_status_by_row_index("Pending", i)
            self.lib.CRS.capture.click_on_the_document_row(i)
            self.lib.CRS.capture.verify_image_exist_in_image_viewer(i, mapped=True)

        links = [self.pages.CRS.order_summary.lnk_new_order_item,
                 self.pages.CRS.order_summary.lnk_return_to_scan_documents,
                 self.pages.CRS.order_summary.lnk_cancel_entire_order,
                 self.pages.CRS.order_summary.lnk_reject_entire_order,
                 self.pages.CRS.order_summary.lnk_return_to_order_queue,
                 self.pages.CRS.order_summary.lnk_send_to_admin]

        for link in links:
            self.lib.general_helper.find(link, wait_displayed=True, timeout=1)

        # Add one more e-file oit
        self.lib.CRS.order_summary.click_new_order_item_icon()
        self.lib.CRS.order_entry.click_start_batch_scan_button()
        for i, ot in enumerate(self.order_types, 1):
            order_type = self.lib.CRS.capture.get_order_type(i, mapped=True)
            assert ot == order_type, f"Expected order type: {ot} is not equal to actual: '{order_type}'"
        self.order_types.append(self.order_types[0])
        self.lib.CRS.capture.start_scan()
        self.lib.CRS.capture.select_order_type(self.order_types[2])
        self.lib.CRS.order_item_type.save_order_in_capture_step(e_file=True)
        self.lib.CRS.order_summary.verify_type_by_row_index(self.order_types[2], 3)
        self.lib.CRS.order_summary.verify_status_by_row_index("Pending", 3)
        self.lib.CRS.capture.verify_image_exist_in_image_viewer(3)

        # Click 'Checkout' and verify warning messages
        self.lib.general_helper.find_and_click(self.pages.CRS.order_summary.btn_checkout)
        self.lib.general_helper.wait_for_spinner()
        warnings = self.lib.general_helper.find_elements(self.pages.CRS.order_summary.txt_review_warning, get_text=True)
        for i, ot in enumerate(self.order_types, 0):
            exp_msg = f"{ot} order item must be reviewed before proceeding."
            assert exp_msg == warnings[i], f"Expected warning message: {exp_msg} is not equal " \
                                           f"to actual: '{warnings[i]}'"
        # Edit the 1-st oit
        self.lib.CRS.order_summary.click_edit_icon_by_row_index(1)
        self.lib.CRS.order_entry.wait_order_item_tab_displayed()
        self.lib.CRS.order_entry.save_entered_doc_type()
        self.lib.required_fields.crs_fill_required_fields()
        self.lib.CRS.order_entry.click_add_to_order()
        self.lib.CRS.order_summary.verify_status_by_row_index("Reviewed", 1)

        # Delete the 2-nd and 3-rd 'Pending' OITs
        self.lib.CRS.order_summary.click_delete_icon_by_row_index(3)
        self.lib.CRS.order_summary.click_delete_icon_by_row_index(2)

        # Add a non e-file oit
        self.lib.CRS.order_summary.click_new_order_item_icon()
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.one_oit_to_summary()
        for i in range(1, 3):
            self.lib.CRS.order_summary.verify_status_by_row_index("Reviewed", i)
            self.lib.CRS.capture.click_on_the_document_row(i)
            self.lib.CRS.capture.verify_image_exist_in_image_viewer(i, should_exist=False if i == 2 else True)

        self.atom.CRS.add_payment.finalize_order()
        self.atom.CRS.general.go_to_crs()

        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_status_capture()

        # Map the non e-file oit and save
        self.lib.CRS.order_item_type.start_batch_scan()
        self.atom.CRS.capture.capture_and_map(row_num=1, oit_num=2, exp_indexing=False)
        # wait for outer spinner
        self.lib.general_helper.wait_for_spinner()
        # wait for image viewer spinner
        self.lib.general_helper.wait_for_spinner()
        self.lib.CRS.order_item_type.save_order_in_capture_step()

        if self.data['async'] == '1':
            with self.lib.db as db:
                db.scheduler_job_update_for_export(scheduler_job_code="OrderItemContentExport")

        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_status_indexing()


if __name__ == '__main__':
    run_test(__file__)
