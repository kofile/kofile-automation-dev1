from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                             # noqa
    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        return self.get("scanner_id")

    def __before__(self):
        self.run_dependencies(("scanner_id",))

    def __test__(self):
        self.set_content_type('application/json')
        self.response = self.session.post(self.get_url(self.api_urls.StopBatchScan), json=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.set("scanner_id", None)


if __name__ == '__main__':
    run_test(__file__, browser="none")
