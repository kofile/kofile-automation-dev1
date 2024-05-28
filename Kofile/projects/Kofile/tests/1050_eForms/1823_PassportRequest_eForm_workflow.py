"""75874 PassportRequest eForm workflow"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
                Steps:
                1. Navigate to Portal and open 'Passport Request eForm'
                2. Submit eForm
                3. Navigate to CRS
                4. Open and finalize eForm
                5. Navigate to Order Search page
                6. Verify 'Archive' order status
              """


class test(TestParent):                                                                              # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: Kiosk Mode is active (INTRANET_DEVICE isActive=1).
                        Workstation IP is configured in internal IP range.
        Post-conditions: eForm is submitted and finalized with status 'Archive'
        """
        # Open Portal
        self.atom.EForm.general.go_to_eform_portal()
        order_type = self.data['config'].test_data(f"{self.data.OIT}.order_type").lower()
        order_tye_loc = self.lib.general_helper.make_locator(
            self.pages.eform.lnk_eform_order_type, order_type)
        # Open 'Passport Request' eForm
        self.actions.click(order_tye_loc)
        self.actions.wait_for_element_displayed(self.pages.eform.btn_next)
        # Click on the 'Next' button
        self.lib.general_helper.find_and_click(self.pages.eform.btn_next)
        # Click on the 'Yes' button for all rest pages
        for i in range(2, 9):
            self.lib.general_helper.find_and_click(
                self.lib.general_helper.make_locator(self.pages.eform.btn_yes, i))
        # Fill required fields
        self.lib.general_helper.find_and_send_keys(self.pages.eform.inp_last_name, 'LastName')
        self.lib.general_helper.find_and_send_keys(self.pages.eform.inp_first_name, 'FirstName')
        self.lib.general_helper.find_and_send_keys(self.pages.eform.inp_number, 1)
        self.actions.press_key(self.pages.eform.inp_number, 'TAB')
        # Submit eForm
        self.lib.general_helper.find_and_click(self.pages.eform.btn_submit)
        # Navigate to Cart and fill Customer Name
        self.actions.wait_for_element_displayed(self.pages.eform.txt_customer_name)
        self.actions.send_keys(self.pages.eform.txt_customer_name, "Test Customer Name")
        self.actions.press_key(self.pages.eform.txt_customer_name, 'TAB')
        self.actions.wait_for_element_enabled(self.pages.eform.btn_checkout)
        self.actions.click(self.pages.eform.btn_checkout)
        self.actions.wait_for_element_displayed(self.pages.eform.pup_submission_txt_order)
        self.actions.store("order_number", self.actions.get_element_text(
            self.pages.eform.pup_submission_txt_order))
        # Find and open the order in CRS
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.crs.click_running_man()
        self.actions.wait_for_element_displayed(self.pages.CRS.order_summary.lbl_order_number)
        # Review and process to archive
        self.atom.CRS.order_summary.edit_oit()
        # Get usertype
        self.data["user_type"] = self.data['config'].order_header_fill(
            f'{self.data.orderheader}.type') \
            # Finalize order
        self.atom.CRS.add_payment.finalize_order()
        # Navigate to Order Search
        self.lib.CRS.crs.go_to_order_search()
        # Search order by Order#
        self.atom.CRS.order_search.search_order_by_order_number()
        # Verify Order Status
        self.lib.CRS.order_search.verify_order_status_archive()


if __name__ == '__main__':
    run_test(__file__)
