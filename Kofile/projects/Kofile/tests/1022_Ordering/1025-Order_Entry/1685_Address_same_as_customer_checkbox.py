from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    - Go to CRS and create new order
    - select an OIT with "Same as customer" checkbox (ex. Birth Certificate-State), fill order header
    - Navigate to tab with "Same as customer" checkbox
    - Check on "Same as customer" checkbox -> Customer address is copied from Order Header to the given tab"""


class test(TestParent):                                                                             # noqa
    user_index = 2

    def __init__(self, data):
        data["OIT"] = "Birth_Certificate_State"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs(self.user_index)
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.fill_order_header_name()
        customer_info = self.lib.CRS.order_entry.get_order_header_customer_info()
        self.lib.general_helper.find_and_click(self.lib.CRS.order_entry.tab_locator("Applicant"))
        self.lib.CRS.order_entry.click_same_as_customer_checkbox()
        same_as_customer = self.lib.CRS.order_entry.get_return_by_mail_values(state_name=True)

        assert same_as_customer == customer_info, f"Expected values " \
                                                  f"'{customer_info}' is not equal to {same_as_customer}"


if __name__ == '__main__':
    run_test(__file__)
