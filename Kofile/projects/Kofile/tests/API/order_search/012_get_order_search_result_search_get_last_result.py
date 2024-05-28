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
        data["OrderNumber"] = self.get("last_row_data")["order_number"]
        return data

    def __before__(self):
        self.run_dependencies(("last_row_data",))

    def __test__(self):
        self.set_content_type('application/x-www-form-urlencoded')
        self.response = self.session.post(self.get_url(self.api_urls.GetOrderSearchResult), data=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]
        row_data = self.api_lib.crs.get_search_result_content_by_index(self.response.content, None)

        self.response = self.session.get(self.get_url(self.api_urls.GetLatestOrderSearchResult))
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]
        second_row_data = self.api_lib.crs.get_search_result_content_by_index(self.response.content, None)
        assert row_data == second_row_data, f"GetLatestOrderSearchResult not equal result from first request\n" \
                                            f"{row_data}\n{second_row_data}"


if __name__ == '__main__':
    run_test(__file__, browser="none")
