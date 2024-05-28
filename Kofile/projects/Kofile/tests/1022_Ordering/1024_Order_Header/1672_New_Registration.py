from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    - Go to CRS Order Queue and click on Add New Order button
    - Click on More Options in Order Header, fill New Registration fields
    - Click on New Registration and verify successful registration confirmation message
    - Type the new email and verify loaded user info
"""


class test(TestParent):                                                                    # noqa

    def __init__(self, data):
        data["OIT"] = "Copies"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.order_queue.add_new_order()
        new_email = self.lib.CRS.order_entry.new_registration()[1]
        customer_info_expected = self.lib.CRS.order_entry.get_order_header_customer_info()
        self.lib.CRS.order_header.fill_order_header_customer("email", new_email.lower())
        self.actions.wait(1)
        customer_info_actual = self.lib.CRS.order_entry.get_order_header_customer_info()
        self.logging.info(
            f"Expected info: {customer_info_expected}, Actual info: {customer_info_actual, customer_info_actual}")
        assert customer_info_actual == customer_info_expected, "Customer info mismatches registration data"


if __name__ == '__main__':
    run_test(__file__)
