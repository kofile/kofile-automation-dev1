"""Print Receipt"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

# FIXME: bug VTC-18242 and Epson receipt
description = """
Create and finalize the order:  
AutoPrint Receipt  is selected "Yes" from Order Header
Check GenericReceipt content
Edit OIT and change any non-financial information
Click Print Duplicate Receipt link
Navigate to Azure wf-content-tenant_code-print-folder and open printed Receipt
Edit OIT and change any financial data
Click "Email Duplicate Receipt" link
Enter valid Email and check email
Navigate to Order Search and click Reprint Receipt icon 
Void the order
"""

tags = ['48999_location_2']


class test(TestParent):  # noqa
    email = "VAutomationTest@yopmail.com"
    compare_function = None
    print_data_names = {
        "EPSONRECIEPT": ["epson_receipt_original_golden", "epson_receipt_duplicate_golden",
                         "epson_receipt_adjusted_golden"],
        "GENERIC": ["generic_receipt_original_golden", "generic_receipt_duplicate_golden",
                    "generic_receipt_adjusted_golden"]
    }

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __48999__(self):
        self.check_pdf_on_email = lambda e: True

    def __48000__(self):
        self.__48999__()

    def __test__(self):
        self.compare_function = self.compare_function if self.compare_function \
            else self.lib.files.download_and_compare_txt
        self.atom.CRS.general.go_to_crs()
        self.atom.CRS.order_queue.add_new_order()
        self.lib.CRS.order_header.select_auto_print_option()
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        self.lib.CRS.order_finalization.click_edit_order(1, True)
        self.atom.CRS.add_payment.finalize_order()
        file_name = str(self.actions.get_current_url().split('=')[-1])
        self.actions.step(f"Generic receipt filename: {file_name}")
        file_name, obj = self.lib.files.get_last_printing_file_from_db()
        self.actions.step(f"PRINTING CONFIG IS {obj.get('name')}")
        getattr(self.lib.files, obj.get("method")).__call__(self.data, self.print_data_names[obj.get("name")][0],
                                                            filename=(file_name,))
        self.lib.CRS.order_finalization.click_edit_order()
        self.lib.CRS.order_entry.click_return_by_mail_checkbox()
        self.lib.CRS.order_entry.fill_return_by_mail_fields(address2="address2")
        self.lib.general_helper.scroll_and_click(self.pages.CRS.order_finalization.btn_save_order)
        self.lib.general_helper.wait_for_spinner()
        self.actions.wait(2)
        file_name_1, obj = self.lib.files.get_last_printing_file_from_db()
        assert file_name == file_name_1, f"Expected file name '{file_name}' is not equal to {file_name_1}"

        self.lib.general_helper.scroll_and_click(self.pages.CRS.order_finalization.lnk_print_dup_receipt)
        self.actions.wait_for_element_present(
            self.pages.CRS.order_finalization.pup_duplicate_receipt_print_success_text)
        self.actions.assert_element_text(self.pages.CRS.order_finalization.pup_duplicate_receipt_print_success_text,
                                         "Duplicate Receipt printing is initiated.")
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.btn_close_pup_print)

        file_name, obj = self.lib.files.get_last_printing_file_from_db()
        self.actions.step(f"PRINTING CONFIG IS {obj.get('name')}")
        getattr(self.lib.files, obj.get("method")).__call__(self.data, self.print_data_names[obj.get("name")][1],
                                                            filename=(file_name,))
        self.lib.CRS.order_finalization.click_edit_order(2, True)
        self.actions.wait(2)
        self.lib.CRS.order_entry.check_address_required_error(should_exist=False)
        self.lib.general_helper.find_and_send_keys(
            self.lib.general_helper.make_locator(self.pages.CRS.add_payment.payment_comment_by_row, 1),
            "some_comment_1", should_exist=False)
        self.lib.general_helper.reset_focus()
        self.lib.CRS.add_payment.click_add_payment_checkout_button(expected_status=["Finalized"])
        file_name, obj = self.lib.files.get_last_printing_file_from_db()
        self.actions.step(f"PRINTING CONFIG IS {obj.get('name')}")
        getattr(self.lib.files, obj.get("method")).__call__(self.data, self.print_data_names[obj.get("name")][2],
                                                            filename=(file_name,))

        order_price = self.actions.get_element_text(self.pages.CRS.order_summary.price_by_row_index())
        exception_list = [self.data['order_number'], self.data['doc_number'], order_price]
        self.check_pdf_on_email(exception_list)

    def check_pdf_on_email(self, exception_list):
        self.lib.general_helper.scroll_and_click(self.pages.CRS.order_finalization.lnk_email_dup_receipt)
        self.lib.CRS.order_finalization.send_email_receipt_address(self.email)
        self.lib.CRS.order_finalization.validate_email_receipt_dialog_popup_message("Email sent successfully")
        downloaded_file = self.lib.files.open_yopmail_in_new_tab_and_download_pdf(self.email, self.names.print_files)
        self.lib.files.compare_print_pdf_files_format(downloaded_file, self.names.print_Reciept_golden_file,
                                                      exception_list)
        self.lib.files.remove_file(downloaded_file)


if __name__ == '__main__':
    run_test(__file__)
