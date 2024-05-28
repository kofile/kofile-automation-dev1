"""initialize drawer test"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Open CRS, initialize drawer from Initialize Drawer tab and go back to Order Queue"""

tags = ["48999_location_2"]


class test(TestParent):                                                # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: no
        Post-conditions: Order Queue page is opened, drawer is initialized
        """
        self.atom.CRS.general.go_to_crs()
        self.atom.CRS.initialize_drawer.initialize_drawer()


if __name__ == '__main__':
    run_test(__file__)
