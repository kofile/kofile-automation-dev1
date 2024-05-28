"""Scan-first (e-file) flow"""

from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS, From order Queue Add New Order -> New "Start Batch Scan" icon is visible near Document Type lookup field
    Click the "Start Batch Scan" button -> "Please Enter Account OR Email OR Name" message is displayed
    Fill order header Name and again click new button -> Scan Documents screen is opened
    Scan 2 rows -> Scanned rows are added with correspond pages, 
                                                    "--Order Type--" DDL is displayed in each row
                                                    While Order type is not selected "Save&Exit" button is disabled
    Click  "--Order Type--" DDL -> configured e-file OITs are shown
    Select 2 different OITs and save -> 2 OITs are displayed in Order Summary screen 
                                                            with scanned images"""

tags = ["48999_location_2"]


class test(TestParent):                                                                               # noqa

    def __init__(self, data):
        self.order_types = [data["OT_1"], data["OT_2"]]
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs()
        self.atom.CRS.order_queue.add_new_order()
        self.lib.CRS.order_entry.click_start_batch_scan_button(expected_error="Please Enter Account OR Email OR Name")
        self.atom.CRS.order_entry.fill_order_header_name()
        self.lib.CRS.order_entry.click_start_batch_scan_button()

        for i, ot in enumerate(self.order_types, 1):
            self.lib.CRS.capture.start_scan()
            self.actions.wait_for_element_not_enabled(self.pages.CRS.capture_summary.btn_save_and_exit)
            self.lib.CRS.capture.select_order_type(ot, row_num=i)
        self.lib.CRS.order_item_type.save_order_in_capture_step(e_file=True)

        for i, ot in enumerate(self.order_types, 1):
            self.lib.CRS.order_summary.verify_type_by_row_index(ot, i)
            self.lib.CRS.capture.click_on_the_document_row(i)
            self.lib.CRS.capture.verify_image_exist_in_image_viewer(i)


if __name__ == '__main__':
    run_test(__file__)
