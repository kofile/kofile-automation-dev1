from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                                   # noqa
    title = "<title>Indexing Entry</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        return {'indexingTaskId': self.get("portal_indexing_task_id")}

    def __before__(self):
        self.run_dependencies(("portal_order_item_saved_in_indexing",))

    def __test__(self):
        self.set_headers(self.api_test_data.indexing_headers)
        self.response = self.session.get(self.get_url(
            self.api_urls.ProcessIndexingTaskAndPickupTheNextOne), params=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]
        self.set("portal_order_indexed", True)


if __name__ == '__main__':
    run_test(__file__, browser="none")
