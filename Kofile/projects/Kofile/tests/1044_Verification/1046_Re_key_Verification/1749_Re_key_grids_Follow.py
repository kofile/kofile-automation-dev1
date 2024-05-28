from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS ->
    Workflow Order Step ->
    Workflow Capture Step ->
    Workflow indexing Step ->
    Re-key configuration flag is enabled for property grids ->
    Check pre-population of fields with indexing data -> 
    Grids not configured as re-key are pre-filled with Indexing data.
    Grids configured as re-key are empty.
    Number of empty rows equals to the number of indexed rows.
    Listing order of property types matches the order in which they were indexed.
    Save and Advance button is disabled.
    Check informational text on re-key gird header ->
    Number of entries (property types) indexed in Indexing is displayed in property grid header in "1-Desc, 1-Subdivsion, 0-Survey" format
    Leave the re-key fields empty or enter any data and navigate out of re-key grid ->
    Data entered in Verification is compared to data entered in Indexing.
    If data mismatch,re-key verification popup appears and Save and Advance button remains disabled.
    If number of property types and data exactly match Indexing data no popup appears and Save and Advance button becomes enabled.

        """

tags = ["48999_location_2"]


class test(TestParent):

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Workflow Capture Step
        self.lib.general_helper.check_order_type()
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order, open_crs=True)
        if self.data["OIT"] == "RP_Recordings":
            self.atom.CRS.general.go_to_crs()
        self.lib.CRS.order_item_type.capture_step()
        if self.data["async"] == "1":
            with self.lib.db as db:
                db.scheduler_job_update_for_export(scheduler_job_code="OrderItemContentExport")
        self.lib.CRS.order_item_type.indexing_step(prop_type=True, store_doc_grids=True, fill_party_names=True,
                                                   store_party_names=True)
        self.lib.CRS.order_item_type.index_order(self.lib.CRS.crs.go_to_verification_queue,
                                                 fill_required_fields=False)

        self.lib.CRS.verification_entry.check_doc_fields_are_empty(self.data)
        self.lib.CRS.verification_entry.fill_doc_fields(self.data)
        self.lib.CRS.verification_entry.check_prop_rekey_fields_are_empty()
        self.lib.CRS.verification_entry.check_prop_rows_count_and_seq()
        self.actions.wait_for_element_not_enabled(
            self.pages.CRS.verification_queue.btn_save_and_advance_verification_entry)
        self.lib.CRS.verification_entry.check_prop_rekey_grid_header()
        default_prop_type = self.data['config'].test_data(f"{self.data.OIT}.indexing.default_ptop_type")
        self.lib.general_helper.find_and_send_keys(self.pages.CRS.verification_entry.instrument_date,
                                                   f"{self.datetime.now() + self.timedelta(days=1):'%m/%d/%Y'}")
        self.focus_pages()
        self.click_return()

        self.lib.general_helper.find_and_send_keys(self.pages.CRS.verification_entry.instrument_date,
                                                   f"{self.datetime.now():'%m/%d/%Y'}")
        self.focus_pages()
        self.check_popup_not_present()

        self.lib.CRS.verification_entry.fill_party_names(self.data, grantor_section=True, grantee_section=True)

        self.lib.general_helper.find_and_send_keys(self.pages.CRS.indexing_entry.grantor_name_input,
                                                   f"  {self.data.grantor_name}  ")
        self.focus_pages()
        self.check_popup_not_present()

        self.lib.general_helper.find_and_send_keys(self.pages.CRS.indexing_entry.grantor_name_input, "NONAME")
        self.focus_pages()
        self.click_return()

        self.lib.general_helper.find_and_send_keys(self.pages.CRS.indexing_entry.grantor_name_input,
                                                   self.data.grantor_name)
        self.focus_pages()
        self.check_popup_not_present()

        self.lib.general_helper.find_and_send_keys(self.pages.CRS.indexing_entry.grantee_name_input,
                                                   f"  {self.data.grantee_name}  ")
        self.focus_pages()
        self.check_popup_not_present()

        self.lib.general_helper.find_and_send_keys(self.pages.CRS.indexing_entry.grantee_name_input, "NONAME")
        self.focus_pages()
        self.click_return()

        self.lib.general_helper.find_and_send_keys(self.pages.CRS.indexing_entry.grantee_name_input,
                                                   self.data.grantee_name)
        self.focus_pages()
        self.check_popup_not_present()

        self.actions.focus_element(
            self.pages.CRS.indexing_entry.property_field_locator(default_prop_type, self.data['config'].test_data(
                f"{self.data.OIT}.indexing.property.{default_prop_type}")[0]))
        self.focus_pages()
        self.click_return()

        self.lib.CRS.indexing_entry.fill_property(step='verification', add_spaces=True)
        self.focus_pages()
        self.check_popup_not_present()

        self.lib.CRS.indexing_entry.fill_property(step='verification')
        self.focus_pages()
        self.check_popup_not_present()

        self.actions.wait_for_element_enabled(
            self.pages.CRS.verification_queue.btn_save_and_advance_verification_entry)

    def focus_pages(self):
        self.actions.wait(2)
        self.lib.general_helper.reset_focus()
        self.actions.focus_element(self.pages.CRS.indexing_entry.referer_page)

    def check_popup_not_present(self):
        self.actions.wait(2)
        self.actions.assert_element_not_present(
            self.pages.CRS.verification_entry.pup_ReKey_Verification_lnk_Return_to_Rekey)

    def click_return(self):
        self.actions.wait_for_element_present(
            self.pages.CRS.verification_entry.pup_ReKey_Verification_lnk_Return_to_Rekey, 20)
        self.actions.wait_for_element_not_enabled(
            self.pages.CRS.verification_queue.btn_save_and_advance_verification_entry)
        self.actions.click(self.pages.CRS.verification_entry.pup_ReKey_Verification_lnk_Return_to_Rekey)


if __name__ == '__main__':
    run_test(__file__)
