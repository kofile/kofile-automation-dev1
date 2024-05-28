from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Go to CRS as non-admin
-> Delete drawer session for non-admin user
-> Create and finalize order with 'Cash' payment method
-> Go to balance drawer and check that payment is correct
Go to CRS as admin 
-> Go to Balance drawer -> Select non-admin opened session and check that payment is correct
-> Close non-admin drawer session
Go to CRS as non-admin
-> Go to initialize drawer -> Click Submit button 
    """

tags = ["48999_location_2"]


class test(TestParent):                                                                  # noqa
    user_index = 1

    def __init__(self, data):
        data["orderheader"] = "guest"
        data["current_oit"] = data["OIT"] = "Copies"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        if self.data.env.get("drawer", {}).get("type") == "workstation":
            self.actions.step("Drawer type - per workstation. Test skipped.")
            return
        # non-admin user
        non_admin = self.data.get("env").get("user")[self.user_index]
        # Go to CRS as non-admin
        self.atom.CRS.general.go_to_crs(self.user_index)
        # Delete drawer session for non-admin user
        drawer_id = self.api.balance_drawer(self.data, self.user_index).get_drawer_id()
        self.lib.db_with_vpn.delete_drawer_session(drawer_id=drawer_id)

        # Add new order and process it
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.order_item_description()
        self.atom.CRS.order_entry.fill_order_header_name()
        self.atom.CRS.order_entry.one_oit_to_summary()
        self.atom.CRS.add_payment.finalize_order()
        # Get drawer data after order
        self.lib.CRS.crs.go_to_order_queue()
        drawer_data = self.lib.CRS.balance_drawer.get_balance_drawer_data()

        # Go to CRS as admin
        self.actions.open_browser()
        self.atom.CRS.general.go_to_crs()
        # Check drawer data for non-admin user and close session
        self.lib.CRS.balance_drawer.select_balance_drawer_session(non_admin)
        drawer_data_2 = self.lib.CRS.balance_drawer.get_balance_drawer_data()
        assert drawer_data == drawer_data_2, f"'CASH' values is not the same!" \
                                             f"\n\tNon-admin: '{drawer_data}'\n\tAdmin: '{drawer_data_2}'"
        self.lib.CRS.balance_drawer.click_post_difference(post=True)

        # Go to CRS with non-admin user and check drawer
        self.actions.open_browser()
        self.atom.CRS.general.go_to_crs(self.user_index)
        self.lib.CRS.balance_drawer.go_to_initialize_drawer(should_be_initialized=False)
        self.lib.CRS.balance_drawer.click_submit_drawer_initialization()
        self.lib.CRS.order_queue.check_popup(warning_popup=False)
        # TOTO Need to add checking that submit button is disabled. after bug fix. Currently Submit button still enabled
        # Delete drawer session for non-admin user
        self.lib.db_with_vpn.delete_drawer_session(drawer_id=drawer_id)


if __name__ == '__main__':
    run_test(__file__)
