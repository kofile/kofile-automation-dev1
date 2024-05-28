"""1940_erProxy_Order Search edit order icon for erProxy"""

from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
1. Submit an erProxy and reject the order
2. Navigate to Order Search and find the rejected order by order number
3. Verify that edit order icon is enabled for rejected erProxy 
4. Click on edit icon and check action links on Order Summary screen 
    - Order item edit pencil is invisible
    - Discount dropdown is invisible 
    - Re-prioritize row arrow is invisible
    - Reject Entire Order link is invisible
    - Return to Order Queue link is invisible 
    - Send to Administrator link is invisible 
    (image version is changed with further upload image story, 
     e-order will no more be rejected due to incorrect image)
"""

tags = ['48999_location_2']


class test(TestParent):                                                                                     # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: erProxy order is rejected, Rejected Order Summary is displayed
        """
        # submit an erProxy order, process to Order Summary
        self.atom.CRS.general.go_to_crs()
        self.data["order_number"] = self.atom.ERProxy.general.create_er_proxy(exit_from_er_proxy=False)[0][0]
        self.lib.CRS.crs.go_to_order_queue()
        self.atom.CRS.order_queue.assign_order()
        self.lib.general_helper.wait_for_spinner()
        self.lib.CRS.crs.click_running_man()
        self.actions.wait_for_element_displayed(self.pages.CRS.order_summary.lbl_order_number)

        # reject order
        self.atom.CRS.order_summary.reject_order()

        # go to order search and check that order is rejected
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
        self.lib.CRS.order_search.verify_order_status("Reject_status")
        self.actions.assert_element_not_present(
            self.pages.CRS.order_search.print_rejection_letter_icon_by_order_number(self.data["order_number"]))

        # click on edit order icon and wait for Rejected Order Summary page
        self.lib.general_helper.find_and_click(
            self.pages.CRS.order_search.edit_order_icon_by_order_number(self.data["order_number"]))
        self.actions.wait_for_element_displayed(
            self.pages.CRS.rejected_order_summary.lbl_rej_order_summary_breadcrumb)

        # check the invisibility of icons and links
        # edit OI
        self.actions.assert_element_not_present(
            self.pages.CRS.order_summary.editicon_by_row_index())

        # discount
        self.actions.assert_element_not_present(
            self.pages.CRS.order_summary.discount_by_row_index())

        # re-prioritize
        self.actions.assert_element_not_present(self.pages.CRS.order_summary.prioritize_by_row_index())

        # Reject Entire Order link
        self.actions.assert_element_not_present(self.pages.CRS.order_summary.lnk_reject_entire_order)

        # Return to Order Queue link
        self.actions.assert_element_not_present(self.pages.CRS.order_summary.lnk_return_to_order_queue)

        # Send to Administrator link
        self.actions.assert_element_not_present(self.pages.CRS.order_summary.lnk_send_to_admin)


if __name__ == '__main__':
    run_test(__file__)
