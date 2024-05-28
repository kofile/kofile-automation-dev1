""" Print from CS """
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test
from datetime import datetime

description = """
Create and process the order up to Archive step and find in CS
Click the "Print" icon
From CS print the document  that has redacted images
Click print
Print with "Redacted " option
"""

tags = ['48999_location_2']


class test(TestParent):                                                                                    # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__, precondition=self._precondition)

    def __test__(self):
        printer_id = self.data["env"].get("printer_id")

        self.atom.CS.general.go_to_cs()
        self.lib.CS.general.search_by_keyword(f'{datetime.now().strftime("%Y")}-{self.data.get("doc_num").lstrip("/")}')
        with self.lib.db as db:
            last_id = db.get_last_device_jobs(device_id=printer_id)[0][0]

            self.lib.CS.general.click_on_printer_by_row_index()
            new_id = None
            for _ in range(30):
                new_id = db.get_device_jobs_id(device_id=printer_id, device_job_id=last_id)
                if last_id < new_id:
                    break
                self.actions.wait(2)

            assert new_id, "new job for print not created"

            self.actions.wait(5)
            db.update_printer_job(self.data.env.printer_id, job_id=new_id)
        self.actions.wait(5)

        self.actions.wait_for_element_displayed(self.pages.PS.main_page.ms_popup_window)
        self.actions.wait_for_element_text(self.pages.PS.main_page.ms_popup_ms, "Printing success")
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.btn_close_pup_print)

        self.lib.files.download_and_compare_pdf_new(self.data, None, device_job_id=new_id,
                                                    folder_pattern="wfcontent-psexchange-{}", equals_pages=4)

    def _precondition(self):
        self.lib.data_helper.test_config()
        self.atom.CS.api_helper.initialize_drawer()
        self.atom.CS.api_helper.create_order()
        self.atom.CS.api_helper.capture_document()
        self.atom.CS.api_helper.index_document()
        self.atom.CS.api_helper.verify_document()
        self.lib.db_with_vpn.scheduler_job_update_for_set_export_document(self.data["test_config"]["dept_id"])


if __name__ == '__main__':
    run_test(__file__)
