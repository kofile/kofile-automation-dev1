"""Cover page printing for multiple OITs"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Create the order with multiple OIT check cover page printing for each OIT
Edit one of the OIT and save
Edit one of the OIT and click "Cancel"
"""

tags = ["48999_location_2"]


class test(TestParent):                                                                               # noqa

    def __init__(self, data):
        data['device_id'] = data.env.printer_id
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.actions.store('msg', "Cover page printing is initiated.")
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        self.lib.CRS.order_finalization.click_edit_order(1, True)
        self.lib.CRS.order_summary.click_new_order_item_icon()
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.one_oit_to_summary()
        self.lib.CRS.order_finalization.click_edit_order(1, True, 2)
        self.atom.CRS.add_payment.finalize_order()

        self.actions.store('doc_sequence_number', 1)
        doc_type = self.lib.general_helper.find(self.pages.CRS.order_finalization.doc_type_by_row_index(self.data['doc_sequence_number']),
                                                get_text=True)
        self.lib.general_helper.prepare_doc_numbers()
        barcode = self.lib.files.get_barcode(self.data, self.data["doc_numbers"][0], doc_type, self.data["doc_year"])
        ex_list = [self.data['order_number'], *self.data["doc_numbers"], barcode]
        self.actions.wait_for_element_displayed(self.pages.CRS.order_finalization.print_coverpage_by_row_index(self.data['doc_sequence_number']))
        self.actions.wait(0.5)
        self.lib.general_helper.find_and_click(self.pages.CRS.order_finalization.print_coverpage_by_row_index(self.data['doc_sequence_number']))
        self.actions.wait_for_element_displayed(self.pages.CRS.image_viewer.pup_print_dialog)
        self.actions.assert_element_text(self.pages.CRS.order_finalization.pup_application_print_success_text,
                                         self.data.msg)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.btn_close_pup_print)
        with self.lib.db as db:
            db.update_printer_job(self.data.env.printer_id)
        self.actions.wait(2)
        self.lib.files.download_and_compare_pdf_new(self.data, "cover_page_return_mail_golden", filename="CoverPage_")

        self.actions.store('doc_sequence_number', 2)
        doc_type = self.lib.general_helper.find(self.pages.CRS.order_finalization.doc_type_by_row_index(self.data['doc_sequence_number']),
                                                get_text=True)
        barcode = self.lib.files.get_barcode(self.data, self.data["doc_numbers"][1], doc_type, self.data["doc_year"])
        self.actions.wait_for_element_displayed(self.pages.CRS.order_finalization.print_coverpage_by_row_index(self.data['doc_sequence_number']))
        self.actions.wait(0.5)
        self.lib.general_helper.find_and_click(self.pages.CRS.order_finalization.print_coverpage_by_row_index(self.data['doc_sequence_number']))
        self.actions.wait_for_element_displayed(self.pages.CRS.image_viewer.pup_print_dialog)
        self.actions.assert_element_text(self.pages.CRS.order_finalization.pup_application_print_success_text,
                                         self.data.msg)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.btn_close_pup_print)
        self.actions.wait(2)
        self.lib.files.download_and_compare_pdf_new(self.data, "cover_page_return_mail_golden", filename="CoverPage_")

        self.lib.CRS.order_finalization.click_edit_order(2, True, 2)
        self.actions.wait(2)
        self.lib.CRS.order_entry.check_address_required_error(should_exist=False)
        self.lib.CRS.add_payment.fill_in_payment_method_comment(2, self.data.msg)
        self.lib.CRS.add_payment.click_add_payment_checkout_button(expected_status=["Finalized", "Finalized"])
        self.lib.files.download_and_compare_pdf_new(self.data, "cover_page_edit_golden_file", filename="CoverPage_")

        self.lib.general_helper.find_and_click(self.pages.CRS.order_finalization.editicon_by_row_index(self.data['doc_sequence_number']))
        self.actions.wait_for_element_displayed(self.pages.CRS.order_entry.btn_cancel_order)
        self.lib.general_helper.scroll_and_click(self.pages.CRS.order_entry.btn_cancel_order)
        self.lib.files.download_and_compare_pdf_new(self.data,  "cover_page_edit_golden_file", filename="CoverPage_")


if __name__ == '__main__':
    run_test(__file__)
