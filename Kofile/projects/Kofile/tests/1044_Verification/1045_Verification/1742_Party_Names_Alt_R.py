"""69873 Shortcut keys and Alt+R functionality"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
                Steps:
                1. Create order and process to Verification
                2. Fill 'Grantor' field with new test_name using account name
                3. Add new Grantor 
                4. Press 'Alt+R'
                5. Verify that inserted name and previous Grantor name are same
                6. Fill 'Grantee' field with new test_name using account name
                7. Add new Grantee
                8. Press 'Alt+R'
                9. Verify that inserted name and previous Grantee name are same
              """

tags = ["48999_location_2"]


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.general_helper.check_order_type()
        # Create and Finalize order
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        if self.data["OIT"] == "RP_Recordings":
            self.atom.CRS.general.go_to_crs()
        # Capture order
        self.lib.CRS.order_item_type.capture_step()
        # Indexing Queue
        self.lib.CRS.order_item_type.indexing_step()
        # Verification Queue
        self.lib.CRS.order_item_type.index_order(self.lib.CRS.crs.go_to_verification_queue)
        self.lib.general_helper.find_and_check_uncheck_checkbox(self.pages.CRS.indexing_entry.type_ahead_checkbox,
                                                                False)
        account_name = self.data.config.order_header_fill(f'{self.data.orderheader}.value') + '-Grantor'
        # Fill Grantor field with test_name using account name
        self.lib.general_helper.find_and_send_keys(
            self.pages.CRS.indexing_entry.grantor_name_input, account_name + self.keys.TAB)
        # Add new Grantor
        self.lib.CRS.order_entry.click_parties__add_grantor()
        index = len(self.actions.get_browser().find_all(self.pages.CRS.indexing_entry.grantor_name_input))
        new_grantor = self.lib.general_helper.find_and_click(self.lib.general_helper.make_locator(
            self.pages.CRS.verification_entry._grantor_name_by_index, index))
        self.actions.wait(2)
        # Press Alt+R in new added Grantor
        self.actions.send_keys(new_grantor, (self.keys.ALT, "r"))
        self.actions.wait(2)
        new_grantor_value = self.actions.get_element_value(new_grantor)[:-1]
        # Verify that inserted name and previous Grantor name are same
        self.actions.assert_equals(new_grantor_value.upper(), account_name.upper())
        account_name = self.data.config.order_header_fill(f'{self.data.orderheader}.value') + '-Grantee'
        # Fill Grantee field with test_name using account name
        self.lib.general_helper.find_and_send_keys(self.pages.CRS.indexing_entry.grantee_name_input,
                                                   account_name + self.keys.TAB)
        # Add new Grantee
        self.lib.CRS.order_entry.click_parties__add_grantee()
        index = len(self.actions.get_browser().find_all(self.pages.CRS.indexing_entry.grantee_name_input))
        new_grantee = self.lib.general_helper.find_and_click(self.lib.general_helper.make_locator(
            self.pages.CRS.verification_entry._grantee_name_by_index, index))
        self.actions.wait(2)
        # Press Alt+R in new added Grantee
        self.actions.send_keys(new_grantee, (self.keys.ALT, "r"))
        self.actions.wait(2)
        new_grantee_value = self.actions.get_element_value(new_grantee)[:-1]
        # Verify that inserted name and previous Grantee name are same
        self.actions.assert_equals(new_grantee_value.upper(), account_name.upper())


if __name__ == '__main__':
    run_test(__file__)
