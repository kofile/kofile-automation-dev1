"""KS QuickDoc Payment Options"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Check KS QuickDoc Payment Options"""

tags = ['48999_location_2']


class test(TestParent):                                                                                   # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        convenience_fee = float(self.data["config"].get_kiosk_search("convenience_fee")) if \
            self.data["config"].get_kiosk_search("convenience_fee") else 0.0
        self.atom.KS.general.login_to_KS()
        doc_number = self.api.clerc_search(self.data).search_document_with_price(exclude_in_workflow=True)
        self.lib.PS.ps_main_page.date_to_set(self.data.get("test_config").get("dept"))
        self.lib.KS.general.search_for_doc_by_doc_number(doc_number)
        row_num = self.lib.KS.general.get_first_row_num_with_add_to_cart()
        self.lib.KS.general.click_on_quick_doc_by_row_num(row_num)
        original_balance = self.lib.KS.general.get_available_balance()
        total_due_ca = self.lib.KS.general.get_total_due()
        self.lib.KS.general.quick_doc_ca_payment(total_due_ca, convenience_fee)
        self.lib.KS.general.new_search()
        self.lib.PS.ps_main_page.date_to_set(self.data.get("test_config").get("dept"))
        self.lib.KS.general.search_for_doc_by_doc_number(doc_number)
        self.lib.KS.general.click_on_quick_doc_by_row_num(row_num)
        expected_new_balance = original_balance - total_due_ca
        actual_new_balance = self.lib.KS.general.get_available_balance()
        assert actual_new_balance == expected_new_balance, f"CA actual Balance {actual_new_balance} is not \
                equal to expected {expected_new_balance}"
        self.lib.general_helper.find_and_click(self.pages.KS.home_page.btn_close_pup)
        self.lib.KS.general.click_on_quick_doc_by_row_num(row_num)
        order_number, total_due_pc = self.lib.KS.general.quick_doc_pay_at_counter()
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.order_queue.find_order_in_order_queue(order_number)


if __name__ == '__main__':
    run_test(__file__)
