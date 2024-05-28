"""Fee Calculation: Fee Adjustment"""
from random import randint
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Edit a finalized order to change the total fee and check the total fee and price amounts"""

tags = ["48999_location_2"]


class test(TestParent):  # noqa
    added_pages = randint(1, 30)

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.general_helper.check_order_type()
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        expected_outstanding_balance = self.added_pages * float(
            self.data['config'].test_data(f"{self.data['OIT']}.per_page_fee"))
        fee_amounts = self.lib.CRS.order_finalization.click_edit_order(add_pages=self.added_pages)
        original_total_fee = fee_amounts[0]
        actual_outstanding_balance = fee_amounts[1]
        assert actual_outstanding_balance == expected_outstanding_balance, \
            f"Outstanding balance {actual_outstanding_balance} is NOT" \
            f" equal to expected {expected_outstanding_balance}"
        expected_new_total = original_total_fee + actual_outstanding_balance
        self.lib.CRS.order_finalization.process_through_admin_payment_screen()
        actual_new_total = float(self.lib.general_helper.find(
            self.pages.CRS.order_finalization.price_by_row_index(1), get_text=True).replace('$', ''))
        assert actual_new_total == expected_new_total, \
            f"New total fee {actual_new_total} is NOT equal to expected {expected_new_total}"


if __name__ == '__main__':
    run_test(__file__)
