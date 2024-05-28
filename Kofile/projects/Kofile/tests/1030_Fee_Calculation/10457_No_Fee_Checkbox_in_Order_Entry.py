from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """1. Open order from preconditions
2. Click on the "No Fee" checkbox
3. Save order
4. Click on the "Checkout" button
5. Click on the "edit"(pencil) button
6. Save order and void"""

tags = ["48999_location_2"]


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.general_helper.check_order_type()
        self.atom.CRS.order_queue.fill_order_entry_tabs()
        self.actions.wait_for_element_displayed(self.pages.CRS.order_entry.no_fee_cb)
        self.actions.assert_element_not_checked(self.pages.CRS.order_entry.no_fee_cb)
        self.actions.assert_element_text_is_not(self.pages.CRS.order_entry.txt_total_amount, self.names.zero_price)
        self.lib.general_helper.find_and_click(self.pages.CRS.order_entry.no_fee_cb)
        self.actions.assert_element_checked(self.pages.CRS.order_entry.no_fee_cb)
        self.actions.wait_for_element_text(self.pages.CRS.order_entry.txt_total_amount, self.names.zero_price)
        for fee in self.lib.general_helper.find_elements(self.pages.CRS.order_entry.lbl_all_fee_amounts):
            if fee.text.strip():
                assert fee.text.strip() == self.names.zero_price, \
                    f"fee price is: {fee.text.strip()}, but must be: {self.names.zero_price}"

        self.lib.CRS.order_entry.click_add_to_order()
        self.lib.general_helper.wait_for_spinner()

        self.actions.wait_for_element_text(
            self.pages.CRS.order_summary.lbl_total_price, self.names.zero_price.strip("$"))
        self.lib.general_helper.scroll_and_click(self.pages.CRS.order_summary.btn_checkout)
        self.lib.general_helper.wait_for_spinner()
        self.actions.wait_for_window_present_by_partial_url("/Order/ShowOrderFinalization")
        self.actions.wait_for_element_text(
            self.pages.CRS.order_summary.lbl_total_price, self.names.zero_price.strip("$"))
        self.actions.assert_element_displayed(self.pages.CRS.order_finalization.lnk_edit_order_payments)

        self.lib.CRS.order_finalization.click_edit_order()
        self.actions.wait_for_element_displayed(self.pages.CRS.order_entry.no_fee_cb)
        self.actions.wait_for_element_text(self.pages.CRS.order_entry.txt_total_amount, self.names.zero_price)
        self.actions.assert_element_checked(self.pages.CRS.order_entry.no_fee_cb)
        self.actions.assert_element_not_present(self.pages.CRS.order_finalization.lnk_view_edit_order_item_funds)


if __name__ == '__main__':
    run_test(__file__)
