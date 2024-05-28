from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Navigate to CRS ->
    Navigate to Front Office ->
    Click on the "Workflow Dates" sub-tab ->
    Click on the edit button for any department e.g. Property Records ->
    Change date using date picker and click on the "Save" button ->
    Wait some minutes and navigate to Clerk Search ->
    Select the same department (step 4) ->
    Look at "Certification Date Range" ->
    Certified End Date is updated
        """

tags = ["48999_location_2"]


class test(TestParent):                                                                        # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.data_helper.get_front_office()
        self.atom.CRS.general.go_to_crs()
        # Navigate to Front Office
        self.actions.wait(1)
        self.lib.CRS.front_office.go_to_front_office()
        # Navigate to workflow dates sub
        self.lib.CRS.front_office.go_to_workflow_dates_sub()

        # check checkboxes
        self.actions.assert_element_checked(self.pages.CRS.front_office.rdb_wd_certification_date_by_department)
        self.actions.assert_element_not_checked(self.pages.CRS.front_office.rdb_mail_back_date_by_recorded_date)

        # edit row
        self.lib.CRS.front_office.click_edit_to_row_by_department()
        self.lib.CRS.front_office.set_new_certified_end_date()

        self.atom.CS.general.go_to_cs()
        self.lib.PS.general.verify_certificate_date()


if __name__ == '__main__':
    run_test(__file__)
