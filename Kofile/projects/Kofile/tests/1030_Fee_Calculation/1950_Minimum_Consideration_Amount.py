"""Fee Calculation: Minimum Consideration Amount"""
from projects.Kofile.Lib.test_parent import TestParent
from selenium.webdriver.common.keys import Keys
from runner import run_test

description = """Check 'Minimum Consideration Amount
                 Configuration data:
                      - min_consideration
                      - increment
                      - tax_rate
                 Steps:
                      1. Add 'Scan First' with 'Real Property OH' OIT
                      2. Fill all required fields -> Save order
                      3. Enter 'Consideration' amount
                      4. Check updated 'Conveyance Fee OH' additional fee according to formula:
                         4.1. if consideration < min_consideration:
                              'Conveyance Fee OH' = (min_consideration / increment) * tax_rate
                         4.2. if consideration >= min_consideration:     
                              'Conveyance Fee OH' = (consideration / increment) * tax_rate 
                      5. Save order and repeat step 4 with different 'Consideration' amount
                      6. Finalize order
                      7. Verify 'Conveyance Fee OH' additional fee        
             '"""

tags = ["48999_location_2"]


class test(TestParent):  # noqa

    def __init__(self, data):
        self.order_types = data["OIT"]
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Add 'Scan First' OITs
        self.atom.CRS.order_queue.add_order_with_scan_first_flow(order_types=self.order_types)

        # Edit OIT: fill all required fields
        self.lib.CRS.order_summary.click_edit_icon_by_row_index(1)
        self.lib.CRS.order_entry.wait_order_item_tab_displayed()
        self.lib.required_fields.crs_fill_required_fields()
        self.lib.CRS.order_entry.click_add_to_order()
        self.lib.CRS.order_summary.verify_status_by_row_index("Reviewed", 1)

        # Set 'Consideration' amount and read configuration data
        consideration = 500
        min_consideration = self.data['config'].test_data(f"{self.data['OIT']}.min_consideration")
        increment = self.data['config'].test_data(f"{self.data['OIT']}.increment")
        tax_rate = self.data['config'].test_data(f"{self.data['OIT']}.tax_rate")
        for i in range(3):
            # Edit OIT
            self.lib.CRS.order_summary.click_edit_icon_by_row_index(1)
            self.lib.CRS.order_entry.wait_order_item_tab_displayed()
            # Click on the 'More' link in fee block, if links
            if self.lib.general_helper.check_if_element_exists(self.pages.CRS.order_entry.lnk_more):
                self.lib.general_helper.find_and_click(self.pages.CRS.order_entry.lnk_more, 10, False)
            # Enter 'Consideration' amount
            self.lib.general_helper.find_and_send_keys(self.pages.CRS.order_entry.inp_consideration_amount,
                                                       str(consideration) + Keys.TAB)
            # Calculate expected conveyance fee according to formula
            if consideration < min_consideration:
                expected_conveyance = round((min_consideration / increment), 0) * tax_rate
            else:
                expected_conveyance = round((consideration / increment), 0) * tax_rate
            # Read actual conveyance fee
            actual_conveyance = self.lib.CRS.order_entry.fee_amount_by_fee_label("Conveyance Fee OH")
            # Compare actual and expected conveyance fees
            assert actual_conveyance == expected_conveyance, \
                (f"Actual 'Conveyance Fee OH' {actual_conveyance} is NOT equal to "
                 f"Expected 'Conveyance Fee OH' {expected_conveyance}")
            # Click on the 'Save Order' button
            self.lib.general_helper.find_and_click(self.pages.CRS.order_entry.btn_add_to_order)
            # Change 'Consideration' amount
            consideration += 1500

        # Finalize order
        self.atom.CRS.add_payment.finalize_order()
        # Edit OIT
        self.lib.CRS.order_finalization.click_edit_order()
        self.lib.CRS.order_entry.wait_order_item_tab_displayed()
        # Click on the 'More' link in fee block
        if self.lib.general_helper.check_if_element_exists(self.pages.CRS.order_entry.lnk_more):
            self.lib.general_helper.find_and_click(self.pages.CRS.order_entry.lnk_more)
        # Read actual conveyance fee
        actual_conveyance = self.lib.CRS.order_entry.fee_amount_by_fee_label("Conveyance Fee OH")
        # Compare actual and expected conveyance fees
        assert actual_conveyance == expected_conveyance, \
            (f"Actual 'Conveyance Fee OH' {actual_conveyance} is NOT equal to "
             f"Expected 'Conveyance Fee OH' {expected_conveyance}")
        # Click on the 'Save Order' button
        self.lib.general_helper.find_and_click(self.pages.CRS.order_entry.btn_add_to_order)


if __name__ == '__main__':
    run_test(__file__)
