"""69953 Create eOrder from e-form in Internal mode"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
                Steps:
                 1. Navigate to Portal with configured Cart
                 2. Add first eForm to Cart: Check Total eForms in Cart
                 3. Add second eForm to Cart: Check Total eForms in Cart
                 4. Delete second eForm: Check Total eForms in Cart
                 5. Checkout first eForm
                 6. Navigate to CRS
                 7. Find created eForm and finalize
                 """


class test(TestParent):                                                                             # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: Workstation IP is configured in internal IP range,
                        so that Portal Home page is opened with Cart Mode
        Post-conditions: Created eForm is finalized in CRS
        """
        self.data["current_oit"] = self.data.OIT
        self.atom.EForm.general.go_to_eform_portal()
        # open the first eForm
        self.atom.EForm.general.open_eform_document()
        # fill the first eForm and add to Cart
        if self.data.OIT == 'Eform_Death_Certified_Copy':
            self.actions.click(self.pages.eform.rbt_death_certificate)
        self.atom.EForm.general.add_to_cart()
        # verify that Total eForms in Cart is 1
        self.actions.assert_equals(self.actions.get_element_text(
            self.pages.eform.txt_total_eforms), '1')
        # navigate to Portal Home Page
        self.lib.general_helper.find_and_click(self.pages.eform.btn_return_to_eform_menu)
        # open second eForm
        order_type = self.data['config'].test_data(f"{self.data.OIT2}.order_type").lower()
        order_tye_loc = self.lib.general_helper.make_locator(
            self.pages.eform.lnk_eform_order_type, order_type)
        self.actions.click(order_tye_loc)
        self.actions.wait_for_element_displayed(self.pages.eform.btn_submit_eform)
        # fill second eForm and add to Cart
        if self.data.OIT2 == 'Eform_Death_Certified_Copy':
            self.actions.click(self.pages.eform.rbt_death_certificate)
        self.atom.EForm.general.add_to_cart()
        # verify that Total eForms in Cart is 2
        self.actions.assert_equals(self.actions.get_element_text(
            self.pages.eform.txt_total_eforms), '2')
        # delete second eForm
        self.lib.general_helper.find_and_click(
            self.lib.general_helper.make_locator(self.pages.eform.btn_remove_eform, 2))
        self.lib.general_helper.wait_for_spinner()
        # verify that Total eForms in Cart is 1
        self.actions.assert_equals(self.actions.get_element_text(
            self.pages.eform.txt_total_eforms), '1')
        # fill Customer Name and checkout
        self.actions.send_keys(self.pages.eform.txt_customer_name, "Test Customer Name")
        self.actions.press_key(self.pages.eform.txt_customer_name, 'TAB')
        self.lib.general_helper.wait_and_click(self.pages.eform.btn_checkout)
        self.actions.wait_for_element_displayed(self.pages.eform.pup_submission_txt_order)
        self.actions.store("order_number", self.actions.get_element_text(
            self.pages.eform.pup_submission_txt_order))
        # find and open the order in CRS
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.crs.click_running_man()
        self.actions.wait_for_element_displayed(self.pages.CRS.order_summary.lbl_order_number)
        # review and process to archive
        self.atom.CRS.order_summary.edit_oit()
        # get usertype
        self.data["user_type"] = self.data['config'].order_header_fill(
            f'{self.data.orderheader}.type')
        if self.data['config'].test_data(f"{self.data.OIT}.start_process_order_from_edit_oi"):
            self.lib.required_fields.crs_fill_required_fields()
            self.lib.CRS.order_entry.click_add_to_order()
        self.atom.CRS.add_payment.finalize_order()


if __name__ == '__main__':
    run_test(__file__)
