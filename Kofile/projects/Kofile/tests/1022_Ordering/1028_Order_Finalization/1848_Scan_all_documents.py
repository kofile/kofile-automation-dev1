"""79177 Scan all documents"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Test cases:
                 1. Finalize first order and save doc number
                 2. Finalize second order
                 3. Click on the 'Scan All Documents' link
                 4. Map document with doc number from first order (negative test)
                 5. Map document with current doc number (positive test)
                 6. Save order and navigate to 'Order Search' page
                 7. Find order and verify that  Queue is 'Indexing' 
               """

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __48000__(self):
        # 'Scan All Documents' link is configured for 'Plats' OIT (qa_dev) and for 'Real Property' OIT (qa_ref)
        self.data["OIT"] = "RP_Recordings"
        self.data["current_oit"] = "RP_Recordings"

    def __test__(self):
        """
        Pre-conditions: no
        Post-conditions: 'Order Search' page is opened. Captured order is found. Queue column is 'Indexing'
        """
        self.lib.data_helper.reload()
        self.lib.general_helper.check_order_type()
        # Create and Finalize first order
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        doc_num = self.data["doc_number"]
        self.lib.general_helper.find_and_click(self.pages.CRS.order_finalization.btn_order_queue)
        # Create and Finalize second order
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order,
                                                               open_crs=False)
        # Click on the 'Scan All Documents' link
        self.lib.general_helper.find_and_click(self.pages.CRS.order_finalization.lnk_scan_all_documents)
        # Start scan
        self.lib.CRS.capture.start_scan()
        self.lib.CRS.capture.click_edit_icon()
        self.lib.CRS.capture.add_doc_group_and_doc_type()
        # Add document number from first order
        self.lib.CRS.capture.add_doc_number(doc_number=doc_num)
        self.lib.CRS.capture.add_pages_count()
        self.lib.CRS.capture.click_edit_icon()
        # Verify validation message
        self.lib.CRS.capture.verify_confirm_pop_up_message(
            "Document does not belong to current order. Please fill document with the correct data.", confirm=False)
        self.lib.general_helper.find_and_click(self.pages.CRS.capture_summary.pup_confirm_btn_cancel)
        # Scan and map document with current document number
        self.atom.CRS.capture.capture_and_map(scan=False)
        self.lib.CRS.capture.open_image_in_image_viewer()
        # Save scanned document
        self.lib.general_helper.find_and_click(self.pages.CRS.capture_summary.btn_save_and_exit)
        self.lib.general_helper.wait_for_spinner()
        self.lib.general_helper.find(self.pages.CRS.order_finalization.btn_void_order, 90)
        self.lib.general_helper.find_and_click(self.pages.CRS.order_finalization.row_numbers, timeout=30, retries=3)
        self.lib.general_helper.wait_for_spinner()
        # Navigate to 'Order Search' page
        self.atom.CRS.order_search.search_order_by_order_number()
        # Verify that Queue is 'Indexing'
        self.lib.CRS.order_search.verify_order_status_indexing()


if __name__ == '__main__':
    run_test(__file__)
