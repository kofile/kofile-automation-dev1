from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS -> Front Office, search company account and disable it, 
    back to CRS, create new order and search company account
    "No results found" expected
        """

tags = ["48999_location_2"]


class test(TestParent):                                                                                 # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.data_helper.get_front_office()
        self.atom.CRS.general.go_to_crs()
        # Navigate to Front Office and deactivate company
        self.lib.CRS.front_office.disable_company_account()
        # Navigate to Order Queue
        self.lib.CRS.front_office.go_to_order_queue()
        # click on "Add new Order" button
        self.lib.CRS.order_queue.add_new_order()
        # enter the account code to the Account# field
        self.lib.CRS.order_entry.fill_in_account_field(self.data.front_office.account_code, should_found=False)
        # Navigate to Front Office and activate company back
        self.lib.CRS.front_office.disable_company_account(disable=False)


if __name__ == '__main__':
    run_test(__file__)
