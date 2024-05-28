import time
from datetime import datetime
from golem.webdriver.extended_webelement import Select
from projects.Kofile.Lib.CRS.CRS_functions import CRS
from projects.Kofile.Lib.DB import DataBaseWithVPN
from projects.Kofile.Lib.Required_fields import RequiredFields
from projects.Kofile.Lib.test_parent import LibParent

crs_fill_required_fields = RequiredFields().crs_fill_required_fields


class Capture(LibParent):
    default_order_num = "New order documents"

    def __init__(self):
        super(Capture, self).__init__()

    def start_scan(self, click=True):
        if click:
            self._general_helper.scroll_and_click(self._pages.CRS.capture_summary.btn_start_scan)
        # if scanner is busy, update status and scan again
        max_time = time.time() + 3
        while time.time() < max_time:
            if 'Scanner is currently busy!' in self._actions.get_browser().page_source:
                self._general_helper.find_and_click(self._pages.CRS.capture_summary.pup_confirm_btn_ok)
                DataBaseWithVPN(self._general_helper.get_data()).update_all_scanner_statuses()
                self._general_helper.find_and_click(self._pages.CRS.capture_summary.btn_start_scan)
                break
            else:
                self._actions.wait(1)

        self._actions.wait_for_element_displayed(self._pages.CRS.capture_summary.lbl_scan_progress_bar)
        self._actions.wait_for_element_not_displayed(self._pages.CRS.capture_summary.lbl_scan_progress_bar, 60)
        self._actions.wait(0.5)

    def add_pre_ml(self):
        self._general_helper.find_and_click(self._pages.CRS.capture_summary.tab_pre_ml)
        self._general_helper.find_and_click(self._pages.CRS.capture_summary.add_pre_ml)

    def scan_re_ml(self, stop=False):
        self._actions.wait_for_element_present(self._pages.CRS.capture_summary.scan_ml_btn_start)
        self._general_helper.find_and_click(self._pages.CRS.capture_summary.scan_ml_btn_start)
        self._actions.wait_for_element_displayed(self._pages.CRS.capture_summary.scan_ml_progressbar)
        if stop:
            self._general_helper.find_and_click(self._pages.CRS.capture_summary.scan_ml_btn_stop)
            self._actions.wait_for_element_not_displayed(self._pages.CRS.capture_summary.scan_ml_progressbar)
        else:
            self._general_helper.wait_element_and_text(self._pages.CRS.capture_summary.scanned_files_ms_count, "1",
                                                       retry=5)

    def check_doc_view(self):
        for _ in range(10):
            self._general_helper.find_and_click(self._pages.CRS.capture_summary.first_doc)
            if self._general_helper.find(self._pages.CRS.capture_summary.image_viewer_container, should_exist=False):
                break
        self._actions.assert_element_displayed(self._pages.CRS.capture_summary.image_viewer_container)
        self._actions.assert_element_attribute(self._pages.CRS.capture_summary.first_doc, "class", "selectedRow")

    def print_application(self, certificate=False):
        self._general_helper.find_and_click(
            self._pages.CRS.capture_summary.print_certificate if certificate else self._pages.CRS.capture_summary.print_app)
        self._general_helper.wait_for_spinner()
        self._actions.wait_for_element_present(self._pages.CRS.capture_summary.print_app_dialog_text)
        self._actions.wait_for_element_text(
            self._pages.CRS.capture_summary.print_app_dialog_text,
            "Front page Print Initiated" if certificate else "Application printing is initiated.")
        self._general_helper.find_and_click(self._pages.CRS.capture_summary.print_app_dialog_close_btn)
        self._actions.wait_for_element_not_present(self._pages.CRS.capture_summary.print_app_dialog_text)

    def click_edit_icon(self, row_num=1, mapped=False):
        if mapped:
            data = self._general_helper.get_data()
            self._general_helper.scroll_and_click(
                self._pages.CRS.capture_summary.edit_mapped_by_row_index(data.get("order_number"), row_num))
        else:
            self._general_helper.scroll_and_click(
                self._pages.CRS.capture_summary.edit_button_not_mapped_by_row_index(row_num))

    def add_doc_group_and_doc_type(self, row_num=1, oit_num=1):
        # add doc group
        data = self._general_helper.get_data()
        oits = data.get("OITs")  # for multiple OITs tests
        oit = oits[oit_num - 1] if oits else data.get("OIT")
        if data.get("historical") and not oit:
            doc_group = data.get("doc_group")
        else:
            doc_group = data['config'].test_data(f"{oit}.doc_group")
        self._general_helper.find_and_send_keys(
            self._pages.CRS.capture_summary.doc_group_not_mapped_by_row_index(row_num),
            str(doc_group)[:-1])
        self._general_helper.scroll_and_click(
            self._general_helper.make_locator(self._pages.CRS.capture_summary.ddl_doc_group_doc_type_by_text,
                                              doc_group))
        self._general_helper.reset_focus()
        # add doc type
        doc_type = data["doc_types"][oit_num - 1] if data.get("doc_types") is not None \
            else data["config"].test_data(f"{oit}.default_doc_type")
        self._general_helper.find_and_send_keys(
            self._pages.CRS.capture_summary.doc_type_not_mapped_by_row_index(row_num),
            doc_type)
        self._general_helper.scroll_and_click(
            self._general_helper.make_locator(self._pages.CRS.capture_summary.ddl_doc_group_doc_type_by_text,
                                              doc_type))
        self._general_helper.reset_focus()

    def add_doc_number(self, row_num=1, oit_num=1, doc_number=None):
        data = self._general_helper.get_data()
        if data.get("historical") and not data.get("doc_number"):
            now = datetime.now()
            self._actions.store("doc_number", now.strftime("%m%d%H%M%S"))
            if not data.get("doc_year"):
                self._actions.store("doc_year", now.year)
                self._actions.wait_for_element_displayed(
                    self._pages.CRS.capture_summary.recorded_year_not_mapped_by_row_index(row_num))
                self._general_helper.find_and_send_keys(
                    self._pages.CRS.capture_summary.recorded_year_not_mapped_by_row_index(row_num), data["doc_year"])
                self._actions.store("doc_year", now.year)
        multi_oit = data.get("doc_numbers")  # for multiple OITs tests
        doc_number = doc_number if doc_number else data["doc_numbers"][oit_num - 1] if multi_oit else data["doc_number"]
        self._general_helper.find_and_send_keys(
            self._pages.CRS.capture_summary.doc_number_not_mapped_by_row_index(row_num),
            doc_number)

    def add_pages_count(self, row_num=1):
        if self._general_helper.get_data().get("historical"):
            return  # pages input absent on historical capture
        image_count = self._general_helper.find(self._pages.CRS.capture_summary.images_not_mapped_by_row_index(row_num),
                                                get_text=True, wait_displayed=True)
        self._general_helper.find_and_send_keys(self._pages.CRS.capture_summary.pages_not_mapped_by_row_index(row_num),
                                                image_count)
        return image_count

    def select_order_type(self, order_type, row_num=1, mapped=False):
        loc = self._pages.CRS.capture_summary.order_type_ddl_not_mapped_by_row_index(row_num) if not mapped else \
            self._pages.CRS.capture_summary.order_type_ddl_mapped_by_row_index(
                self._general_helper.get_data().get("order_number"),
                row_num)
        Select(self._general_helper.find(loc, wait_displayed=True)).select_by_visible_text(order_type)

    def click__apply_all__order_types(self):
        self._general_helper.find_and_click(self._pages.CRS.capture_summary.lnk_scan_documents__apply_all)

    def get_order_type(self, row_num=1, order_num=None, mapped=False):
        loc = self._pages.CRS.capture_summary.order_type_ddl_mapped_by_row_index(order_num, row_num) if mapped \
            else self._pages.CRS.capture_summary.order_type_ddl_not_mapped_by_row_index(row_num)
        ot = self._general_helper.find(loc, get_attribute="value")
        return self._general_helper.find(
            ("xpath", f"//option[@value='{ot}']", f"Order Type[{row_num}]"), get_text=True) if ot else ot

    def get_doc_group(self, order_num=default_order_num, row_num=1):
        return self._general_helper.find(
            self._pages.CRS.capture_summary.doc_group_mapped_by_row_index(order_num, row_num),
            get_text=True)

    def get_doc_type(self, order_num=default_order_num, row_num=1):
        return self._general_helper.find(
            self._pages.CRS.capture_summary.doc_type_mapped_by_row_index(order_num, row_num),
            get_text=True)

    def get_recorded_year(self, order_num=default_order_num, row_num=1):
        return self._general_helper.find(
            self._pages.CRS.capture_summary.recorded_year_mapped_by_row_index(order_num, row_num),
            get_text=True)

    def expanded_indexing(self, save=True):
        self._general_helper.wait_for_spinner()
        crs_fill_required_fields()
        if save:
            self._actions.wait_for_element_enabled(self._pages.CRS.capture_summary.btn_save_and_exit)

    def click_on_the_document_row(self, row_num=1, mapped=False):
        data = self._general_helper.get_data()
        if "/OrderSummary" in self._actions.get_current_url():
            locator = self._pages.CRS.order_summary.type_by_row_index(row_num)
        else:
            locator = self._pages.CRS.capture_summary.images_not_mapped_by_row_index(row_num) if not mapped else \
                self._pages.CRS.capture_summary.images_mapped_by_row_index(data.get("order_number"), row_num)
        self._general_helper.find_and_click(locator)
        self._general_helper.wait_for_spinner()

    def verify_image_exist_in_image_viewer(self, row_num=1, mapped=False, should_exist=True):
        self._general_helper.wait_for_spinner()
        if not self._general_helper.find(self._pages.CRS.capture_summary.img__document_image, timeout=1,
                                         should_exist=False):
            self.click_on_the_document_row(row_num, mapped=mapped)
        img_path = self._general_helper.find(self._pages.CRS.capture_summary.img__document_image, get_attribute="src")
        if should_exist:
            assert "PlaceHolderPage" not in img_path, f"Image isn't exist in image viewer: '{img_path}'"
        else:
            assert "PlaceHolderPage" in img_path, f"Image unexpectedly exist in image viewer: '{img_path}'"

    def get_order_status(self):
        CRS().click_all_show_all_action_links()
        order_number = self._general_helper.get_data()["order_number"]
        status = self._general_helper.find(self._pages.CRS.general.status_desc_by_order_number(order_number),
                                           get_text=True)
        if not status:
            status = self._general_helper.find(self._pages.CRS.general.status_by_order_number(order_number),
                                               get_text=True)
        return status

    def fill_reason_popup(self, page="/ShowCaptureQueue"):
        self._general_helper.find_and_send_keys(self._pages.CRS.capture_summary.inp_reason_popup__reason, "Some reason")
        self._general_helper.find_and_send_keys(self._pages.CRS.capture_summary.inp_reason_popup__description,
                                                "Some description")
        self._general_helper.find_and_click(self._pages.CRS.capture_summary.btn_reason_popup__submit)
        self._actions.wait_for_window_present_by_partial_url(page)
        return self.get_order_status()

    def save_batch_for_later_processing(self, expected_status="Suspended"):
        self._general_helper.scroll_and_click(self._pages.CRS.capture_summary.lnk_save_batch_for_later_processing)
        status = self.fill_reason_popup()
        assert status == expected_status, f"Incorrect order[{self._general_helper.get_data()['order_number']}] " \
                                          f"status after 'Save Batch for Later Processing':\n" \
                                          f"Expected: '{expected_status}' but actual: '{status}'"

    def send_to_administrator(self, expected_status="Admin Suspend"):
        self._general_helper.scroll_and_click(self._pages.CRS.capture_summary.lnk_send_to_administrator)
        status = self.fill_reason_popup()
        assert status == expected_status, f"Incorrect order[{self._general_helper.get_data()['order_number']}] status" \
                                          f" after 'Send to Administrator':\n" \
                                          f"Expected: '{expected_status}' but actual: '{status}'"

    def get_expanded_indexing_values(self):
        fields = self._general_helper.find_elements(self._pages.CRS.capture_summary.expanded_indexing_fields)
        values = {}
        for i in fields:
            value = i.get_attribute("value")
            name = i.get_attribute("placeholder")
            if value and name:
                values.update({name if name not in values.keys() else f"{name}_1": value})
        self._logging.info(values)
        return values

    def open_image_in_image_viewer(self, timeout=30, retries=3):
        self._general_helper.find_and_click(self._pages.CRS.capture_summary.img_capture_summary, timeout=timeout,
                                            retries=retries)
        self._general_helper.wait_for_spinner()

    def verify_order_status(self, status):
        """Verify status of order in capture queue"""
        data = self._general_helper.get_data()
        self._actions.assert_equals(self.get_order_status(), data['config'].get_status(f'Capture.{status}.value'))

    def verify_order_item_status(self, expected_status, oi_index):
        data = self._general_helper.get_data()
        actual_status = self._general_helper.find(
            self._pages.CRS.capture_summary.status_mapped_by_row_index(data["order_number"], oi_index),
            get_text=True)
        self._actions.assert_equals(actual_status, expected_status)

    def verify_confirm_pop_up_message(self, expected_message, confirm=True):
        msg = self._general_helper.find(self._pages.CRS.capture_summary.pup_confirm_lbl_message, wait_displayed=True,
                                        get_text=True,
                                        timeout=5)
        assert msg == expected_message, f"Expected pop-up message '{expected_message}' is not equal to actual: '{msg}'"
        self._general_helper.find_and_click(self._pages.CRS.capture_summary.pup_confirm_btn_ok) if confirm else None

    def get_all_multiselect_checkbox(self, expected_cb=4):
        all_checkbox = list()
        for _ in range(20):
            all_checkbox = self._general_helper.find_elements(self._pages.CRS.image_viewer.multi_selectdoc_checkbox)
            if len(all_checkbox) > 0:
                self._general_helper.scroll_into_view(all_checkbox[-1])
            all_checkbox = [i for i in all_checkbox if i.is_displayed()]
            if len(all_checkbox) == expected_cb:
                break
            self._actions.wait(1)
        assert len(
            all_checkbox) == expected_cb, f"Multi doc checkbox count {len(all_checkbox)}, but must be {expected_cb}"
        return all_checkbox

    def click_multi_select(self):
        for _ in range(40):
            self._general_helper.find_and_click(self._pages.CRS.image_viewer.multi_selectdoc_button)
            error = self._general_helper.find(self._pages.CRS.image_viewer.apply_error_button, should_exist=False,
                                              timeout=5)
            if error:
                error.click()
                self._actions.wait(3)
            else:
                break

    def check_secure_doc_button_title(self, new_title):
        for _ in range(10):
            if self._general_helper.find(self._pages.CRS.image_viewer.set_secured_document_content_button,
                                         get_attribute="title") == new_title:
                break
            else:
                self._actions.wait(2)
        self._actions.assert_element_attribute(self._pages.CRS.image_viewer.set_secured_document_content_button,
                                               "title", new_title)

