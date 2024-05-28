from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS, create new order -> process order, add tracking ID
    -> search order by tracking ID - > Edit found order -> remove tracking ID and finalize order
    -> search order by tracking ID - > Not found
        """

tags = ['48999_location_2']


class test(TestParent):                                                                             # noqa

    def __init__(self, data):
        data["current_oit"] = data["OIT"] = "Copies"
        data["orderheader"] = "guest"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to CRS
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.order_summary.add_tracking_id)
        # Search order by Tracking ID
        self.atom.CRS.order_search.search_order_by_tracking_id()
        # Edit found order
        edit_order_loc = self.pages.CRS.order_search.edit_order_icon_by_order_number(self.data.order_number)
        self.lib.general_helper.find_and_click(edit_order_loc)
        # Remove Tracking ID
        self.lib.CRS.order_summary.click_remove_tracking_id_button()
        # Finalize
        self.atom.CRS.add_payment.finalize_order()
        # Search order by Tracking ID
        self.lib.CRS.crs.go_to_order_search()
        self.atom.CRS.order_search.search_order_by_tracking_id()
        # Order should not be found
        assert not self.lib.CRS.order_search.check_order_present_in_result(self.data.order_number)


if __name__ == '__main__':
    run_test(__file__)
