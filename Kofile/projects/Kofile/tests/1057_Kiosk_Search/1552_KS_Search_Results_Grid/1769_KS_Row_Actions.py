"""KS row actions"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Verify row icons in KS"""

tags = ['48999_location_2']


class test(TestParent):                                                                                 # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.KS.general.login_to_KS()
        self.lib.PS.ps_main_page.date_to_set(self.data.get("test_config").get("dept"))
        self.lib.KS.general.click_on_search_button()
        row = self.lib.KS.general.get_first_row_num_with_add_to_cart()
        self.lib.KS.general.verify_row_icons_by_row_num(row)


if __name__ == '__main__':
    run_test(__file__)
