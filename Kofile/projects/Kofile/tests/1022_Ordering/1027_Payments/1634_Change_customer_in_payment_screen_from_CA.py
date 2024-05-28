from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Go to CRS, create new order with company account -> process order -> Check available payment methods
-> Select Company account payment method and check 'Checkout' button
-> remove company account from header and fill email field -> Check available payment methods
-> finalize order with any payment method
    """

tags = ['48999_location_2']


class test(TestParent):                                                                           # noqa

    def __init__(self, data):
        data["current_oit"] = data["OIT"] = "Copies"
        data["orderheader"] = "account"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to CRS
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        # Finalize order with custom comment
        self.lib.CRS.order_summary.click_order_summary_checkout_button()
        self.atom.CRS.add_payment.add_payments("Company Account")
        # Checkout button should be enabled
        self.lib.CRS.add_payment.check_add_payment_checkout_button()
        # Clear header fields and enter another
        self.lib.CRS.order_entry.clear_order_header_fields()
        self.data["orderheader"] = "email"
        self.atom.CRS.order_entry.fill_order_header_name()
        # "Company Account" should not in payment methods list
        self.atom.CRS.add_payment.add_payments(forbidden_payments="Company Account")
        # Finalize order
        self.lib.CRS.add_payment.click_add_payment_checkout_button()


if __name__ == '__main__':
    run_test(__file__)
