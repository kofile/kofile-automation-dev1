from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    o to CRS ->
    Workflow Order Step ->
    Workflow Capture Step ->
    Workflow indexing Step ->
    Re-key configuration flag is enabled for property grids ->
    Fill in a different number of property types than in Indexing and navigate out of the Property grid -> 
    Number of property types entered in Verification is compared to that of Indexing and
    "Indexed data contains n rows, ReKeyed data contains m rows. Return to ReKey? Yes/No" validation message is
    displayed to indicate mismatch. -> Click on Yes option ->
    Pop-up disappears with focus on re-key grids to adjust the data.
    -> Click on No option ->
    Save and Advance button becomes enabled. Clerk is allowed to proceed.
    -> Enter data into empty fields that mismatch indexing data and navigate out of Property grid ->
    ReKey Verification Options popup appears to choose between Save ReKey data or Restore Indexed Data.
    Save Changes button is disabled.
    All mismatching data is refreshed in RED font.
    All mismatching empty fields are refreshed with RED borders.
    -> Click the Return to Rekey link ->
    The popup is closed and Clerk is allowed to continue with re-key verification
    -> Repeat the step 4 and select the Save Rekey Data option in ReKey Verification Options popup ->
    Document Property data is updated with the re-keyed data.
    Indexed Property data is moved to version tables after Save&Advance.
    -> Repeat the step 4 and select the Restore Indexed Data. option in ReKey Verification Options popup ->
    -> Property grid is refreshed with indexing data, ignoring all data entered in verification ->
    Send order back to Capture queue and process to verification ->
    Re-keyed data is not displayed after document comes back from Capture
        """

tags = []


class test(TestParent):

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Workflow Capture Step
        self.lib.general_helper.check_order_type()
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order,
                                                               open_crs=True)
        if self.data["OIT"] == "RP_Recordings":
            self.atom.CRS.general.go_to_crs()
        self.lib.CRS.order_item_type.capture_step()
        if self.data["async"] == "1":
            with self.lib.db as db:
                db.scheduler_job_update_for_export(scheduler_job_code="OrderItemContentExport")
        self.lib.CRS.order_item_type.indexing_step(prop_type=True, store_doc_grids=True, store_party_names=True)
        self.lib.CRS.order_item_type.index_order(self.lib.CRS.crs.go_to_verification_queue,
                                                 fill_required_fields=False)
        self.lib.CRS.verification_entry.fill_doc_fields(self.data)
        self.lib.CRS.verification_entry.fill_party_names(self.data, True, True)
        self.lib.CRS.verification_entry.check_property_re_key_n_rows()
        self.actions.refresh_page()
        self.lib.CRS.verification_entry.fill_doc_fields(self.data)
        self.lib.CRS.verification_entry.fill_party_names(self.data, True, True)
        self.lib.CRS.verification_entry.return_to_rekey_property()
        self.lib.CRS.indexing_entry.fill_property(step='verification')
        self.lib.CRS.verification_entry.update_re_key_data_property()
        self.actions.refresh_page()
        self.lib.CRS.verification_entry.fill_doc_fields(self.data)
        self.lib.CRS.verification_entry.fill_party_names(self.data, True, True)
        self.lib.CRS.indexing_entry.fill_property(step='verification')
        self.lib.CRS.verification_entry.restore_re_key_data_property()


if __name__ == '__main__':
    run_test(__file__)
