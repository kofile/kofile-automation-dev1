from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS ->
    Workflow Order Step ->
    Workflow Capture Step ->
    Workflow indexing Step ->
    Re-key configuration flag is enabled for Party Names, Document grids ->
    Check Grantor/Grantee field data is blank and their count the same as in indexing ->
    Fill Grantor/Grantee field with data different from that entered in indexing step and tab out of the Grantor grid ->
    ReKey Verification Options popup appears, Verification Entry fields become read-only ->
    Resolve re-key popup by selecting one of the radio buttons ->
    Re-key field saves the data entered in verification or replaces with indexing data depending on the option
    selected -> Tab out to other grids -> System allows to navigate to other grids and edit them ->
    Repeat steps 1-4 with filling rekey grids via 'Copy Names' links ->
    Expected result for steps 1-4 -> Edit the document from Verification Summary page ->
    Data in re-Key fields is preserved on Verification Entry page as the page is opened ->
    Send the order back to indexing and re-process to Verification ->
    On Verification Entry page, Re key grids are blank again when opened even though previously re-keyed
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
        self.lib.CRS.order_item_type.indexing_step(store_doc_grids=True, store_party_names=True)
        # Verification Queue
        self.lib.CRS.order_item_type.index_order(self.lib.CRS.crs.go_to_verification_queue,
                                                 fill_required_fields=False)
        self.lib.CRS.verification_entry.fill_doc_fields(self.data)
        # Check Grantor/Grantee field data is blank and their count
        self.lib.CRS.verification_entry.check_party_names_are_empty()
        self.lib.CRS.verification_entry.check_party_names_count(self.data)
        # Check data comparison for Grantor/Grantee field
        self.lib.CRS.verification_entry.return_to_rekey_parties('Grantor Name', 'Grantee Name')
        self.actions.refresh_page()
        self.lib.CRS.verification_entry.fill_doc_fields(self.data)
        self.lib.CRS.verification_entry.return_to_rekey_parties('Grantee Name', 'Grantor Name')
        self.actions.refresh_page()
        self.lib.CRS.verification_entry.fill_doc_fields(self.data)
        self.lib.CRS.verification_entry.update_re_key_data_parties(self.data)
        self.actions.refresh_page()
        self.lib.CRS.verification_entry.fill_doc_fields(self.data)
        self.lib.CRS.verification_entry.restore_re_key_data_parties(self.data)
        # Checking  data comparison via 'Copy Names' functionality
        self.actions.refresh_page()
        self.lib.CRS.verification_entry.fill_doc_fields(self.data)
        self.lib.CRS.verification_entry.check_rekey_after_copy_names(self.data, 'Grantor')
        self.lib.CRS.verification_entry.check_rekey_after_copy_names(self.data, 'Grantee')
        # Edit document form the Verification summary screen and check party names data
        self.actions.refresh_page()
        self.lib.CRS.verification_entry.process_order_item_trough_verification_entry(self.data)
        self.lib.CRS.verification_summary.click_edit_order_item()
        self.lib.CRS.verification_entry.check_party_names_are_not_empty(self.data)
        # Send the order back to Indexing and re-process to Verification
        self.lib.CRS.verification_entry.process_rekey_and_send_to_indexing(self.data)
        self.lib.CRS.verification_summary.send_order_to_indexing()
        self.lib.CRS.order_item_type.indexing_step()
        self.lib.CRS.order_item_type.index_order(self.lib.CRS.crs.go_to_verification_queue,
                                                 fill_required_fields=False)
        self.lib.CRS.verification_entry.check_party_names_are_empty()


if __name__ == '__main__':
    run_test(__file__)
