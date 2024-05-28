"""erProxy several OIts"""

import re
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Multi-OIT erProxy order finalization"""

tags = ['48999_location_2']


class test(TestParent):                                                                                # noqa

    def __init__(self, data, oit_count=2):
        self.oit_count = oit_count
        self.crop_data = tuple(map(lambda _: int(_), re.split(
            ' ', data.doc_number_coordinate_on_img))) if 'doc_number_coordinate_on_img' in data else ()
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: Multi-OIT erProxy order is finalized
        """
        self.atom.CRS.general.go_to_crs()
        # submit erProxy and get the created order number
        self.data["order_number"] = self.atom.ERProxy.general.create_er_proxy(oit_count=self.oit_count)[0][0]
        self.lib.CRS.crs.go_to_order_queue()
        # check that order status is Pending
        self.atom.CRS.order_queue.check_status_of_order('Pending')
        # assign the order
        self.atom.CRS.order_queue.assign_order()
        self.lib.general_helper.wait_for_spinner()
        # edit the order
        self.lib.CRS.crs.click_running_man()
        self.actions.wait_for_element_displayed(self.pages.CRS.order_summary.lbl_order_number)
        # check that in Order Header all fields are disabled, except Auto_Print Receipt No, Email options
        if self.lib.general_helper.find(self.pages.CRS.order_header.txt_organization_name, should_exist=False,
                                        timeout=5):
            self.actions.verify_element_has_attribute(self.pages.CRS.order_header.txt_organization_name, "readonly")
        else:
            self.actions.verify_element_has_attribute(self.pages.CRS.order_header.txt_accountname, "readonly")
        self.actions.verify_element_has_attribute(self.pages.CRS.order_header.txt_email, "readonly")
        self.actions.verify_element_has_attribute(self.pages.CRS.order_header.txt_customername, "readonly")
        if self.lib.general_helper.find(self.pages.CRS.order_header.organization_balance_field, should_exist=False,
                                        timeout=5):
            self.actions.verify_element_has_attribute(self.pages.CRS.order_header.organization_balance_field,
                                                      "readonly")
        else:
            self.actions.verify_element_has_attribute(self.pages.CRS.order_header.company_account_balance_field,
                                                      "readonly")
        self.actions.verify_element_has_attribute(self.pages.CRS.order_header.rbn_auto_print_receipt_yes, "disabled")
        self.actions.verify_element_has_not_attribute(self.pages.CRS.order_header.rbn_auto_print_receipt_no, "disabled")
        self.actions.verify_element_has_not_attribute(self.pages.CRS.order_header.rbn_auto_print_receipt_email,
                                                      "disabled")
        # check that OITs have pending status and do not have a delete icon on the row
        for i in range(1, self.oit_count + 1):
            self.lib.CRS.order_summary.verify_status_by_row_index("Pending", row=i)
            self.actions.verify_element_not_displayed(self.lib.general_helper.make_locator(
                self.pages.CRS.order_summary.delete_row_by_row_index(i)))
        # check that new order link is not available
        if self.lib.general_helper.check_if_element_exists(self.pages.CRS.order_summary.lnk_new_order_item):
            self.logging.info("lnk_new_order_item not exist")
        # click on Checkout and check warning message to review the order item
        self.lib.CRS.order_summary.click_order_summary_checkout_button()
        if len(self.lib.general_helper.find_elements(self.pages.CRS.order_summary.txt_review_warning)) == 0:
            self.actions.error("Warning message is not displayed!")
        # edit the oit
        self.atom.CRS.order_summary.edit_oit()
        # get the number of image pages from image viewer before finalization
        rows = self.lib.general_helper.find_elements(self.pages.CRS.order_summary.row_numbers)
        total_image_before_finalization = []
        for row in rows:
            self.actions.click(row)
            self.lib.general_helper.wait_for_spinner()
            total_image = int(self.actions.get_element_text(self.pages.CRS.image_viewer.lbl_total_images))
            total_image_before_finalization.append(total_image)
        # get Current Balance and Total price before finalization
        current_balance_before_finalization = float(self.actions.get_element_attribute(
            self.pages.CRS.order_header.company_account_balance_value, 'value'))
        total = float(self.actions.get_element_text(self.pages.CRS.order_summary.lbl_total_price))
        # finalize the order
        self.atom.CRS.add_payment.finalize_order()
        # check the availability of print cover page icon for each row
        for i in range(1, self.oit_count + 1):
            self.pages.CRS.order_finalization.print_coverpage_by_row_index(i)
        # execute the OrderItemContentExport scheduler
        if self.data['async'] == '1':
            self.lib.db_with_vpn.scheduler_job_update_for_export(scheduler_job_code="OrderItemContentExport")
            self.lib.db_with_vpn.check_async_export_executed(self.data["order_number"])
        # check that cover page is added after finalization
        total_image_after_finalization = []
        rows = self.lib.general_helper.find_elements(self.pages.CRS.order_finalization.txt_table_data_order_status)
        for i in range(0, len(rows)):
            self.actions.click(rows[i])
            self.lib.general_helper.wait_for_spinner()
            self.actions.wait(1)
            total_image = int(self.actions.get_element_text(self.pages.CRS.image_viewer.lbl_total_images))
            total_image_after_finalization.append(total_image - 1)
            self.data["doc_number"] = self.actions.get_element_text(
                self.pages.CRS.order_finalization.docnum_by_row_index(i + 1))
            self.lib.CRS.image_viewer.verify_text_on_image(self.data, text=self.data["doc_number"],
                                                           last_page=True, step="order", accuracy=60,
                                                           crop=self.crop_data)
        # check that the number of image pages is the same before and after finalization
        if total_image_before_finalization != total_image_after_finalization:
            self.logging.error("Cover page is not added!")
        # check that Company Balance is reduced
        current_balance_after_finalization = float(self.actions.get_element_attribute(
            self.pages.CRS.order_header.company_account_balance_value, 'value'))
        assert current_balance_before_finalization - total == current_balance_after_finalization, \
            "Balance is incorrect!"


if __name__ == '__main__':
    run_test(__file__)
