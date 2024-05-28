from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Go to CRS as admin
-> Delete drawer session for non-admin from DB
-> Go to Drawer initialization and initialize drawer for non-admin user
Go to CRS as non-admin
-> Go to Drawer initialization > Drawer should be initialized
    """

tags = ["48999_location_2"]


class test(TestParent):                                                                # noqa
    user_index = 1

    def __init__(self, data):
        data["orderheader"] = "guest"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        if self.data.env.get("drawer", {}).get("type") == "workstation":
            self.actions.step("Drawer type - per workstation. Test skipped.")
            return
        non_admin = self.data.get("env").get("user")[self.user_index]
        drawer_id = self.api.balance_drawer(self.data, self.user_index).get_drawer_id()
        # Go to CRS
        self.atom.CRS.general.go_to_crs()
        # Delete drawer session for non-admin user
        self.lib.db_with_vpn.delete_drawer_session(drawer_id=drawer_id)
        # Go to Initialize Balance drawer
        self.lib.CRS.balance_drawer.go_to_initialize_drawer()
        # and init drawer for non-admin user
        self.lib.CRS.balance_drawer.initialize_drawer_for_another_user(user_name=non_admin)
        assert self.lib.db_with_vpn.get_active_balance_session(
            drawer_id=drawer_id), "The balance session didn't initialized"
        # Login to CRS with non-admin user and check drawer
        self.actions.open_browser()
        self.atom.CRS.general.go_to_crs(self.user_index)
        self.lib.CRS.balance_drawer.go_to_initialize_drawer(should_be_initialized=True)


if __name__ == '__main__':
    run_test(__file__)
