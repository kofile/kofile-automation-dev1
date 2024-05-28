"""smoke test"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
 1. Create and finalize order
 2. Edit order after finalization
 3. Change Fee Fund Distribution
 4. Save Order
 5. Edit Order one more time
 6. Verify Fee Fund changes are saved """

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
        # Adjust Fee Fund Values
        # This wait is necessary for qa1 48999
        self.actions.wait(15)
        changed_fee_fund = self.lib.CRS.order_entry.change_fee_fund_distribution()
        # Close Fund Distribution Popup
        self.actions.click(self.pages.CRS.order_entry.btn_submit_distribution_popup)
        # Save Order
        self.lib.required_fields.crs_fill_required_fields()
        # This elem is necessary for sending fund changes to backend
        self.actions.wait_for_element_present((
            "xpath", "//input[@name='feeDistribution']", "Elem that contains Fund Distribution changes"), timeout=10)
        self.actions.click(self.pages.CRS.order_entry.btn_add_to_order)
        self.lib.general_helper.wait_for_spinner()
        # Edit Order after saving
        self.lib.CRS.order_finalization.click_edit_order()
        self.lib.general_helper.scroll_and_click(self.pages.CRS.order_entry.lnk_fund_distribution)
        fee_fund_values_el = self.lib.general_helper.find_elements(self.pages.CRS.order_entry.lbl_fund_value)
        for i in range(len(fee_fund_values_el)):
            assert float(self.actions.get_element_text(
                fee_fund_values_el[i]).split('$')[1]
                         ) == changed_fee_fund[i], " Fee Fund value is incorrect after adjustment"
        self.actions.click(self.pages.CRS.order_entry.btn_add_to_order)
        self.lib.general_helper.wait_for_spinner()


if __name__ == '__main__':
    run_test(__file__)
