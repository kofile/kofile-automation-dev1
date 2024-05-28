""" Email Receipt for eRecording order """
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Create eRecording order
Finalize the order
Click Print Duplicate Receipt link
"""

tags = ['48999_location_2']


class test(TestParent):
    save_order_btn = None
    print_data_names = {
        "EPSONRECIEPT": "epson_reciept_erProxy_golden",
        "GENERIC": "generic_reciept_erProxy_golden"
    }

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __48999__(self):
        self.save_order_btn = self.pages.CRS.order_summary.btn_save_order
        self.check_pdf_on_email = lambda e: True

    def __48000__(self):
        self.__48999__()

    def __test__(self):
        self.actions.store('msg', "Duplicate Receipt printing is initiated.")
        self.actions.store('email', "VAutomationTest@yopmail.com")
        self.actions.store('email_msg', "Email sent successfully")

        self.atom.CRS.general.go_to_crs()
        self.data["order_number"] = self.atom.ERProxy.general.create_er_proxy()[0][0]
        account_name = self.data.config.config_file.ORDER_HEADER["er_proxy_account_name_password"]['name']
        self.lib.CRS.crs.go_to_order_queue()
        self.atom.CRS.order_queue.assign_order()
        self.lib.general_helper.wait_for_spinner()
        self.data["current_oit"] = self.data.OIT
        self.lib.CRS.crs.click_running_man()
        self.lib.general_helper.find(self.pages.CRS.order_summary.btn_checkout, wait_displayed=True)
        self.actions.wait(3)
        self.actions.wait_for_element_displayed(self.pages.CRS.order_summary.lbl_order_number)
        st = self.lib.CRS.order_header.return_state_of_field_is_selected_or_no(
            self.pages.CRS.order_header.rbn_auto_print_receipt_no[1])
        assert st, f"The radiobutton AutoPrintReceipt automatically not selected No for ErProxy order"
        self.atom.CRS.order_summary.edit_oit(edit_all=True)
        self.lib.CRS.order_header.select_auto_print_option("email")
        self.lib.general_helper.find(
            self.save_order_btn if self.save_order_btn else self.pages.CRS.order_finalization.btn_save_order,
            wait_displayed=True)
        self.atom.CRS.add_payment.finalize_order()

        self.lib.general_helper.scroll_and_click(self.pages.CRS.order_finalization.lnk_print_dup_receipt)
        self.actions.assert_element_text(self.pages.CRS.order_finalization.pup_duplicate_receipt_print_success_text,
                                         self.data.msg)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.btn_close_pup_print)

        order_price = self.actions.get_element_text(self.pages.CRS.order_summary.price_by_row_index())
        account_balance = self.lib.db_with_vpn.select_account_balance_by_account_code(account_name)
        account_balance = "{0:,.2f}".format(account_balance[0][0])
        ex_list = [self.data['order_number'], self.data['doc_number'], order_price, account_balance]
        file_name, obj = self.lib.files.get_last_printing_file_from_db()
        self.actions.step(f"PRINTING CONFIG IS {obj.get('name')}")
        getattr(self.lib.files, obj.get("method")).__call__(self.data, self.print_data_names[obj.get("name")],
                                                            filename=(file_name,))
        self.check_pdf_on_email(ex_list)

    def check_pdf_on_email(self, exception_list):
        self.lib.general_helper.scroll_and_click(self.pages.CRS.order_finalization.lnk_email_dup_receipt)
        self.lib.CRS.order_finalization.send_email_receipt_address(self.data.email)
        self.lib.CRS.order_finalization.validate_email_receipt_dialog_popup_message(self.data.email_msg)
        downloaded_file = self.lib.files.open_yopmail_in_new_tab_and_download_pdf(self.data.email,
                                                                                  self.names.print_files)
        self.lib.files.compare_print_pdf_files_format(downloaded_file, self.names.print_Reciept_golden_file,
                                                      exception_list)
        self.lib.files.remove_file(downloaded_file)


if __name__ == '__main__':
    run_test(__file__)
