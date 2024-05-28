from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test
import re
import json

description = """
"""

tags = ['API']


class test(ApiTestParent):
    response = None
    title = "<title>Index Queue</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __before__(self):
        self.run_dependencies(("cs_re_index_order_number",))

    def __test__(self):
        number = self.get("cs_re_index_order_number")
        order_id, indexing_task_id, indexing_status_id, counter = None, None, None, 10
        while (not indexing_task_id) and counter:
            try:
                self.response = self.session.get(self.get_url(self.api_urls.ShowIndexQueue), timeout=300)
                assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
                if data := re.findall(r'(\{"Order_OrderId[^\{]+:"%s"[^\{]+\})' % number, self.response.text):
                    json_data = json.loads(data[0])
                    order_id = json_data["Order_OrderId"]
                    indexing_task_id = json_data["IndexingTaskId"]
                    indexing_status_id = json_data["IndexingTaskStatus"]
                    break
            except Exception as e:
                self.logging.warning(f"Request error: {type(e).__name__}")
            counter -= 1
        assert self.response, "Cant load indexing page"
        assert self.title in self.response.text[:200]
        assert indexing_task_id, f"Cant find indexing task id in indexing queue for order number {number}"
        assert order_id, f"Cant find order id in indexing queue for order number {number}"
        assert indexing_status_id, f"Cant find order item type id in indexing queue for order number {number}"
        self.set("cs_re_index_indexing_task_id", indexing_task_id)
        self.set("cs_re_index_order_id", order_id)
        self.set("cs_re_index_indexing_status_id", indexing_status_id)


if __name__ == '__main__':
    run_test(__file__, browser="none")
