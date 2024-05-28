from datetime import datetime

from dateutil.relativedelta import relativedelta

from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
        1.Navigate to CRS and create ML order with Marriage License order item.
        2.Open the order item tab.
        3.Set anticipated, effective, expiration date pickers with correct data. Fill in all required fields except of 
        applicant's birth dates.
        4.Set applicant's 1 Birth date so difference between Birth and Anticipated date will be less or equal 16 years.
        5.Set applicant's 2 Birth date so difference between Birth and Anticipated date will be less or equal 16 years.
        6.Change anticipated date to different date so difference between Birth and Anticipated date will be less or 
        equal 16 years.
        7.Change anticipated date to different date so difference between Birth and Anticipated date will be more than 
        16 years.
        8.Change applicant's 1 Birth date so difference between Birth and Anticipated date will be more than 16 years.
        9.Change applicant's 2 Birth date so difference between Birth and Anticipated date will be more than 16 years.
        10.Clear value from the Anticipated date and repeat steps 3 - 9 with comparing applicants birth date and 
        expiration date.
    """

tags = []


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def change_applicant_dob(self, applicant_id: int, applicant_age: int):
        self.lib.general_helper.find_and_click(
            self.lib.general_helper.make_locator(self.pages.CRS.order_entry.lnk_order_entry_tab,
                                                 f"Applicant{applicant_id + 1}"))
        self.actions.clear(
            self.lib.general_helper.make_locator(self.pages.CRS.order_entry.applicant_birth_date, applicant_id))
        self.actions.send_keys(
            self.lib.general_helper.make_locator(self.pages.CRS.order_entry.applicant_birth_date, applicant_id),
            (datetime.strptime(self.data.checking_date, "%m/%d/%Y") - relativedelta(
                years=applicant_age)).strftime("%m%d%Y"))
        self.lib.general_helper.reset_focus()
        self.actions.wait(1)
        if applicant_age <= 18:
            self.lib.general_helper.find_and_click(self.pages.CRS.order_entry.yes_button)

    def change_anticipated_or_expiration_date(self, date: str):
        date_picker_locator = self.pages.CRS.order_entry.anticipated_date_picker if int(
            self.data.flag) else self.pages.CRS.order_entry.expiration_date_picker
        self.lib.general_helper.find_and_click(
            self.lib.general_helper.make_locator(self.pages.CRS.order_entry.lnk_order_entry_tab, "Order Item"))
        self.actions.clear(date_picker_locator)
        self.actions.send_keys(date_picker_locator, date)
        self.lib.general_helper.reset_focus()

    def __test__(self):
        self.lib.general_helper.check_order_type()
        # step 1, 2
        self.atom.CRS.general.go_to_crs()
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.fill_order_header_name()
        self.atom.CRS.order_entry.select_order_type()
        self.actions.select_by_text(self.pages.CRS.fields.document_type_ddl_by_oi_index(), self.data.doc_type)
        self.actions.store("checking_date", self.names.FIELDS_VALUE["Strings"]["AnticipatedDate"][0] if int(
            self.data.flag) else self.actions.get_element_value(self.pages.CRS.order_entry.expiration_date_picker))
        # step 3
        self.lib.required_fields.rs_fill_required_fields()
        # step 4, 5
        for applicant in range(2):
            self.change_applicant_dob(applicant, 16)
            self.actions.assert_element_text(
                self.lib.general_helper.make_locator(self.pages.CRS.order_entry.ml_dob_error_text, applicant),
                f"Applicant {applicant + 1} will not be of a legal age to marry!")
            self.actions.assert_element_enabled(self.pages.CRS.order_entry.btn_add_to_order)
        # step 6
        self.change_anticipated_or_expiration_date(self.data.checking_date)
        self.actions.wait_for_element_displayed(self.pages.CRS.order_entry.confirmation_pop_up_text)
        self.actions.assert_element_text(self.pages.CRS.order_entry.confirmation_pop_up_text,
                                         "Applicants are not be of a legal age to marry!")
        self.lib.general_helper.find_and_click(self.pages.CRS.initialize_drawer.btn_ok_on_warning_popup)
        # steps 8, 9
        for applicant in range(2):
            self.change_applicant_dob(applicant, 17)
            self.actions.assert_element_not_present(
                self.lib.general_helper.make_locator(self.pages.CRS.order_entry.ml_dob_error_text, applicant))
            self.actions.assert_element_enabled(self.pages.CRS.order_entry.btn_add_to_order)
        # step 7
        self.change_anticipated_or_expiration_date(self.data.checking_date)
        self.actions.assert_element_not_present(self.pages.CRS.order_entry.confirmation_pop_up_text)
        # step 6
        self.change_applicant_dob(0, 16)
        self.change_anticipated_or_expiration_date(self.data.checking_date)
        self.actions.wait_for_element_displayed(self.pages.CRS.order_entry.confirmation_pop_up_text)
        self.actions.assert_element_text(self.pages.CRS.order_entry.confirmation_pop_up_text,
                                         "Applicant 1 will not be of a legal age to marry!")
        self.lib.general_helper.find_and_click(self.pages.CRS.initialize_drawer.btn_ok_on_warning_popup)
        self.change_applicant_dob(0, 17)
        self.change_applicant_dob(1, 16)
        self.change_anticipated_or_expiration_date(self.data.checking_date)
        self.actions.wait_for_element_displayed(self.pages.CRS.order_entry.confirmation_pop_up_text)
        self.actions.assert_element_text(self.pages.CRS.order_entry.confirmation_pop_up_text,
                                         "Applicant 2 will not be of a legal age to marry!")
        self.lib.general_helper.find_and_click(self.pages.CRS.initialize_drawer.btn_ok_on_warning_popup)
        # step 10 covered by .csv config file, just add a new one row with the CIVIL UNION (MC) doc_type


if __name__ == '__main__':
    run_test(__file__)
