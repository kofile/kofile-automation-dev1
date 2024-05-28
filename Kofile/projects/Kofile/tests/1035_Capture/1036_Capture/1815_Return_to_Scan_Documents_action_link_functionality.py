"""Scan-first (e-file) flow"""

from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS, click on Add New Order button and fill order header
    Click the "Start Batch Scan" button
    Scan 2 rows rows and select different Order Types
    Save scanned documents and check Order Summary screen
    Click "Return to Scan Document(s)" link -> Scan Documents screen is opened, Scanned rows are displayed 
                                                with selected OITs and with the ability change OIT
    Add new pages on one of the documents and save
    Edit OIT and save -> Order summary screen is opened, OIT has Reviewed status. Document type is displayed
    Click "Return to Scan Document(s)" link
    Change the 1-st order type, save and check Order Summary screen
    Click + New Order Item action link and add non e-file OIT -> "Return to Scan Document(s)" link is still shown
    Remove all e-file service type OITs -> Only the non e-file OIT is shown. Return to Scan Document(s) link disappears
    """

tags = ["48999_location_2"]


class test(TestParent):                                                                               # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):

        order_types = [self.data["OT_1"], self.data["OT_2"]]

        # Scan 2 rows and select order types
        self.atom.CRS.order_queue.add_order_with_scan_first_flow(order_types=order_types)

        self.lib.CRS.order_summary.click_return_to_scan_documents_link()
        for i, ot in enumerate(order_types, 1):
            order_type = self.lib.CRS.capture.get_order_type(i, mapped=True)
            assert ot == order_type, f"Expected order type: {ot} is not equal to actual: '{order_type}'"
        self.lib.CRS.capture.verify_image_exist_in_image_viewer(1, mapped=True)

        # Add new pages and save
        self.lib.CRS.capture.start_scan()
        self.lib.CRS.order_item_type.save_order_in_capture_step(e_file=True)

        # Edit the 1-st oit
        self.lib.CRS.order_summary.click_edit_icon_by_row_index(1)
        self.lib.required_fields.crs_fill_required_fields()
        self.lib.CRS.order_entry.click_add_to_order()

        self.lib.CRS.order_summary.click_return_to_scan_documents_link()
        for i, ot in enumerate(order_types, 1):
            order_type = self.lib.CRS.capture.get_order_type(i, mapped=True)
            assert ot == order_type, f"Expected order type: {ot} is not equal to actual: '{order_type}'"

        # Change the 1-st order type
        self.lib.CRS.capture.select_order_type(order_types[1], row_num=1, mapped=True)
        self.lib.CRS.order_item_type.save_order_in_capture_step(e_file=True)

        for i, ot in enumerate([order_types[1]] * 2, 1):
            self.lib.CRS.order_summary.verify_type_by_row_index(ot, i)
            self.lib.CRS.order_summary.verify_status_by_row_index("Pending", i)

        # Add a non e-file oit
        self.lib.CRS.order_summary.click_new_order_item_icon()
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.one_oit_to_summary()
        # 'Return to scan documents' should be ENABLED
        self.lib.general_helper.find(self.pages.CRS.order_summary.lnk_return_to_scan_documents, wait_displayed=True)

        # Delete the e-file OITs
        self.lib.CRS.order_summary.click_delete_icon_by_row_index(2)
        self.lib.CRS.order_summary.click_delete_icon_by_row_index(1)
        # 'Return to scan documents' should disappear
        assert not self.lib.general_helper.check_if_element_exists(
            self.pages.CRS.order_summary.lnk_return_to_scan_documents), \
            "Return to Scan Document(s) link is unexpectedly found!"


if __name__ == '__main__':
    run_test(__file__)
