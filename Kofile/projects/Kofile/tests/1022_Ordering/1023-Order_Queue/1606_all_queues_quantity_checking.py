from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Go to CRS, count order numbers in all queues and compare with total order number for each queue"""


tags = ['48999_location_2']


class test(TestParent):                                                                      # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # go to CRS
        self.atom.CRS.general.go_to_crs()
        self.actions.wait_for_element_displayed(self.pages.CRS.general.btn_add_new_order)
        self.lib.CRS.crs.check_count_orders()

        # check orders in Capture queue
        self.lib.CRS.crs.go_to_capture_queue()
        self.actions.wait_for_element_displayed(self.pages.CRS.capture_queue.btn_start_batch_scan)
        self.lib.CRS.crs.check_count_orders()

        # check orders in Indexing queue
        self.lib.CRS.crs.go_to_indexing_queue()
        self.actions.wait_for_element_displayed(self.pages.CRS.indexing_queue.btn_add_new_indexing_task)
        self.lib.CRS.crs.check_count_orders()

        # check orders in Verification queue
        self.lib.CRS.crs.go_to_verification_queue()
        self.actions.wait_for_element_displayed(self.pages.CRS.general.btn_refresh)
        self.lib.CRS.crs.check_count_orders()


if __name__ == '__main__':
    run_test(__file__)
