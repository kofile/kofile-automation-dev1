from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS ->
    Workflow Order Step ->
    Workflow Capture Step ->
    Enter a Party First Name and Last Name ->
    Check the flip checkbox -> First Name and Last Name are reversed in order
    Uncheck the flip checkbox ->
    Names are flipped back to original text
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

        self.lib.CRS.indexing_entry.flip_party_names()


if __name__ == '__main__':
    run_test(__file__)
