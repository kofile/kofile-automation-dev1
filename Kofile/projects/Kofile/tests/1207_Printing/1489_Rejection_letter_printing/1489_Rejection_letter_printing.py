"""Rejection Letter Printing"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Create order and select order item type that has configured rejection letter template
Click the link "Reject Entire Order"
Enter the reason and submit
Navigate to Azure wf-content-tenant_code-print-folder
Navigate to order Search and find the order
Click the icon "Print Rejection Letter"
"""

tags = ["48999_location_2"]


class test(TestParent):                                                                                # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.order_summary.reject_order)
        # Get and compare PDF
        self.lib.files.download_and_compare_pdf_new(self.data, "print_rejection_golden")

        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.general_helper.find_and_click(self.pages.CRS.order_search.print_rejection_letter_icon_by_order_number(
            self.data['order_number']))
        # Get and compare PDF
        self.lib.files.download_and_compare_pdf_new(self.data, "print_rejection_golden")


if __name__ == '__main__':
    run_test(__file__)
