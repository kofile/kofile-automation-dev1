from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test
import re

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                               # noqa
    response = None
    title = "<title>Verification Queue</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __before__(self):
        self.run_dependencies(("order_indexed",))

    def __test__(self):
        self.set_headers(self.api_test_data.indexing_headers)
        order_id = self.get("order_id")
        verification_task_id, counter = None, 10
        while (not verification_task_id) and counter:
            try:
                self.response = self.session.get(self.get_url(self.api_urls.ShowVerificationQueue), timeout=300)
                assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
                verification_task_id = re.findall('"Order_OrderId":{},"VerificationTaskId":(.*?),"'.format(
                    order_id), self.response.text)
            except Exception as e:
                print("Request error", type(e).__name__)
            counter -= 1
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]
        assert verification_task_id, f"Cant found verification task id in verification queue for order id {order_id}"
        self.set("verification_task_id", verification_task_id[0])


if __name__ == '__main__':
    run_test(__file__, browser="none")
