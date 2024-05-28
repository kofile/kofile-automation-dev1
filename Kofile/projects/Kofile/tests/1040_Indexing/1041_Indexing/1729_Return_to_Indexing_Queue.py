from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS ->
    Workflow Order Step ->
    Workflow Capture Step ->
    click on Return to Indexing Queue link ->
    Indexing Queue page is displayed
    Order Status = In Process, Assignment to Clerk is preserved
        """

tags = []


class test(TestParent):                                                                            # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Workflow Capture Step
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order, open_crs=True)
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.order_item_type.scan_and_map()
        self.lib.CRS.order_item_type.save_order_in_capture_step()
        self.lib.CRS.order_item_type.index_order()
        self.lib.general_helper.find_and_click(self.pages.CRS.indexing_entry.btn_cancel)
        self.lib.CRS.indexing_entry.return_to_indexing_queue()


if __name__ == '__main__':
    run_test(__file__)
