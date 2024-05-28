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
        data = self.api_test_data.package_search_data.copy()
        now = self.datetime.now()
        data["FromDate"] = (now - timedelta(days=30)).strftime("%m/%d/%Y")
        data["ToDate"] = now.strftime("%m/%d/%Y")
        return data

    def __test__(self):
        self.set_content_type('application/x-www-form-urlencoded')
        self.response = self.session.post(self.get_url(self.api_urls.GetPackageSearchResult), data=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]

        self.api_lib.crs.get_package_search_result_content_by_index(self.response.content, 0)


if __name__ == '__main__':
    run_test(__file__, browser="none")
