"""smoke test"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
1.Create and finalize order
2.Edit Order after finalization
3.Check Fee Fund Distribution names and values
4.Close Popup after checking
5.Save Order
6.Click Void button
7.Compare fee distribution on popup
8.Click Cancel on popup"""

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: no
        Post-conditions: Order is processed from Order Queue to Finalization
        """
        self.lib.general_helper.check_order_type()
        # Finalize Order
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        # Edit Order and check fee fund distribution
        self.lib.CRS.order_finalization.click_edit_order()
        self.lib.general_helper.scroll_and_click(self.pages.CRS.order_entry.lnk_fund_distribution)
        self.actions.wait_for_element_displayed(self.pages.CRS.order_entry.btn_submit_distribution_popup)
        # Check fee fund distribution
        self.lib.CRS.order_entry.verify_fund_distribution()
        # Close Popup after verification
        self.actions.click(self.pages.CRS.order_entry.btn_submit_distribution_popup)
        self.actions.click(self.pages.CRS.order_entry.btn_add_to_order)
        self.lib.general_helper.wait_for_spinner()
        # Click void button
        self.actions.click(self.pages.CRS.order_finalization.btn_void_order)
        self.actions.wait_for_element_displayed(self.pages.CRS.void_order_summary.pup_fee_desc_btn_submit)
        # Check fee fund distribution on void popup
        self.lib.CRS.order_entry.verify_fund_distribution(void=True)
        self.actions.click(self.pages.CRS.void_order_summary.pup_fee_desc_btn_close)


if __name__ == '__main__':
    run_test(__file__)
