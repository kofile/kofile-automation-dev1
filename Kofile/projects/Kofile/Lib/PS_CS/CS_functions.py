import os
import PyPDF2
import csv
import openpyxl

from projects.Kofile.Atom.CRS.general import General
from projects.Kofile.Atom.CS.general import General as CSGeneral
from projects.Kofile.Lib.CRS.CRS_functions import CRS
from projects.Kofile.Lib.DB import DataBaseWithVPN, DB
from projects.Kofile.Lib.work_with_files import Files
from projects.Kofile.Lib.test_parent import LibParent

CRS_functions, work_with_files = CRS(), Files()


class CS(LibParent):
    def __init__(self):
        super(CS, self).__init__()

    def send_created_doc_to_recapture(self, data, dept_id):
        cs_general_atom = CSGeneral()
        cs_doc = self.export_and_find_created_doc_in_cs(data, dept_id)
        assert cs_doc["Filename"], "Image does NOT exist in Clerk Search!"
        # send the document to Re-Capture, Re-Capture option is passed in test csv
        cs_general_atom.submit_to_crs()
        # open the Re-Capture order
        General().go_to_crs()
        CRS_functions.go_to_capture_queue()
        error = None
        for _ in range(5):
            try:
                CRS_functions.click_running_man()
                error = None
                break
            except Exception as e:
                error = e
                self._actions.wait(5)
                self._actions.refresh_page()
        if error:
            raise error

    def export_and_find_created_doc_in_cs(self, data, dept_id, retry_cs=10):
        cs_general_atom = CSGeneral()
        DataBaseWithVPN(data).scheduler_job_update_for_set_export_document(dept_id)
        cs_general_atom.go_to_cs()
        data["doc_num"] = f"{data['doc_year']}-{data['doc_number']}"
        for _ in range(retry_cs):
            cs_doc = self._api.clerc_search(data).search_by_doc_number(doc_number=data["doc_num"])
            if cs_doc["Filename"]:
                return cs_doc
            self._actions.wait(1)


    def print_doc(self, data):
        self._actions.wait_for_element_present(self._pages.PS.main_page.print_button)
        with DB(data) as db:
            last_job_id = db.get_last_device_jobs(device_id=data["env"]["printer_id"])[0][0]
            self._general_helper.find_and_click(self._pages.PS.main_page.print_button)
            apply = self._general_helper.find(self._pages.PS.main_page.apply_print, should_exist=False, timeout=10,
                                              wait_displayed=10)
            if apply:
                apply.click()
            self._actions.wait_for_element_displayed(self._pages.PS.main_page.locator_spinner)
            self._general_helper.wait_until(
                lambda: db.get_last_device_jobs(device_id=data["env"]["printer_id"])[0][0] > last_job_id, 60, 2.0)
            counter = 20
            while self._general_helper.find(self._pages.PS.main_page.locator_spinner, should_exist=False,
                                            wait_displayed=1, timeout=1) and counter:
                db.update_printer_job(data["env"]["printer_id"])
                self._actions.wait(1.5)
                counter -= 1
        self._actions.wait_for_element_displayed(self._pages.PS.main_page.ms_popup_window)
        self._actions.assert_element_text(self._pages.PS.main_page.ms_popup_window, "Printing success")
        self._general_helper.find_and_click(self._pages.PS.main_page.close_popup_btn)

    def download_file(self):
        work_with_files.clear_download_folder(self._names.download_dir, False)

        self._actions.wait_for_element_present(self._pages.PS.main_page.print_icon)
        self._general_helper.find_and_click(self._pages.PS.main_page.print_icon)
        apply_download = self._general_helper.find(self._pages.PS.main_page.print_icon_confirm, should_exist=False,
                                                   timeout=10,
                                                   wait_displayed=10)
        if apply_download:
            apply_download.click()

        files_count = work_with_files.clear_download_folder(self._names.download_dir)
        assert files_count, "File not been downloaded"

    def export_search_result(self, file_format: str) -> str:
        formats = self._pages.PS.main_page.export_manager_files.keys()
        assert file_format.lower() in formats, "file_format must been one of {}".format(", ".join(formats))
        self._general_helper.find_and_click(self._pages.PS.main_page.export_result_btn)
        self._actions.wait_for_element_displayed(self._pages.PS.main_page.export_manager_form)
        self._general_helper.find_and_click(self._pages.PS.main_page.export_manager_files.get(file_format.lower()))
        work_with_files.clear_download_folder(self._names.download_dir, wait_for_file=False)
        self._general_helper.find_and_click(self._pages.PS.main_page.apply_export)
        file_path = work_with_files.get_last_downloaded_file(self._names.download_dir)
        assert file_path, "Exported file not found"
        return file_path

    @staticmethod
    def check_exported_file(file_path: str, file_format: str, doc_number: str):
        if file_format == "pdf":
            with open(file_path, 'rb') as f:
                file_reader = PyPDF2.PdfFileReader(f)
                page_text = file_reader.getPage(0).extractText()
        elif file_format == "exel":
            wb_obj = openpyxl.load_workbook(file_path)
            sheet_obj = wb_obj.active
            page_text = ""
            for a in range(1, sheet_obj.max_row + 1):
                for i in range(1, sheet_obj.max_column + 1):
                    cell_obj = sheet_obj.cell(row=a, column=i)
                    page_text += cell_obj.value + "\n"
        elif file_format == "csv":
            with open(file_path, 'r') as f:
                csv_reader = csv.reader(f, delimiter=',')
                page_text = "\n".join([" ".join(i) for i in csv_reader])
        else:
            raise ValueError("File format not allowed")
        assert doc_number in page_text.replace("-\n", "-"), f"Document {doc_number} not found in file {file_path}"
        os.remove(file_path)

    def check_sort(self, row, data_field):
        self._general_helper.find_and_click(row)
        self._general_helper.wait_for_spinner()
        date_one = self._general_helper.find(data_field, get_text=True)
        self._general_helper.find_and_click(row)
        self._general_helper.wait_for_spinner()
        date_two = self._general_helper.find(data_field, get_text=True)
        assert date_one != date_two, f"Sort by date error asc {date_one} desc {date_two}"

    def go_to_department_by_dept_id(self, dept_id):
        locator = self._general_helper.make_locator(self._pages.CS.main_page.lnk_department_tab_by_dept_id_, dept_id)
        self._general_helper.find_and_click(locator)
        self._general_helper.wait_for_spinner()

    def search_ml_docs_by_date(self, date_from, date_to, date_name="application"):
        self._actions.wait(2)
        locator_date_from = self._pages.CS.main_page.txt_application_date_from if date_name == "application" \
            else self._pages.CS.main_page.txt_recorded_date_from
        locator_date_to = self._pages.CS.main_page.txt_application_date_to if date_name == "application" \
            else self._pages.CS.main_page.txt_recorded_date_to
        self._general_helper.find_and_send_keys(locator_date_from, date_from)
        self._general_helper.find_and_send_keys(locator_date_to, date_to)
        self.click_on_search_button()

    def clear_dates(self, date_name="application"):
        locator_date_from = self._pages.CS.main_page.txt_application_date_from if date_name == "application" \
            else self._pages.CS.main_page.txt_recorded_date_from
        locator_date_to = self._pages.CS.main_page.txt_application_date_to if date_name == "application" \
            else self._pages.CS.main_page.txt_recorded_date_to
        self._actions.clear_element(locator_date_from)
        self._actions.clear_element(locator_date_to)

    def verify_doc_number_in_results(self, doc_number, should_exist):
        locator = self._general_helper.make_locator(self._pages.CS.main_page.row_by_doc_num_, doc_number)
        self._general_helper.find(locator, should_exist=should_exist, timeout=5)
        self._logging.info(f"Doc number {doc_number} is {'' if should_exist else 'NOT '}found in search results")

    def click_on_search_option(self, search_option):
        self._general_helper.find_and_click(
            self._general_helper.make_locator(self._pages.CS.main_page.cbx_search_options_, search_option))

    def click_on_search_button(self):
        self._general_helper.find_and_click(self._pages.CS.main_page.btn_search)
        self._general_helper.wait_for_spinner()

    def click_on_column_sort(self, column_index):
        locator = self._general_helper.make_locator(self._pages.CS.main_page.column_header_by_column_index_,
                                                    column_index)
        self._general_helper.find_and_click(locator)
        self._general_helper.wait_for_spinner()
        self._general_helper.find_and_click(self._pages.CS.main_page.icn_expand_all)

    def double_click_on_column_sort(self, column_index):
        for _ in range(2):
            self.click_on_column_sort(column_index)

    def search_by_keyword(self, keyword):
        self._general_helper.find_and_send_keys(self._pages.CS.main_page.txt_search_input, keyword)
        self.click_on_search_button()

    def reset_search(self):
        self._general_helper.find_and_click(self._pages.CS.main_page.lnk_reset_search)
        self._general_helper.wait_for_spinner()

    def click_on_printer_by_row_index(self, row=1):
        print_icon = ("xpath", f"(//*[@class='iconPrinter icon_table'])[{row}]", "CS print icon")
        self._actions.wait_for_element_displayed(print_icon)
        self._general_helper.find_and_click(print_icon)

    def get_column_name_by_index(self, column_index):
        return self._actions.get_element_text(
            self._general_helper.make_locator(self._pages.CS.main_page.column_header_by_column_index_, column_index))
