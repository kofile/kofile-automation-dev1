"""Fee Calculation: No of certifications/copies"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Check the calculation of 'Certification Fee'"""

tags = ["48999_location_2"]


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.general_helper.check_order_type()
        self.atom.CRS.order_queue.fill_order_entry_tabs()
        self.lib.CRS.order_entry.enter_and_verify_fee_amounts_by_fee_criteria(
            self.data.fee_name, ["pages", "certifications"])
        self.lib.CRS.order_summary.click_edit_icon_by_row_index(1)
        self.lib.CRS.order_entry.enter_and_verify_fee_amounts_by_fee_criteria(
            self.data.fee_name, ["pages", "certifications"])


if __name__ == '__main__':
    run_test(__file__)
