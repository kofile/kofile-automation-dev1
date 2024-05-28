from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS with admin user
    -> Go to Balance Drawer Cash Reconciliation screen
    -> Input any data to all input fields
    -> Click 'Submit' button
    -> Check actual amount for CASH
        """

tags = ["48999_location_2"]


class test(TestParent):                                                                     # noqa

    def __init__(self, data):
        data["orderheader"] = "guest"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to CRS
        self.atom.CRS.general.go_to_crs()
        # Initialize drawer via API and go to Balance drawer
        self.lib.CRS.balance_drawer.go_to_balance_drawer(initialize=True)
        # Fill cash reconciliation fields and check total
        total_cash = self.lib.CRS.balance_drawer.fill_cash_reconciliation()
        # Click 'Submit' button
        self.lib.CRS.balance_drawer.click_submit_cash_reconciliation()
        # Get Actual cash from Drawer Summary and compare with total cash from reconciliation screen
        actual_cash = float(self.lib.CRS.balance_drawer.get_balance_drawer_data()["Cash"]["Actual"])
        assert total_cash == actual_cash, f"Actual CASH '{actual_cash}' not equal to " \
                                          f"total CASH '{total_cash}' in reconciliation screen"


if __name__ == '__main__':
    run_test(__file__)
