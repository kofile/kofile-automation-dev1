from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS -> Front Office and register new company account without user, 
    """

tags = ["48999_location_2"]


class test(TestParent):                                                                           # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs()
        # Create new account without user
        self.lib.CRS.front_office.create_new_account()


if __name__ == '__main__':
    run_test(__file__)
