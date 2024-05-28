from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test
from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlparse

description = """
"""

tags = ['API']


class test(ApiTestParent):  #
    title = "<title>Indexing Entry</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        return {
            'indexingTaskId': self.get("cs_re_index_indexing_task_id"),
            'indexingStatusId': self.get("cs_re_index_indexing_status_id"),
        }

    def __before__(self):
        self.run_dependencies(("cs_re_index_indexing_task_id", "cs_re_index_indexing_status_id"))

    def __test__(self):
        self.response = self.session.get(self.get_url(self.api_urls.GetIndexingTask), params=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]
        soup = BeautifulSoup(self.response.text, "lxml")
        dm_id = soup.find("input", id="dmId").get("value")
        assert dm_id, 'Cant find dmId on the page'
        self.set("re_index_order_dm_id", dm_id)

        doc_type_id = soup.find("input", id="docTypeId").get("value")
        assert doc_type_id, 'Cant find docTypeId on the page'
        self.set("re_index_order_doc_type_id", doc_type_id)

        captured_value = parse_qs(urlparse(self.response.url).query)
        self.set("re_index_order_item_id", captured_value["orderItemId"][0])
        self.set("re_index_order_item_type_id", captured_value["orderItemTypeId"][0])
        self.set("re_index_order_type_id", captured_value["orderTypeId"][0])


if __name__ == '__main__':
    run_test(__file__, browser="none")
