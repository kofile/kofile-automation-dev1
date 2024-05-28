"""Order Summary Test Case - Copy Order Items '+' row icon/Delete Order Item x row icon"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Copy Order Items '+' row icon/Delete Order Item x row icon"""

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: no
        Post-conditions: Order Finalization page with copied Order Items
        """
        self.lib.general_helper.check_order_type()
        # Create first OIT
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        # Order Summary page
        copy_icon_el = self.lib.general_helper.make_locator(self.pages.CRS.order_summary.icn_copy_orderitem, 1)
        self.lib.general_helper.scroll_and_click(copy_icon_el)
        self.actions.wait_for_element_present(self.pages.CRS.order_summary.txt_quantity_field)
        self.actions.send_keys(self.pages.CRS.order_summary.txt_quantity_field, 5)
        # Verify that new Items are not added after Cancel
        self.actions.click(self.pages.CRS.order_summary.btn_copy_oit_cancel)
        row_numbers = self.lib.CRS.order_summary.get_number_of_rows()
        # Verify that total Order Item is 1
        self.actions.assert_equals(row_numbers, 1)
        # Verify Copy Items
        # Copy 5 Items
        self.lib.CRS.order_summary.copy_oit(5, row_index=1)
        self.actions.wait_for_element_not_present(self.pages.CRS.order_summary.btn_copy_oit_submit)
        row_numbers = self.lib.CRS.order_summary.get_number_of_rows()
        # Verify that total Order Item is 6
        self.actions.assert_equals(row_numbers, 6)
        # Verify Deleting last Item
        delete_icon_el = self.lib.general_helper.make_locator(self.pages.CRS.order_summary._btn_oit_delete, 6)
        self.actions.click(delete_icon_el)
        self.actions.wait_for_element_not_present(delete_icon_el)
        row_numbers = self.lib.CRS.order_summary.get_number_of_rows()
        # Verify that total Order Item is 5
        self.actions.assert_equals(row_numbers, 5)
        self.atom.CRS.add_payment.finalize_order()
        row_numbers = self.lib.CRS.order_finalization.get_number_of_rows()
        # Verify that total Order Item is 5
        self.actions.assert_equals(row_numbers, 5)


if __name__ == '__main__':
    run_test(__file__)
