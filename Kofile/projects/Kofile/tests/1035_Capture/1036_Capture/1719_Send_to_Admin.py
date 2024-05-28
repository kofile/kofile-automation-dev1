from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS, add an order, ex, RP and finalize
    - Navigate to Capture Queue and scan an image
    - Click on the document row, enter doc group, doc type, year, doc number, pages and click on the edit button
    - Click on the "Send to Administrator" link
    - Enter reason and description and click on the "Submit" button
    - Search order via order number -> Order is found. Order status is "Admin Suspend"
    - Click on the Running man -> "Capture Summary" page is opened. Document row is shown. Document status is "Scanned"
    - Click on the document row -> Image is available in image viewer
    - Click "Save & Exit" button
    - Go to Search and Search order -> Order is moved to Indexing
        """

tags = ["48999_location_2"]


class test(TestParent):                                                                     # noqa

    def __init__(self, data, ind=2):
        self.ind = ind
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order, ind=self.ind)
        self.lib.CRS.order_item_type.scan_and_map()
        self.lib.CRS.capture.verify_image_exist_in_image_viewer(mapped=True)
        self.lib.CRS.capture.send_to_administrator()

        self.lib.CRS.crs.click_running_man()
        self.lib.CRS.capture.verify_image_exist_in_image_viewer(mapped=True)
        self.lib.CRS.order_item_type.save_order_in_capture_step()

        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_status_indexing()


if __name__ == '__main__':
    run_test(__file__)
