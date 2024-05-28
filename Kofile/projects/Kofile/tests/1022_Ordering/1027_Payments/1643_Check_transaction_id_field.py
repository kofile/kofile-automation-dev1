from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS, create new order -> process order with 'Check' payment method
    -> 'Transaction ID' field should be required -> finalize order
        """

tags = ['48999_location_2']


class test(TestParent):                                                                              # noqa

    def __init__(self, data):
        data["current_oit"] = data["OIT"] = "Copies"
        data["orderheader"] = "guest"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to CRS
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        # Finalize order with custom comment
        self.lib.CRS.order_summary.click_order_summary_checkout_button()
        self.atom.CRS.add_payment.add_payments("Check")
        self.lib.CRS.add_payment.click_add_payment_checkout_button()


if __name__ == '__main__':
    run_test(__file__)
