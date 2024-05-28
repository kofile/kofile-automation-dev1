from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                                # noqa
    title = "<title>Company Accounts</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.response = self.session.get(self.get_url(self.api_urls.CompanyAccounts))
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]


if __name__ == '__main__':
    run_test(__file__, browser="none")
