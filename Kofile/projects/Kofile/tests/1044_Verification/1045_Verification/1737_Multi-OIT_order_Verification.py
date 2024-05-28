"""69868_Multi-OIT_order_Verification"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
                Steps:
                1. Process order with 2 OITs to Verification
                2. Open and save first OIT
              """

tags = ['48999_location_2']


class test(TestParent):                                                                             # noqa

    def __init__(self, data, oi_count=2):
        self.oi_count = oi_count
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: no
        Post-conditions: Second OIT with correct doc number in verification header is opened
        """
        # Create and finalize order with 2 OITs
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order, open_crs=True,
                                                               oi_count=self.oi_count)
        self.atom.CRS.general.go_to_crs()
        # Capture order
        self.lib.CRS.order_item_type.scan_and_map(self.oi_count)
        self.lib.CRS.order_item_type.save_order_in_capture_step()
        # Index first OIT
        self.lib.CRS.order_item_type.index_order()
        self.lib.general_helper.find_and_click(self.pages.CRS.indexing_entry.btn_save_and_advance)
        self.actions.wait_for_element_displayed(self.pages.CRS.indexing_entry.indexing_header)
        # Index second OIT
        self.lib.general_helper.find(
            self.pages.CRS.indexing_entry.btn_save_and_advance, wait_displayed=True)
        self.lib.required_fields.crs_fill_required_fields()
        self.lib.general_helper.find_and_click(self.pages.CRS.indexing_entry.btn_save_and_advance)
        self.actions.wait_for_element_displayed(self.pages.CRS.indexing_summary.btn_next_order)
        self.lib.CRS.order_item_type.next_order_in_index_summary()
        # Process first OIT in Verification
        self.lib.CRS.order_item_type.index_order(self.lib.CRS.crs.go_to_verification_queue)
        self.lib.CRS.order_item_type.re_key_in_verification()
        self.lib.general_helper.scroll_and_click(
            self.pages.CRS.verification_entry.btn_save_and_advance, timeout=60)
        # Wait for opening second OIT with correct doc number in verification header
        self.actions.wait_for_element_displayed(
            self.pages.CRS.verification_entry.verification_header)
        self.actions.wait_for_element_text_contains(
            self.pages.CRS.verification_entry.verification_header, self.data.get("doc_numbers")[1])


if __name__ == '__main__':
    run_test(__file__)
