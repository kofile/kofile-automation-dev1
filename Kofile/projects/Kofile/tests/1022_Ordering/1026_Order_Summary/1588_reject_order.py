from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """From Order Summary Reject Order, Verify Order status in Order Queue.
                Verify that order is found in Order Search by order number,
                Send order back to order queue. From order queue order status"""

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: Order Queue
        Post-conditions: Order is rejected
        """
        self.data["current_oit"] = self.data.OIT
        self.lib.general_helper.check_order_type()
        # atom test
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.order_summary.reject_order)
        # go to search tab
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
        # Check Order Status
        self.actions.verify_element_displayed(
            self.pages.CRS.order_search.print_rejection_letter_icon_by_order_number(self.data['order_number']))
        self.lib.CRS.order_search.verify_order_status("Reject_status")

        self.actions.wait_for_element_displayed(
            self.pages.CRS.order_search.resend_rejection_icon(self.data['order_number']))
        
        self.actions.wait(1)

        self.actions.click(
            self.pages.CRS.order_search.resend_rejection_icon(self.data['order_number']))
        
        # check popup appearance
        self.actions.wait_for_element_present(self.pages.CRS.order_search.btn_resend_rejection)
        self.lib.CRS.order_search.click_resend_rejection(self.data.env.email_user)

        self.actions.wait_for_element_not_present(self.pages.CRS.order_search.txt_resend_rejection)
        self.lib.general_helper.wait_for_spinner()

        # Sand order back to order queue
        self.actions.click(
            self.pages.CRS.order_search.send_back_to_order_queue_icon_by_order_number(self.data["order_number"]))
        self.actions.wait_for_element_displayed(self.pages.CRS.general.btn_add_new_order)
        # find order in order queue
        self.atom.CRS.order_queue.check_status_of_order('In_Process')
        # go to search tab
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
        # verify order status
        self.lib.CRS.order_search.verify_order_status("order_status")


if __name__ == '__main__':
    run_test(__file__)
