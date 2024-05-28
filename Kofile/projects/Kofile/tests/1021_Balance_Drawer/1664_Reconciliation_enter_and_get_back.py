from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS with non-admin user
    -> Go to Balance Drawer
    -> For each available payment method click reconciliation icon
    -> Click cancel in each payment method reconciliation screen
        """

tags = ["48999_location_2"]


class test(TestParent):                                                                      # noqa
    user_index = 1

    def __init__(self, data):
        data["orderheader"] = "guest"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to CRS > Balance Drawer
        self.atom.CRS.general.go_to_crs(self.user_index)
        self.lib.CRS.balance_drawer.go_to_balance_drawer(initialize=True, user_index=self.user_index)
        payments = self.lib.CRS.balance_drawer.get_payments_with_reconciliation_button()
        # Click on each 'Reconciliation' icon and then 'Cancel' reconciliation
        for i in payments:
            self.lib.CRS.balance_drawer.click_reconciliation_button(payment_method=i)
            self.lib.CRS.balance_drawer.click_cancel_button()
            self.actions.wait_for_window_present_by_partial_url("/Balance/ShowDrawer")


if __name__ == '__main__':
    run_test(__file__)
