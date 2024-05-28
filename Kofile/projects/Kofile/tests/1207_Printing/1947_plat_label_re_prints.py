from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
1. Print Document (Zebra) label from order finalization screen - Label is successfully printed
2. Open azure 'wfcontent-NNNNN-printfolder' folder - ZebraLabelPrinterConfig_*.txt file is present
3. Check the printed label content - Recorded Clerk name (who recorded the order) is displayed on the printing Label
"""

tags = ["48999_location_2"]


class test(TestParent):                                                                            # noqa
    file_pattern, print_data = "ZebraLabelPrinterConfig", "zebra_label_printer"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        self.lib.general_helper.find_and_click(self.pages.CRS.order_summary.print_barcode_btn)
        self.actions.wait_for_element_displayed(self.pages.CRS.order_entry.warning_popup)
        self.actions.assert_element_text(self.pages.CRS.balance_drawer.pup_success_print_drawer_summary, "Success")
        self.actions.assert_element_text(self.pages.CRS.capture_summary.print_app_dialog_text,
                                         "Barcode label printing is initiated.")
        # Get and compare PDF
        self.lib.files.download_and_compare_txt_new(self.data, self.print_data, filename=self.file_pattern)


if __name__ == '__main__':
    run_test(__file__)
