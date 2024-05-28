"""smoke test"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS, create new order, finalize the order, capture and map, self
    index the order, verify the order, order is in archive"""

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: no
        Post-conditions: Order is processed from Order Queue to Archive
        """

        self.lib.general_helper.check_order_type()
        # atom

        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        if self.data["OIT"] == "RP_Recordings":
            self.atom.CRS.general.go_to_crs()
        self.lib.CRS.order_item_type.capture_step()
        self.lib.CRS.order_item_type.indexing_step()
        self.lib.CRS.order_item_type.verification_step()
        # verify order is in archive
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
        self.lib.CRS.order_search.verify_order_status("archive_status")


if __name__ == '__main__':
    run_test(__file__)
