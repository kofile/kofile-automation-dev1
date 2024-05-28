"""Return mail information printing"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Create an order with Return by mail checkbox (e.g. RP) and check the checkbox "Return by mail" 
Fill in required fields
Click Copy From Order Header link
Click Copy From Prior Order Item link
Fill all required fields and finalize the order
"""

tags = ["48999_location_2"]


class test(TestParent):                                                                                  # noqa
    msg = "Cover page printing is initiated."

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs()
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.fill_order_header_name()
        self.atom.CRS.order_entry.fill_order_header_address()
        self.lib.CRS.order_entry.click_return_by_mail_checkbox()
        by_mail_fill = self.lib.CRS.order_entry.fill_return_by_mail_fields()
        self.atom.CRS.order_entry.one_oit_to_summary()
        self.lib.CRS.order_finalization.click_edit_order(1, True)
        self.atom.CRS.add_payment.finalize_order()

        self.lib.general_helper.find_and_click(self.pages.CRS.order_finalization.print_coverpage_by_row_index())
        self.actions.wait_for_element_displayed(self.pages.CRS.image_viewer.pup_print_dialog)
        self.actions.assert_element_text(self.pages.CRS.order_finalization.pup_application_print_success_text, self.msg)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.btn_close_pup_print)
        # Get and compare PDF
        self.lib.files.download_and_compare_pdf_new(self.data, "cover_page_email_golden")

        self.lib.CRS.order_finalization.click_edit_order()
        by_mail = self.lib.CRS.order_entry.get_return_by_mail_values()
        assert by_mail == by_mail_fill, f"Expected values '{by_mail_fill}' is not equal to {by_mail}"

        customer_info = self.lib.CRS.order_entry.get_order_header_customer_info()
        self.lib.CRS.order_entry.click_copy_from_order_header_link()
        return_by_mail = self.lib.CRS.order_entry.get_return_by_mail_values()
        assert return_by_mail == customer_info, f"Expected values '{customer_info}' is not equal to {return_by_mail}"
        self.lib.general_helper.scroll_and_click(self.pages.CRS.order_finalization.btn_save_order)

        self.lib.general_helper.find_and_click(self.pages.CRS.order_finalization.print_coverpage_by_row_index())
        self.actions.wait_for_element_displayed(self.pages.CRS.image_viewer.pup_print_dialog)
        self.actions.assert_element_text(self.pages.CRS.order_finalization.pup_application_print_success_text, self.msg)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.btn_close_pup_print)
        # Get and compare PDF
        self.lib.files.download_and_compare_pdf_new(self.data, "cover_page_guest_golden")


if __name__ == '__main__':
    run_test(__file__)
