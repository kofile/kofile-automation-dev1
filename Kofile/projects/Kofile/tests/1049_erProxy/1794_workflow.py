"""erProxy workflow"""

from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test
import datetime

description = """erProxy end-to end workflow to Archive, document in CS"""

tags = ['48999_location_2']


class test(TestParent):                                                                                    # noqa

    def __init__(self, data):
        self.column_index = 6
        data["use_doc_type_in_api_CS"] = True
        super(test, self).__init__(data, __name__)

    def __48999__(self):
        self.column_index = 7

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: erProxy order is processed to Archive, doc is exported and found in CS
        """

        # submit an erProxy and get the created order number, package_id
        er_proxy_data = self.atom.ERProxy.general.create_er_proxy(exit_from_er_proxy=False)
        self.data["order_number"] = er_proxy_data[0][0]
        self.data["package_id"] = er_proxy_data[1][0]
        # find and open the submitted order in CRS
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.crs.go_to_order_queue()
        self.atom.CRS.order_queue.assign_order()
        self.lib.general_helper.wait_for_spinner()
        # review the order item
        self.lib.CRS.crs.click_running_man()
        self.actions.wait_for_element_displayed(self.pages.CRS.order_summary.lbl_order_number)
        self.atom.CRS.order_summary.edit_oit()
        # finalize the order
        self.atom.CRS.add_payment.finalize_order()
        # check the visibility of Get Next, Void, Order Queue buttons and Receipts links
        self.actions.wait_for_element_displayed(self.pages.CRS.order_finalization.btn_get_next)
        self.actions.wait_for_element_displayed(self.pages.CRS.order_finalization.btn_void_order)
        self.actions.wait_for_element_displayed(self.pages.CRS.order_finalization.btn_order_queue)
        self.actions.wait_for_element_enabled(self.pages.CRS.order_finalization.lnk_email_dup_receipt)
        self.actions.wait_for_element_enabled(self.pages.CRS.order_finalization.lnk_print_dup_receipt)
        if self.data['config'].test_data(f"{self.data.OIT}.cover_page"):
            self.actions.wait_for_element_enabled(self.pages.CRS.order_finalization.lnk_edit_order_payments)
        # get the Recorded date on Order Finalization page
        self.data["recording_date"] = self.actions.get_element_text(self.pages.CRS.order_header.lbl_recorded_date)
        formatted_date = str(datetime.datetime.strptime(self.data["recording_date"], '%m/%d/%Y').strftime('%m/%d/%Y'))
        # update OrderItemContentExport scheduler job and check that package status ="Recorded" (16) in DB
        with self.lib.db as db:
            db.update_scheduler_next_execution_date("OrderItemContentExport")
            assert self.lib.general_helper.wait_until(lambda: db.get_package_status(
                self.data["order_number"]) == 16, 300, 4), \
                f"Wrong status, must be 16 but have value {db.get_package_status(self.data['order_number'])}"
        # export document data to CS and find the document via doc number
        cs_doc = self.lib.CS.general.export_and_find_created_doc_in_cs(
            self.data, self.data['config'].test_data(f'{self.data["current_oit"]}.dept_id'))
        self.lib.CS.general.search_by_keyword(self.data["doc_num"])
        self.actions.step(str(self.data["doc_num"]))
        doc_number_in_row = self.pages.CS.main_page.column_data_by_row_and_column_index(
            1, column_index=self.column_index)
        self.actions.step(str(doc_number_in_row))
        assert self.data["doc_num"] == doc_number_in_row, "Doc Number isn't found!"
        assert cs_doc["Filename"], "Image doesn't exist in Clerk Search!"
        self.atom.CRS.general.go_to_crs()
        # go to Order Search and check that document data is correct
        self.lib.CRS.crs.go_to_order_search()
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
        self.actions.verify_element_text_contains(self.pages.CRS.order_search.recorded_on_by_order_number(
            self.data["order_number"]), formatted_date)
        self.actions.verify_element_text_contains(self.pages.CRS.order_search.recorded_by_by_order_number(
            self.data["order_number"]), self.lib.CRS.crs.assign_user_name(self.actions.execution.data["user_index"]))
        self.lib.CRS.order_search.verify_order_status_indexing()
        self.actions.wait_for_element_enabled(
            self.pages.CRS.order_search.edit_order_icon_by_order_number(self.data["order_number"]))
        self.actions.wait_for_element_enabled(
            self.pages.CRS.order_search.send_to_admin_icon_by_order_number(self.data["order_number"]))
        self.actions.wait_for_element_enabled(self.pages.CRS.order_search.reprint_receipt_icon_by_order_number(
            self.data["order_number"]))
        # navigate to Packages tab and find the submitted erProxy
        self.actions.click(self.pages.CRS.order_search.lnk_go_to_packages)
        self.lib.CRS.package_search.fill_package_id(self.data['package_id'])
        self.lib.CRS.package_search.wait_and_click_search_lookup(self.data['package_id'])
        self.lib.CRS.package_search.click_search_button()
        self.lib.general_helper.find_and_click(self.pages.CRS.package_search.order_number(self.data["order_number"]))
        # click on edit order
        self.lib.CRS.order_search.click_edit_icon(self.data["order_number"])
        self.lib.CRS.order_search.click_pup_in_workflow_btn_yes()
        self.actions.wait_for_element_displayed(self.pages.CRS.order_finalization.lbl_order_finalize_label)
        # click on Edit Payment link and check the payment method
        self.lib.CRS.order_finalization.click_edit_order_payments()
        payment_methods = self.lib.CRS.add_payment.get_all_payment_methods()
        if not (self.data["payment"] in payment_methods and len(payment_methods) == 1):
            self.actions.error("Payment method is not correct.")
        # find the order in Indexing queue and process (through KDI)
        self.lib.CRS.crs.go_to_indexing_queue()
        self.lib.CRS.crs.click_all_show_all_action_links()
        self.lib.CRS.order_search.verify_order_status(
            self.data['config'].get_status('Order.Pending.value'))
        self.lib.CRS.order_item_type.indexing_step()
        self.lib.CRS.order_item_type.verification_step()
        self.lib.CRS.crs.go_to_order_search()
        self.atom.CRS.order_search.search_order_by_order_number()
        it = self.data['config'].test_data(f"{self.data.OIT}.indexing.indexing_type")
        self.lib.CRS.order_search.verify_order_status("indexing_status" if it == 'scheduled_kdi' else "archive_status")
        # re-export document data after KDI and find the document in CS via doc number
        cs_doc = self.lib.CS.general.export_and_find_created_doc_in_cs(
            self.data, self.data['config'].test_data(f'{self.data["current_oit"]}.dept_id'))
        self.lib.CS.general.search_by_keyword(self.data["doc_num"])
        self.actions.step(str(self.data["doc_num"]))
        doc_number_in_row = self.pages.CS.main_page.column_data_by_row_and_column_index(1, self.column_index)
        self.actions.step(str(doc_number_in_row))
        assert self.data["doc_num"] == doc_number_in_row, "Doc Number isn't found!"
        assert cs_doc["Filename"], "Image doesn't exist in Clerk Search!"
        # update OrderItemContentExport scheduler job and check that package status ="Recorded" (16) in DB
        with self.lib.db as db:
            db.update_scheduler_next_execution_date("OrderItemContentExport")
            assert self.lib.general_helper.wait_until(lambda: db.get_package_status(
                self.data["order_number"]) == 16, 300, 4), \
                f"Wrong status, must be 16 but have value {db.get_package_status(self.data['order_number'])}"


if __name__ == '__main__':
    run_test(__file__)
