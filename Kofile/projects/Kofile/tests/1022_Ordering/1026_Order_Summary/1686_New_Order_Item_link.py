"""Order Summary Test Case - New Order Item link on summary screen"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """New Order Item link on summary screen"""

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: no
        Post-conditions: Order Summary page is opened with 2 OITs
        """
        self.lib.general_helper.check_order_type()
        # Create first OIT
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        self.actions.wait_for_element_displayed(self.pages.CRS.order_summary.lnk_new_order_item)
        self.actions.click(self.pages.CRS.order_summary.lnk_new_order_item)
        # Create second OIT
        self.actions.wait_for_element_displayed(self.pages.CRS.order_entry.ddl_order_type)
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.order_item_description()
        self.atom.CRS.order_entry.fill_order_header_name()
        self.atom.CRS.order_entry.one_oit_to_summary()
        row_numbers = self.lib.CRS.order_summary.get_number_of_rows()
        # Verify that Count of Order Items is 2 at Order Summary page
        self.actions.assert_equals(row_numbers, 2)
        # Verify that New Order Item link is displayed at Order Summary page
        self.actions.verify_element_displayed(self.pages.CRS.order_summary.lnk_new_order_item)


if __name__ == '__main__':
    run_test(__file__)
