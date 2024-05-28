"""69872 Alt Slash functionality"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
                Steps:
                1. Create order and process to Verification
                2. Fill 'Grantor' field with new test_name using account name
                3. Move cursor back to left with several positions
                4. Press 'Alt+/'
                5. Check that Grantor name is split into 2 names
                6. Check that Grantor1+Grantor2 equals test_name
                7. Fill 'Grantee' field with new test_name using account name
                8. Move cursor back to left with several positions
                9. Press 'Alt+/'
                10. Check that Grantee name is split into 2 names
                11. Check that Grantee1+Grantee2 equals test_name   
              """

tags = []


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
        account_name = self.data.config.order_header_fill(f'{self.data.orderheader}.value')
        # Fill Grantor field with test_name using account name
        gr = self.lib.general_helper.find_and_send_keys(self.pages.CRS.indexing_entry.grantor_name_input,
                                                        account_name)
        # Move cursor back to left with several positions
        for _ in range(4):
            self.actions.send_keys(gr, self.keys.LEFT)
        self.actions.wait(2)
        # Press 'Alt+/'
        self.actions.send_keys(gr, (self.keys.ALT, "/"))
        self.actions.wait(1)
        first_grantor_row = self.actions.get_element_value(gr)[:-1]
        index = len(self.actions.get_browser().find_all(self.pages.CRS.indexing_entry.grantor_name_input))
        # Check that Grantee name is split into 2 names
        self.actions.assert_equals(index, 2)
        second_grantor_row = self.actions.get_element_value(self.lib.general_helper.make_locator(
            self.pages.CRS.verification_entry._grantor_name_by_index, index))
        # Check that Grantor1 + Grantor2 equals original name
        self.actions.assert_equals((first_grantor_row + second_grantor_row).lower(), account_name.lower())
        # Fill Grantee field with test_name using account name
        ge = self.lib.general_helper.find_and_send_keys(self.pages.CRS.indexing_entry.grantee_name_input,
                                                        account_name)
        # Move cursor back to left with several positions
        for _ in range(4):
            self.actions.send_keys(ge, self.keys.LEFT)
        self.actions.wait(2)
        # Press 'Alt+/'
        self.actions.send_keys(ge, (self.keys.ALT, "/"))
        self.actions.wait(1)
        first_grantee_row = self.actions.get_element_value(ge)[:-1]
        index = len(self.actions.get_browser().find_all(self.pages.CRS.indexing_entry.grantor_name_input))
        # Check that Grantee name is split into 2 names
        self.actions.assert_equals(index, 2)
        second_grantee_row = self.actions.get_element_value(self.lib.general_helper.make_locator(
            self.pages.CRS.verification_entry._grantee_name_by_index, index))
        # Check that Grantee1 + Grantee2 equals original name
        self.actions.assert_equals((first_grantee_row + second_grantee_row).lower(), account_name.lower())


if __name__ == '__main__':
    run_test(__file__)
