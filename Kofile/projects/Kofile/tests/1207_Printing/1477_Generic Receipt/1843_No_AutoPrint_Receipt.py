"""No AutoPrint Receipt"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Create and finalize order with AutoPrint Receipt "No" option:
Receipt is not printed automatically, but in order finalization screen there is ability to print/email 
        Duplicate copy with the following links:
Email Duplicate Receipt
Print Duplicate Receipt
"""

tags = ['48999_location_2']


class test(TestParent):                                                                                 # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.order_queue.add_new_order()
        self.lib.CRS.order_header.select_auto_print_option("no")
        with self.lib.db as db:
            self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
            file_name = db.get_file_name_by_started_pattern_from_xml("Reciept")
            if file_name:
                self.actions.error(f'The filename including pattern was found: {file_name}')
            else:
                self.actions.step('Receipt is not automatically printed after finalization')
        self.actions.assert_element_present(self.pages.CRS.order_finalization.lnk_print_dup_receipt)
        self.actions.assert_element_present(self.pages.CRS.order_finalization.lnk_email_dup_receipt)


if __name__ == '__main__':
    run_test(__file__)
