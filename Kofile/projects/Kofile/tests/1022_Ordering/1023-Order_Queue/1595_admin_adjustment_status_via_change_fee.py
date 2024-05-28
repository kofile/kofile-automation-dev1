"""cancel order test"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Create order with user4, finalize order.
                Edit order price after finalization, via change No of pages. 
                Go to Order queue after changing fee and verify Order Status admin adjustment"""

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data, ind=1):
        self.ind = ind
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: Order Queue
        Post-conditions: Order is in order queue with admin adjustment status
        """
        self.data["current_oit"] = self.data.OIT
        self.lib.general_helper.check_order_type()
        # atom
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order, self.ind)
        # edit order
        self.actions.wait_for_element_displayed(self.pages.CRS.order_finalization.lbl_order_finalize_label)
        edit_el = self.pages.CRS.order_finalization.editicon_by_row_index()
        self.actions.click(edit_el)
        self.actions.wait_for_element_displayed(self.pages.CRS.order_entry.btn_cancel_order)
        # fill required fields if exist
        self.lib.required_fields.crs_fill_required_fields()
        self.lib.CRS.order_item_type.change_number_of_page_amount()
        # Wait for outstanding balance is displayed
        self.lib.general_helper.wait_and_click(self.pages.CRS.order_entry.btn_add_to_order, scroll=True,
                                               wait_for=self.pages.CRS.order_entry.lbl_all_outstand_labels)
        self.lib.CRS.order_entry.send_to_admin()
        self.lib.CRS.order_queue.wait_for_order_queue_is_displayed()
        # Verify status is admin adjustment
        self.lib.CRS.crs.verify_order_status("Admin_Adjustment_status")


if __name__ == '__main__':
    run_test(__file__)
