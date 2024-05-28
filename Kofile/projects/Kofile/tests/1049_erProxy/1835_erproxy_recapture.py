"""erProxy Re-Capture"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Create and process an erProxy order to Re-Capture and check the cover page presence"""

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data):
        data["use_doc_type_in_api_CS"] = True
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: erProxy order is created, processed to Archive, sent to Recapture and re-Archived
        """
        self.lib.data_helper.test_config()

        self.lib.general_helper.check_order_type()
        cover_page_text = self.data['config'].test_data(f"{self.data.OIT}.cover_page_text")

        self.atom.ERProxy.general.create_and_finalize_er_proxy(self.data)
        # Indexing
        self.lib.CRS.order_item_type.indexing_step()
        # Verification
        self.lib.CRS.order_item_type.verification_step(open_crs_in_end=False)
        # verify Archive status in Order Search
        self.lib.CRS.crs.go_to_order_search()
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
        self.lib.CRS.order_search.verify_order_status_archive()
        # send order to ReCapture
        self.lib.db_with_vpn.scheduler_job_update_for_set_export_document(1)
        self.lib.CS.general.send_created_doc_to_recapture(self.data, dept_id=1)
        self.lib.CRS.capture.open_image_in_image_viewer()
        if self.data['config'].test_data(f"{self.data.OIT}.cover_page"):
            self.lib.CRS.image_viewer.verify_text_on_image(
                self.data, text=cover_page_text, last_page=True,
                step="ReCapture", should_exist=True, crop=True, offset=500)
        self.lib.CRS.order_item_type.save_order_in_capture_step()


if __name__ == '__main__':
    run_test(__file__)
