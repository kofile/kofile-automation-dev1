"""erProxy DS Processing Fee"""

from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    - Submit an erProxy DS order to CRS
    - (Navigate to CRS -> Front Office
    - Find the submitter account and set the 'Direct Submission Processing Fee' to "Per Package (Order)"
      Front Office 'Direct Submission Processing Fee' radiobutton config is missing yet on 48999 !)
    
    - Find the erProxy order in CRS, finalize it and verify that Processing Fee amount is correct within Order Total
    - Verify that company account balance has changed by Order Total amount including the processing fee
    - Click on Edit Payment link and verify that Processing Fee label and amount are correct on Admin Payment page
    - Process through Admin Payment screen
    - Void the order and recheck the company account balance
"""

tags = ['48999_location_6']


class test(TestParent):                                                                                      # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: erProxy DS order is voided
        """

        expected_processing_fee = float(self.data['processing_fee_amount'])

        # submit an erProxy DS order and get the created order number, package_id
        er_proxy_data = self.atom.ERProxy.general.create_er_proxy(
            exit_from_er_proxy=False, ds=True)
        # er_proxy_data is a list of lists of order num and package id
        self.data["order_number"] = er_proxy_data[0][0]
        self.data["package_id"] = er_proxy_data[1][0]

        # # navigate to Front Office and find the submitter account
        # test_data_helper = self.lib.general_helper.get_data().config
        # er_proxy_ds_account = test_data_helper.order_header_fill(
        #     'er_proxy_account_name_password')['name']
        # self.atom.CRS.general.go_to_crs()
        # self.lib.CRS.front_office.search_account(er_proxy_ds_account)
        # self.lib.CRS.front_office.click_on_account_edit_icon()
        # # set the 'Direct Submission Processing Fee' to "Per Package (Order)
        # # radiobutton is NOT configured yet in 48999

        # find and open the submitted order in CRS
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.crs.go_to_order_queue()
        self.atom.CRS.order_queue.assign_order()
        self.lib.general_helper.wait_for_spinner()
        self.lib.CRS.crs.click_running_man()
        self.actions.wait_for_element_displayed(self.pages.CRS.order_summary.lbl_order_number)

        # get company account balance initial value
        initial_balance = self.lib.CRS.order_header.get_ca_balance_numeric()

        # review the order
        self.atom.CRS.order_summary.edit_oit()

        # finalize the order and verify that Processing Fee amount is correct within Order Total
        self.atom.CRS.add_payment.finalize_order()
        oi_price = self.lib.CRS.order_finalization.get_price_by_row_index()
        order_total = self.lib.CRS.order_finalization.get_order_total()
        finalization_processing_fee = order_total - oi_price
        assert finalization_processing_fee == expected_processing_fee, \
            f"Processing Fee actual amount ${finalization_processing_fee} within Order Total " \
            f"is NOT equal to expected ${expected_processing_fee}"

        # verify that company account balance has changed by Order Total amount including the processing fee
        new_balance = self.lib.CRS.order_header.get_ca_balance_numeric()
        difference = abs(new_balance - initial_balance)
        assert difference == order_total, \
            f"Company account balance change {difference} is NOT equal to Order Total amount ${order_total}"

        # click on Edit Payment link and verify that Processing Fee label and amount
        # are correct on Admin Payment page
        self.lib.CRS.order_finalization.click_edit_order_payments()
        self.lib.CRS.admin_payments.get_processing_fee_label()
        admin_payment_processing_fee = self.lib.CRS.admin_payments.get_processing_fee_amount()
        assert admin_payment_processing_fee == expected_processing_fee, \
            f"Processing Fee actual amount ${admin_payment_processing_fee} in Admin Payment " \
            f"is NOT equal to expected ${expected_processing_fee}"

        # process though Admin Payment
        self.lib.general_helper.scroll_and_click(self.pages.CRS.add_payment.btn_checkout)
        self.lib.general_helper.find(self.pages.CRS.order_finalization.btn_void_order, wait_displayed=True)

        # void the order
        self.lib.CRS.order_finalization.click_void_order_button()
        self.actions.wait_for_element_displayed(self.pages.CRS.void_order_summary.pup_fee_desc_btn_submit)
        self.lib.general_helper.scroll_into_view(self.pages.CRS.void_order_summary.pup_fee_desc_btn_submit)
        self.actions.wait_for_element_enabled(self.pages.CRS.void_order_summary.pup_fee_desc_btn_submit)
        self.actions.click(self.pages.CRS.void_order_summary.pup_fee_desc_btn_submit)
        self.lib.CRS.void_order_summary.click_void_button()
        self.lib.CRS.void_order_payment.click_finalize_void_button()

        # recheck CA balance
        post_void_balance = self.lib.CRS.order_header.get_ca_balance_numeric()
        assert post_void_balance == initial_balance, \
            f"Company account balance {post_void_balance} after void is NOT equal to initial balance {initial_balance}"


if __name__ == '__main__':
    run_test(__file__, env="qa_48999_loc_6")
