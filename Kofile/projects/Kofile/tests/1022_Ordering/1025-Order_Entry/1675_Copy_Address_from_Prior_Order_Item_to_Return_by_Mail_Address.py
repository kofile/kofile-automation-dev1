from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    - Go to CRS and create new order
    - Select RP OIT, fill all required fields and 'Return by mail' fields and click 'Add to order'
    - On Order Summary Screen: click on New order item icon and add another OIT with Return By mail checkbox
    - Click 'Return by mail' checkbox
    - Click Copy From Prior Order Item link -> Information from first order is filled in Return by mail fields"""


class test(TestParent):                                                                               # noqa
    user_index = 2

    def __init__(self, data):
        data["OIT"] = "RP_Recordings"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs(self.user_index)
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.fill_order_header_name()
        self.lib.CRS.order_entry.click_return_by_mail_checkbox()
        return_by_mail = self.lib.CRS.order_entry.fill_return_by_mail_fields()
        self.atom.CRS.order_entry.one_oit_to_summary()

        self.data["current_oit"] = "Copies"
        self.lib.CRS.order_summary.click_new_order_item_icon()
        self.atom.CRS.order_entry.select_order_type()
        self.lib.CRS.order_entry.click_copy_from_prior_order_item_link()
        return_by_mail_copy = self.lib.CRS.order_entry.get_return_by_mail_values()
        assert return_by_mail == return_by_mail_copy, f"Expected values '{return_by_mail}' " \
                                                      f"is not equal to {return_by_mail_copy}"


if __name__ == '__main__':
    run_test(__file__)
