from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
From Capture step Upload  .TIFF files from the source storage and drag and drop them to the drop zone.
Click on edit pencil in the capture row
select Doc group doc type for OI CCM
fill in missing data and click the edit pencil again
fill in the Meeting Date required field and Agenda Item required/not required (according to configuration ) 
field from the expanded CCM OIT form  opened by the system. then click on Save and Exit button
"""

tags = ['48999_location_2']


class test(TestParent):

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        self.lib.CRS.crs.go_to_capture_queue()
        self.lib.general_helper.scroll_and_click(self.pages.CRS.capture_queue.btn_start_batch_scan)
        self.lib.general_helper.find_and_click(self.pages.CRS.capture_summary.upload_tab)
        drop_zone = self.lib.general_helper.find(self.pages.CRS.capture_summary.drop_zone)
        self.lib.general_helper.drop_file(drop_zone, self.names.tiff_file_path)

        self.lib.general_helper.find_and_click(self.pages.CRS.capture_summary.edit_button)
        self.lib.CRS.capture.add_doc_group_and_doc_type()
        self.lib.CRS.capture.add_doc_number()
        page_count = self.lib.CRS.capture.add_pages_count()
        self.lib.general_helper.find_and_click(self.pages.CRS.capture_summary.edit_button)
        self.lib.general_helper.wait_for_spinner()
        self.actions.wait(3)
        self.lib.general_helper.find_and_click(self.pages.CRS.capture_summary.btn_save_and_exit)
        self.lib.general_helper.wait_for_spinner()
        self.actions.wait_for_window_present_by_partial_url("ShowCaptureQueue")

        self.lib.CRS.crs.go_to_indexing_queue()
        self.atom.CRS.order_queue.assign_order()
        self.lib.CRS.crs.click_running_man()

        self.actions.wait_for_element_displayed(self.pages.CRS.image_viewer.lbl_total_images, timeout=120)
        self.actions.wait_for_element_text(self.pages.CRS.image_viewer.lbl_total_images, page_count)


if __name__ == '__main__':
    run_test(__file__)
