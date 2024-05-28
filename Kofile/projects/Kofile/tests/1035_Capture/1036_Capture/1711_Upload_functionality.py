from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS
    - Add new Plat OIT and finalize
    - Navigate to Capture Queue
    - Search order via order number -> Order found. Order status is Pending.
                                       Upload button is shown on the right side of Clerk's name
    - Click on the Upload button -> "Choose image" popup is shown
    - verify that doc_group_doc_number ddl exists
    - Select image and click on the "Reset" link
    - Select image and click on the "Return Current Page To Folder action link" link
    - Select image and click on the "Upload" button -> Order is moved to Indexing Queue
        """

tags = ["48999_location_2"]


class test(TestParent):                                                                             # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__, precondition=self._precondition)

    def __test__(self):
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)

        self.lib.CRS.crs.go_to_capture_queue()
        self.atom.CRS.capture.upload_image()

        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_status_indexing()

    def _precondition(self):
        with self.lib.db as db:
            active_files = db.get_active_files_in_upload_folder(
                folder_name=self.data['config'].test_data(f"{self.data.OIT}.capture.upload_image.folder"))
            if not active_files:
                db.update_files_in_upload_folder(
                    folder_name=self.data['config'].test_data(f"{self.data.OIT}.capture.upload_image.folder"),
                    file_number=10)


if __name__ == '__main__':
    run_test(__file__)
