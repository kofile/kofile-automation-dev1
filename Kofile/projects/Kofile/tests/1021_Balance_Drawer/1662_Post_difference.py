from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Go to CRS -> Balance Drawer
-> Click 'Post Difference' -> Click 'Cancel' on 'Post Difference pop-up' 
-> Click 'Post Difference' again -> Select payment and click post
-> Go back to Order Queue -> Balance Drawer > Drawer isn't initialized
    """

tags = ["48999_location_2"]


class test(TestParent):                                                                    # noqa
    user_index = 0

    def __init__(self, data):
        data["orderheader"] = "guest"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to CRS
        self.atom.CRS.general.go_to_crs(self.user_index)
        # Go to Balance drawer
        drawer_api = self.api.balance_drawer(self.data, self.user_index)
        self.lib.db_vpn.delete_drawer_session(drawer_id=drawer_api.get_drawer_id())
        self.lib.CRS.balance_drawer.go_to_balance_drawer(initialize=True, user_index=self.user_index)
        # Click 'Post Difference' button > and Cancel
        self.lib.CRS.balance_drawer.click_post_difference()
        self.lib.CRS.balance_drawer.click_post_difference__cancel()
        # Click 'Post Difference' button > and Post
        self.lib.CRS.balance_drawer.click_post_difference()
        self.lib.CRS.balance_drawer.click_post_difference__post()
        # Go to 'Initialize Drawer' and check drawer
        self.lib.CRS.balance_drawer.go_to_initialize_drawer(should_be_initialized=False)
        # Unpost drawer session
        drawer_api.unpost_drawer_session(self.user_index)


if __name__ == '__main__':
    run_test(__file__)
