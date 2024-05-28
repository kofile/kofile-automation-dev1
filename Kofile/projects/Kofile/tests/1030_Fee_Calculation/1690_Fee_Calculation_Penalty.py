"""Fee Calculation: Penalty"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Check 'Penalty Fee' calculation"""

tags = ["48999_location_2"]


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.general_helper.check_order_type()
        self.atom.CRS.order_queue.fill_order_entry_tabs()
        total_fee = self.lib.CRS.order_entry.enter_and_verify_penalty_fee_amounts(self.data.fee_name)
        self.lib.CRS.order_entry.click_add_to_order()
        self.lib.general_helper.wait_for_spinner()
        total_price = float(self.lib.general_helper.find(self.pages.CRS.order_summary.price_by_row_index(1),
                                                         get_text=True).split('$')[1])
        assert total_price == total_fee, "Total Price amount is NOT correct"


if __name__ == '__main__':
    run_test(__file__)
