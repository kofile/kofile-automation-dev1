from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS
    - Navigate to Capture Queue and Click on the "Historical Capture" tab
    - Scan an image and click on the document row -> Image is available in image viewer
    - Map document to any historical capture doc group (use query to find them) e.g. RP, new do number 
    - Scan a second image and map it with the same data using the ALT+R keyboard combination
        """

tags = ["48999_location_2"]


class test(TestParent):                                                                               # noqa
    new_order_documents = "New order documents"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.actions.store("historical", True)

        with self.lib.db as db:
            doc_group_id, doc_group, oit_name = db.get_historical_capture_doc_groups()[int(self.data["db_row_index"])]
        self.actions.store("doc_group", doc_group)

        self.atom.CRS.general.go_to_crs()
        self.actions.store('doc_types', [self.api.capture(self.data).get_doc_type(doc_group=doc_group)])
        # Scan an image and map to new historical document
        self.lib.CRS.order_item_type.scan_and_map()
        orig_doc_group = self.lib.CRS.capture.get_doc_group(self.new_order_documents, 1)
        orig_doc_type = self.lib.CRS.capture.get_doc_type(self.new_order_documents, 1)
        orig_year = self.lib.CRS.capture.get_recorded_year(self.new_order_documents, 1)
        # Scan a 2-nd image
        self.lib.CRS.capture.start_scan()
        # Map it with the same data using the ALT+R keyboard combination
        self.lib.CRS.capture.click_edit_icon()
        row1 = self.lib.general_helper.find_and_click(
            self.pages.CRS.capture_summary.doc_group_not_mapped_by_row_index())
        row1.send_keys(self.keys.ALT, "r")
        self.lib.CRS.capture.click_edit_icon()
        self.lib.general_helper.wait_for_spinner()

        copied_doc_group = self.lib.CRS.capture.get_doc_group(self.new_order_documents, 2)
        copied_doc_type = self.lib.CRS.capture.get_doc_type(self.new_order_documents, 2)
        copied_year = self.lib.CRS.capture.get_recorded_year(self.new_order_documents, 2)

        assert orig_doc_group == copied_doc_group, \
            f"Expected DOC GROUP '{orig_doc_group}' is not equal to actual '{copied_doc_group}'"
        assert orig_doc_type == copied_doc_type, \
            f"Expected DOC TYPE '{orig_doc_type}' is not equal to actual '{copied_doc_type}'"
        assert orig_year == copied_year, f"Expected Recorded Year '{orig_year}' is not equal to actual '{copied_year}'"


if __name__ == '__main__':
    run_test(__file__)
