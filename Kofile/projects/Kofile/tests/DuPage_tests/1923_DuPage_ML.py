"""88905_DuPage_ML"""
from datetime import datetime, timedelta
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Check validations for Anticipated, Effective and Expiration Dates:
Anticipated Date valid range = Current date + preconfigured n number of days
Effective Date pre-populated default value and valid range = Current date + preconfigured n number of days
Expiration Date pre-populated default value and valid range = Effective Date + preconfigured n number of days
"""


class test(TestParent):  # noqa
    pnd_1 = 0  # preconfigured number of antic days
    # pnd_2 = 0  # preconfigured number of effective days - not set on DuPage
    pnd_3 = 61  # preconfigured number of expiration days
    current_date = datetime.now().strftime("%m/%d/%Y")
    invalid_past_date = (datetime.now() - timedelta(1)).strftime("%m/%d/%Y")
    # valid_future_antic_date = (datetime.now() + timedelta(pnd_1)).strftime("%m/%d/%Y")
    invalid_future_antic_date = (datetime.now() + timedelta(pnd_1 + 1)).strftime("%m/%d/%Y")
    # valid_future_eff_date = (datetime.now() + timedelta(pnd_2)).strftime("%m/%d/%Y")
    # invalid_future_eff_date = (datetime.now() + timedelta(pnd_2+1)).strftime("%m/%d/%Y")
    valid_future_exp_date = (datetime.now() + timedelta(pnd_3)).strftime("%m/%d/%Y")
    invalid_future_exp_date = (datetime.now() + timedelta(pnd_3 + 1)).strftime("%m/%d/%Y")

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: ML order is created
        """
        self.lib.general_helper.check_order_type()
        self.atom.go_to_crs(ind=0)
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.fill_order_header_name()
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.order_item_description()
        self.lib.general_helper.find(self.lib.CRS.order_entry.tab_locator("Order_Item"), wait_displayed=True)
        self.actions.wait_for_element_displayed(self.pages.CRS.order_entry.inp_effective_date)

        # check the default values for dates
        effective_date_default = self.actions.get_element_value(self.pages.CRS.order_entry.inp_effective_date)
        assert effective_date_default >= self.current_date, \
            f"Effective Date default value {effective_date_default} should be >= current date!"
        expiration_date_default = self.actions.get_element_value(self.pages.CRS.order_entry.inp_expiration_date)
        assert expiration_date_default >= effective_date_default, \
            f"Expiration date default value {expiration_date_default} should be >= Effective Date!"

        # fill the rest of required fields
        self.lib.required_fields.crs_fill_required_fields()
        # set valid values for dates (since Required field may enter values from names that are valid for one
        #  tenant and invalid for another) and verify that Add to order button is enabled
        self.lib.general_helper.find_and_click(self.lib.CRS.order_entry.tab_locator("Order_Item"))
        self.lib.general_helper.find_and_send_keys(self.pages.CRS.order_entry.inp_expiration_date,
                                                   self.valid_future_exp_date, reset_focus=True)
        self.lib.general_helper.find_and_send_keys(self.pages.CRS.order_entry.inp_effective_date, self.current_date,
                                                   reset_focus=True)
        self.lib.general_helper.find_and_send_keys(self.pages.CRS.order_entry.inp_anticipated_date,
                                                   self.current_date, reset_focus=True)
        self.actions.assert_element_enabled(self.pages.CRS.order_entry.btn_add_to_order)

        # enter invalid dates and verify validation message texts
        # Anticipated Date > Expiration Date-------------------------------------------------------------------
        # set the Expiration Date value
        self.lib.general_helper.find_and_send_keys(self.pages.CRS.order_entry.inp_expiration_date,
                                                   self.invalid_past_date, reset_focus=True)
        expected_message = "Anticipated Date should be less than or equal to Expiration Date"
        assertion_message = "Anticipated Date > Expiration Date validation is incorrect!"
        self.check_validation_message(self.pages.CRS.order_entry.inp_anticipated_date, self.current_date,
                                      expected_message, assertion_message)
        # reset the Expiration Date to a valid value
        self.lib.general_helper.find_and_send_keys(self.pages.CRS.order_entry.inp_expiration_date,
                                                   self.current_date,
                                                   reset_focus=True)
        # Anticipated Date < current date
        expected_message = "Invalid date!"
        assertion_message = "Anticipated Date < current date validation is incorrect!"
        self.check_validation_message(self.pages.CRS.order_entry.inp_anticipated_date, self.invalid_past_date,
                                      expected_message, assertion_message)
        # Anticipated Date > n days
        expected_message = "Invalid date!"
        assertion_message = "Anticipated Date > n days validation is incorrect!"
        self.check_validation_message(self.pages.CRS.order_entry.inp_anticipated_date,
                                      self.invalid_future_antic_date,
                                      expected_message, assertion_message)
        # reset the Anticipation Date to a valid value
        self.lib.general_helper.find_and_send_keys(self.pages.CRS.order_entry.inp_anticipated_date,
                                                   self.current_date, reset_focus=True)
        # Effective Date < current date-------------------------------------------------------------------------
        expected_message = "Invalid date!"
        assertion_message = "Effective Date < current date validation is incorrect!"
        self.check_validation_message(self.pages.CRS.order_entry.inp_effective_date, self.invalid_past_date,
                                      expected_message, assertion_message)
        # Effective Date > n days - currently n days are not set on DuPage
        # expected_message = "Invalid Effective Date"
        # assertion_message = "Effective Date > n days validation is incorrect!"
        # self.check_validation_message(self.pages.CRS.order_entry.inp_anticipated_date, invalid_future_eff_date,
        #                               expected_message, assertion_message)
        # # reset the Effective Date to a valid value
        self.lib.general_helper.find_and_send_keys(self.pages.CRS.order_entry.inp_effective_date, self.current_date,
                                                   reset_focus=True)
        self.actions.wait(1)
        # Expiration Date > n days------------------------------------------------------------------------------
        self.lib.general_helper.find_and_send_keys(self.pages.CRS.order_entry.inp_expiration_date,
                                                   self.invalid_future_exp_date, reset_focus=True)
        expected_message = "Expiration Date exceeds the allowed maximum date!"
        actual_message = self.lib.general_helper.find(self.pages.CRS.order_entry.msg_expiration_date, get_text=True)
        assert actual_message == expected_message, "Expiration Date > n days validation is incorrect!"
        self.actions.assert_element_enabled(self.pages.CRS.order_entry.btn_add_to_order)  # message is warning only
        self.lib.CRS.order_entry.click_add_to_order()
        self.lib.general_helper.find(self.pages.CRS.order_summary.btn_checkout, wait_displayed=True)

    def check_validation_message(self, locator, value, expected_message, assertion_message):
        self.lib.general_helper.find_and_send_keys(locator, value, reset_focus=True)
        actual_message = self.actions.get_element_attribute((locator[0], locator[1]), "data-val-title")
        self.actions.step(f"The actual message text is {actual_message}")
        assert actual_message == expected_message, assertion_message
        self.actions.assert_element_not_enabled(self.pages.CRS.order_entry.btn_add_to_order)


if __name__ == '__main__':
    run_test(__file__, env="qa_dupage")
