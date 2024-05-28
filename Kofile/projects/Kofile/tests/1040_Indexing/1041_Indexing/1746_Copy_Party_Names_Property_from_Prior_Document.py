from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS ->
    Workflow Order Step ->
    Workflow Capture Step ->
    Check navigation to next order item -> 
    Click on Copy Names link in Parties section -> A pop up is opened to search for existing document
    Click on Copy from Prior Document link -> Prior OIT Party Names/Property is copied into current OIT fields
        """

tags = []


class test(TestParent):                                                                                   # noqa

    def __init__(self, data, oi_count=2, test_name="test"):
        self.oi_count, self.test_name = oi_count, test_name
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Workflow Capture Step
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order, open_crs=True,
                                                               oi_count=self.oi_count)
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.order_item_type.scan_and_map(self.oi_count)
        self.lib.CRS.order_item_type.save_order_in_capture_step()
        self.lib.CRS.order_item_type.index_order()

        self.lib.general_helper.find_and_send_keys(self.pages.CRS.indexing_entry.grantor_name_input, self.test_name)
        self.lib.general_helper.find_and_click(self.pages.CRS.indexing_entry.btn_save_and_advance)
        self.actions.wait_for_element_displayed(self.pages.CRS.indexing_entry.indexing_header)

        self.lib.CRS.indexing_entry.copy_names_from_prior_document(self.test_name)


if __name__ == '__main__':
    run_test(__file__)
