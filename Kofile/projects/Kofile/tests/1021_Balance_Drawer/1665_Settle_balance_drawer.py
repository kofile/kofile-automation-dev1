from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS -> Balance Drawer
    -> Click 'Post Difference' -> Click 'Cancel' on 'Post Difference pop-up' 
    -> Click 'Settle' button > "Drawer was successfully settled message" is displayed
        """

tags = ["48999_location_2"]


class test(TestParent):                                                                       # noqa
    user_index = 0

    def __init__(self, data):
        data["orderheader"] = "guest"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to CRS
        self.atom.CRS.general.go_to_crs(self.user_index)
        # Go to Balance drawer
        self.lib.CRS.balance_drawer.go_to_balance_drawer(initialize=True, user_index=self.user_index)
        # Click 'Settle' button
        self.lib.CRS.balance_drawer.click_settle_button()


if __name__ == '__main__':
    run_test(__file__)
