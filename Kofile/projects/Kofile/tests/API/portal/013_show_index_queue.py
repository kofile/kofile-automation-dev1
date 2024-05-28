from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test
import re

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                               # noqa
    response = None
    title = "<title>Index Queue</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __before__(self):
        self.run_dependencies(("portal_scan_complete",))

    def __test__(self):
        order_id = self.get("portal_order_id")
        indexing_task_id, counter = None, 10
        while (not indexing_task_id) and counter:
            try:
                self.response = self.session.get(self.get_url(self.api_urls.ShowIndexQueue), timeout=300)
                assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
                indexing_task_id = re.findall('"Order_OrderId":{},"IndexingTaskId":(.*?),'.format(order_id), self.response.text)
            except Exception as e:
                print("Request error", type(e).__name__)
            counter -= 1
        assert self.response
        assert self.title in self.response.text[:200]
        assert indexing_task_id, f"Cant found indexing task id in indexing queue for order id {order_id}"
        self.set("portal_indexing_task_id", indexing_task_id[0])


if __name__ == '__main__':
    run_test(__file__, browser="none")
