from datetime import datetime
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS > Capture Queue
    - Click on the "Start Batch Scan" button
    - Click on the "Start Scan" button
    - Click on the document row
    - Enter doc group, doc type, doc#, pages and click on the edit (pencil) button 
        for OIT which start from Capture step(e.g. Commissioner Courts)
    - Fill expended forms(if exists) and click on the "Save & Exit" button
    - Go to Clerk Search > Search document by doc number
        """

tags = ["48999_location_2"]


class test(TestParent):                                                                       # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.data_helper.test_config()
        # Go to CRS
        self.atom.CRS.general.go_to_crs()
        now = datetime.now()
        # Generate doc number
        self.data["doc_number"] = now.strftime("%m%d%H%M%S")
        doc_number = f"{now.year}-{self.data['doc_number']}"
        self.lib.CRS.order_item_type.scan_and_map()
        self.lib.CRS.order_item_type.save_order_in_capture_step()

        # Update scheduler export job date in DB
        self.lib.db_with_vpn.scheduler_job_update_for_set_export_document(
            dept_id=self.data["test_config"]["dept_id"])
        # Go to CS
        self.atom.CS.general.go_to_cs(load_config=False)
        # Search document in CS
        self.api.clerc_search(self.data).search_by_doc_number(doc_number)


if __name__ == '__main__':
    run_test(__file__)
