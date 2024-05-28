from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                             # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def schema(self):
        return {
            "type": "object",
            "properties": {
                "IsLoggedIn": {"type": "boolean"},
                "ItemsCount": {"type": "object",
                               "properties": {
                                   "Ordering": {"type": "string"},
                                   "Capturing": {"type": "string"},
                                   "Indexing": {"type": "string"},
                                   "Verification": {"type": "string"},
                               },
                               },
            },
        }

    def __test__(self):
        self.response = self.session.get(self.get_url(self.api_urls.GetQueuesItemCounts))
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"

        self.validate(instance=self.response.json(), schema=self.schema)


if __name__ == '__main__':
    run_test(__file__, browser="none")
