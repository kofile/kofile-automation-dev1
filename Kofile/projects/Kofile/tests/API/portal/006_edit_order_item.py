from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):
    title = "<title>Edit Order Item</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __before__(self):
        self.run_dependencies(("portal_order_item_id", "portal_order_item_type_id", "portal_order_id"))

    def __test__(self):
        params = {
            'orderId': self.get("portal_order_id"),
            'orderItemId': self.get("portal_order_item_id"),
            'orderTypeId': self.get("portal_order_item_type_id"),
        }
        self.response = self.session.get(self.get_url(self.api_urls.EditOrderItem), params=params)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]


if __name__ == '__main__':
    run_test(__file__, browser="none")
