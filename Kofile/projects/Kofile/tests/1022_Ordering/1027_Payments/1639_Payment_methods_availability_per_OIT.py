from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS, create new order -> process order to add payment screen
    -> Get from DB payment methods configured for current OIT
    -> From Add Payment screen get all available payment methods
    -> Compare payment methods from DB and from Add payment screen
        """

tags = ['48999_location_2']


class test(TestParent):                                                                             # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to CRS
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        # Click Order Summary Checkout button
        self.lib.CRS.order_summary.click_order_summary_checkout_button()

        all_payments_db = self.lib.db_with_vpn.get_payment_methods(self.data["order_number"])
        # Get all available payment methods
        all_payments = self.lib.CRS.add_payment.get_all_payment_methods(remove_credit_card=False)

        assert all(i in all_payments for i in all_payments_db), \
            f"Payment methods from DB: '{all_payments_db}' not equal to payment methods in UI: '{all_payments}'"


if __name__ == '__main__':
    run_test(__file__)
