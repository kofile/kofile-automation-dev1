"""smoke test"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test
from random import randint

description = """
1. Add Order adn finalize
2. Edit order from finalization screen and change no of page
3. Save order
4. Edit order from order finalization screen
5. Verify fund distribution
"""

tags = ['48999_location_2']


class test(TestParent):  # noqa
    added_pages = randint(1, 30)

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: no
        Post-conditions: Order is processed from Order Queue to Finalization
        """
        self.lib.general_helper.check_order_type()
        # Finalize Order
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        # Edit Order and check fee fund distribution
        self.lib.CRS.order_finalization.click_edit_order(add_pages=self.added_pages)
        self.lib.CRS.order_finalization.process_through_admin_payment_screen()
        self.lib.CRS.order_finalization.click_edit_order()
        self.lib.general_helper.scroll_and_click(self.pages.CRS.order_entry.lnk_fund_distribution)
        self.lib.CRS.order_entry.verify_fund_distribution()
        self.actions.click(self.pages.CRS.order_entry.btn_add_to_order)
        self.lib.general_helper.wait_for_spinner()


if __name__ == '__main__':
    run_test(__file__)
