from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    - Go to CRS and create new order
    - Select RP OIT
    - In parties tab add several new party and fill parties
    - Click delete icon next to one of parties -> Party is deleted
    - Change Parties ordering (via Up/Down icons) -> Ordering is changed"""


class test(TestParent):                                                                         # noqa
    user_index = 2
    parties_1 = {"Grantor": ["Grantor_first_1", "Grantor_last_1", "Grantor_middle_1", "Mr. 1"],
                 "Grantee": ["Grantee_first_1", "Grantee_last_1", "Grantee_middle_1", "Mrs. 1"]}
    parties_2 = {"Grantor": ["Grantor_first_2", "Grantor_last_2", "Grantor_middle_2", "Mr. 2"],
                 "Grantee": ["Grantee_first_2", "Grantee_last_2", "Grantee_middle_2", "Mrs. 2"]}
    parties_3 = {"Grantor": ["Grantor_first_3", "Grantor_last_3", "Grantor_middle_3", "Mr. 3"],
                 "Grantee": ["Grantee_first_3", "Grantee_last_3", "Grantee_middle_3", "Mrs. 3"]}
    errors = []

    def __init__(self, data):
        data["OIT"] = "RP_Recordings"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs(self.user_index)
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.select_order_type()
        self.lib.CRS.order_entry.fill_parties_values(self.parties_1["Grantor"], self.parties_1["Grantee"])
        parties_1 = self.lib.CRS.order_entry.get_parties_values()
        # add and fill 2-nd parties
        self.lib.CRS.order_entry.click_parties__add_grantor()
        self.lib.CRS.order_entry.click_parties__add_grantee()
        self.lib.CRS.order_entry.fill_parties_values(self.parties_2["Grantor"], self.parties_2["Grantee"], index=2)
        parties_2 = self.lib.CRS.order_entry.get_parties_values(2)
        # add and fill 3-rd parties
        self.lib.CRS.order_entry.click_parties__add_grantor()
        self.lib.CRS.order_entry.click_parties__add_grantee()
        self.lib.CRS.order_entry.fill_parties_values(self.parties_3["Grantor"], self.parties_3["Grantee"], index=3)
        parties_3 = self.lib.CRS.order_entry.get_parties_values(3)
        # move parties
        self.lib.CRS.order_entry.click_parties__up_button(index=2)  # move 2-nd grantor UP
        self.lib.CRS.order_entry.click_parties__down_button(grantor=False, index=1)  # move 1-st grantee down
        moved_parties_1 = self.lib.CRS.order_entry.get_parties_values(1)
        moved_parties_2 = self.lib.CRS.order_entry.get_parties_values(2)
        if moved_parties_1 != parties_2:
            msg = f"2-nd and 1-st parties should be reversed." \
                  f"\nExpected values '{parties_2}' is not equal to '{moved_parties_1}'."
            self.errors.append(msg)
            self.actions.error(msg)
        if moved_parties_2 != parties_1:
            msg = f"1-st and 2-nd parties should be reversed.\n" \
                  f"Expected values '{parties_1}' is not equal to '{moved_parties_2}'."
            self.errors.append(msg)
            self.actions.error(msg)
        # delete parties
        self.lib.CRS.order_entry.click_parties__delete_button(index=2)  # delete 2-nd grantor
        self.lib.CRS.order_entry.click_parties__delete_button(grantor=False, index=2)  # delete 2-nd grantee
        moved_parties_3 = self.lib.CRS.order_entry.get_parties_values(2)
        if moved_parties_3 != parties_3:
            msg = f"2-nd parties should be removed.\n" \
                  f"Expected values '{parties_3}' is not equal to '{moved_parties_3}'."
            self.errors.append(msg)
            self.actions.error(msg)
        assert not self.errors, self.errors


if __name__ == '__main__':
    run_test(__file__)
