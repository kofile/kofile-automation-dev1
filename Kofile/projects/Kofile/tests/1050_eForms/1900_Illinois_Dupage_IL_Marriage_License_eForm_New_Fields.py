from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test
from datetime import datetime
from dateutil.relativedelta import relativedelta

description = """
        1.Fill the Applicant1/2 Email Address and Phone Number fields with correct data.
        2.Fill in the 'County', 'Country' fields for Applicant 1/2 sections 151 characters.
        3.Fill the 'County', 'Country' fields for Applicant 1/2 sections with correct data.
        4.Try to save form without filling the Gender DDL for Applicant1/2 sections.
        5.Check the 'Gender' DDL for Applicant1/2 sections.
        6.Select any of values in the 'Gender' DDL for Applicant1/2 sections.
        7.Select any allowed past date in the Date of Birth date picker for Applicant1/2 sections.
        8.Try to save form without filling the Previous Marriage field for Applicant1/2 sections.
        9.Try to input not numeric value in the Previous Marriage field for Applicant1/2 sections.
        10.Input '0' value to the Previous Marriage field and click TAB button for Applicant1/2 sections.
        11.Input > 0 value in the field and click TAB button for Applicant1/2 sections.
        12.Try to save form without filling the --Select Reason-- DDL for Applicant1/2 sections.
        13.Click on the --Select Reason-- DDL for Applicant1/2 sections.
        14.Type existing reason keyword in the selected --Select Reason-- DDL for Applicant1/2 sections.
        15.Select highlighted reason for Applicant1/2 sections.
        16.Try to save form without filling the Date Ended date picker for Applicant1/2 sections.
        17.Select '04/00/2017' value in the Date Ended date picker for Applicant1/2 sections.
        18.Try to save form without filling the End State DDL for Applicant1/2 sections.
        19.Click the End State DDL for Applicant1/2 sections.
        20.Select any value from End State DDL for Applicant1/2 sections.
        21.Try to save form without filling the 'Ended in Country', 'Ended in County' fields for Applicant1/2 sections.
        22.Fill in the 'Ended in Country', 'Ended in County' fields for Applicant 1/2 sections 151 characters.
        23.Fill in the 'Ended in Country', 'Ended in County' fields for Applicant 1/2 sections with correct data.
        24.Try to save form without filling the #Education Elementary or Secondary and Education College field for Applicant1/2 sections.
        25.Try to type out of allowed range value (20) in the #Education Elementary field for Applicant1/2 sections.
        26.Type any of allowed range value (>0 and <20) in the #Education Elementary field for Applicant1/2 sections.
        27.Try to save form without filling the --Select Occupation-- DDL for Applicant1/2 sections.
        28.Click on the --Select Occupation-- DDL.
        29.Type existing reason keyword in the selected --Select Occupation-- DDL for Applicant1/2 sections.
        30.Select highlighted reason for Applicant1/2 sections.
        31.Try to save form without filling the --Select Race-- DDL for Applicant1/2 sections.
        32.Click on the --Select Race-- DDL.
        33.Select 'Hispanic' or 'Other' value in the --Select Race-- DDL for Applicant1/2 sections.
        34.Try to save form without filling the --Select Ancestry-- DDL for Applicant1/2 sections.
        35.Click on the --Select Ancestry-- DDL.
        36.Type existing value keyword in the selected --Select Ancestry-- DDL for Applicant1/2 sections.
        37.Select highlighted reason for Applicant1/2 sections.
        38.Check Applicant1/2 Father section.
        39.Check the 'is Deceased' checkbox for Applicant1/2 Father section.
        40.Fill in the 'Fathers Name', 'Surname at Birth', 'City', 'Country', 'Fathers State/Country of Birth' fields for Applicant 1/2 Father section 151 characters.
        41.Fill in the 'Fathers Name', 'Surname at Birth', 'City', 'Country', 'Fathers State/Country of Birth' fields for Applicant 1/2 Father section with correct data.
        42.Check Applicant1/2 Mother section.
        43.Fill in the 'Mothers Name', 'Surname at Birth', 'City', 'Country', 'Mothers State/Country of Birth' fields for Applicant 1/2 Mother section 151 characters.
        44.Fill in the 'Mothers Name', 'Surname at Birth', 'City', 'Country', 'Mothers State/Country of Birth' fields for Applicant 1/2 Mother section with correct data.
        45.Check the Applicants relationship TRUE/FALSE radio.
        46.Select False value in the radio.
        47.Select True value in the radio.
        48.Type > 100 characters in the Relationship field and move out cursor from the field.
        49.Type <= 100 characters in the Relationship field and click Submit to saving form.
        50.Navigate to CRS open order item to process and check data in the related field
    """

