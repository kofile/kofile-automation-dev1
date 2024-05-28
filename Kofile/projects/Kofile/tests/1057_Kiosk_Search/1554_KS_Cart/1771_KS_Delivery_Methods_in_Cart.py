"""KS Delivery Methods in Cart"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Verify Delivery Methods in KS Cart"""

tags = ['48999_location_2']


class test(TestParent):                                                                                    # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.KS.general.login_to_KS()
        doc_number = self.api.clerc_search(self.data).search_document_with_price(exclude_in_workflow=True)
        self.lib.PS.ps_main_page.date_to_set(self.data.get("test_config").get("dept"))
        self.lib.KS.general.search_for_doc_by_doc_number(doc_number)
        row_num = self.lib.KS.general.get_first_row_num_with_add_to_cart()
        self.lib.KS.general.add_doc_to_cart_by_row_num(row_num)
        self.lib.KS.general.go_to_cart()
        self.lib.KS.general.verify_delivery_method_by_text(self.names.KS_Cart_options["option_1"])


if __name__ == '__main__':
    run_test(__file__)
