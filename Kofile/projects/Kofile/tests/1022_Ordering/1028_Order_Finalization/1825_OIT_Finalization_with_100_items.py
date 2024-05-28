from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test
import time

description = """Go to CRS, create new order with 100 items and finalize. Log checkout and finalization time"""

tags = []


class test(TestParent):  # noqa

    def __init__(self, data, expected_time=1200):
        self.expected_time = expected_time
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: no
        Post-conditions: Order is finalized,  Order Finalization screen is displayed
        """
        self.data["current_oit"] = self.data.OIT
        self.lib.general_helper.check_order_type()
        self.atom.CRS.order_queue.create_and_action_with_order(None)

        self.lib.CRS.order_summary.copy_oit(50)
        self.lib.general_helper.wait_for_spinner(spinner_in=7, spinner_out=60)
        self.lib.general_helper.scroll_into_view(self.pages.CRS.order_summary.lbl_order_number)
        self.lib.CRS.order_summary.copy_oit(49)
        self.lib.general_helper.wait_for_spinner(spinner_in=7, spinner_out=60)
        order_id = int(
            self.lib.general_helper.find(self.pages.CRS.order_summary.txt_order_id, get_attribute="value"))
        # Update OITs statuses to Reviewed
        self.lib.db_with_vpn.update_oit_status_in_order_summary(order_id)
        # checkout after update status
        self.lib.general_helper.scroll_and_click(self.pages.CRS.order_summary.btn_checkout)
        self.actions.wait_for_element_displayed(self.pages.CRS.add_payment.btn_checkout)
        self.atom.CRS.add_payment.add_payments()
        start_finalization = time.time()
        self.lib.CRS.add_payment.click_add_payment_checkout_button(expected_status=100 * ['Finalized'],
                                                                   expected_total=None, timeout=120)
        # calculate finalization time
        finalization_time = round(time.time() - start_finalization)
        assert int(finalization_time) < self.expected_time, f"Finalization time  {finalization_time} " \
                                                            f"not less than  expected time: {self.expected_time}"
        self.actions.step(f"Finalization time is {finalization_time}")


if __name__ == '__main__':
    run_test(__file__)
