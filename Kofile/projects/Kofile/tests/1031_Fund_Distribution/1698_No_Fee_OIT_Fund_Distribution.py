"""smoke test"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
1.Create and finalize order with no fee
2. Click edit order
3. Verify Fee Distribution link is absent in Order Entry screen"""

tags = ['48999_location_2']


class test(TestParent):  # noqa

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
        self.lib.CRS.order_finalization.click_edit_order()
        "Fee Distribution link exists for no fee OIT"
        self.lib.general_helper.scroll_into_view(self.pages.CRS.order_entry.btn_add_to_order)
        assert len(self.lib.general_helper.find_elements(self.pages.CRS.order_entry.lnk_fund_distribution)) == 0
        self.actions.click(self.pages.CRS.order_entry.btn_add_to_order)
        self.lib.general_helper.wait_for_spinner()


if __name__ == '__main__':
    run_test(__file__)
