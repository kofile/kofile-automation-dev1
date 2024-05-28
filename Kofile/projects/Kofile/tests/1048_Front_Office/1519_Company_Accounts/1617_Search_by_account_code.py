from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS -> Front Office, search company account by account code, 
    check found company name
        """

tags = ["48999_location_2"]


class test(TestParent):                                                                     # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.data_helper.get_front_office()
        self.atom.CRS.general.go_to_crs()
        # Navigate to Front Office and search account by code
        self.lib.CRS.front_office.search_account(self.data.front_office.account_code)
        # Check found company name
        self.lib.CRS.front_office.check_company_name(self.data.front_office.company_name)


if __name__ == '__main__':
    run_test(__file__)
