from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):
    title = "<title>Order Finalization</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __before__(self):
        self.run_dependencies(("copy_order_price", "copy_order_item_id", "copy_order_item_type_id",
                               "copy_order_id", "copy_package_id", "cs_copy_order_number"))

    @property
    def post_data(self):
        data = self.api_test_data.portal_checkout_data.copy()
        data.append(('Order.OrderId', self.get("copy_order_id")))
        data.append(('orderId', self.get("copy_order_id")))
        data.append(('receivedByMailList',
                     '{"orderId":%s,"orderItems":[{"orderItemId":%s,"orderItemTypeId":%s,"orderItemTypeDesc":"Assumed Name eForm","orderItemSequence":1}]}' % (
                         self.get("copy_order_id"), self.get("copy_order_item_id"),
                         self.get("copy_order_item_type_id"))))
        data.append(('Order.OrderHeader.PackageId', self.get("copy_package_id")))
        data.append(('Order.OrderHeader.OrderNumber', self.get("cs_copy_order_number")))
        data.append(('OrderPayment[0].Amount', self.get("copy_order_price")))
        return data

    def __test__(self):
        self.set_content_type()
        self.response = self.session.post(self.get_url(self.api_urls.PostAction), data=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200], self.response.text[:200]
        self.call_module(self.data_mapping.get("search_by_order_number"),
                         order_number=self.get("cs_copy_order_number"), status="Archive")


if __name__ == '__main__':
    run_test(__file__, browser="none")
