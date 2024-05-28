"""Application Printing"""
from golem import actions
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test
from datetime import date

description = """
Create order for which application is configured (e.g. ML)
Click on the icon Print Application
Navigate to Azure wf-content-tenant_code-print-folder and open Application
Checkout the order
Click the "Print Application" icon and find the Application
Click F -"Print certificate Front Page" icon
Click B -"Print certificate Back Page" icon
Click L -"Print certificate" icon
"""

tags = ['48999_location_2']


# todo 48999_location_2 not have print application button

def setup(data):
    day = int(date.today().strftime('%d'))
    if (3 < day < 21) or (23 < day < 31):
        day = str(day) + 'th'
    else:
        suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
        day = str(day) + suffixes[day % 10]
    actions.store('day', day)
    actions.store('app_msg', "Application printing is initiated.")
    actions.store('fr_msg', "Front page Print Initiated")
    actions.store('bc_msg', "Back page Print Initiated")
    actions.store('fr_bc_msg', "Front and back pages Print Initiated")


class test(TestParent):                                                                               # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        doc_num = self.lib.general_helper.find(
            self.pages.CRS.order_summary.docnumber_by_row_index(), get_text=True).split("/")[-1]

        self.lib.general_helper.find_and_click(self.pages.CRS.order_summary.printapp_image_by_row_index())
        self.actions.wait_for_element_displayed(self.pages.CRS.image_viewer.pup_print_dialog)
        self.actions.assert_element_text(self.pages.CRS.order_finalization.pup_application_print_success_text,
                                         self.data.app_msg)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.btn_close_pup_print)
        self.lib.general_helper.find(self.pages.CRS.image_viewer.pup_print_dialog, should_exist=False, timeout=10)
        # Get and compare PDF
        ex_list = [self.data['order_number'], doc_num, self.data.day]
        self.lib.files.download_and_compare_pdf(self.data, self.names.print_application_golden_file, ex_list)

        self.atom.CRS.add_payment.finalize_order()
        self.lib.general_helper.find_and_click(self.pages.CRS.order_finalization.print_cert_front_page_by_row_index())
        self.actions.wait_for_element_displayed(self.pages.CRS.image_viewer.pup_print_dialog)
        self.actions.assert_element_text(self.pages.CRS.order_finalization.pup_application_print_success_text,
                                         self.data.fr_msg)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.btn_close_pup_print)
        self.lib.general_helper.find(self.pages.CRS.image_viewer.pup_print_dialog, should_exist=False, timeout=10)
        # Get and compare PDF
        self.lib.files.download_and_compare_pdf(self.data, self.names.print_certificate_golden_file, ex_list)

        self.lib.general_helper.find_and_click(self.pages.CRS.order_finalization.print_application_by_row_index())
        self.actions.wait_for_element_displayed(self.pages.CRS.image_viewer.pup_print_dialog)
        self.actions.assert_element_text(self.pages.CRS.order_finalization.pup_application_print_success_text,
                                         self.data.app_msg)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.btn_close_pup_print)
        self.lib.general_helper.find(self.pages.CRS.image_viewer.pup_print_dialog, should_exist=False, timeout=10)
        # Get and compare PDF
        self.lib.files.download_and_compare_pdf(self.data, self.names.print_application_golden_file, ex_list)

        self.lib.general_helper.find_and_click(self.pages.CRS.order_finalization.print_cert_back_page_by_row_index())
        self.actions.wait_for_element_displayed(self.pages.CRS.image_viewer.pup_print_dialog)
        self.actions.assert_element_text(self.pages.CRS.order_finalization.pup_application_print_success_text,
                                         self.data.bc_msg)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.btn_close_pup_print)
        self.lib.general_helper.find(self.pages.CRS.image_viewer.pup_print_dialog, should_exist=False, timeout=10)
        # Get and compare PDF
        self.lib.files.download_and_compare_pdf(self.data, self.names.print_certificate_golden_file, ex_list)

        self.lib.general_helper.find_and_click(self.pages.CRS.order_finalization.print_cert_by_row_index())
        self.actions.wait_for_element_displayed(self.pages.CRS.image_viewer.pup_print_dialog)
        self.actions.assert_element_text(self.pages.CRS.order_finalization.pup_application_print_success_text,
                                         self.data.fr_bc_msg)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.btn_close_pup_print)
        # Get and compare PDF
        self.lib.files.download_and_compare_pdf(self.data, self.names.print_certificate_golden_file, ex_list)


if __name__ == '__main__':
    run_test(__file__)
