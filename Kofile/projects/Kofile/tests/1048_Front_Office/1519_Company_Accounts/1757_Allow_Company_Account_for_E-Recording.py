from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Open CRS ->
    Navigate to Front Office ->
    Search existing Company Account ->
    Click on the "Edit" (pencil) button ->
    Click on the "Allow Company Account for E-Recording" checkbox ->
    Click on the "Save" button ->
    Run erProxy submitter (name folder with the package in Payloads should be in the following format:
    ACCT_CODE-erSUBMITTER_PASSWORD e.g. 'Account-Account' ->
    Navigate to CRS ->
    Open submitted erProxy ->
    Verify "Account#" field -> "Account#" field is filled with correct Company Account
        """

tags = ["48999_location_2"]


class test(TestParent):                                                                           # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.data_helper.get_front_office()
        er_schema = self.lib.data_helper.get_er_schema()
        self.atom.CRS.general.go_to_crs()
        # Navigate to Front Office and check 'Allow Company Account with Ordering' option
        self.lib.CRS.front_office.choose_allow_ordering_option()
        self.lib.CRS.order_queue.add_new_order()
        # Register new users
        code, user1 = self.lib.CRS.order_entry.new_registration()
        # Create new account with 2 users
        self.lib.CRS.front_office.create_new_account(unique_number=code, emails=[user1], allow_public_search=True,
                                                     credit_limit="500")
        # submit erProxy and get created erProxy order number
        with self.lib.db as db:
            db.set_account_password(code)
            db.set_er_schema(code, er_schema.get("CONFIG_ID"), er_schema.get("ER_SCHEMA_NAME"))
        er_proxy_order_number = self.atom.ERProxy.general.create_er_proxy(account_name=code, account_password=code)[0]

        # assign order
        self.data["order_number"] = er_proxy_order_number[0]
        self.lib.CRS.crs.go_to_order_queue()
        self.atom.CRS.order_queue.assign_order()
        self.lib.general_helper.wait_for_spinner()

        # edit order
        self.data["current_oit"] = self.data.OIT
        self.lib.CRS.crs.click_running_man()
        self.actions.wait_for_element_displayed(self.pages.CRS.order_summary.lbl_order_number)

        self.actions.verify_element_value(self.pages.CRS.order_header.txt_accountname, f"{code} - {user1}")


if __name__ == '__main__':
    run_test(__file__)
