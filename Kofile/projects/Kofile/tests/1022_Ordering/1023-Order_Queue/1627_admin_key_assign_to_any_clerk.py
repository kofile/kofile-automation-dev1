"""admin key assign to any clerk"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
                 1. Open Order Queue
                 2. Click on the Admin key
                 3. Find first order with assign button
                 4. Save order status
                 5. Assign order to Clerk
                 6. Checking assigned username after assignment
                 7. Checking order status after assignment  
                  """

tags = ['48999_location_2']


class test(TestParent):                                                                                # noqa

    def __init__(self, data, ind=1):
        self.ind = ind
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # atom
        self.atom.CRS.general.go_to_crs()
        # check if order queue is empty print error message for add orders to the queue
        count = self.lib.CRS.crs.count_orders_in_queue()
        if count != '0':
            self.actions.assert_element_enabled(self.pages.CRS.general.btn_admin_key)
            self.actions.click(self.pages.CRS.general.btn_admin_key)
            self.actions.wait(2)
            # get orders in order queue
            orders_list = self.lib.CRS.crs.get_list_of_orders()
            for order in orders_list:
                assign_button = self.pages.CRS.general.assign_icon_by_order_number(order)
                self.data['order_number'] = order
                # check if assign button is displayed
                if self.lib.general_helper.find(assign_button).is_displayed():
                    # save order status before assignment
                    default_order_status = self.actions.get_element_text(
                        self.pages.CRS.general.status_by_order_number(order))
                    # assign order
                    self.lib.CRS.crs.go_to_order_queue()
                    self.atom.CRS.order_queue.assign_order(ind=self.ind)
                    # save assigned username
                    assigned_to_loc = self.pages.CRS.general.assigned_to_by_order_number_text(order)
                    # comparing user names
                    self.actions.verify_element_attribute(assigned_to_loc, 'value',
                                                          self.lib.CRS.crs.assign_user_name(ind=self.ind))
                    # save order status after assigment
                    actual_order_status = self.actions.get_element_text(
                        self.pages.CRS.general.status_by_order_number(order))
                    # comparing order statuses
                    self.actions.assert_equals(default_order_status, actual_order_status)
                    break


if __name__ == '__main__':
    run_test(__file__)
