"""process next order"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Go to CRS, identify order should be processed by get next button. 
                 click get next, verify that correct order is processed """

tags = ['48999_location_2']


class test(TestParent):                                                                            # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # atom
        self.atom.CRS.general.go_to_crs()
        self.lib.general_helper.wait_for_page_load()
        # check if order queue is empty print error message for add orders to the queue
        count = self.lib.CRS.crs.count_orders_in_queue()
        if count != '0':
            # get orders in order queue
            available_order = None
            login_user = self.lib.CRS.crs.assign_user_name()
            orders_list = self.lib.CRS.crs.get_list_of_orders()
            # Loop in order list and search first order which is in Process/Pending statuses assigned to current clerk
            # or erProxy order with pending status
            for order in orders_list:
                order_status = self.actions.get_element_text(self.pages.CRS.general.status_by_order_number(order))
                assigned_clerk_el = self.pages.CRS.general.assigned_to_by_order_number_text(order)
                self.lib.general_helper.scroll_into_view(assigned_clerk_el)
                assigned_clerk = self.actions.get_element_attribute(assigned_clerk_el, 'value')
                origin = self.actions.get_element_text(self.pages.CRS.general.origin_by_order_number(order))

                if (order_status in (self.data['config'].get_status('Order.In_Process.value'),
                                     self.data['config'].get_status('Order.Pending.value'))
                    and assigned_clerk == login_user) or \
                        (origin == 'erProxy' and order_status == self.data['config'].get_status('Order.Pending.value')
                         and assigned_clerk == ''):
                    available_order = order
                    break
                else:
                    self.actions.step("There is no available order for Get Next")

            # Click get next, if there is order
            self.atom.CRS.order_queue.get_next_order()
            if 'No Order To Process.' not in self.actions.get_page_source():
                self.actions.wait_for_element_displayed(self.pages.CRS.order_summary.lbl_order_number)
                self.actions.verify_element_text(self.pages.CRS.order_summary.lbl_order_number, str(available_order))
            else:
                self.actions.step("There is no  order to process, popup displays")


if __name__ == '__main__':
    run_test(__file__)
