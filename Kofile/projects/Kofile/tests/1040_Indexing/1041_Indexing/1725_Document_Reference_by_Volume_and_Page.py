from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS ->
    Workflow Order Step ->
    Workflow Capture Step ->
    Enter the Volume and Page of existing document in Document Reference field ->
    The existing document is found and its Type and Doc Number are correctly displayed next to the field
        """

tags = []


class test(TestParent):                                                                            # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Workflow Capture Step
        self.lib.data_helper.get_dept_id()
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order, open_crs=True)
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.order_item_type.scan_and_map()
        self.lib.CRS.order_item_type.save_order_in_capture_step()
        self.lib.CRS.order_item_type.index_order()
        self.lib.CRS.indexing_entry.set_reference_document_by_vol_and_page()


if __name__ == '__main__':
    run_test(__file__)
