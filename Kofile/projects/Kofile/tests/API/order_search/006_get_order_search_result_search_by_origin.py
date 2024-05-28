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
        value = self.get('origin_ids').get(self.get("last_row_data")["origin"])
        assert value, f"Cant find {self.get('last_row_data')['origin']} in:\n{self.get('origin_ids')}"
        data["OriginId"] = value
        return data

    def __before__(self):
        self.run_dependencies(("last_row_data", "origin_ids"))

    def __test__(self):
        self.set_content_type('application/x-www-form-urlencoded')
        self.response = self.session.post(self.get_url(self.api_urls.GetOrderSearchResult), data=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]

        row_data = None
        last_row_data = self.get("last_row_data")
        for row in self.api_lib.crs.get_search_result_content_by_index(self.response.content, None):
            if row.get("order_id") == last_row_data.get("order_id"):
                row_data = row
                break
        assert row_data, f'Cant find order with id {last_row_data["order_id"]} and order number ' \
                         f'{last_row_data["order_number"]} in result by origin {last_row_data["origin"]}'
        assert last_row_data == row_data, f"Expected result on first row:\n {last_row_data}\n" \
                                          f"Actual result:\n {row_data}"


if __name__ == '__main__':
    run_test(__file__, browser="none")
