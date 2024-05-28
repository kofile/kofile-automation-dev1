from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Navigate to CRS as admin
    -> Finalize order with no fee OIT
    -> Check Edit Order Payment(s) link existence
    -> Edit Order Payment(s) link disable
        """

tags = ['48999_location_2']


class test(TestParent):                                                                         # noqa

    def __init__(self, data):
        data["current_oit"] = data["OIT"] = "Child_Support_Lien"
        data["orderheader"] = "email"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        self.lib.CRS.order_finalization.check_not_clickable_edit_order_payments_link()


if __name__ == '__main__':
    run_test(__file__)
