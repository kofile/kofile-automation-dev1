from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    - Go to CRS and create new order
    - Select Assumed Name OIT, fill party name and address information
    - Click 'Copy to Return by Mail' link and navigate to Order item tab
    - check fields under 'Return By Mail' checkbox
    -> Party address is copied to Return by Mail section"""


class test(TestParent):                                                                          # noqa
    user_index = 2

    def __init__(self, data):
        data["OIT"] = "Assumed_Name"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs(self.user_index)
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.select_order_type()
        parties = self.lib.CRS.order_entry.fill_business_name_and_address_fields()
        self.lib.CRS.order_entry.click_copy_to_return_by_mail_link()
        self.lib.general_helper.find_and_click(self.lib.CRS.order_entry.tab_locator("Order_Item"))
        copied_parties = self.lib.CRS.order_entry.get_return_by_mail_values()

        assert parties == copied_parties, f"Expected values '{parties}' is not equal to {copied_parties}"


if __name__ == '__main__':
    run_test(__file__)
