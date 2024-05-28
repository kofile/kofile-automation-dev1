"""send to admin test"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Go to CRS, Create Order and send to admin from order summary. Verify status is admin hold. 
                Click on running man next to this order.
                Click Return to order queue link from order summary. 
                Find order from Order queue, verify order status is 'In Process'. 
                Verify user assigned to logged in user"""

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: Order Queue
        Post-conditions: Order is in process status, assigned to clerk
        """
        self.data["current_oit"] = self.data.OIT
        self.lib.general_helper.check_order_type()
        # atom
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.order_summary.send_to_admin)
        self.atom.CRS.order_queue.check_status_of_order("Send_to_Admin_status")
        #  click on running guy next to order
        run_guy = self.pages.CRS.general.running_man_by_order_number(self.data["order_number"])
        self.actions.click(run_guy)
        # click return to order queue link from order summary
        self.lib.general_helper.wait_and_click(self.pages.CRS.order_summary.lnk_return_to_order_queue)
        self.actions.wait_for_element_displayed(self.pages.CRS.general.btn_admin_key)
        # click show all on order queue
        self.lib.CRS.crs.click_all_show_all_action_links()
        # get login user, assigned user names, and order status
        login_user = self.lib.CRS.crs.assign_user_name()
        assigned_to_loc = self.pages.CRS.general.assigned_to_by_order_number_text(self.data['order_number'])

        # Verify order status and assigned user
        self.lib.CRS.crs.refresh_queue()
        self.lib.CRS.crs.click_all_show_all_action_links()

        self.lib.general_helper.scroll_into_view(assigned_to_loc)
        self.actions.verify_element_attribute(assigned_to_loc, 'value', login_user)
        self.atom.CRS.order_queue.check_status_of_order("In_Process")


if __name__ == '__main__':
    run_test(__file__)
