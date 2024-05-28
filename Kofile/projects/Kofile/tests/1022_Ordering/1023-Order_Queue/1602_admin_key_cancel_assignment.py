"""cancel order test"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Login with user1, Go to CRS, add new OIT, from order summary screen click "Return to Order Queue"
                 Find order from order queue, assign order to user4, cancel assignment, 
                 check that order assigned to user1"""

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data, ind=1):
        self.ind = ind
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: Order Queue
        Post-conditions: Order Queue is opened, Order assignment is cancelled
        """
        self.data["current_oit"] = self.data.OIT
        self.lib.general_helper.check_order_type()
        # atom
        self.atom.CRS.order_queue.create_and_action_with_order(None)

        #  click Return to Order Queue
        self.actions.click(self.pages.CRS.order_summary.lnk_return_to_order_queue)
        # wait order queue is opened
        self.lib.general_helper.wait_and_click(self.pages.CRS.general.btn_admin_key)
        self.lib.CRS.crs.click_all_show_all_action_links()
        # get assigned user name
        assigned_to_loc = self.pages.CRS.general.assigned_to_by_order_number_text(self.data['order_number'])
        self.lib.general_helper.scroll_into_view(assigned_to_loc)
        assigned_user = self.actions.get_element_attribute(assigned_to_loc, 'value')

        # assign to new user and click 'Cancel'
        self.lib.CRS.crs.assign_order_by_user_name(self.data['order_number'], ind=self.ind, add=False)
        self.lib.CRS.crs.refresh_queue()
        self.lib.CRS.crs.click_all_show_all_action_links()
        # Verify that assigned user is not changed
        self.lib.general_helper.scroll_into_view(assigned_to_loc)
        self.actions.verify_element_attribute(assigned_to_loc, 'value', assigned_user)


if __name__ == '__main__':
    run_test(__file__)
