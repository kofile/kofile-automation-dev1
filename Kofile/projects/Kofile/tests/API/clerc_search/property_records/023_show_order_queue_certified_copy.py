from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test
import re
import json

description = """
"""

tags = ['API']


class test(ApiTestParent):  # noqa
    title = "<title>Order Queue</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __before__(self):
        self.run_dependencies(("cs_certified_copy_order_number",))

    def __test__(self):
        self.response = self.session.get(self.get_url(self.api_urls.ShowOrderQueue))
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]

        number = self.get("cs_certified_copy_order_number")
        data = re.findall(r'(\{"OrderId[^\{]+:"%s"[^\{]+\})' % number, self.response.text)
        assert data, f"Cant find order {number} in capture queue"
        json_data = json.loads(data[0])
        self.set("certified_copy_order_id", json_data["OrderId"])
        self.set("certified_copy_order_status_id", json_data["OrderStatusId"])
        self.set("certified_copy_package_id", json_data["OrderHeader_PackageId"])


if __name__ == '__main__':
    run_test(__file__, browser="none")
