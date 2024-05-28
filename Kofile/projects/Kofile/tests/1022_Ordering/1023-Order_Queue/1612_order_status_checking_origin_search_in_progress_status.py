"""order status checking for crs origin"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """ Create test data, orders in order queue in following statuses:
                (admin hold, suspended, re-entry, in process). Origin Search
                From Order Queue Click Running man next to each order, edit order and save.
                Navigate to any queue then back to order queue
                Verify that order in status "In Process" and assigned to the Clerk"""

tags = ['48999_location_2']


class test(TestParent):                                                                        # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.data["current_oit"] = self.data.OIT
        #  IN PROCESS STATUS
        self.actions.step("IN PROCESS STATUS")
        self.atom.CS.general.process_order_from_cs_to_order_summary()

        self.lib.CRS.crs.go_to_indexing_queue()
        self.actions.wait_for_element_displayed(self.pages.CRS.indexing_queue.btn_add_new_indexing_task)
        self.lib.CRS.crs.go_to_order_queue()
        # verify status is pending
        self.atom.CRS.order_queue.check_status_of_order(status='Pending')
        self.lib.CRS.order_queue.click_running_man()
        # edit OIT
        self.atom.CRS.order_summary.edit_oit()
        self.actions.click(self.pages.CRS.order_summary.lnk_return_to_order_queue)
        self.actions.wait_for_element_displayed(self.pages.CRS.general.btn_add_new_order)
        # atom test
        self.atom.CRS.order_queue.check_status_of_order(status='In_Process')
        self.atom.CRS.order_entry.check_order_data_after_origin_search('Pending')


if __name__ == '__main__':
    run_test(__file__)
