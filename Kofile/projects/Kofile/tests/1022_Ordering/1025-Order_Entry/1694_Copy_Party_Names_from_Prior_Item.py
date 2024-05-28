from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    - Go to CRS and create new order
    - Select RP OIT, fill Parties and all required fields 
    - Click 'Add to order'
    - on Order Summary screen Click 'Add new Order' and add another OIT with Parties
    - Navigate to Party tab and click 'Copy Names' -> Pop-up is opened
    - Click 'Copy From Prior Item' link
    -> Parties names from 1st OIT is filled correspondingly"""


class test(TestParent):                                                                           # noqa
    user_index = 2
    parties = {"Grantor": ["Grantor_first", "Grantor_last", "Grantor_middle", "Mr."],
               "Grantee": ["Grantee_first", "Grantee_last", "Grantee_middle", "Mrs."]}

    def __init__(self, data):
        data["OIT"] = "RP_Recordings"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs(self.user_index)
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.fill_order_header_name()
        # fill Parties
        self.lib.CRS.order_entry.fill_parties_values(self.parties["Grantor"], self.parties["Grantee"])
        parties = self.lib.CRS.order_entry.get_parties_values()
        self.atom.CRS.order_entry.one_oit_to_summary()
        # add new OIT
        self.lib.CRS.order_summary.click_new_order_item_icon()
        self.atom.CRS.order_entry.select_order_type()
        # Copy names from prior item and check values
        self.lib.CRS.order_entry.copy_parties_names()
        copied_parties = self.lib.CRS.order_entry.get_parties_values()

        assert parties == copied_parties, f"Expected values '{parties}' is not equal to {copied_parties}"


if __name__ == '__main__':
    run_test(__file__)
