"""Test-Date Range Validation"""
from datetime import timedelta, datetime
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test
import pytz

description = """Check default values and validation messages for date range in Order Search"""

tags = ['48999_location_2']


class test(TestParent):                                                                                   # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: Order Search is performed by date range, search results displayed
        """
        # go to Order Search (atom tests)
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.crs.go_to_order_search()

        # verify default values for date fields
        utc_now = pytz.utc.localize(datetime.utcnow())
        now = utc_now.astimezone(pytz.timezone(self.lib.general_helper.TIMEZONE)).date()

        today = now.strftime(self.lib.general_helper.DATE_PATTERN)
        self.lib.CRS.order_search.verify_from_date(today)
        self.lib.CRS.order_search.verify_to_date(today)

        # verify max date range 90 days message
        from_date = (now - timedelta(days=91)).strftime(self.lib.general_helper.DATE_PATTERN)
        self.lib.CRS.order_search.fill_date_and_search(from_date, today)
        self.lib.CRS.order_search.verify_date_range_validation_text("Maximum date range is 90 days")

        # verify invalid date range message on from_date > to_date
        from_date = (now + timedelta(days=1)).strftime(self.lib.general_helper.DATE_PATTERN)
        self.lib.CRS.order_search.fill_date_and_search(from_date, today)
        self.lib.CRS.order_search.verify_date_range_validation_text("Please type valid date range date")


if __name__ == '__main__':
    run_test(__file__)
