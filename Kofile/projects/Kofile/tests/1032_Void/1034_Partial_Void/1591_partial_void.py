"""Partial Void"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Go to CRS, create and finalize an order, 
                 uncheck last oit checkbox and partially void the order. 
                 Check oit statuses on Order Finalization screen"""

tags = ["48999_location_2"]


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: Order is partially voided,  Order Finalization screen is displayed
        """
        self.lib.general_helper.check_order_type()
        with_payment = self.data['config'].test_data(f"{self.data.OIT}.finalization.with_payment")
        # atom tests
        self.atom.CRS.general.go_to_crs()
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.order_item_description()
        self.atom.CRS.order_entry.fill_order_header_name()
        self.atom.CRS.order_entry.many_oits_to_summary()
        self.atom.CRS.add_payment.finalize_order()

        self.lib.CRS.order_finalization.click_void_order_button()
        self.lib.CRS.void_order_summary.submit_fee_distribution_popup()
        self.lib.CRS.void_order_summary.uncheck_last_oit_checkbox(with_payment)
        self.lib.CRS.void_order_summary.click_void_button()

        if with_payment:
            self.lib.CRS.void_order_payment.clear_transaction_id_fields_and_fill_again()
            self.lib.CRS.void_order_payment.fill_refund_to_fields_if_exist()
            self.lib.CRS.void_order_payment.click_finalize_void_button()
            self.lib.CRS.void_order_payment.fill_and_submit_finalize_void_comment_if_exists()

        # check oit statuses
        rows_number = len(self.actions.get_browser().find_all(self.pages.CRS.order_finalization.row_numbers))
        for row in range(1, rows_number + 1):
            if int(row) != rows_number:
                self.lib.CRS.order_finalization.verify_order_status_is_voided(row)
            else:
                self.lib.CRS.order_finalization.verify_order_status_is_finalized(row)


if __name__ == '__main__':
    run_test(__file__)
