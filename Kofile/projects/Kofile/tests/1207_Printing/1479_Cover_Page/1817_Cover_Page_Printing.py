"""Cover Page Printing"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Finalized the CRS  order with order item type for which cover page and stamps is configured
Navigate to DB and find the device_job record by Order_ID
      open config XML file, copy and find in Azure in wf-content-tenant-code-print-folder
Click "Print Cover Page" icon
Navigate to Azure wf-content-tenant-code-print-folder
Check Barcode content
"""

tags = ["48999_location_2"]


class test(TestParent):                                                                                   # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.actions.store('msg', "Cover page printing is initiated.")
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        self.lib.CRS.order_finalization.click_edit_order(1, True)
        self.atom.CRS.add_payment.finalize_order()

        self.lib.general_helper.find_and_click(self.pages.CRS.order_finalization.print_coverpage_by_row_index())
        self.actions.wait_for_element_displayed(self.pages.CRS.order_finalization.pup_application_print_success_text)
        self.actions.assert_element_text(self.pages.CRS.order_finalization.pup_application_print_success_text,
                                         self.data.msg)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.btn_close_pup_print)
        # Get and compare PDF
        self.lib.files.download_and_compare_pdf_new(self.data, "cover_page_guest_golden")


if __name__ == '__main__':
    run_test(__file__)
