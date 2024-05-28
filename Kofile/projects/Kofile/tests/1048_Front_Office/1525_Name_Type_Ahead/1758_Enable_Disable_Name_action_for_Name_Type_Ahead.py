from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Navigate to CRS -> Navigate to Front Office -> Navigate to "Name Type-Ahead" sub-tab ->
    Select department e.g. "Real Property Records" in dropdown list ->
    Click on the "Search" button ->
    Enter any existing party name e.g. "Arthur" ->
    Select name with unchecked "Disable" checkbox e.g. "Arthur Baker" and check checkbox ->
    Click on the "Save" button ->
    Navigate to Order Queue ->
    Add new order e.g. RP and process to Indexing ->
    Navigate to Indexing Queue and open processed order ->
    Check "Party Name Type Ahead" checkbox ->
    Navigate to Grantor/Grantee field and enter"Arthur" party name ->
    Navigate to Front Office and uncheck "Disable" checkbox for "Arthur Baker" party name ->
    Click on the "Save" button ->
    Navigate back to Indexing Entry page ->
    Navigate to Grantor/Grantee field and enter"Arthur" party name ->
    Save order and process to the next step ->
    Repeat entering party name with enabled/disabled action in Front Office ->
    Party name is displayed in party names list if it is enabled in Front Office,
    otherwise party name is missing in party names list
    """

tags = []


class test(TestParent):                                                                          # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.data_helper.get_front_office()
        self.atom.CRS.general.go_to_crs()
        # Navigate to Front Office and check 'Allow Company Account with Ordering' option
        self.lib.CRS.front_office.go_to_name_type_ahead()
        self.lib.CRS.front_office.select_department()
        self.lib.CRS.front_office.enable_name_and_select_by_name(False)
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.order_item_type.scan_and_map()
        self.lib.CRS.order_item_type.save_order_in_capture_step()

        # check indexing with enabled type and head
        self.lib.CRS.order_item_type.index_order()
        self.lib.general_helper.find_and_check_uncheck_checkbox(self.pages.CRS.indexing_entry.type_ahead_checkbox, True)
        self.lib.CRS.indexing_entry.check_exist_grantor_and_grantee_type_and_head()

        # check indexing with disable type and head
        self.lib.CRS.front_office.go_to_name_type_ahead()
        self.lib.CRS.front_office.select_department()
        self.lib.CRS.front_office.enable_name_and_select_by_name(True)
        self.lib.CRS.order_item_type.index_order()
        self.lib.general_helper.find_and_check_uncheck_checkbox(self.pages.CRS.indexing_entry.type_ahead_checkbox, True)
        self.lib.CRS.indexing_entry.check_exist_grantor_and_grantee_type_and_head(False)

        # provide order to verification step
        self.lib.CRS.order_item_type.save_order_in_index_entry()
        self.lib.CRS.order_item_type.next_order_in_index_summary()

        # check verification with disable type and head
        self.lib.CRS.order_item_type.index_order(self.lib.CRS.crs.go_to_verification_queue)
        self.lib.general_helper.find_and_check_uncheck_checkbox(self.pages.CRS.indexing_entry.type_ahead_checkbox, True)
        self.lib.CRS.indexing_entry.check_exist_grantor_and_grantee_type_and_head(False)

        # check verification with enabled type and head
        self.lib.CRS.front_office.go_to_name_type_ahead()
        self.lib.CRS.front_office.select_department()
        self.lib.CRS.front_office.enable_name_and_select_by_name(False)
        self.lib.CRS.order_item_type.index_order(self.lib.CRS.crs.go_to_verification_queue)
        self.lib.general_helper.find_and_check_uncheck_checkbox(self.pages.CRS.indexing_entry.type_ahead_checkbox, True)
        self.lib.CRS.indexing_entry.check_exist_grantor_and_grantee_type_and_head(True)
        self.actions.step(f"--- SMOKE TEST END --- {__name__} ---")


if __name__ == '__main__':
    run_test(__file__)
