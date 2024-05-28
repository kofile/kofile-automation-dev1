"""smoke test"""
import time
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    1. Go to Portal, submit an e-form order item, get the order number
    2. Go to CRS, find the order number, review OI and finalize the order
    3. Scan and map, index, verify Order
    4. Go To Order Search, find the order and check Order Status
    5. Void the order
    """

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.general_helper.check_order_type()
        # atom - create and submit e-form
        self.atom.EForm.general.create_and_submit_eform()
        # find and open the order in CRS
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.crs.click_running_man()
        self.actions.wait_for_element_displayed(self.pages.CRS.order_summary.lbl_order_number)
        # review and process to archive
        if self.data['config'].test_data(f"{self.data.OIT}.start_process_order_from_edit_oi"):
            self.lib.required_fields.crs_fill_required_fields()
            self.lib.CRS.order_entry.click_add_to_order()
        else:
            self.atom.CRS.order_summary.edit_oit()
        # get usertype
        self.data["user_type"] = self.data['config'].order_header_fill(f'{self.data.orderheader}.type')
        self.atom.CRS.add_payment.finalize_and_process_to_archive()
        # edit order from Order Search and void
        self.lib.CRS.order_search.click_edit_icon(self.data["order_number"])
        max_ = time.time() + 3
        while time.time() < max_:
            if 'Warning' in self.actions.get_browser().page_source:
                self.lib.CRS.order_search.click_pup_in_workflow_btn_yes()
                break
            else:
                self.actions.wait(0.5)
        self.atom.CRS.order_finalization.void_order()
        # check order status is voided
        self.lib.CRS.crs.go_to_order_search()
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
        self.lib.CRS.order_search.verify_order_status_voided()


if __name__ == '__main__':
    run_test(__file__)
