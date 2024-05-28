from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Navigate to CRS ->
    Navigate to Front Office ->
    Open existing company account for edit ->
    Check "Allow Company Account with Public Search" checkbox ->
    Add company account user (email) and check "Enabled" and "Administrator" checkboxes ->
    Click on the "Save" button ->
    Navigate to PS ->
    Sign In with the same email user (from step 5) ->
    Check account balance: click on the user name and then click on the "Manage Account" link ->
    Search a document with fee and add to Cart ->
    Navigate to Cart ->
    Select Delivery Method with NOT NULL price e.g. Certified Copy ->
    Fill Delivery Address Details fields and save changes ->
    Click on the "Company Account Checkout" button
        """

tags = []


class test(TestParent):                                                                           # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.data_helper.get_front_office()
        password_data = self.lib.data_helper.get_ps_password()
        self.atom.CRS.general.go_to_crs()
        # Navigate to Front Office and check 'Allow Company Account with Ordering' option
        self.lib.CRS.front_office.choose_allow_ordering_option()
        self.lib.CRS.order_queue.add_new_order()
        # Register new users
        code, user1 = self.lib.CRS.order_entry.new_registration()
        # Create new account with 1 user
        self.lib.CRS.front_office.create_new_account(unique_number=code, emails=[user1], allow_public_search=True,
                                                     credit_limit="500")
        # Go to Public Search
        self.atom.CS.general.go_to_cs(clerk=False, oit="Marriage_License", public_search=True)
        # auth
        password_hash, password_hash_salt = password_data.get("password_hash"), password_data.get("password_hash_salt")
        password = password_data.get("password")
        with self.lib.db as db:
            db.confirm_user_by_email(user1, password_hash, password_hash_salt)
        self.lib.PS.general.auth(user1, password)

        # search and purchase document
        self.api.clerc_search(self.data).search_document_with_price()
        self.lib.PS.general.go_to_marriage_license_tab()
        self.lib.PS.general.search_document_by_number()
        self.lib.PS.general.purchase_first_document()

        # check account balance
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.order_queue.add_new_order()
        self.lib.CRS.order_header.fill_order_header_customer("account", code)
        self.lib.CRS.order_header.check_account_balance(format(-self.data.doc_price, '.2f'))


if __name__ == '__main__':
    run_test(__file__)
