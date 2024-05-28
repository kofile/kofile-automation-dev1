"""69869 Party Name Type Ahead checkbox and functionality"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
                Steps:
                1. Navigate to Front Office-> Name Type-Ahead, uncheck 'Disable' option for test name if it is checked
                2. Create order and process to Verification
                3. Insert test name in Grantor/Grantee fields. Check that test name is available in DDL
                4. Navigate to Front Office-> Name Type-Ahead and check 'Disable' option for test name
                5. Navigate to Verification Entry page
                6. Insert test name in Grantor/Grantee fields. Check that test name is not available in DDL
                7. Navigate to Front Office-> Name Type-Ahead and uncheck 'Disable' option for test name
                8. Navigate to Verification Entry page
                9. Insert test name in Grantor/Grantee fields. Check that test name is available in DDL
             """

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: no
        Post-conditions: Order in Verification Entry page is opened.
        Grantor/Grantee fields are filled with test name. Test name is available in DDL
        """
        self.lib.data_helper.get_front_office()
        self.atom.CRS.general.go_to_crs()
        # Navigate to Front Office and uncheck 'Disable' option for test name if it is checked
        self.lib.CRS.front_office.go_to_name_type_ahead()
        self.lib.CRS.front_office.select_department()
        self.lib.CRS.front_office.enable_name_and_select_by_name(False)
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
        self.lib.CRS.order_item_type.re_key_in_verification()
        # Check that test name is available in DDL if 'Disable' option is unchecked
        self.lib.general_helper.find_and_check_uncheck_checkbox(
            self.pages.CRS.indexing_entry.type_ahead_checkbox, True)
        self.lib.CRS.indexing_entry.check_exist_grantor_and_grantee_type_and_head(
            True)
        # Check that test name is not available in DDL if 'Disable' option is checked
        self.lib.CRS.front_office.go_to_name_type_ahead()
        self.lib.CRS.front_office.select_department()
        self.lib.CRS.front_office.enable_name_and_select_by_name(True)
        self.lib.CRS.order_item_type.index_order(self.lib.CRS.crs.go_to_verification_queue)
        self.lib.CRS.order_item_type.re_key_in_verification()
        self.lib.general_helper.find_and_check_uncheck_checkbox(
            self.pages.CRS.indexing_entry.type_ahead_checkbox, True)
        self.lib.CRS.indexing_entry.check_exist_grantor_and_grantee_type_and_head(
            False)
        # Check that test name is available in DDL if 'Disable' option is unchecked
        self.lib.CRS.front_office.go_to_name_type_ahead()
        self.lib.CRS.front_office.select_department()
        self.lib.CRS.front_office.enable_name_and_select_by_name(False)
        self.lib.CRS.order_item_type.index_order(self.lib.CRS.crs.go_to_verification_queue)
        self.lib.CRS.order_item_type.re_key_in_verification()
        self.lib.general_helper.find_and_check_uncheck_checkbox(
            self.pages.CRS.indexing_entry.type_ahead_checkbox, True)
        self.lib.CRS.indexing_entry.check_exist_grantor_and_grantee_type_and_head(
            True)


if __name__ == '__main__':
    run_test(__file__)
