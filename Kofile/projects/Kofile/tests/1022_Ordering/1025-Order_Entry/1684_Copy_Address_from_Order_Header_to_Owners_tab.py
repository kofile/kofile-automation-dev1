from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    - Go to CRS and create new order
    - Select Marks and Brands OIT, fill order header
    - Navigate to Owners tab with 'Copy Mailing Address' option
    - Click 'Copy Mailing Address' link -> Customer address is copied from Order Header to Owners tab"""


class test(TestParent):                                                                           # noqa
    user_index = 2

    def __init__(self, data):
        data["OIT"] = "Marks_and_Brands"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs(self.user_index)
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.fill_order_header_name()
        customer_info = self.lib.CRS.order_entry.get_order_header_customer_info(state_name=False)
        self.lib.general_helper.find_and_click(self.lib.CRS.order_entry.tab_locator("Owners"))
        self.lib.CRS.order_entry.click_copy_mailing_address_link()
        return_by_mail = self.lib.CRS.order_entry.get_return_by_mail_values()

        assert return_by_mail == customer_info, f"Expected values '{customer_info}' is not equal to '{return_by_mail}'"


if __name__ == '__main__':
    run_test(__file__)
