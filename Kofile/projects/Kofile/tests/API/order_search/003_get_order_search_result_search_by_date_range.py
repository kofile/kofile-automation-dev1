from datetime import timedelta

from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):  # noqa
    title = "<title>Order Queue</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        data = self.api_test_data.order_search_data.copy()
        now = self.datetime.now()
        data["FromDate"] = (now - timedelta(days=30)).strftime("%m/%d/%Y")
        data["ToDate"] = now.strftime("%m/%d/%Y")
        return data

    def __test__(self):
        self.set_content_type('application/x-www-form-urlencoded')
        self.response = self.session.post(self.get_url(self.api_urls.GetOrderSearchResult), data=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]

        row_data = self.api_lib.crs.get_search_result_content_by_index(self.response.content, -1)
        self.set("last_row_data", row_data)

        self.set("location_ids", self.api_lib.crs.get_drop_down_values(self.response.content, "LocationId"))
        self.set("department_ids", self.api_lib.crs.get_drop_down_values(self.response.content, "DepartmentId"))
        self.set("origin_ids", self.api_lib.crs.get_drop_down_values(self.response.content, "OriginId"))
        self.set("assigned_to", self.api_lib.crs.get_drop_down_values(self.response.content, "AssignedTo"))
        self.set("order_payment_type_ids",
                 self.api_lib.crs.get_drop_down_values(self.response.content, "OrderPaymentTypeId"))


if __name__ == '__main__':
    run_test(__file__, browser="none")
