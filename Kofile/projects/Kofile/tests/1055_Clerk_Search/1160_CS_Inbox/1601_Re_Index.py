from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Go to CS, submit 'Re-Index' to CRS by DOC number, finalize and check order
    """

tags = ['48999_location_2']


class test(TestParent):                                                                                     # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__, precondition=self._precondition)

    def __test__(self):
        self.atom.CS.general.go_to_cs()
        # Get random doc number for OIT
        self.api.clerc_search(self.data).get_document_number(not_in_workflow=True)
        # Submit document to CRS
        self.atom.CS.general.submit_to_crs()
        # Go to CRS
        self.atom.CRS.general.go_to_crs()
        # Go to 'Order Search' and verify document status
        self.atom.CRS.order_search.verify_order_status("Indexing")
        # Go to 'Indexing Queue' and process Re-Index order
        self.atom.CRS.indexing.process_reindex_order()
        # Go to 'Order Search' and verify document status
        self.atom.CRS.order_search.verify_order_status("Archive")


    def _precondition(self):
        self.lib.data_helper.test_config()
        self.atom.CS.api_helper.initialize_drawer()
        self.atom.CS.api_helper.create_order()
        self.atom.CS.api_helper.capture_document()
        self.atom.CS.api_helper.index_document()
        self.atom.CS.api_helper.verify_document()
        self.lib.db_with_vpn.scheduler_job_update_for_set_export_document(self.data["test_config"]["dept_id"])

if __name__ == '__main__':
    run_test(__file__)
