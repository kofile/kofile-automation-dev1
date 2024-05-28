from runner import run_test
from projects.Kofile.Lib.test_parent import TestParent

description = """
    Go to CRS ->
    Workflow Order Step ->
    Workflow Capture Step ->
    Workflow indexing Step ->
    Re-key configuration flag is enabled for property grids, document grids, party names ->
    Check the availability of View Indexing data action link for Property section ->
    Click View Indexing Data -> INDEXED PROPERTY with all indexing data visible as read-only is opened at the top left
    corner of the Verification window ->
    Check the number of rows in INDEXED PROPERTY grid -> INDEXED PROPERTY fits 5 rows. If number of rows exceeds 5 rows
    a scroll appears. ->
    Check implicit auto-closing of INDEXED PROPERTY grid -> INDEXED PROPERTY is auto-closed upon navigating avay from
    the re-key grids.
    Check the availability of View Indexing data action link for Document section ->
    Click View Indexing Data -> INDEXED PROPERTY with all indexing data visible as read-only is opened at the top left
    corner of the Verification window ->
    Check the number of rows in INDEXED PROPERTY grid -> INDEXED PROPERTY fits 5 rows. If number of rows exceeds 5 rows
    a scroll appears. ->
    Check implicit auto-closing of INDEXED PROPERTY grid -> INDEXED PROPERTY is auto-closed upon navigating avay from
    the re-key grids.
    Check the availability of View Indexing data action link for Party names section ->
    Click View Indexing Data -> INDEXED PROPERTY with all indexing data visible as read-only is opened at the top left
    corner of the Verification window ->
    Check the number of rows in INDEXED PROPERTY grid -> INDEXED PROPERTY fits 5 rows. If number of rows exceeds 5 rows
    a scroll appears. ->
    Check implicit auto-closing of INDEXED PROPERTY grid -> INDEXED PROPERTY is auto-closed upon navigating avay from
    the re-key grids.
        """

tags = []


class test(TestParent):

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.general_helper.check_order_type()
        # Create and Finalize order
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        # Capture order
        self.lib.general_helper.find_and_click(("id", "ScanAllDocuments", "ScanAllDocuments btn"))
        self.lib.CRS.order_item_type.capture_step()
        # Indexing Queue
        self.lib.CRS.order_item_type.indexing_step(prop_type=True, store_doc_grids=True, store_party_names=True)
        # Verification Queue
        self.lib.CRS.order_item_type.index_order(self.lib.CRS.crs.go_to_verification_queue,
                                                 fill_required_fields=False)
        # Check View Indexing Data for Document section
        self.lib.CRS.verification_entry.check_view_indexing_data('document',
                                                                 self.pages.CRS.verification_entry.parcel_id_input)
        # Check View Indexing Data for Party Names section
        self.actions.refresh_page()
        self.lib.CRS.verification_entry.check_view_indexing_data('grantor',
                                                                 self.pages.CRS.verification_entry.parcel_id_input)
        self.actions.refresh_page()
        self.lib.CRS.verification_entry.check_view_indexing_data('grantee',
                                                                 self.pages.CRS.verification_entry.parcel_id_input)
        # Check View Indexing Data for Property section
        self.actions.refresh_page()
        self.lib.CRS.verification_entry.check_view_indexing_data('property',
                                                                 self.pages.CRS.verification_entry.parcel_id_input)


if __name__ == '__main__':
    run_test(__file__)
