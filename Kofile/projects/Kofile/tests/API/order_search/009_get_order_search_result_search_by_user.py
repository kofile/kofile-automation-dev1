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
        username = f'{self.data["env"]["user_first"][0]} {self.data["env"]["user_last"][0]}'
        value = self.get('assigned_to').get(username)
        assert value, f"Cant find {username} in:\n{self.get('assigned_to')}"
        data["AssignedTo"] = value
        return data

    def __before__(self):
        self.run_dependencies(("last_row_data", "assigned_to"))

    def __test__(self):
        self.set_content_type('application/x-www-form-urlencoded')
        self.response = self.session.post(self.get_url(self.api_urls.GetOrderSearchResult), data=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]

        self.api_lib.crs.get_search_result_content_by_index(self.response.content, None)


if __name__ == '__main__':
    run_test(__file__, browser="none")
