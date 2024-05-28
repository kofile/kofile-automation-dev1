from projects.Kofile.Atom.CRS.general import General
from projects.Kofile.Atom.CRS.capture import Capture as CaptureAom
from projects.Kofile.Atom.CRS.order_queue import OrderQueue
from projects.Kofile.Lib.Required_fields import RequiredFields
from projects.Kofile.Lib.DB import DB
from projects.Kofile.Lib.CRS.CRS_functions import CRS
from projects.Kofile.Lib.CRS.IndexingEntry_functions import IndexingEntry
from projects.Kofile.Lib.CRS.Capture_functions import Capture
from projects.Kofile.Lib.test_parent import LibParent

CRS_functions, IndexingEntry_functions, Capture_functions = CRS(), IndexingEntry(), Capture()

Required_fields = RequiredFields()


class OIT(LibParent):
    def __init__(self):
        super(OIT, self).__init__()

    def start_batch_scan(self):
        # Go to Capture
        CRS_functions.go_to_capture_queue()
        self._general_helper.scroll_and_click(self._pages.CRS.capture_queue.btn_start_batch_scan)

    def scan_and_map(self, oi_count=1, scan_count=1):
        """scans and maps without processing to next step"""
        capture_atom = CaptureAom()
        self.start_batch_scan()
        if self._general_helper.get_data().get("historical"):
            self._general_helper.find_and_click(self._pages.CRS.capture_summary.lnk__historical_capture_tab)
            self._actions.wait(0.5)
        # capture and map
        for i in range(oi_count):
            capture_atom.capture_and_map(oit_num=i + 1, to_row=i + 1, scan_count=scan_count)

    def scan_and_map_pre_ml(self):
        """scans and maps without processing to next step"""
        capture_atom = CaptureAom()
        self.start_batch_scan()
        # capture and map
        capture_atom.capture_and_map_pre_ml()

    def save_order_in_capture_step(self, e_file=False, spinner_count=10):
        """saves already scanned and mapped order"""
        self._general_helper.scroll_and_click(self._pages.CRS.capture_summary.btn_save_and_exit)
        for _ in range(spinner_count):
            self._general_helper.wait_for_spinner(spinner_in=3, spinner_out=20)
            if e_file:
                if "/Order/OrderSummary" in self._actions.get_current_url():
                    break
            else:
                if self._general_helper.find(
                        self._pages.CRS.capture_queue.btn_start_batch_scan, wait_displayed=True,
                        should_exist=False, timeout=3):
                    break

    def capture_step(self, oi_count=1, scan_count=1, save_after_scan=True):
        """processes through capture to next step"""
        data = self._general_helper.get_data()
        if data['config'].test_data(f"{data.OIT}.capture.step"):
            self.scan_and_map(oi_count, scan_count=scan_count)
            if save_after_scan:
                self.save_order_in_capture_step()
                if data['config'].test_data(f"{data.OIT}.capture.capture_review"):
                    self.capture_review_step(oi_count)

    def index_order(self, go_to_tab=CRS_functions.go_to_indexing_queue, verify_status_before=None, verify_notes=None,
                    fill_required_fields=True):
        """indexes without processing to next step"""
        go_to_tab()
        self._general_helper.find(self._pages.CRS.indexing_queue.btn_administrative, wait_displayed=True)
        CRS_functions.click_all_show_all_action_links()
        if verify_status_before:
            CRS_functions.verify_order_status(verify_status_before)
        if verify_notes:
            CRS_functions.verify_order_notes(verify_notes)
        # assign the order
        OrderQueue().assign_order()
        # click running man
        CRS_functions.click_running_man()
        # fill required fields
        if fill_required_fields:
            self._general_helper.find(self._pages.CRS.indexing_entry.btn_save_and_advance, wait_displayed=True)
            Required_fields.crs_fill_required_fields()

    def save_order_in_index_entry(self):
        """saves already indexed OI"""
        self._general_helper.scroll_and_click(self._pages.CRS.indexing_entry.btn_save_and_advance)
        self._general_helper.find(self._pages.CRS.indexing_summary.btn_next_order, wait_displayed=True)

    def next_order_in_index_summary(self):
        """takes next OI to index"""
        self._general_helper.scroll_and_click(self._pages.CRS.indexing_summary.btn_next_order)
        try:
            self._general_helper.find(self._pages.CRS.indexing_entry.btn_save_and_advance, wait_displayed=True)
            CRS_functions.go_to_indexing_queue()
            self._general_helper.find(self._pages.CRS.indexing_queue.btn_administrative, wait_displayed=True)
        except Exception as e:
            self._logging.info(e)
            self._actions.step("No more indexing tasks")
            self._general_helper.find(self._pages.CRS.general.btn_admin_key, wait_displayed=True)

    def indexing_step(self, prop_type=False, add_remark=False, set_ref=False, verify_status_before=None,
                      store_doc_grids=False, store_party_names=False, fill_party_names=False):
        """processes through index to next step"""
        data = self._general_helper.get_data()
        if data['config'].test_data(f"{data.OIT}.indexing.step"):
            if data['config'].test_data(f"{data.OIT}.indexing.indexing_type") == 'self':
                # index the order
                self.index_order(verify_status_before=verify_status_before)
                if store_doc_grids:
                    IndexingEntry_functions.store_documents_grids()
                if fill_party_names:
                    name = self._random.choice(self._names.FIELDS_VALUE["Strings"]["FirstName"])
                    grantor_name = f"{name}_{self._random.randint(1000, 10000)}"
                    self._general_helper.find_and_send_keys(self._pages.CRS.indexing_entry.grantor_name_input, grantor_name)
                    self._actions.store("grantor_name", grantor_name)
                    grantee_name = f"{name}_{self._random.randint(1000, 10000)}"
                    self._general_helper.find_and_send_keys(self._pages.CRS.indexing_entry.grantee_name_input, grantee_name)
                    self._actions.store("grantee_name", grantee_name)
                if store_party_names:
                    IndexingEntry_functions.store_party_names(data)
                if prop_type:
                    IndexingEntry_functions.fill_property(step='indexing')
                if add_remark and self._general_helper.find(self._pages.CRS.indexing_summary.remark_link,
                                                            should_exist=False,
                                                            timeout=1):
                    self._general_helper.find_and_click(self._pages.CRS.indexing_summary.remark_link)
                    self._actions.wait_for_element_displayed(self._pages.CRS.indexing_summary.remark_input)
                    self._general_helper.find_and_send_keys(self._pages.CRS.indexing_summary.remark_input,
                                                            "test remark")
                if set_ref:
                    IndexingEntry_functions.set_reference_document_by_vol_and_page()
                self.save_order_in_index_entry()
                self.next_order_in_index_summary()
            else:
                # kdi index
                with DB(data) as db:
                    db.kdi_export(data["order_number"])

    def re_key_in_verification(self):
        data = self._general_helper.get_data()
        reentry_grids = data['config'].test_data(f"{data.OIT}.verification.reentry").keys()
        grid_first_elements = {
            "reenter_document": self._pages.CRS.verification_entry.txt_document_tab_first_field,
            "reenter_grantor": self._pages.CRS.indexing_entry.grantor_name_input,
            "reenter_grantee": self._pages.CRS.indexing_entry.grantee_name_input,
            "reenter_property": self._pages.CRS.verification_entry.txt_property_tab_first_field,
        }
        for reentry_grid in reentry_grids:
            if data['config'].test_data(f"{data.OIT}.verification.reentry.{reentry_grid}"):
                self._general_helper.scroll_and_click(grid_first_elements[reentry_grid])
                self._general_helper.scroll_and_click(self._pages.CRS.verification_entry.txt_last_field)
                self.re_key_save_verification()
        self._actions.wait_for_element_enabled(self._pages.CRS.verification_entry.btn_save_and_advance)

    def re_key_save_verification(self):
        try:
            self._general_helper.scroll_and_click(
                self._pages.CRS.verification_entry.pup_ReKey_Verification_rdb_save_rekey_date)
            self._general_helper.scroll_and_click(
                self._pages.CRS.verification_entry.pup_ReKey_Verification_lnk_Save_Changes)
        except Exception as e:
            self._logging.info(e)

    def save_order_in_verification_entry(self):
        """saves already verified OI"""
        self._general_helper.scroll_and_click(self._pages.CRS.verification_entry.btn_save_and_advance, timeout=60)
        self._general_helper.find(self._pages.CRS.verification_summary.btn_next_order, wait_displayed=True)

    def next_order_in_verification_summary(self, open_crs_in_end):
        """takes next OI to verify"""
        self._general_helper.scroll_and_click(self._pages.CRS.verification_summary.btn_next_order)
        self._general_helper.find_and_click(self._pages.CRS.verification_summary.editicon_by_row(), should_exist=False,
                                            timeout=10,
                                            retries=1)
        try:
            self._general_helper.find(self._pages.CRS.verification_entry.btn_save_and_advance, wait_displayed=True)
            CRS_functions.go_to_verification_queue()
            self._general_helper.find(self._pages.CRS.general.btn_admin_key, wait_displayed=True)
        except Exception as e:
            self._actions.step(f"No more verification tasks: {e}")
            if open_crs_in_end:
                General().go_to_crs()
            else:
                self._general_helper.find(self._pages.CRS.verification_queue.btn_administrative, wait_displayed=True)

    def verification_step(self, open_crs_in_end=True):
        """processes through verification to archive"""
        data = self._general_helper.get_data()
        if data['config'].test_data(f"{data.OIT}.verification.step"):
            # verify order
            self.index_order(CRS_functions.go_to_verification_queue)
            if data['config'].test_data(f"{data.OIT}.verification.rekey"):
                self.re_key_in_verification()
            self.save_order_in_verification_entry()
            self.next_order_in_verification_summary(open_crs_in_end)

    def change_number_of_page_amount(self):
        loc_order_item_tab = self._general_helper.make_locator(
            self._pages.CRS.order_entry.lnk_order_entry_tab,
            self._general_helper.get_data()['config'].get_tab_name("Tabs.Order_Item.value"))
        self._general_helper.find_and_click(loc_order_item_tab)
        self._general_helper.find_and_send_keys(self._pages.CRS.fields.no_of_pages_input_by_oi_index(),
                                                self._names.ANY_DATA['edit_no_of_pages'])

    def capture_review_step(self, oi_count=1):
        Capture_functions.verify_order_status("Review_status")
        CRS_functions.click_running_man()
        for i in range(oi_count):
            Capture_functions.verify_order_item_status("Pending", oi_index=i + 1)
            Capture_functions.click_on_the_document_row(row_num=i + 1, mapped=True)
            Capture_functions.verify_order_item_status("Reviewed", oi_index=i + 1)
        self._actions.wait_for_element_enabled(self._pages.CRS.capture_summary.btn_save_and_exit)
        self.save_order_in_capture_step()
