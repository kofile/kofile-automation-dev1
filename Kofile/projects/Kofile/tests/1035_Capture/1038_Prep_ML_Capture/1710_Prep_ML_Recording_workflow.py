from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS ->
    Workflow Order Step for ML ->
    Navigate to Capture Queue ->
    Click on the "Start Batch Scan" button -> "Capture Summary" page is opened
    Click on the "Prep ML Recording" tab -> "Prep ML Recording" tab is selected
    Click on the "Add Row" (+) button -> New document row is added
    Click on the edit button (pencil) ->
    Enter doc group, doc type, doc# values from finalized ML order ->
    Click on the edit button (pencil) -> Mapping is correct
                                        Expanded form is shown
    Fill all required fields -> Additional buttons in document row are available:
                                - Print Application
                                - Print Certificate
                                - Start Scan
                                - Stop Scan (disabled by default)
    Click on the "Print Application" button -> Application form is printed
    Click on the "Print Certificate" button -> Certificate form is printed
    Click on the "Start Scan" button -> "Stop Scan" button is available during scanning
    Click on the "Stop Scan" -> Scanning is stopped
    Click on the "Start Scan" button -> Document is scanned
    Click on the document row -> Image is available in image viewer "Save & Exit" button is available
    Click on the "Save & Exit" button -> Order is moved to Archive
    Navigate to CS ->
    Search order via doc number -> Document is found
    Click on the document row->
    Preview popup is opened
    Image is available in image viewer
        """

tags = []


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Workflow Capture Step
        self.lib.general_helper.check_order_type()
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order,
                                                               open_crs=True)
        self.lib.CRS.order_item_type.scan_and_map_pre_ml()
        self.lib.CRS.capture.print_application()
        self.lib.CRS.capture.print_application(True)
        self.lib.CRS.capture.scan_re_ml(stop=True)
        self.lib.CRS.capture.scan_re_ml()
        self.actions.wait_for_element_enabled(self.pages.CRS.capture_summary.btn_save_and_exit)
        self.lib.CRS.capture.check_doc_view()


if __name__ == '__main__':
    run_test(__file__)
