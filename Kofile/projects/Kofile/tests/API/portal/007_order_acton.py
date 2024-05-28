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
        self.run_dependencies(("portal_order_item_id", "portal_order_item_type_id", "portal_order_id",
                               "portal_package_id", "portal_order_number"))

    @property
    def post_data(self):
        data = self.api_test_data.portal_edit_order_data.copy()
        data.append(('Order.OrderId', self.get("portal_order_id")))
        data.append(('Order.OrderItems[0].OrderItemId', self.get("portal_order_item_id")))
        data.append(('Order.OrderItems[0].OrderItemType.Id', self.get("portal_order_item_type_id")))
        data.append(('Order.OrderHeader.PackageId', self.get("portal_package_id")))
        data.append(('Order.OrderHeader.OrderNumber', self.get("portal_order_number")))
        return data

    def __test__(self):
        self.response = self.session.post(self.get_url(self.api_urls.OrderActions), data=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]

        portal_order_price = re.findall(r'"Price":(\d+.\d+).', self.response.text)
        assert portal_order_price, f"Cant find price for order {self.get('portal_order_number')}"
        self.set("portal_order_price", portal_order_price[0])




if __name__ == '__main__':
    run_test(__file__, browser="none")
