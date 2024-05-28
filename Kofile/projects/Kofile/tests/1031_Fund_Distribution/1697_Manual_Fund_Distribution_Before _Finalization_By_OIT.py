"""smoke test"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
1.Add Governmental OIT with Fee
2.Fill all required fields and click Add to Order
3.On opened popup select OIT from csv config file (with 1 Fund)
4.Verify OIT total amount is equal to fund total amount
5.Save Order ad Finalize
6.Edit Order
7.Open Fee Distribution Link
8.Check Submit button is disabled until fund value is inserted
9.Insert the same fund value
10.Click Submit button"""

tags = ['']


# currently can run on QA48000

class test(TestParent):  # noqa
    cursor = 'default'

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __48999__(self):
        self.cursor = 'pointer'

    def __test__(self):
        """
        Pre-conditions: no
        Post-conditions: Order is processed from Order Queue to Finalization
        """
        self.lib.general_helper.check_order_type()
        self.atom.CRS.order_queue.fill_order_entry_tabs()
        # Finalize Order
        self.actions.send_keys(self.pages.CRS.order_entry.inp_amount, int(
            self.lib.general_helper.random_string(2, 1)))
        self.lib.required_fields.crs_fill_required_fields()
        oit_fee = self.actions.get_element_text(self.pages.CRS.order_entry.txt_total_amount)
        self.lib.general_helper.scroll_and_click(self.pages.CRS.order_entry.btn_add_to_order)
        self.actions.wait_for_element_displayed(self.pages.CRS.order_entry.ddl_gov_fee_distribution_copy_from)
        self.lib.general_helper.wait_for_spinner()
        self.actions.click(self.pages.CRS.order_entry.ddl_gov_fee_distribution_copy_from)
        self.actions.select_option_by_text(self.pages.CRS.order_entry.ddl_gov_fee_distribution_copy_from,
                                           self.data.copyFrom)
        self.lib.general_helper.wait_for_spinner()
        # Get fee fund name and total amount
        fee_fund_name = self.actions.get_element_text(
            self.pages.CRS.order_entry.lbl_gov_fee_distribution_fee_fund_name)
        fee_fund_total = self.actions.get_element_text(
            self.pages.CRS.order_entry.lbl_gov_fee_distribution_fee_total_amount)
        # Check total fund distribution is equal to OIT total amount
        assert fee_fund_total == oit_fee
        self.actions.click(self.pages.CRS.order_entry.btn_gov_fee_distribution_submit)
        self.lib.general_helper.wait_for_spinner()
        self.actions.wait(2)
        self.actions.click(self.pages.CRS.order_summary.btn_checkout)
        self.atom.CRS.add_payment.add_payments()
        self.lib.CRS.add_payment.click_add_payment_checkout_button()
        self.actions.wait_for_element_displayed(self.pages.CRS.order_finalization.lbl_order_finalize_label)
        # Edit Order After Finalization
        self.lib.CRS.order_finalization.click_edit_order()
        self.lib.general_helper.scroll_and_click(self.pages.CRS.order_entry.lnk_fund_distribution)
        self.actions.wait_for_element_displayed(self.pages.CRS.order_entry.btn_submit_distribution_popup)
        # Check  fund name and value on opened popup
        fund_value = self.actions.get_element_text(self.pages.CRS.order_entry.lbl_fund_value)
        assert self.actions.get_element_text(self.pages.CRS.order_entry.lbl_fund_desc) == fee_fund_name
        assert fund_value.replace(" ", "") == fee_fund_total.replace(" ", "")
        # Assert submit button is disabled
        submit_attr = self.actions.get_element_attribute(self.pages.CRS.order_entry.btn_submit_distribution_popup,
                                                         'style')
        assert f"cursor: {self.cursor}" in submit_attr
        # Input fund value
        self.actions.send_keys(self.pages.CRS.order_entry.inp_fund_value,
                               str(fund_value.replace(" ", "").split('$')[1]))
        self.actions.press_key(self.pages.CRS.order_entry.inp_fund_value, 'ENTER')
        self.actions.click(self.pages.CRS.order_entry.btn_submit_distribution_popup)
        self.lib.general_helper.wait_for_spinner()
        self.actions.click(self.pages.CRS.order_entry.btn_add_to_order)


if __name__ == '__main__':
    run_test(__file__)
