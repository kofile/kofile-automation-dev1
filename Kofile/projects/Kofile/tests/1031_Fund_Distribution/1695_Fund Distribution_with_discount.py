"""smoke test"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
1.Create Order
2.Apply RA discount
3.Finalize order
4.Edit order after finalization
5.Open Fee Fund distribution popup. 
6.Check Fee Fund Distribution names and values
7.Close Popup and Save Order"""

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
        # Create OIT
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        # Apply discount RA
        self.lib.CRS.order_summary.apply_discount(discount_type="RA", comment="test-comment-1")
        # Checkout Order
        self.actions.click(self.pages.CRS.order_summary.btn_checkout)
        self.atom.CRS.add_payment.add_payments()
        self.lib.CRS.add_payment.click_add_payment_checkout_button()
        self.actions.wait_for_element_displayed(self.pages.CRS.order_finalization.lbl_order_finalize_label)
        # Edit Order After Finalization
        self.lib.CRS.order_finalization.click_edit_order()
        self.lib.general_helper.scroll_and_click(self.pages.CRS.order_entry.lnk_fund_distribution)
        self.actions.wait_for_element_displayed(self.pages.CRS.order_entry.btn_submit_distribution_popup)
        self.lib.CRS.order_entry.verify_fund_distribution(discount=True)
        # Close Popup after verification
        self.actions.click(self.pages.CRS.order_entry.btn_submit_distribution_popup)
        self.actions.click(self.pages.CRS.order_entry.btn_add_to_order)
        self.lib.general_helper.wait_for_spinner()


if __name__ == '__main__':
    run_test(__file__)
