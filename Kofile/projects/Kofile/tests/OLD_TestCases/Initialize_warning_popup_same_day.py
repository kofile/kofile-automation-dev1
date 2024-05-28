from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Go to CRS -> Balance Drawer -> Init drawer if needed
-> Close drawer session
-> Go to Order Queue -> Click 'Add new order(+)' > Warning pop-up should displays
-> Go to Balance Drawer and unpost closed session
-> Go to Order Queue -> Click 'Add new order(+)' > New order page opened
    """

tags = []


class test(TestParent):                                                             # noqa
    user_index = 0

    def __init__(self, data):
        data["orderheader"] = "guest"
        super(test, self).__init__(data, __name__)

    def __test__(self):

        if not self.data.env.get("drawer", {}).get("init_same_day_popup", True):
            self.actions.step("Drawer 'same day init pop-up' isn't configured for current tenant. Test skipped.")
            return
        # Go to CRS
        self.atom.CRS.general.go_to_crs(self.user_index)
        # Go to Initialize Balance drawer
        if not self.lib.CRS.balance_drawer.go_to_initialize_drawer():  # If drawer NOT initialized
            # try to restore closed drawer session
            # if closed session not found
            session_closed = self.api.balance_drawer(self.data).unpost_drawer_session(self.user_index)
            if not session_closed:
                # Init drawer
                self.lib.CRS.balance_drawer.click_submit_drawer_initialization()
        # Close drawer session
        self.lib.CRS.balance_drawer.go_to_balance_drawer()
        self.lib.CRS.balance_drawer.click_post_difference(post=True)
        # Click (+) and check Warning pop-up
        self.lib.CRS.order_queue.add_new_order(warning_popup=True)
        # Restore drawer session
        self.lib.CRS.balance_drawer.go_to_initialize_drawer()
        self.lib.CRS.balance_drawer.restore_closed_drawer_session(
            user_name=self.data.get("env").get("user")[self.user_index])
        # Back to Order Queue and add new order
        self.lib.CRS.crs.go_to_order_queue()
        self.lib.CRS.order_queue.add_new_order(warning_popup=False)


if __name__ == '__main__':
    run_test(__file__)