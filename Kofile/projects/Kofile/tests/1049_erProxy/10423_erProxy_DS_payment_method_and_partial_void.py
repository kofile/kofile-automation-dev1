"""erProxy DS payment method and partial void"""

from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    - Submit an erProxy DS order with 2 OIs to CRS and finalize
    - Click on Edit Payment link and verify that the only payment method is Direct Submission
    - Process through Admin Payment and verify that partial void of erProxy DS order is NOT allowed
"""

tags = ['48999_location_6']


class test(TestParent):                                                                                   # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: erProxy DS order with 2 OIs is finalized
        """

        # submit an erProxy DS order with 2 OIs and get the created order number, package_id
        er_proxy_data = self.atom.ERProxy.general.create_er_proxy(oit_count=2,
                                                                  exit_from_er_proxy=False, ds=True)
        self.data["order_number"] = er_proxy_data[0][0]
        self.data["package_id"] = er_proxy_data[1][0]

        # open the submitted order in CRS
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.crs.go_to_order_queue()
        self.atom.CRS.order_queue.assign_order()
        self.lib.general_helper.wait_for_spinner()
        self.lib.CRS.crs.click_running_man()
        self.actions.wait_for_element_displayed(self.pages.CRS.order_summary.lbl_order_number)

        # review the OIs and finalize the order
        self.atom.CRS.order_summary.edit_oit(edit_all=True)
        self.atom.CRS.add_payment.finalize_order()

        # click on Edit Payment link and verify that the only payment method is Direct Submission
        self.lib.CRS.order_finalization.click_edit_order_payments()
        payment_methods = self.lib.CRS.add_payment.get_all_payment_methods(remove_credit_card=False)
        assert len(payment_methods) == 1, "More than one payment methods are found"
        payment_method = payment_methods[0]
        assert payment_method == self.data['payment_method'], \
            f"Payment method {payment_method} is NOT equal to {self.data['payment_method']}"

        # process though Admin Payment
        self.lib.general_helper.scroll_and_click(self.pages.CRS.add_payment.btn_checkout)
        self.lib.general_helper.find(self.pages.CRS.order_finalization.btn_void_order, wait_displayed=True)

        # verify that partial void checkboxes are missing for erProxy DS order
        self.actions.verify_element_not_present(
            self.pages.CRS.void_order_summary.checkbox_by_row_index(row_num=1))
        self.actions.verify_element_not_present(
            self.pages.CRS.void_order_summary.checkbox_by_row_index(row_num=2))


if __name__ == '__main__':
    run_test(__file__, env="qa_48999_loc_6")
