from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS, create new order -> process order with 1 payment method -> finalize order
    -> Void order, Change Cash payment method to Void Refund -> 
    "Address is required!" message appears in order header
    -> 'More options' -> Fill 'Refund to' fields 
    -> Finalize order and check status
        """

tags = ['48999_location_2']


class test(TestParent):                                                                            # noqa

    def __init__(self, data):
        data["current_oit"] = data["OIT"] = "Copies"
        data["orderheader"] = "email"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to CRS
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        # Click Order Summary Checkout button
        self.lib.CRS.order_summary.click_order_summary_checkout_button()
        # Add payment
        self.atom.CRS.add_payment.add_payments()
        # Finalize
        self.lib.CRS.add_payment.click_add_payment_checkout_button()
        # Void order
        self.lib.CRS.order_finalization.process_void_order()
        # Edit 2-nd payment method
        self.atom.CRS.add_payment.add_payments(payments="Void Refund", tr_id=None, comment=None, amount=None,
                                               start_from=2, edit_payment=True)
        # Check error and fill in 'Return to' fields
        self.lib.CRS.order_entry.check_address_required_error(expected_error="Address is required!",
                                                              fill_in_required_fields=True)
        # Finalize order and check status
        self.lib.CRS.order_finalization.click_finalize_void_button()


if __name__ == '__main__':
    run_test(__file__)
