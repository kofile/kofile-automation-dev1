"""process next order"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Case 1. Login with admin user and check if order in admin_adj, admin_hold, suspended, finalized, re_entry statuses or
(when order in status in_process or pending (when it is not erProxy order)) and assigned to logged in clerk 
or not assigned to any clerk 
=> running man should be visible.

    In case when order in cancelled status or in status pending or in process and not assigned to the logged in clerk 
=> running man should not be visible.

Case 2. Log out and log in with not admin clerk and check if order in suspended, re-entry statuses, or 
(order status is finalized and assigned to logged in clerk) 
or (order status is pending, when origin not erProxy) and assigned to logged in clerk or not assigned to any clerk 
=> running man should be visible.

    In case when order status in admin adj, admin _hold, cancelled statuses, or 
(order status is in_process, finalized or pending and order assigned to not logged in clerk) 
=> running man should not be visible
"""

tags = []


class test(TestParent):                                                                                  # noqa

    def __init__(self, data, ind=1):
        self.ind = ind
        super(test, self).__init__(data, __name__)

    def __test__(self):
        cancelled = self.data['config'].get_status('Order.Cancel_status.value')
        admin_hold = self.data['config'].get_status('Order.Send_to_Admin_status.value')
        suspended = self.data['config'].get_status('Order.Save_status.value')
        finalized = self.data['config'].get_status('Order.Finalized_status.value')
        admin_adj = self.data['config'].get_status('Order.Admin_Adjustment_status.value')
        re_entry = self.data['config'].get_status('Order.Re_Entry.value')
        in_process = self.data['config'].get_status('Order.In_Process.value')
        pending = self.data['config'].get_status('Order.Pending.value')

        self.atom.CRS.general.go_to_crs()
        # check if order queue is empty print error message for add orders to the queue
        count = self.lib.CRS.crs.count_orders_in_queue()

        if count != '0':
            login_user = self.lib.CRS.crs.assign_user_name()
            self.actions.wait(2)
            # get orders in order queue
            orders_list = self.lib.CRS.crs.get_list_of_orders()
            self.lib.general_helper.scroll_into_view(self.pages.CRS.order_queue.btn_refresh)
            # Loop in order list and check order status and assigned clerk
            for n, order in enumerate(orders_list, 1):
                loc = self.pages.CRS.order_queue.get_admin_assign_path(order)
                el = self.lib.general_helper.find(loc, should_exist=False, timeout=0.5)
                if not el:
                    break
                print(f"{n}:({order}) of {len(orders_list)}")
                order_status, assigned_clerk_el, assigned_clerk, origin, run_man = \
                    self.lib.CRS.order_queue.get_order_info_in_queue(order)
                if order_status in (admin_adj, admin_hold, suspended, finalized, re_entry) \
                        or (order_status == pending and origin == 'erProxy' and assigned_clerk == login_user) \
                        or (order_status == in_process or (order_status == pending and origin != 'erProxy')) \
                        and (assigned_clerk == login_user or assigned_clerk == ''):
                    self.lib.CRS.order_queue.run_man_existence(run_man, order)
                # assert running man is not displayed
                elif order_status == cancelled or (order_status == pending and assigned_clerk != login_user) \
                        or (order_status == in_process and assigned_clerk != login_user):
                    self.lib.CRS.order_queue.run_man_existence(run_man, order, False)
                # print message that status is not found
                else:
                    self.actions.error(f'New order status in queue for following order number - {order}')
        self.actions.close_browser()

        # login with non admin user
        self.actions.open_browser()

        self.actions.step('NON ADMIN USER')
        self.atom.CRS.general.go_to_crs(ind=self.ind)
        login_user_non_admin = self.lib.CRS.crs.assign_user_name(ind=self.ind)
        self.actions.step(login_user_non_admin)
        count_non_admin = self.lib.CRS.crs.count_orders_in_queue()
        if count_non_admin != '0':
            self.actions.wait(2)
            orders_list = self.lib.CRS.crs.get_list_of_orders()
            self.lib.general_helper.scroll_into_view(self.pages.CRS.order_queue.btn_refresh)

            for n, order in enumerate(orders_list, 1):
                print(f"{n}:({order}) of {len(orders_list)}")
                order_status, assigned_clerk_el, assigned_clerk, origin, run_man = \
                    self.lib.CRS.order_queue.get_order_info_in_queue(order)
                # assert running man is  displayed
                if order_status in (suspended, re_entry) or \
                        (order_status == finalized and assigned_clerk == login_user_non_admin) \
                        or (order_status == in_process or (order_status == pending and origin != 'erProxy')) \
                        and (assigned_clerk == login_user_non_admin or assigned_clerk == ''):
                    self.lib.CRS.order_queue.run_man_existence(run_man, order)
                # assert running man is not displayed
                elif order_status in (admin_adj, admin_hold, cancelled) \
                        or (order_status in [in_process, pending, finalized] and
                            assigned_clerk != login_user_non_admin):
                    self.lib.CRS.order_queue.run_man_existence(run_man, order, False)
                #  print message that status is not found
                else:
                    self.actions.error('New order status in queue for following order number-' + order)


if __name__ == '__main__':
    run_test(__file__)
