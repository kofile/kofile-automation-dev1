from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS -> Front Office, search company account and change 'Credit limit', 
    edit account again and check new 'Credit limit'
        """

tags = ["48999_location_2"]


class test(TestParent):                                                                                    # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.data_helper.get_front_office()
        self.atom.CRS.general.go_to_crs()
        # Navigate to Front Office and change 'Credit limit' option
        self.lib.CRS.front_office.change_credit_limit(self.data, 50)
        # change 'Credit limit' option back
        self.lib.CRS.front_office.change_credit_limit(self.data, 0)


if __name__ == '__main__':
    run_test(__file__)
