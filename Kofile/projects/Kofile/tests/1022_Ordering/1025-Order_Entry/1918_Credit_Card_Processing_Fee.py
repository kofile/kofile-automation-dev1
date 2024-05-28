"""save order from order summary test"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """From Order Summary Save Order, Verify Order status in Order Queue.
                Verify that order is found in Order Search by order number"""

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: Order Queue
        Post-conditions: Order is saved
        """
        self.data["current_oit"] = self.data.OIT
        self.lib.general_helper.check_order_type()
        # Go to CRS
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        # Click Order Summary Checkout button
        self.lib.CRS.order_summary.click_order_summary_checkout_button()
        # Add payment cash with balance_due / 2
        order_amount = self.lib.CRS.add_payment.get_balance_due_amount()
        payed_amount = order_amount / 2
        # Get amount payed by credit card
        self.atom.CRS.add_payment.add_payments(amount=payed_amount)
        self.lib.CRS.add_payment.add_payment_method()
        # Add credit card payment method
        self.lib.CRS.add_payment.fill_in_payment_method(row=2, method='Credit Card')
        self.lib.CRS.add_payment.fill_in_payment_method_transaction_id(row=2)
        # Check processing fee is correct
        processing_fee_actual = self.lib.CRS.add_payment.get_processing_fee()
        assert processing_fee_actual == self.lib.CRS.add_payment.get_expected_processing_fee(payed_amount)
        # Check add Payment Method link is disabled
        link_class_attr = self.lib.general_helper.find(self.pages.CRS.add_payment.btn_new_payment_method,
                                                       get_attribute='class')
        assert 'disablelinks' in link_class_attr
        # Finalize order
        self.lib.CRS.add_payment.click_add_payment_checkout_button()
        # Check Processing fee distribution
        processing_fee_distribution = self.lib.db_with_vpn.get_processing_fee_fund_distribution(
            self.data['order_number'])
        assert processing_fee_actual == float(processing_fee_distribution)
        # Check total amount
        self.lib.CRS.order_finalization.check_order_finalization__order_total_amount(
            order_amount + processing_fee_actual)


if __name__ == '__main__':
    run_test(__file__)
