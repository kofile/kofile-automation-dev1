"""Test-Edit Order from Order Search"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Create/Finalize Order, click on Edit Order from Order Search and check navigation to correct page"""

tags = ['48999_location_2']


class test(TestParent):                                                                                  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: Order is opened for Edit in Order Summary or Order Finalization pages
        """
        self.data['current_oit'] = self.data.OIT
        # create order, search order in Order Search (atom tests)
        self.atom.CRS.order_queue.create_and_action_with_order(
            action=False, ind=0, summary=self.atom.CRS.order_entry.one_oit_to_summary, open_crs=True)
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])

        # CHECK SUMMARY PAGE--------------------------------------------------------------------------------
        self.lib.CRS.order_search.click_edit_icon(self.data["order_number"])
        self.lib.general_helper.wait_for_spinner()
        assert self.data.expected_page1 in self.actions.get_browser().page_source, \
            f"{self.data.expected_page1} page is not located"
        self.atom.CRS.add_payment.finalize_order()

        # CHECK FINALIZATION PAGE--------------------------------------------------------------------------
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
        self.lib.CRS.order_search.click_edit_icon(self.data["order_number"])
        # if OIT is still in workflow, click on "in workflow" popup
        self.lib.CRS.order_search.click_pup_in_workflow_btn_yes()

        # verify Order Finalization page
        self.lib.general_helper.wait_for_spinner()
        assert self.data.expected_page2 in self.actions.get_browser().page_source, \
            f"{self.data.expected_page2} page is not located"


if __name__ == '__main__':
    run_test(__file__)
