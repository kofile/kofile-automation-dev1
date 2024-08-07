from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS -> Front Office, search company account and enable 'Allow Company Account with Ordering', 
    back to CRS, create new order and search company account ->
    Select Company Account
        """

tags = ["48999_location_2"]


class test(TestParent):                                                                               # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.data_helper.get_front_office()
        self.atom.CRS.general.go_to_crs()
        # Navigate to Front Office and check 'Allow Company Account with Ordering' option
        self.lib.CRS.front_office.choose_allow_ordering_option()
        self.lib.CRS.order_queue.add_new_order()
        # Register new users
        code, user1 = self.lib.CRS.order_entry.new_registration()
        code2, user2 = self.lib.CRS.order_entry.new_registration()
        # Create new account with 2 users
        self.lib.CRS.front_office.create_new_account(unique_number=code, emails=[user1, user2])
        # Navigate to Order Queue
        self.lib.CRS.front_office.go_to_order_queue()
        # click on "Add new Order" button
        self.lib.CRS.order_queue.add_new_order()
        # enter the account code to the Account# field
        self.lib.CRS.order_entry.fill_in_account_field(
            account_code=code, should_found=[f"{code} - {user1}", f"{code} - {user2}"], select=user1)


if __name__ == '__main__':
    run_test(__file__)
