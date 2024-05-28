"""Test-Search by Date Range"""
from datetime import datetime, date, timedelta
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Perform search by date range in Order Search and check the date range of results"""

tags = ['48999_location_2']


class test(TestParent):                                                                                    # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: Order Search is performed by date range, search results displayed
        """
        # yesterday
        self.data['from_date'] = (date.today() - timedelta(1)).strftime(self.lib.general_helper.DATE_PATTERN)
        # today
        self.data['to_date'] = date.today().strftime(self.lib.general_helper.DATE_PATTERN)

        # search order in Order Search by date range (atom tests)
        self.atom.CRS.general.go_to_crs()
        self.atom.CRS.order_search.search_orders_by_date_range()

        # convert date strings to date objects for results date comparison
        from_date = datetime.strptime(self.data['from_date'], self.lib.general_helper.DATE_PATTERN).date()
        to_date = datetime.strptime(self.data['to_date'], self.lib.general_helper.DATE_PATTERN).date()

        # if results are found, iterate over result rows and verify that Ordered On matches the entered dates
        assert self.data['result_rows'], "Could not search for results"
        result_rows = self.data['result_rows'][:50]  # take the first 50 rows
        for row_index, row in enumerate(result_rows, 1):  # row is necessary in for each syntax, not used later
            order_number = self.lib.CRS.order_search.get_order_number_by_row_index(row_index)
            ordered_on_date = self.lib.CRS.order_search.get_ordered_on_date_by_order_number(order_number)
            assert from_date <= ordered_on_date <= to_date, \
                f"Incorrect results are displayed at row {row_index}"
        self.actions.step(f"Results match the given date range: '{self.data['from_date']} - {self.data['to_date']}'")


if __name__ == '__main__':
    run_test(__file__)
