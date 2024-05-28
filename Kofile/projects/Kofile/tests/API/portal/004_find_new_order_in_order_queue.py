from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test
import re

description = """
"""

tags = ['API']


class test(ApiTestParent):
    title = "<title>Order Queue</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __before__(self):
        self.run_dependencies(("portal_order_number",))

    def __test__(self):
        self.response = self.session.get(self.get_url(self.api_urls.ShowOrderQueue))
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]

        data = re.findall(
            r'{"OrderId":(\d+),"OrderHeader_PackageId":"Eforms-(\d+)","OrderHeader_OrderNumber":"%s",' % self.get(
                "portal_order_number"), self.response.text)
        assert data, f'Order with # {self.get("portal_order_number")} not found in order queue'
        self.set("portal_order_id", data[0][0])
        self.set("portal_package_id", data[0][1])


if __name__ == '__main__':
    run_test(__file__, browser="none")
