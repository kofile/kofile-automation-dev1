from PIL import Image, ImageChops, ImageStat
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test
from bs4 import BeautifulSoup

description = """
    Create a new order in CRS, finalize, scan and map, self-index and verify the order.
    On each step where image of doc is available, click the 
    print icon in image viewer (if configured) and verify that success popup is opened"""

tags = ['48999_location_2']


class test(TestParent):  # noqa
    old_device_job_id = 0
    steps = {
        "CAPTURE": "capture",
        "INDEXING ENTRY": "indexing",
        "INDEXING SUMMARY": "indexing",
        "VERIFICATION ENTRY": "verification",
        "VERIFICATION SUMMARY": "verification"
    }

    def __init__(self, data):
        super(test, self).__init__(data, __name__)
        self.lib.db.disconnect_from_db(use_vpn=True)

    def get_last_printing_file(self):
        device_id = self.data.env.get("printer_id")
        self.lib.general_helper.wait_until(lambda: self.lib.db.get_last_device_jobs(
            device_id=device_id)[0][0] != self.old_device_job_id, timeout=30)
        device_job = self.lib.db.get_last_device_jobs(device_id=device_id)
        self.old_device_job_id = device_job[0][0]
        filepath = BeautifulSoup(device_job[0][5], "lxml").find("filepath").text
        return self.lib.azure.check_blob_existence_in_container(
            file_name=filepath, container=f"genimages-{self.data.env.code}").download_blob().readall()

    def get_images_from_page(self):
        result = dict()
        page_count = int(self.lib.general_helper.find(self.pages.CRS.image_viewer.lbl_total_images, get_text=True))
        for page in range(page_count):
            self.actions.wait_for_element_present(self.pages.CRS.image_viewer.page_number_input)
            self.actions.clear_element(self.pages.CRS.image_viewer.page_number_input)
            self.actions.send_keys(self.pages.CRS.image_viewer.page_number_input, (f"{page + 1}", self.keys.ENTER))
            self.lib.general_helper.wait_until(lambda: self.lib.general_helper.find(
                self.pages.CRS.image_viewer.image_src, get_attribute="src") is not None, timeout=10)
            src = self.lib.general_helper.find(self.pages.CRS.image_viewer.image_src, get_attribute="src")
            if src:
                result[page + 1] = Image.open(self.lib.image_recognition.load_image(src).raw)
        return result

    def images_equals(self, step, limit):
        printed_images = self.lib.files.pdf_to_images(self.get_last_printing_file())
        page_images = self.get_images_from_page()
        for key, image in page_images.items():
            if self.data['config'].test_data(f"{self.data.OIT}.{self.steps[step]}.first_page_to_last_page"):
                image_key = 1 if key == len(page_images) else key + 1
            else:
                image_key = key
            self.lib.image_recognition.verify_image_changes_on_viewer(
                f"{image_key} origin", element=printed_images[key], retry=1, place=f"page: {key}, printed from {step}",
                click_fit=False)
            img_2 = printed_images[key].resize(image.size).convert("RGB")
            diff = ImageChops.difference(image.convert("RGB"), img_2)
            stat = ImageStat.Stat(diff)
            diff_ratio = sum(stat.mean) / (len(stat.mean) * 255)
            image.close()
            img_2.close()
            printed_images[key].close()
            assert diff_ratio * 100 < limit, f"Different {diff_ratio * 100} on page {key}. Step {step}"

    def __test__(self):
        self.lib.db.connect_to_db(use_vpn=True)
        self.data["current_oit"] = self.data.OIT
        self.lib.general_helper.check_order_type()
        # atom - create and finalize order
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        # if OIT is RP, reload the page to navigate further
        if self.data["OIT"] == "RP_Recordings":
            self.atom.CRS.general.go_to_crs()

        # if OIT has Capture step, scan and map
        if self.data['config'].test_data(f"{self.data.OIT}.capture.step"):
            self.lib.CRS.order_item_type.scan_and_map()
            # print from image viewer in capture
            self.actions.click(self.pages.CRS.capture_summary.img_capture_summary)
            self.actions.step('CAPTURE')
            self.old_device_job_id = self.lib.db.get_last_device_jobs(device_id=self.data.env.get("printer_id"))[0][0]
            self.atom.CRS.image_viewer.print_checking()
            self.images_equals("CAPTURE", 3)
            # save the order
            self.lib.CRS.order_item_type.save_order_in_capture_step()

        # if OIT has indexing step, index
        if self.data['config'].test_data(f"{self.data.OIT}.indexing.step"):
            if self.data['config'].test_data(f"{self.data.OIT}.indexing.indexing_type") == 'self':
                # index the order
                self.lib.CRS.order_item_type.index_order()
                # print from image viewer in indexing entry
                self.actions.step('INDEXING ENTRY')
                self.old_device_job_id = self.lib.db.get_last_device_jobs(device_id=self.data.env.get("printer_id"))[0][
                    0]
                self.atom.CRS.image_viewer.print_checking()
                self.images_equals("INDEXING ENTRY", 5)
                # save the order
                self.lib.CRS.order_item_type.save_order_in_index_entry()
                # print from image viewer in indexing summary
                self.actions.click(self.pages.CRS.indexing_summary.image())
                self.actions.step('INDEXING SUMMARY')
                self.old_device_job_id = self.lib.db.get_last_device_jobs(device_id=self.data.env.get("printer_id"))[0][
                    0]
                self.atom.CRS.image_viewer.print_checking()
                self.images_equals("INDEXING SUMMARY", 5)
                # click next order
                self.lib.CRS.order_item_type.next_order_in_index_summary()

        # if OIT has verification step, verify
        if self.data['config'].test_data(f"{self.data.OIT}.verification.step"):
            # verify the order
            self.lib.CRS.order_item_type.index_order(self.lib.CRS.crs.go_to_verification_queue)
            self.lib.CRS.order_item_type.re_key_in_verification()
            # print from image viewer in verification entry
            self.actions.step('VERIFICATION ENTRY')
            self.old_device_job_id = self.lib.db.get_last_device_jobs(device_id=self.data.env.get("printer_id"))[0][0]
            self.atom.CRS.image_viewer.print_checking()
            self.images_equals("VERIFICATION ENTRY", 5)
            # save the order
            self.lib.CRS.order_item_type.save_order_in_verification_entry()
            # print from image viewer in verification summary
            self.actions.click(self.pages.CRS.verification_summary.img_table_data)
            self.actions.step('VERIFICATION SUMMARY')
            self.old_device_job_id = self.lib.db.get_last_device_jobs(device_id=self.data.env.get("printer_id"))[0][0]
            self.atom.CRS.image_viewer.print_checking()
            self.images_equals("VERIFICATION SUMMARY", 5)
            # click next order
            self.lib.CRS.order_item_type.next_order_in_verification_summary(open_crs_in_end=False)

            # check document is exported to CS
            self.lib.db_with_vpn.scheduler_job_update_for_set_export_document(
                dept_id=self.data.config.test_config()["dept_id"])
            self.atom.CS.general.go_to_cs(load_config=False)
            cs_doc = self.api.clerc_search(self.data).search_by_doc_number(
                doc_number=f"{self.data['doc_year']}-{self.data['doc_number']}")
            assert cs_doc["Filename"], "Image isn't exist in Clerc Search!"


if __name__ == '__main__':
    run_test(__file__)
