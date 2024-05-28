from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Go to CRS
-> Go to Balance Drawer
-> Click 'Order Queue' button
-> Check opened page
    """
    
tags = ["48999_location_2"]


class test(TestParent):                                                                  # noqa

    def __init__(self, data):
        data["orderheader"] = "guest"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to CRS
        self.atom.CRS.general.go_to_crs()
        # Go to Balance drawer
        self.lib.CRS.balance_drawer.go_to_balance_drawer()
        # Go to Order Queue
        self.lib.CRS.crs.go_to_order_queue()


if __name__ == '__main__':
    run_test(__file__)
