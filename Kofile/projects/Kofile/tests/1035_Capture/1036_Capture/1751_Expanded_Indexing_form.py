from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS, create and finalize an ML order
    - Go to Capture Queue and start Batch Scan
    - Scan an image and map it to ML order
    - Fill all fields and remember them, click on Save and Exit -> Order moves to Archive
    - Verify in CS -> Image exist and fields from expanded indexing saved in CS
        """

tags = ["48999_location_2"]


class test(TestParent):                                                                              # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.data_helper.test_config()

        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        self.lib.CRS.order_item_type.scan_and_map()
        exp_ind = self.lib.CRS.capture.get_expanded_indexing_values()
        self.lib.CRS.order_item_type.save_order_in_capture_step()

        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_status_verification()

        # Update scheduler export job date in DB
        self.lib.db_with_vpn.scheduler_job_update_for_set_export_document(
            dept_id=self.data["test_config"]["dept_id"])
        # Go to CS
        self.atom.CS.general.go_to_cs(load_config=False)
        # Search document in CS
        cs_doc = self.api.clerc_search(self.data).search_by_doc_number(
            doc_number=f"{self.data['doc_year']}-{self.data['doc_number']}")

        assert cs_doc["Filename"], "Document doesn't exist in Clerk Search!"
        assert cs_doc["Applicant1"][0] == exp_ind[self.data['config'].test_data(
            f'{self.data.OIT}.expended_form.Applicant1')].rstrip(), "Wrong Applicant1 name:\n " \
            f"Expected: {self.data['config'].test_data(f'{self.data.OIT}.expended_form.Applicant1')} \
                Actual: {cs_doc['Applicant1']}"
        assert cs_doc["Applicant2"][0] == exp_ind[self.data['config'].test_data(
            f'{self.data.OIT}.expended_form.Applicant2')].rstrip(), "Wrong Applicant2 name:\n " \
            f"Expected: {self.data['OIT']['Applicant2']} \nActual: {cs_doc['Applicant2']}"
        for i in self.data['config'].test_data(f'{self.data.OIT}.expended_form.ReturnAddress'):
            assert exp_ind[i] in cs_doc["ReturnAddress"], f"Some of expected address fields not found in\
                CS: {exp_ind[i]} not in {cs_doc['ReturnAddress']}"


if __name__ == '__main__':
    run_test(__file__)
