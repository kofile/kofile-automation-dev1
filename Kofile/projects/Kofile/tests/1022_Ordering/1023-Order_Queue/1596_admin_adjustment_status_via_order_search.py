"""cancel order test"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Create order with user1, finalize order.
                Find Order from Order Search. Send to Admin. Find Order in Order Search and check order status"""

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: Order Queue
        Post-conditions: Order is in order queue with admin adjustment status
        """
        self.data["current_oit"] = self.data.OIT
        self.lib.general_helper.check_order_type()
        # atom
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)

        # go to search tab
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
        # send to admin
        send_to_admin_loc = self.pages.CRS.order_search.send_to_admin_icon_by_order_number(
            self.data["order_number"])
        self.actions.click(send_to_admin_loc)
        # fill reason and description and submit action reason popup
        self.lib.CRS.crs.fill_reason(self.pages.CRS.order_search.pup_send_to_admin)
        self.actions.wait_for_element_has_not_attribute(self.pages.CRS.order_search.pup_send_to_admin,
                                                        'data-callback-url')
        self.actions.wait_for_element_not_exist(self.pages.CRS.order_search.pup_send_to_admin, timeout=50)
        # go to order queue
        self.lib.CRS.crs.go_to_order_queue()
        self.lib.CRS.order_queue.wait_for_order_queue_is_displayed()
        self.lib.CRS.crs.verify_order_status("Admin_Adjustment_status")


if __name__ == '__main__':
    run_test(__file__)
