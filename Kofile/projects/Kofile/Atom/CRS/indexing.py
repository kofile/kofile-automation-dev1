import logging
import os
from datetime import datetime, timedelta
from shutil import copy

import psutil

from projects.Kofile.Atom.CRS.general import General
from projects.Kofile.Atom.CRS.order_queue import OrderQueue
from projects.Kofile.Lib.test_parent import AtomParent

general = General()


class Indexing(AtomParent):
    def __init__(self):
        super(Indexing, self).__init__()

    def birth_death_verification_step(self, data):
        self._actions.step(f"--- ATOMIC TEST --- {__name__} ---")

        if data['config'].test_data(f"{data.OIT}.verification.step"):
            self._lib.CRS.crs.go_to_verification_queue()
            self._lib.CRS.crs.click_all_show_all_action_links()
            data["order_number"] = self._lib.general_helper.find(
                self._pages.CRS.general.order_number_by_doc_number(data["doc_number"]),
                get_text=True)
            OrderQueue().assign_order(ind=0)
            self._lib.CRS.crs.click_running_man()
            self._lib.required_fields.crs_fill_required_fields()
            self._lib.CRS.verification_entry.click_save_and_advance_button()
            self._lib.CRS.verification_summary.click_next_order_button()

        self._actions.step(f"--- ATOMIC TEST END --- {__name__} ---")

    def check_status_of_order_in_indexing(self, status):
        """
            Pre-conditions: Indexing  Queue page is displayed
            Post-conditions: Indexing Queue page is displayed, order status is checked
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        self._actions.wait_for_element_displayed(self._pages.CRS.general.lbl_order_count)
        self._lib.CRS.crs.click_all_show_all_action_links()
        self._actions.wait_for_element_displayed(self._pages.CRS.general.lbl_order_count)
        self._lib.CRS.indexing_queue.verify_order_status(status)
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def create_new_indexing_task(self, data):
        """
            Pre-conditions: There are images in Birth/Death sub-folders
            Post-conditions: Created doc number is stored in data
            """
        self._actions.step(f"--- ATOMIC TEST --- {__name__} ---")

        general.go_to_crs()
        self._lib.CRS.indexing_queue.select_new_indexing_task(data)
        self._lib.CRS.indexing_entry.upload_birth_death_image(data)
        self._lib.required_fields.crs_fill_required_fields()
        doc_number = str(datetime.now().timestamp())[:-7]
        self._lib.CRS.indexing_entry.fill_doc_number(doc_number)
        self._lib.CRS.indexing_entry.fill_recorded_date()
        self._lib.CRS.indexing_entry.click_birth_death_record_save_button()
        self._actions.wait_for_element_displayed(self._pages.CRS.indexing_entry.txt_doc_number)
        data["doc_number"] = doc_number
        data['doc_year'] = datetime.now().year

        self._actions.step(f"--- ATOMIC TEST END --- {__name__} ---")

    def OCR_Image_Upload(self, birth_count=0, death_count=0, plat_count=0):
        """
            Pre-conditions: No
            Post-conditions: Template images are copied to upload folders, where CRS_Agent will take images from.
            OCR device job status and next execution date are updated
            """
        self._actions.step(f"--- SMOKE TEST --- {__name__} ---")

        # copy template images to folders for upload (root folder for OCR order and sub-folders for Image Upload)
        if birth_count:
            self.__copy_and_rename_images(birth_count, f"{self._names.ocr_templates}/BirthTemplate",
                                          f"{self._names.ocr_images}/BirthOCR",
                                          f"{self._names.ocr_images}/BirthOCR/BirthUpload", "_Birth.TIF")

        if death_count:
            self.__copy_and_rename_images(death_count, f"{self._names.ocr_templates}/DeathTemplate",
                                          f"{self._names.ocr_images}/DeathOCR",
                                          f"{self._names.ocr_images}/DeathOCR/DeathUpload", "_Death.TIF")

        if plat_count:
            self.__copy_and_rename_images(plat_count, f"{self._names.ocr_templates}/PlatTemplate",
                                          f"{self._names.ocr_images}/PlatOCR",
                                          f"{self._names.ocr_images}/PlatOCR/PlatUpload", "_Plat.TIF")

        # update OCR device job in DB
        self._lib.db_vpn.update_device_job_for_ocr()
        app_name = 'Kofile.Vanguard.Device.Service.WindowsHost.exe'
        path_to_app = os.path.join(self._data.env.get('device_service_path'), app_name)
        self.__check_and_stop_if_app_already_launched(app_name)
        os.startfile(path_to_app)
        start_time = datetime.now()
        self._actions.log(f'{app_name} launched process is: {self.__check_is_app_already_launched(app_name)}')
        self._actions.log(
            f"Before uploading folder BirthOCR contains: {os.listdir(os.path.join(self._names.ocr_images, 'BirthOCR'))}")
        self._actions.log(
            f"Before uploading folder DeathOCR contains: {os.listdir(os.path.join(self._names.ocr_images, 'DeathOCR'))}")
        while ((os.listdir(os.path.join(self._names.ocr_images, 'BirthOCR', 'BirthUpload')) or
                os.listdir(os.path.join(self._names.ocr_images, 'DeathOCR', 'DeathUpload'))) and
               datetime.now() < start_time + timedelta(minutes=2)):
            self._actions.wait(2)
        self._actions.log(
            f"After uploading folder BirthOCR contains: {os.listdir(os.path.join(self._names.ocr_images, 'BirthOCR'))}")
        self._actions.log(
            f"After uploading folder DeathOCR contains: {os.listdir(os.path.join(self._names.ocr_images, 'DeathOCR'))}")
        self.__check_and_stop_if_app_already_launched(app_name)

        self._actions.step(f"--- SMOKE TEST END --- {__name__} ---")

    # HELPER FUNCTION---------------------------------------------------------------------------------------------------
    def __copy_and_rename_images(self, image_count, template_folder, root_folder, sub_folder, suffix):
        """
        deletes old files in target folders, makes copies of template images in target folders and renames the files
        """
        self._lib.files.clear_download_folder(root_folder, wait_for_file=False)
        self._lib.files.clear_download_folder(sub_folder, wait_for_file=False)
        for _ in range(image_count):
            old_name = f"{template_folder}/template.TIF"
            new_name = f"{datetime.now().timestamp()}{suffix}"
            copy(old_name, f"{root_folder}/{new_name}")
            copy(old_name, f"{sub_folder}/{new_name}")

    @staticmethod
    def __check_and_stop_if_app_already_launched(app_name):
        for proc in psutil.process_iter():
            try:
                if proc.name() == app_name:
                    proc.terminate()
                    proc.wait()
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    @staticmethod
    def __check_is_app_already_launched(app_name):
        for proc in psutil.process_iter():
            if proc.name() == app_name:
                return proc
        return f"No process found by given name: {app_name}"

    def process_reindex_order(self):
        """
            Pre-conditions: Document sent to Re-Index, order number saved to data['order_num']
            Post-conditions: Re-Index order processed and sent to archive
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        # Go to Indexing Queue
        self._lib.general_helper.scroll_and_click(self._pages.CRS.indexing_queue.lnk_go_to_indexing)
        # Wait loading page
        self._lib.general_helper.find(self._pages.CRS.indexing_queue.btn_add_new_indexing_task)
        # Process order
        self._lib.CRS.crs.click_running_man()
        # Wait loading page
        self._lib.general_helper.find(self._pages.CRS.indexing_entry.btn_cancel)
        # Fill required fields if needed
        self._lib.required_fields.crs_fill_required_fields()
        # Save order
        self._lib.general_helper.scroll_and_click(self._pages.CRS.indexing_entry.btn_save_and_advance)
        # Click Next order button
        self._lib.general_helper.find_and_click(self._pages.CRS.indexing_summary.btn_next_order)
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def process_review_order(self):
        """
           Pre-conditions: Indexing Queue is opened. Order status is 'Review'
           Post-conditions: Indexing Summary page is opened
           """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        # Go to Indexing Queue
        self._lib.CRS.crs.go_to_indexing_queue()
        # Verify that order status is 'Reviewed'
        self.check_status_of_order_in_indexing("Review_status")
        self._lib.general_helper.find(
            self._pages.CRS.indexing_queue.btn_administrative, wait_displayed=True)
        self._lib.CRS.crs.click_all_show_all_action_links()
        # click running man
        self._lib.CRS.crs.click_running_man()
        # fill required fields
        self._lib.general_helper.find(
            self._pages.CRS.indexing_entry.btn_save_and_advance, wait_displayed=True)
        self._lib.required_fields.crs_fill_required_fields()
        self._lib.CRS.order_item_type.save_order_in_index_entry()
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def search_birth_death_in_indexing(self, data):
        """
           Pre-conditions: Birth/Death document is pre-created from Capture, Indexing or OCR and archived.
           Doc number is stored in data.
           Post-conditions: Document is found in Indexing search by recorded year and doc number.
           """
        self._actions.step(f"--- ATOMIC TEST --- {__name__} ---")

        general.go_to_crs()
        self._lib.CRS.indexing_queue.select_new_indexing_task(data)
        self._lib.CRS.indexing_entry.click_on_upload_button()
        self._lib.general_helper.find_and_send_keys(
            self._pages.CRS.indexing_entry.pup_choose_image_txt_recorded_year,
            data["doc_year"])
        self._lib.general_helper.find_and_send_keys(self._pages.CRS.indexing_entry.pup_choose_image_txt_doc_number,
                                                    data["doc_number"])
        self._lib.general_helper.find_and_click(self._pages.CRS.indexing_entry.pup_choose_image_btn_search)
        self._lib.general_helper.wait_for_spinner()
        assert not (self._lib.general_helper.find(self._pages.CRS.indexing_entry.pup_choose_image_txt_birth_date,
                                                  get_text=True) or
                    self._lib.general_helper.find(self._pages.CRS.indexing_entry.pup_choose_image_txt_infant_name,
                                                  get_text=True)), \
            "Document is NOT found in Indexing search"
        self._lib.general_helper.scroll_and_click(self._pages.CRS.indexing_entry.pup_choose_image_btn_upload)
        self._lib.general_helper.wait_for_spinner()
        self._actions.wait_for_element_displayed(self._pages.CRS.indexing_entry.txt_doc_number)
        logging.info(f"Document {data['doc_year']}-{data['doc_number']} is found in Indexing")

        self._actions.step(f"--- ATOMIC TEST END --- {__name__} ---")

    def send_back_to_capture(self, reason="test_reason", description="test_description"):
        """
            Pre-conditions: Indexing Entry or Indexing Summary page is opened
            Post-conditions: 'Send Back to Capture' form is submitted
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        # Click on the 'Send Order to Capture Queue' link
        if (self._lib.general_helper.check_if_element_exists(
                self._pages.CRS.indexing_entry.lnk_send_order_to_capture_queue)):
            self._lib.general_helper.scroll_and_click(
                self._pages.CRS.indexing_entry.lnk_send_order_to_capture_queue, timeout=60)
        else:
            self._lib.general_helper.scroll_and_click(
                self._pages.CRS.indexing_summary.lnk_Send_order_to_capture_queue, timeout=60)
        self._actions.wait_for_element_displayed(
            self._pages.CRS.indexing_entry.pup_send_order_to_capture_txt_reason)
        # Fill reason and descriptions fields
        self._lib.general_helper.find_and_send_keys(
            self._pages.CRS.indexing_entry.pup_send_order_to_capture_txt_reason, reason)
        self._lib.general_helper.find_and_send_keys(
            self._pages.CRS.indexing_entry.pup_send_order_to_capture_txt_description, description)
        # Click on the 'Submit' button
        self._lib.general_helper.find_and_click(
            self._pages.CRS.indexing_entry.pup_send_order_to_capture_lnk_submit)
        self._actions.wait_for_element_displayed(
            self._pages.CRS.indexing_queue.btn_administrative)
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))
