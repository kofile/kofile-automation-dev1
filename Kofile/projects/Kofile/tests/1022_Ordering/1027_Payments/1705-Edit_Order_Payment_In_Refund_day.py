from projects.Kofile.Lib.DB import DB
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Connect to DB, make sure that 'Cash' payment method's Is_Refundable = 1 and refund_days = 1 in 
    Payments Methods table(update otherwise)
    -> Navigate to CRS as admin
    -> Create order with OIT which has fee
    -> Checkout order with Cash
    -> Click on 'Edit Order Payments(s)' link
    -> Check payment methods availability
    -> Update with other payment method and finalize order
    -> Order is finalized with another payment method
        """

tags = ['']


def setup(data):
    with DB(data) as db:
        db.update_refundable_and_refund_days_from_payment_method()


class test(TestParent):                                                                             # noqa
    payment = ['Cash', 'Check', 'Credit Card']

    def __init__(self, data):
        data["current_oit"] = data["OIT"] = "RP_Recordings"
        data["orderheader"] = "email"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        self.lib.CRS.order_finalization.click_edit_order_payments()
        self.lib.CRS.add_payment.check_all_payment_methods_count()
        self.atom.CRS.add_payment.add_payments(payments=self.payment)
        self.lib.CRS.add_payment.click_add_payment_checkout_button()
        self.actions.wait_for_element_displayed(self.pages.CRS.order_finalization.btn_void_order)


if __name__ == '__main__':
    run_test(__file__, env="qa_dallas")
