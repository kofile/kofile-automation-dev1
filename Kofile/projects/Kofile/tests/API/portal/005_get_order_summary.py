from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test
import re

description = """
"""

tags = ['API']


class test(ApiTestParent):
    title = "<title>Order Summary</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __before__(self):
        self.run_dependencies(("portal_order_id",))

    def __test__(self):
        params = {
            'orderId': self.get("portal_order_id"),
            'orderStatus': '1',
        }
        self.response = self.session.get(self.get_url(self.api_urls.OrderSummary), params=params)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]

        portal_order_item_id = re.findall(r'"OrderItemId":(\d{2,}),', self.response.text)
        assert portal_order_item_id, f"Cant find OrderItemId for order with id {self.get('portal_order_id')}"
        self.set("portal_order_item_id", portal_order_item_id[0])

        portal_order_item_type_id = re.findall(r'"OrderItemType_Id":(\d+),', self.response.text)
        assert portal_order_item_type_id, f"Cant find OrderItemType_Id for order with id {self.get('portal_order_id')}"
        self.set("portal_order_item_type_id", portal_order_item_type_id[0])


if __name__ == '__main__':
    run_test(__file__, browser="none")
