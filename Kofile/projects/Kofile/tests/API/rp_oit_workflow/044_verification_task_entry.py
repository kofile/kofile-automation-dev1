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
        return (
            ('orderId', self.get("order_id")),
            ('orderItemId', self.get("second_oit_id")),
            ('orderTypeId', '1'),
            ('verificationTaskId', self.get("verification_task_id")),
        )

    def __before__(self):
        self.run_dependencies(("verification_task_id",))

    def __test__(self):
        self.set_headers(self.api_test_data.indexing_headers)
        self.response = self.session.get(self.get_url(self.api_urls.VerificationTaskEntry), params=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]


if __name__ == '__main__':
    run_test(__file__, browser="none")
