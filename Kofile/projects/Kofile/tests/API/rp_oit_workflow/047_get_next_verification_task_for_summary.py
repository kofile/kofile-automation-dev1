from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                               # noqa
    title = "<title>Verification Entry</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        return ('VerificationTaskId', self.get("verification_task_id")), ('DepartmentId', '1'),

    def __before__(self):
        self.run_dependencies(("order_item_saved_in_verification",))

    def __test__(self):
        self.set_headers(self.api_test_data.indexing_headers)
        self.response = self.session.get(self.get_url(
            self.api_urls.GetNextVerificationTaskForSummary), params=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]


if __name__ == '__main__':
    run_test(__file__, browser="none")
