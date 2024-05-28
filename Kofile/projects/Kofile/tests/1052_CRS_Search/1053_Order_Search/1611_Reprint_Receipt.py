"""Test-Reprint Receipt from Order Search"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Finalize an order and Reprint Receipt from Order Search"""

tags = ['48999_location_2']


class test(TestParent):                                                                              # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: Order Search page is displayed, receipt is reprinted from Order Search
        """
        self.data['current_oit'] = self.data.OIT
        # create order, finalize order, search order in Order Search (atom tests)
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])

        self.lib.CRS.order_search.click_reprint_receipt_icon(self.data['order_number'])
        self.lib.CRS.order_search.verify_receipt_preview_order_number(self.data['order_number'])

        # Print Duplicate Copy and verify the success message
        self.lib.CRS.order_search.click_print_duplicate_receipt()
        self.lib.CRS.order_search.verify_receipt_message(self.data.print_message)

        self.lib.CRS.order_search.fill_email_field(self.data.email)
        self.lib.CRS.order_search.click_email_duplicate_receipt()
        self.lib.CRS.order_search.verify_receipt_message(self.data.email_message)


if __name__ == '__main__':
    run_test(__file__)
