"""Scan-first (e-file) flow"""

from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS, from order Queue Add New Order and fill order header
    Click the "Start Batch Scan" button -> Scan Documents screen is opened
    Start Scan 3 times to add to different rows -> 
                --Order Type-- drop-down and 'Apply All' action link added to the capture header
                NOT MAPPED label is available under the Order# 
                Only "Order Type" field is available on each row
                While Order Type is not selected Apply All link is disabled
    Click "--Order Type--" DDL on capture header -> configured e-file OITs (e.g AN and RP) are shown
    Select one of the options (e.g. RP) -> 'Apply All' action link becomes enabled
    Click the link -> -- Order Type -- automatically updated to the selected order type for all rows 
                    with ability manually change Order Type for 
                    "Edit" action icon is hidden from row level actions only delete action is visible
    Check the links -> 'Save Batch For Later Processing','Send to Administrator' action links are hidden
    Click each row -> Images are displayed on image viewer"""

tags = ["48999_location_2"]


class test(TestParent):                                                                         # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        order_type = self.data["order_type"]

        self.atom.CRS.general.go_to_crs()
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.fill_order_header_name()
        self.lib.CRS.order_entry.click_start_batch_scan_button()

        # Add 3 rows and check order type
        for i in range(1, 4):
            self.lib.CRS.capture.start_scan()
            assert not self.lib.CRS.capture.get_order_type(i), f"Order type[{i}] unexpectedly selected"

        self.actions.verify_element_attribute(self.pages.CRS.capture_summary.lnk_scan_documents__apply_all, "class",
                                              "disable")
        # Select order type on capture header and apply it for all rows
        self.lib.CRS.capture.select_order_type(order_type, row_num=0)
        self.lib.CRS.capture.click__apply_all__order_types()
        for i, ot in enumerate([order_type] * 3, 1):
            order_type = self.lib.CRS.capture.get_order_type(i)
            assert ot == order_type, f"Expected order type: {ot} is not equal to actual: '{order_type}'"
            self.lib.CRS.capture.click_on_the_document_row(i)
            self.lib.CRS.capture.verify_image_exist_in_image_viewer(i)

        self.actions.verify_element_not_present(self.pages.CRS.capture_summary.lnk_save_batch_for_later_processing)
        self.actions.verify_element_not_present(self.pages.CRS.capture_summary.lnk_send_to_administrator)


if __name__ == '__main__':
    run_test(__file__)
