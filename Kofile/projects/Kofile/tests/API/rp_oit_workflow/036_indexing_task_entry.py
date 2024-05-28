from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test
from bs4 import BeautifulSoup

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                            # noqa
    title = "<title>Indexing Entry</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        return (
            ('orderId', self.get("order_id")),
            ('orderItemId', self.get("second_oit_id")),
            ('orderItemTypeId', '1'),
            ('orderTypeId', '1'),
            ('indexingTaskId', self.get("indexing_task_id")),
        )

    def __before__(self):
        self.run_dependencies(("indexing_task_id",))

    def __test__(self):
        self.response = self.session.get(self.get_url(self.api_urls.IndexingTaskEntry), params=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]
        soup = BeautifulSoup(self.response.text, "lxml")
        dm_id = soup.find("input", id="dmId").get("value")
        assert dm_id
        self.set("dm_id", dm_id)


if __name__ == '__main__':
    run_test(__file__, browser="none")
