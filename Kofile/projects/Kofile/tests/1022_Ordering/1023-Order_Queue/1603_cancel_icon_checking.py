"""cancel order test"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Go to CRS, add new OIT, from order summary screen save order
                 Find order from order queue, if cancel icon is configured click cancel icon from queue table, 
                 cancel order cancelling, 
                 check that status of order is not changed. One more time click cancel icon and submit cancellation. 
                 Check that order status is changed to Cancel"""

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: Order Queue
        Post-conditions: Order Queue is opened, Order is cancelled
        """
        self.data["current_oit"] = self.data.OIT
        self.lib.general_helper.check_order_type()
        # atom
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.order_summary.save_order)

        # wait order queue is opened
        self.lib.general_helper.wait_and_click(self.pages.CRS.general.btn_admin_key)
        self.lib.CRS.crs.click_all_show_all_action_links()

        # if cancel icon exist check cancel icon, else say that icon is not exist for current tenant
        cancel_icon = self.pages.CRS.general.cancel_by_order_number_text(self.data['order_number'])
        cancel_icon_config = False
        try:
            self.actions.wait_for_element_displayed(cancel_icon, timeout=3)
            cancel_icon_config = True
        except Exception:
            self.lib.general_helper.add_log("Cancel icon is not configured for current tenant")
        #  if cancel icon is configured click cancel then cancel popup

        if cancel_icon_config is True:
            self.lib.general_helper.scroll_and_click(cancel_icon)
            self.lib.CRS.crs.fill_reason(self.pages.CRS.order_queue.pup_cancel_txt_reason, False)
            self.lib.CRS.crs.refresh_queue()

            # locate order and check that status is not changed
            self.lib.CRS.crs.verify_order_status("Save_status")

            # again click cancel icon and submit cancellation
            self.lib.general_helper.scroll_and_click(cancel_icon)
            self.lib.CRS.crs.fill_reason(self.pages.CRS.order_queue.pup_cancel_txt_reason)
            self.lib.general_helper.wait_for_spinner()
            self.lib.CRS.crs.refresh_queue()
            self.actions.wait(0.5)
            self.lib.CRS.crs.verify_order_status("Cancel_status")


if __name__ == '__main__':
    run_test(__file__)
