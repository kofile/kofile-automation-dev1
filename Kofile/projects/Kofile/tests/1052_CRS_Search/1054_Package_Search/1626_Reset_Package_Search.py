"""Test-Reset Package Search"""
from datetime import date, timedelta
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Search packages in Package Search by yesterday's date, then reset search"""

tags = ['48999_location_2']


class test(TestParent):                                                                                # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: Package Search screen is displayed, search criteria are reset
        """
        # initialize dates for search
        today = date.today().strftime(self.lib.general_helper.DATE_PATTERN)
        yesterday = (date.today() - timedelta(days=1)).strftime(self.lib.general_helper.DATE_PATTERN)
        self.data['from_date'] = yesterday
        self.data['to_date'] = yesterday

        # search packages in Package Search by date range (atom tests)
        self.atom.CRS.general.go_to_crs()
        self.atom.CRS.package_search.search_packages_by_date_range()

        # reset search
        self.lib.CRS.package_search.click_reset_search()

        # verify that dates are reset
        self.lib.CRS.package_search.verify_from_date(today)
        self.lib.CRS.package_search.verify_to_date(today)

        # verify that search results are reset
        if self.data['result_rows']:
            result_rows = self.lib.CRS.package_search.get_result_table_all_rows()
            assert not result_rows, "Search results have NOT been reset"
        # verify that "No match found" text is reset
        else:
            assert "No match found" not in self.actions.get_browser().page_source, "Search results have NOT been reset"


if __name__ == '__main__':
    run_test(__file__)
