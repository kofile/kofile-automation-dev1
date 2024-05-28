""" Cover page printing for eRecording """
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Submit erProxy
Finalized eRecording origin Order
Print Cover page by "Print Cover Page" icon
In order finalization screen click "Reprint All Cover Pages"
"""

tags = ['48999_location_2']


class test(TestParent):                                                                           # noqa
    msg1 = "Cover page printing is initiated."
    msg2 = "Cover Pages printing is initiated."

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs()
        self.data["order_number"] = self.atom.ERProxy.general.create_er_proxy(oit_count=2)[0][0]
        self.lib.CRS.crs.go_to_order_queue()
        self.atom.CRS.order_queue.assign_order()
        self.lib.general_helper.wait_for_spinner()
        self.data["current_oit"] = self.data.OIT
        self.lib.CRS.crs.click_running_man()
        self.actions.wait_for_element_displayed(self.pages.CRS.order_summary.lbl_order_number)
        self.atom.CRS.order_summary.edit_oit(edit_all=True)
        self.lib.general_helper.find(self.pages.CRS.order_finalization.btn_save_order, wait_displayed=True)
        self.atom.CRS.add_payment.finalize_order()
        # TODO: Add Cover page checking on image viewer

        doc_type1 = self.lib.general_helper.find(self.pages.CRS.order_finalization.doc_type_by_row_index(),
                                                 get_text=True)
        doc_type2 = self.lib.general_helper.find(self.pages.CRS.order_finalization.doc_type_by_row_index(2),
                                                 get_text=True)
        barcode1 = self.lib.files.get_barcode(self.data, self.data["doc_numbers"][0], doc_type1, self.data["doc_year"])
        barcode2 = self.lib.files.get_barcode(self.data, self.data["doc_number"][1], doc_type2, self.data["doc_year"])
        ex_list1 = [self.data['order_number'], self.data['doc_number'][0], barcode1]
        ex_list2 = [self.data['order_number'], self.data['doc_number'][1], barcode2]

        self.actions.wait_for_element_displayed(self.pages.CRS.order_finalization.print_coverpage_by_row_index())
        self.actions.wait(0.5)
        self.lib.general_helper.find_and_click(self.pages.CRS.order_finalization.print_coverpage_by_row_index())
        self.actions.wait_for_element_displayed(self.pages.CRS.image_viewer.pup_print_dialog)
        self.actions.assert_element_text(self.pages.CRS.order_finalization.pup_application_print_success_text,
                                         self.msg1)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.btn_close_pup_print)
        # Get and compare PDF
        self.lib.files.download_and_compare_pdf(self.data, self.names.print_CoverPage_erProxy_golden_file, ex_list1, 0)

        self.lib.general_helper.find_and_click(self.pages.CRS.order_finalization.lnk_print_all_cover_pages)
        self.lib.general_helper.wait_for_spinner()
        self.actions.wait_for_element_displayed(self.pages.CRS.image_viewer.pup_print_dialog)
        self.actions.assert_element_text(self.pages.CRS.balance_drawer.pup_print_success_text, self.msg2)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.btn_close_pup_print)

        self.lib.files.download_and_compare_pdf(self.data, self.names.print_CoverPage_erProxy_golden_file, ex_list2, 0)
        self.lib.files.download_and_compare_pdf(self.data, self.names.print_CoverPage_erProxy_golden_file, ex_list1, 1)


if __name__ == '__main__':
    run_test(__file__)
