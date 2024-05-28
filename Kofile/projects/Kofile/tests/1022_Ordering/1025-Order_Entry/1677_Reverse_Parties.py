from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    - Go to CRS and create new order
    - Select RP OIT, fill Parties fields 
    - Click 'Reverse Parties' -> Grantor and Grantee values are changed in places"""


class test(TestParent):                                                                               # noqa
    user_index = 2
    parties = {"Grantor": ["Grantor_first_reverse", "Grantor_last_reverse", "Grantor_middle_reverse",
                           "Mr. reverse"],
               "Grantee": ["Grantee_first_reverse", "Grantee_last_reverse", "Grantee_middle_reverse",
                           "Mrs. reverse"]}

    def __init__(self, data):
        data["OIT"] = "RP_Recordings"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs(self.user_index)
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.select_order_type()

        self.lib.CRS.order_entry.fill_parties_values(self.parties["Grantor"], self.parties["Grantee"])
        parties_ = self.lib.CRS.order_entry.get_parties_values()
        self.lib.CRS.order_entry.click_reverse_parties_link()
        expected_parties = {"Grantor": parties_["Grantee"], "Grantee": parties_["Grantor"]}
        reversed_parties = self.lib.CRS.order_entry.get_parties_values()

        assert expected_parties == reversed_parties, f"Expected values '{expected_parties}' " \
                                                     f"is not equal to {reversed_parties}"


if __name__ == '__main__':
    run_test(__file__)
