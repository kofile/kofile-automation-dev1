"""smoke test"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
1.Add new OIT with additional fees
2.Enter all additional fees and finalize order
3.Edit order after finalization
4.Check Fee Fund Distribution names and values
5. Save order after checking"""

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: no
        Post-conditions: Order is processed from Order Queue to Finalization
        """
        if self.data['config'].test_data(f"{self.data.OIT}.additional_fee_labels"):
            self.lib.general_helper.check_order_type()
            # Finalize Order
            if self.data['scan_first']:
                order_types = [self.data.OIT, self.data.OIT2]
                self.atom.CRS.order_queue.add_order_with_scan_first_flow(order_types=order_types)
                self.lib.CRS.order_summary.click_edit_icon_by_row_index(row=1)
            else:
                self.atom.CRS.order_queue.fill_order_entry_tabs()
            no_of = self.lib.CRS.order_entry.enter_all_additional_fees(add_btn=True, consideration=True)
            self.lib.required_fields.crs_fill_required_fields()
            self.lib.general_helper.scroll_into_view(self.pages.CRS.order_entry.btn_add_to_order)
            self.actions.click(self.pages.CRS.order_entry.btn_add_to_order)
            self.lib.general_helper.wait_for_spinner()
            self.actions.click(self.pages.CRS.order_summary.btn_checkout)
            self.atom.CRS.add_payment.add_payments()
            self.lib.CRS.add_payment.click_add_payment_checkout_button()
            self.actions.wait_for_element_displayed(self.pages.CRS.order_finalization.lbl_order_finalize_label)
            # Edit Order After Finalization
            self.lib.CRS.order_finalization.click_edit_order()
            self.lib.general_helper.scroll_and_click(self.pages.CRS.order_entry.lnk_fund_distribution)
            self.lib.CRS.order_entry.verify_fund_distribution_with_additional_fees(no_of)
            self.actions.click(self.pages.CRS.order_entry.btn_add_to_order)
            self.lib.general_helper.wait_for_spinner()
        else:
            self.actions.step(f"{self.data.OIT} not not have additional fee on this tenant")


if __name__ == '__main__':
    run_test(__file__)
