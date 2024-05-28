"""Fund distribution with Penalty"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Apply Penalty to a finalized order and check that fund distribution amounts are doubled"""

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.general_helper.check_order_type()
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        total_price_1 = self.lib.CRS.order_finalization.check_order_finalization__order_total_amount(
            expected_amount=None)
        number_of_funds_1, actual_fund_values_1, total_amount_1 = \
            self.lib.CRS.order_finalization.get_actual_fund_amounts()
        self.lib.general_helper.find(self.lib.CRS.order_entry.tab_locator("Order_Item"), wait_displayed=True)
        self.lib.general_helper.find_and_click(self.pages.CRS.order_entry.chk_penalty)
        self.actions.wait_for_element_displayed(self.pages.CRS.order_finalization.txt_outstanding_balance_due)
        self.lib.CRS.order_finalization.close_edit_screen()
        self.lib.CRS.order_finalization.process_through_admin_payment_screen()
        total_price_2 = self.lib.CRS.order_finalization.check_order_finalization__order_total_amount(
            expected_amount=None)
        assert total_price_2 == 2 * total_price_1, \
            f"Actual total price {total_price_2} != expected {2 * total_price_1}"
        number_of_funds_2, actual_fund_values_2, total_amount_2 = \
            self.lib.CRS.order_finalization.get_actual_fund_amounts(message=True)
        assert number_of_funds_2 == number_of_funds_1, "Numbers of funds mismatch"
        for i in range(number_of_funds_2):
            assert actual_fund_values_2[i] == 2 * actual_fund_values_1[i], \
                f"Fund #{[i]} value {actual_fund_values_2[i]} != expected {2 * actual_fund_values_1[i]}"
        assert total_amount_2 == 2 * total_amount_1, f"Total fund {total_amount_2} != expected {2 * total_amount_1}"
        # process the order to clean the queue
        try:
            self.lib.general_helper.scroll_and_click(self.pages.CRS.order_entry.btn_add_to_order)
            self.lib.general_helper.wait_for_spinner()
        except Exception as e:
            self.logging(type(e).__name__)


if __name__ == '__main__':
    run_test(__file__)
