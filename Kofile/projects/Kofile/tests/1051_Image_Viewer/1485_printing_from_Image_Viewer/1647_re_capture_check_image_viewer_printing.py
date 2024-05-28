from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Go to CS, submit 'Re-Capture', find order from capture queue, open,
click on capture summary row,click print icon on image viewer (if configured) and verify that success popup is opened
    """

tags = ['48999_location_2']


class test(TestParent):                                                                                    # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to Clerk Search
        self.atom.CS.general.go_to_cs()
        # Get random doc number for OIT
        self.api.clerc_search(self.data).get_document_number(not_in_workflow=True)
        # Submit document to CRS
        self.atom.CS.general.submit_to_crs()
        # Go to CRS
        self.atom.CRS.general.go_to_crs()
        # Go to 'Capture Queue' and process Re-Capture order
        self.lib.general_helper.scroll_and_click(self.pages.CRS.capture_queue.lnk_go_to_capture)
        # Wait loading page
        self.lib.general_helper.find(self.pages.CRS.capture_queue.btn_start_batch_scan, 90)
        # Process order
        self.lib.CRS.crs.click_running_man()
        # Wait capture summary screen is opened
        self.lib.general_helper.find(self.pages.CRS.capture_summary.btn_cancel_order)
        # Wait loading page
        self.lib.general_helper.wait_for_spinner()
        # Click on Capture table row
        self.lib.general_helper.find_and_click(self.pages.CRS.capture_summary.capture_table_row_before)
        # check printing from image viewer
        self.atom.CRS.image_viewer.print_checking()
        # save order
        self.lib.general_helper.scroll_and_click(self.pages.CRS.capture_summary.btn_save_and_exit)
        self.lib.general_helper.wait_for_spinner()
        # Wait loading page
        self.lib.general_helper.find(self.pages.CRS.capture_queue.btn_start_batch_scan, 90)


if __name__ == '__main__':
    run_test(__file__)
