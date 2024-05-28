from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test


description = """
Go to CRS
-> Create and finalize order without document
-> Delete drawer session from DB
-> Click 'Add new order' > Drawer initialization pop-up displays -> Close pop-up
-> Click 'Next order' > Drawer initialization pop-up displays -> Close pop-up
-> Go to Order Search, find created order
-> Click Edit Order and Assert drawer initialization popup exists   
-> Click Initialize and wait finalization screen is opened        
    """

tags = ["48999_location_2"]


class test(TestParent):                                                              # noqa
    user_index = 0

    def __init__(self, data):
        data["orderheader"] = "guest"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        if not self.data.env.get("drawer", {}).get("init_popup", True):
            self.actions.step("Drawer init pop-up isn't configured for current tenant. Test skipped.")
            return

        # Go to CRS
        self.atom.CRS.general.go_to_crs(self.user_index)
        # Create and finalize OIT without doc
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)

        # Delete drawer session from DB
        self.lib.db_with_vpn.delete_drawer_session(
            drawer_id=self.api.balance_drawer(self.data, self.user_index).get_drawer_id())
        self.lib.CRS.crs.go_to_order_queue()
        # Click (+) and check init pop-up
        self.lib.CRS.order_queue.add_new_order(init_popup=True, init=False)
        self.lib.CRS.crs.go_to_order_queue()
        # Click (Next order) and check init pop-up
        self.lib.CRS.order_queue.next_order(init_popup=True, init=False)
        self.lib.CRS.crs.go_to_order_search()
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
        # Click edit icon and verify drawer initialization popup is appeared
        self.lib.CRS.order_search.click_edit_icon(self.data["order_number"])
        assert self.lib.general_helper.check_if_element_exists(self.pages.CRS.balance_drawer.pup_drawer_initialization)
        # Click initialize button on popup
        self.actions.click(self.pages.CRS.balance_drawer.pup_drawer_btn_inititialize)
        # Wait order finalization screen is opened
        self.actions.wait_for_element_displayed(self.pages.CRS.order_finalization.lbl_order_finalize_label)


if __name__ == '__main__':
    run_test(__file__)
