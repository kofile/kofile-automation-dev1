"""erProxy rejection"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Reject erProxy order"""

tags = ['48999_location_2']


class test(TestParent):                                                                                    # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: Noe
        Post-conditions: erProxy order is rejected
        """

        # submit an erProxy order and get the created order number
        self.atom.CRS.general.go_to_crs()
        self.data["order_number"] = self.atom.ERProxy.general.create_er_proxy(exit_from_er_proxy=False)[0][0]
        self.lib.CRS.crs.go_to_order_queue()
        self.atom.CRS.order_queue.assign_order()
        self.lib.general_helper.wait_for_spinner()

        # edit order
        self.lib.CRS.crs.click_running_man()
        self.actions.wait_for_element_displayed(self.pages.CRS.order_summary.lbl_order_number)

        # reject order
        self.atom.CRS.order_summary.reject_order()

        # go to order search and check that order is rejected
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])

        # check Order Status
        self.lib.CRS.order_search.verify_order_status("Reject_status")

        with self.lib.db as db:
            assert self.lib.general_helper.wait_until(lambda: db.get_package_status(
                self.data["order_number"]) == 32, 120), \
                f"Wrong status, must be 32 but have value {db.get_package_status(self.data['order_number'])}"

        # Check that send back order queue is not displayed
        self.actions.assert_element_not_present(
            self.pages.CRS.order_search.send_back_to_order_queue_icon_by_order_number(self.data["order_number"]))


if __name__ == '__main__':
    run_test(__file__)
