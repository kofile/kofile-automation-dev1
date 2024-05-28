"""Test-Reset Order Search"""
from datetime import date, timedelta
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Search orders in Order Search by yesterday's date, then reset search"""

tags = ['48999_location_2']


class test(TestParent):                                                                                     # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: Order Search screen is displayed, search criteria are reset
        """
        today = date.today().strftime(self.lib.general_helper.DATE_PATTERN)
        yesterday = (date.today() - timedelta(days=1)).strftime(self.lib.general_helper.DATE_PATTERN)
        self.data['from_date'] = yesterday
        self.data['to_date'] = yesterday

        # search orders in Order Search by date
        self.atom.CRS.general.go_to_crs()
        self.atom.CRS.order_search.search_orders_by_date_range()

        self.lib.CRS.order_search.click_reset_search()

        # verify that dates are reset
        self.lib.CRS.order_search.verify_from_date(today)
        self.lib.CRS.order_search.verify_to_date(today)

        # verify that search results are reset
        if self.data['result_rows']:
            result_rows = self.lib.CRS.order_search.get_result_table_all_rows()
            assert not result_rows, \
                "Search results have NOT been reset"
        # verify that "No match found" text is reset
        else:
            assert not self.lib.CRS.order_search.check_no_matches_found(), \
                "Search results have NOT been reset"


if __name__ == '__main__':
    run_test(__file__)
