from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Go to CRS with admin user, create and finalize order with 'Check' payment method
-> Go to Balance Drawer Cash Reconciliation screen
-> Input any data to all input fields
-> Compare Sum of amounts with Total Amount > Values are the same
-> Click on Clear button > All input fields are empty, Total amount also removed
    """

tags = ["48999_location_2"]


class test(TestParent):                                                              # noqa
    user_index = 0

    def __init__(self, data):
        data["orderheader"] = "guest"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to CRS
        self.atom.CRS.general.go_to_crs(self.user_index)
        # Initialize drawer via API and go to Balance drawer
        self.lib.CRS.balance_drawer.go_to_balance_drawer(initialize=True, user_index=self.user_index)
        # Fill cash reconciliation fields and check total
        self.lib.CRS.balance_drawer.fill_cash_reconciliation()
        # 'Clear' cash reconciliation fields and check all fields and total
        self.lib.CRS.balance_drawer.clear_cash_reconciliation()


if __name__ == '__main__':
    run_test(__file__)