tags = []


class test(TestParent):  # noqa
    gender_list, gender_count = ['Male', 'Female', 'X'], 4
    age_list, buffer = [18, 22], {}

    def __init__(self, data):
        self.eform_strings = self.names.FIELDS_VALUE["Strings"]["eForm"]
        super(test, self).__init__(data, __name__)

    def __is_required__(self, loc):
        validation_ms = self.actions.get_element_attribute(loc, "data-val-title")
        return "is required" in str(validation_ms).lower()

    def is_required(self, loc):
        assert self.__is_required__(loc), f"Field {loc} is not required"

    def is_not_required(self, loc):
        assert not self.__is_required__(loc), f"Field {loc} is required"

    def check_field_validation(self, loc, val, ms):
        self.lib.general_helper.find_and_send_keys(loc, val)
        self.lib.general_helper.reset_focus()
        self.actions.assert_element_attribute(loc, "data-val-title", ms)

    def __test__(self):
        self.lib.general_helper.check_order_type()
        with self.lib.db as db:
            status_list = db.get_states()

        self.atom.EForm.general.go_to_eform_portal()
        self.atom.EForm.general.open_eform_document()

        for applicant_int in range(2):
            applicant, applicant_id = str(applicant_int), applicant_int + 1
            age = self.age_list[applicant_int]

            # step 1
            self.lib.general_helper.find_and_send_keys(
                self.lib.general_helper.make_locator(self.pages.eform.applicant_email, applicant),
                self.eform_strings["email"].format(applicant_id))
            self.lib.general_helper.find_and_send_keys(
                self.lib.general_helper.make_locator(self.pages.eform.applicant_phone, applicant),
                self.eform_strings["phone"].format(applicant_id))

            # step 2
            self.check_field_validation(
                self.lib.general_helper.make_locator(self.pages.eform.applicant_county, applicant), "a" * 151,
                "Value must be max 150 digits!")
            self.check_field_validation(
                self.lib.general_helper.make_locator(self.pages.eform.applicant_country, applicant), "a" * 151,
                "Value must be max 150 digits!")

            # step 3
            self.check_field_validation(
                self.lib.general_helper.make_locator(self.pages.eform.applicant_county, applicant),
                self.eform_strings["county"].format(applicant_id), "")
            self.check_field_validation(
                self.lib.general_helper.make_locator(self.pages.eform.applicant_country, applicant),
                self.eform_strings["country"].format(applicant_id), "")

            # step 4 !not configured!
            # self.is_required(self.lib.general_helper.make_locator(self.pages.eform.applicant_gender, applicant))

            # step 5
            self.lib.general_helper.verify_drop_down_options(
                self.lib.general_helper.make_locator(self.pages.eform.applicant_gender, applicant),
                options_count=self.gender_count, text_list=self.gender_list)

            # step 6
            self.actions.select_option_by_text(
                self.lib.general_helper.make_locator(self.pages.eform.applicant_gender, applicant),
                self.gender_list[applicant_int])

            # step 7
            self.lib.general_helper.find_and_send_keys(
                self.lib.general_helper.make_locator(self.pages.eform.applicant_age_field, applicant),
                (datetime.now() - relativedelta(years=age, months=2)).strftime(
                    "%m%d%Y"))
            self.lib.general_helper.reset_focus()
            self.actions.wait_for_element_text(
                self.lib.general_helper.make_locator(self.pages.eform.applicant_age_number, applicant),
                str(age), 5)

            # step 8 !not configured!
            # self.is_required(self.lib.general_helper.make_locator(self.pages.eform.previous_marriages, applicant))

            # step 9
            self.lib.general_helper.find_and_send_keys(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages, applicant), "a")
            self.actions.assert_element_value(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages, applicant), "")
            self.lib.general_helper.find_and_send_keys(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages, applicant), "!")
            self.actions.assert_element_value(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages, applicant), "")

            # step 10
            self.lib.general_helper.find_and_send_keys(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages, applicant), "0")
            self.actions.verify_element_not_enabled(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages_reason, applicant))
            self.actions.verify_element_not_enabled(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages_date, applicant))
            self.actions.verify_element_not_enabled(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages_state, applicant))
            self.actions.verify_element_not_enabled(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages_country, applicant))
            self.actions.verify_element_not_enabled(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages_county, applicant))

            # step 11
            self.lib.general_helper.find_and_send_keys(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages, applicant),
                str(applicant_id))
            self.actions.verify_element_enabled(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages_reason, applicant))
            self.actions.verify_element_enabled(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages_date, applicant))
            self.actions.verify_element_enabled(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages_state, applicant))
            self.actions.verify_element_enabled(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages_country, applicant))
            self.actions.verify_element_enabled(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages_county, applicant))

            # steep 12 !not configured!
            # self.is_required(self.lib.general_helper.make_locator(self.pages.eform.previous_marriages_reason, applicant))

            # step 13, 14 and 15
            reason_box = self.lib.general_helper.find(
                self.lib.general_helper.make_locator(self.pages.eform.prev_marriage_reason_box, applicant))
            reason_field = reason_box.find_element_by_tag_name("input")
            _, data_list_options = self.lib.general_helper.verify_drop_down_options(self.pages.eform.data_list,
                                                                                    parent=reason_box)
            assert len(data_list_options) > 0
            reason_field.send_keys(data_list_options[0])
            self.buffer["reason"] = data_list_options[0]

            # # step 16 !not configured!
            # self.is_required(self.lib.general_helper.make_locator(self.pages.eform.previous_marriages_date, applicant))

            # step 17
            self.lib.general_helper.find_and_send_keys(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages_date, applicant),
                self.eform_strings["end_date"].strip("/"))
            # # step 18 !not configured!
            # self.is_required(self.lib.general_helper.make_locator(self.pages.eform.previous_marriages_state, applicant))

            # step 19
            self.lib.general_helper.verify_drop_down_options(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages_state, applicant),
                text_list=status_list)

            # step 20
            data_list, _ = self.lib.general_helper.verify_drop_down_options(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages_state, applicant))
            self.actions.select_option_by_text(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages_state, applicant),
                data_list[1])
            self.buffer["end_state"] = data_list[1]

            # step 21 !not configured!
            # self.is_required(self.lib.general_helper.make_locator(self.pages.eform.previous_marriages_state, applicant))

            # step 22 and 23
            self.check_field_validation(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages_county, applicant),
                "1" * 151, "Value must be max 150 digits!")
            self.lib.general_helper.find_and_send_keys(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages_county, applicant),
                self.eform_strings["ended_county"].format(applicant_id))

            self.check_field_validation(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages_country, applicant),
                "1" * 151, "Value must be max 150 digits!")
            self.lib.general_helper.find_and_send_keys(
                self.lib.general_helper.make_locator(self.pages.eform.previous_marriages_country, applicant),
                self.eform_strings["ended_country"].format(applicant_id))

            # step 24 !not configured!
            # self.is_required(self.lib.general_helper.make_locator(self.pages.eform.education_years, applicant))
            # self.is_required(self.lib.general_helper.make_locator(self.pages.eform.college_years, applicant))

            # step 25
            self.check_field_validation(
                self.lib.general_helper.make_locator(self.pages.eform.education_years, applicant),
                "1" * 21, "Value must be max 20 characters!")
            self.check_field_validation(
                self.lib.general_helper.make_locator(self.pages.eform.college_years, applicant),
                "6", "Allowed values are 0, 1, 2, 3, 4, 5 and +")

            # step 26
            self.lib.general_helper.find_and_send_keys(
                self.lib.general_helper.make_locator(self.pages.eform.education_years, applicant),
                self.eform_strings["education"].format(applicant_id))
            self.lib.general_helper.find_and_send_keys(
                self.lib.general_helper.make_locator(self.pages.eform.college_years, applicant),
                self.eform_strings["college"].format(applicant_id))

            # step 27 !not configured!
            # self.is_required(self.lib.general_helper.make_locator(self.pages.eform.occupation, applicant))

            # step 28, 29 and 30
            box = self.lib.general_helper.find(
                self.lib.general_helper.make_locator(self.pages.eform.occupation_box, applicant))
            field = box.find_element_by_tag_name("input")
            _, options = self.lib.general_helper.verify_drop_down_options(self.pages.eform.occupation_data_list,
                                                                          parent=box)
            assert len(options) > 0
            field.send_keys(options[0])
            self.buffer["occupation"] = options[0]

            # step 31 !not configured!
            # self.is_required(self.lib.general_helper.make_locator(self.pages.eform.race_select, applicant))

            # step 32
            races, _ = self.lib.general_helper.verify_drop_down_options(
                self.lib.general_helper.make_locator(self.pages.eform.race_select, applicant))
            races = races[1:]
            assert races == list(sorted(races)), "Preconfigured reasons must be stored alphabetically in the DDL."
            assert self.eform_strings["race"] in races, f"Races must contain {self.eform_strings['race']}"

            # step 33
            self.actions.select_option_by_text(
                self.lib.general_helper.make_locator(self.pages.eform.race_select, applicant),
                self.eform_strings["race"])
            self.actions.verify_element_enabled(
                self.lib.general_helper.make_locator(self.pages.eform.ancestry_select, applicant))

            # step 34
            self.is_required(self.lib.general_helper.make_locator(self.pages.eform.ancestry_select, applicant))

            # step 35
            _, ancestry = self.lib.general_helper.verify_drop_down_options(
                self.lib.general_helper.make_locator(self.pages.eform.ancestry_select_data_list,
                                                     "G" if applicant_int == 0 else "B"))
            assert len(ancestry) > 0
            assert ancestry == list(
                sorted(ancestry)), "Preconfigured reasons must be stored alphabetically in the DDL."

            # step 36 and 37
            self.lib.general_helper.find_and_send_keys(
                self.lib.general_helper.make_locator(self.pages.eform.ancestry_select, applicant),
                ancestry[0])
            self.buffer["ancestry"] = ancestry[0]

            for parent in range(2):
                # step 38, 39 and 42
                parent = str(parent)
                self.is_required(
                    self.lib.general_helper.make_locator(self.pages.eform.parent_name, applicant, parent))
                self.is_required(
                    self.lib.general_helper.make_locator(self.pages.eform.parent_city, applicant, parent))
                self.is_required(
                    self.lib.general_helper.make_locator(self.pages.eform.parent_state, applicant, parent))
                self.lib.general_helper.find_and_check_uncheck_checkbox(
                    self.lib.general_helper.make_locator(self.pages.eform.parent_deceased, applicant, parent), True)
                self.is_not_required(
                    self.lib.general_helper.make_locator(self.pages.eform.parent_name, applicant, parent))
                self.is_not_required(
                    self.lib.general_helper.make_locator(self.pages.eform.parent_city, applicant, parent))
                self.is_not_required(
                    self.lib.general_helper.make_locator(self.pages.eform.parent_state, applicant, parent))

                # step 40 and 43
                self.check_field_validation(
                    self.lib.general_helper.make_locator(self.pages.eform.parent_name, applicant, parent),
                    "1" * 151, "Value must be max 150 digits!")
                self.check_field_validation(
                    self.lib.general_helper.make_locator(self.pages.eform.surname_at_birth, applicant, parent),
                    "1" * 151, "Value must be max 150 digits!")
                self.check_field_validation(
                    self.lib.general_helper.make_locator(self.pages.eform.parent_city, applicant, parent),
                    "1" * 151, "Value must be max 150 characters!")
                self.check_field_validation(
                    self.lib.general_helper.make_locator(self.pages.eform.parent_county, applicant, parent),
                    "1" * 151, "Value must be max 150 digits!")
                self.check_field_validation(
                    self.lib.general_helper.make_locator(self.pages.eform.county_of_birth, applicant, parent),
                    "1" * 151, "Value must be max 150 digits!")

                # step 41 and 44
                self.lib.general_helper.find_and_send_keys(
                    self.lib.general_helper.make_locator(self.pages.eform.parent_name, applicant, parent),
                    self.eform_strings["parent_name"].format(applicant_id, parent))
                self.lib.general_helper.find_and_send_keys(
                    self.lib.general_helper.make_locator(self.pages.eform.surname_at_birth, applicant, parent),
                    self.eform_strings["surname_at_birth"].format(applicant_id, parent))
                self.lib.general_helper.find_and_send_keys(
                    self.lib.general_helper.make_locator(self.pages.eform.parent_city, applicant, parent),
                    self.eform_strings["parent_city"].format(applicant_id, parent))
                self.lib.general_helper.find_and_send_keys(
                    self.lib.general_helper.make_locator(self.pages.eform.parent_county, applicant, parent),
                    self.eform_strings["parent_county"].format(applicant_id, parent))
                self.lib.general_helper.find_and_send_keys(
                    self.lib.general_helper.make_locator(self.pages.eform.county_of_birth, applicant, parent),
                    self.eform_strings["parent_county_of_birth"].format(applicant_id, parent))

                data_list, _ = self.lib.general_helper.verify_drop_down_options(
                    self.lib.general_helper.make_locator(self.pages.eform.parent_state_code, applicant, parent))
                self.actions.select_option_by_text(
                    self.lib.general_helper.make_locator(self.pages.eform.parent_state_code, applicant, parent),
                    data_list[1])
                self.buffer[f"applicant:{applicant} parent:{parent}"] = data_list[1]

                # fil ssn
                self.lib.general_helper.find_and_send_keys(
                    self.lib.general_helper.make_locator(self.pages.eform.ssn, applicant),
                    self.eform_strings["ssn"].format(applicant_id))

        # step 45
        self.actions.assert_element_has_not_attribute(self.pages.eform.applicant_relationship_true_radiobutton,
                                                      "checked")
        self.actions.assert_element_has_not_attribute(self.pages.eform.applicant_relationship_false_radiobutton,
                                                      "checked")

        # step 46
        self.lib.general_helper.find_and_click(self.pages.eform.applicant_relationship_false_radiobutton)
        self.actions.assert_element_attribute(self.pages.eform.applicant_relationship_false_radiobutton, "checked",
                                              "true")
        self.actions.assert_element_has_not_attribute(self.pages.eform.applicant_relationship_true_radiobutton,
                                                      "checked")
        self.actions.verify_element_not_present(self.pages.eform.applicant_relationship_input)

        # step 47
        self.lib.general_helper.find_and_click(self.pages.eform.applicant_relationship_true_radiobutton)
        self.actions.assert_element_has_not_attribute(self.pages.eform.applicant_relationship_false_radiobutton,
                                                      "checked")
        self.actions.assert_element_attribute(self.pages.eform.applicant_relationship_true_radiobutton, "checked",
                                              "true")
        self.actions.wait_for_element_displayed(self.pages.eform.applicant_relationship_input)

        # step 48
        self.is_required(self.pages.eform.applicant_relationship_input)
        self.check_field_validation(self.pages.eform.applicant_relationship_input, "1" * 101,
                                    "Value must be max 100 characters!")

        # step 49
        self.lib.general_helper.find_and_send_keys(self.pages.eform.applicant_relationship_input, "a" * 100)
        self.lib.general_helper.reset_focus()
        self.is_not_required(self.pages.eform.applicant_relationship_input)

        # step 50
        self.atom.EForm.general.submit_eform()

        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.crs.click_running_man()
        self.actions.wait_for_element_displayed(self.pages.CRS.order_summary.lbl_order_number)
        self.atom.CRS.order_summary.edit_oit()

        for applicant_id in range(2):
            applicant = str(applicant_id + 1)
            age = self.age_list[applicant_id]
            self.lib.general_helper.find_and_click(
                self.lib.general_helper.make_locator(self.pages.CRS.order_entry.lnk_order_entry_tab,
                                                     f"Applicant{applicant}"))
            self.actions.wait_for_element_displayed(
                self.lib.general_helper.make_locator(self.pages.CRS.order_entry.applicant_county, applicant_id))
            self.actions.assert_element_value(
                self.lib.general_helper.make_locator(self.pages.CRS.order_entry.applicant_county, applicant_id),
                self.eform_strings["county"].format(applicant))
            self.actions.assert_element_value(
                self.lib.general_helper.make_locator(self.pages.CRS.order_entry.applicant_country, applicant_id),
                self.eform_strings["country"].format(applicant))
            self.actions.assert_element_value(
                self.lib.general_helper.make_locator(self.pages.CRS.order_entry.applicant_ssn, applicant_id),
                self.eform_strings["ssn"].format(applicant))
            self.actions.assert_selected_option_by_text(
                self.lib.general_helper.make_locator(self.pages.CRS.order_entry.applicant_gender, applicant_id),
                self.gender_list[applicant_id])
            self.actions.assert_element_value(
                self.lib.general_helper.make_locator(self.pages.CRS.order_entry.applicant_email, applicant_id),
                self.eform_strings["email"].format(applicant).upper())
            self.actions.assert_element_value(
                self.lib.general_helper.make_locator(self.pages.CRS.order_entry.applicant_birth_date, applicant_id),
                (datetime.now() - relativedelta(years=age, months=2)).strftime("%m/%d/%Y"))
            self.actions.assert_element_text(
                self.lib.general_helper.make_locator(self.pages.CRS.order_entry.applicant_age, applicant_id),
                str(age))
            self.actions.assert_element_value(
                self.lib.general_helper.make_locator(self.pages.CRS.order_entry.end_date, applicant_id),
                self.eform_strings["end_date"])
            self.actions.assert_element_value(
                self.lib.general_helper.make_locator(self.pages.CRS.order_entry.reason, applicant_id),
                self.buffer["reason"])
            self.actions.assert_element_value(
                self.lib.general_helper.make_locator(self.pages.CRS.order_entry.prev_marriage, applicant_id),
                applicant)
            self.actions.assert_element_value(
                self.lib.general_helper.make_locator(self.pages.CRS.order_entry.end_county, applicant_id),
                self.eform_strings["ended_county"].format(applicant).upper())
            self.actions.assert_element_value(
                self.lib.general_helper.make_locator(self.pages.CRS.order_entry.end_country, applicant_id),
                self.eform_strings["ended_country"].format(applicant).upper())
            self.actions.assert_element_value(
                self.lib.general_helper.make_locator(self.pages.CRS.order_entry.years_of_education, applicant_id),
                self.eform_strings["education"].format(applicant))
            self.actions.assert_element_value(
                self.lib.general_helper.make_locator(self.pages.CRS.order_entry.years_of_college, applicant_id),
                self.eform_strings["college"].format(applicant))
            self.actions.assert_element_value(
                self.lib.general_helper.make_locator(self.pages.CRS.order_entry.occupation, applicant_id),
                self.buffer["occupation"].upper())
            self.actions.assert_selected_option_by_text(
                self.lib.general_helper.make_locator(self.pages.CRS.order_entry.race, applicant_id),
                self.eform_strings["race"])
            self.actions.assert_element_value(
                self.lib.general_helper.make_locator(self.pages.CRS.order_entry.ancestry, applicant_id),
                self.buffer["ancestry"].upper())
            self.actions.assert_selected_option_by_text(
                self.lib.general_helper.make_locator(self.pages.CRS.order_entry.end_state, applicant_id),
                self.buffer["end_state"])

            for parent in range(2):
                parent = str(parent)
                self.actions.assert_element_value(
                    self.lib.general_helper.make_locator(self.pages.CRS.order_entry.parent_name, applicant_id,
                                                         parent),
                    self.eform_strings["parent_name"].format(applicant, parent))
                self.actions.assert_element_value(
                    self.lib.general_helper.make_locator(self.pages.CRS.order_entry.parent_birth, applicant_id,
                                                         parent),
                    self.eform_strings["surname_at_birth"].format(applicant, parent))
                self.actions.assert_element_value(
                    self.lib.general_helper.make_locator(self.pages.CRS.order_entry.parent_city, applicant_id,
                                                         parent),
                    self.eform_strings["parent_city"].format(applicant, parent))
                self.actions.assert_element_value(
                    self.lib.general_helper.make_locator(self.pages.CRS.order_entry.parent_county, applicant_id,
                                                         parent),
                    self.eform_strings["parent_county"].format(applicant, parent))
                self.actions.assert_element_value(
                    self.lib.general_helper.make_locator(self.pages.CRS.order_entry.parent_county_of_birth,
                                                         applicant_id, parent),
                    self.eform_strings["parent_county_of_birth"].format(applicant, parent))

                self.actions.assert_selected_option_by_text(
                    self.lib.general_helper.make_locator(self.pages.CRS.order_entry.parent_state, applicant_id,
                                                         parent),
                    self.buffer[f"applicant:{applicant_id} parent:{parent}"])

            if applicant == "1":
                self.actions.assert_element_has_not_attribute(
                    self.pages.CRS.order_entry.applicant_relationship_false_checkbox,
                    "checked")
                self.actions.assert_element_attribute(
                    self.pages.CRS.order_entry.applicant_relationship_true_checkbox, "checked",
                    "true")
                self.actions.assert_element_value(self.pages.CRS.order_entry.applicant_relationship_input,
                                                  "a" * 100)


if __name__ == '__main__':
    run_test(__file__)
