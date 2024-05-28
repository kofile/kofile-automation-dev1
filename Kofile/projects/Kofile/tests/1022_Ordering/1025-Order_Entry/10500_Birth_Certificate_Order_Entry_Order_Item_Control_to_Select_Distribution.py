from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """

"""

tags = ["48999_location_2"]


class test(TestParent):

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.order_queue.create_and_action_with_order(None, summary=self.fill_data)
        self.actions.click(self.pages.CRS.order_entry.birth_verification_letter)
        self.actions.wait_for_element_not_present(self.pages.CRS.order_entry.county_cert_distribution)
        self.actions.wait_for_element_not_present(self.pages.CRS.order_entry.state_cert_distribution)
        self.actions.click(self.pages.CRS.order_entry.birth_certificate)
        self.actions.wait_for_element_present(self.pages.CRS.order_entry.county_cert_distribution)
        self.actions.wait_for_element_present(self.pages.CRS.order_entry.state_cert_distribution)
        self.actions.assert_element_checked(self.pages.CRS.order_entry.county_cert_distribution)
        self.actions.wait_for_element_enabled(self.pages.CRS.order_finalization.btn_save_order)
        self.lib.general_helper.scroll_and_click(self.pages.CRS.order_finalization.btn_save_order)
        self.set_serial_number()
        self.actions.wait_for_element_enabled(self.pages.CRS.order_summary.btn_checkout)
        self.atom.CRS.add_payment.finalize_order()

    def fill_data(self):
        self.actions.assert_element_not_checked(self.pages.CRS.order_entry.county_cert_distribution)
        self.actions.assert_element_not_checked(self.pages.CRS.order_entry.state_cert_distribution)
        self.actions.assert_element_not_enabled(self.pages.CRS.order_finalization.btn_save_order)
        self.actions.click(self.pages.CRS.order_entry.county_cert_distribution)
        self.actions.wait_for_element_enabled(self.pages.CRS.order_finalization.btn_save_order)

    def set_serial_number(self):
        self.actions.wait_for_element_present(self.pages.CRS.order_entry.serial_number_btn)
        self.lib.general_helper.find(self.pages.CRS.order_entry.serial_number_btn).click()
        self.actions.wait_for_element_present(self.pages.CRS.order_summary.txt_start_serial_number)
        counter = 0
        while "disablelinks" in self.lib.general_helper.find(self.pages.CRS.order_summary.btn_serial_number_submit,
                                                             get_attribute="class") and counter < 20:
            num = self.random.randint(1, 99999999)
            self.lib.general_helper.find_and_send_keys(self.pages.CRS.order_summary.txt_start_serial_number,
                                                       "" + self.keys.TAB)
            self.lib.general_helper.find_and_send_keys(self.pages.CRS.order_summary.txt_end_serial_number,
                                                       "" + self.keys.TAB)
            self.lib.general_helper.find_and_send_keys(self.pages.CRS.order_summary.txt_start_serial_number, f"{num}" + self.keys.TAB)
            self.actions.wait(3)
            self.lib.general_helper.find_and_send_keys(self.pages.CRS.order_summary.txt_end_serial_number, f"{num}" + self.keys.TAB)
            self.actions.wait(3)
            counter += 1
        self.actions.click(self.pages.CRS.order_summary.btn_serial_number_submit)


if __name__ == '__main__':
    run_test(__file__)
