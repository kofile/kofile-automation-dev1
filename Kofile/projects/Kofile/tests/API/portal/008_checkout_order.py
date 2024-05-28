from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test
import re

description = """
"""

tags = ['API']


class test(ApiTestParent):
    title = "<title>Order Finalization</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __before__(self):
        self.run_dependencies(("portal_order_price", "portal_order_item_id", "portal_order_item_type_id",
                               "portal_order_id", "portal_package_id", "portal_order_number"))

    @property
    def post_data(self):
        data = self.api_test_data.portal_checkout_data.copy()
        data.append(('Order.OrderId', self.get("portal_order_id")))
        data.append(('orderId', self.get("portal_order_id")))
        data.append(('receivedByMailList',
                     '{"orderId":%s,"orderItems":[{"orderItemId":%s,"orderItemTypeId":%s,"orderItemTypeDesc":"Assumed Name eForm","orderItemSequence":1}]}' % (
                         self.get("portal_order_id"), self.get("portal_order_item_id"),
                         self.get("portal_order_item_type_id"))))
        data.append(('Order.OrderHeader.PackageId', self.get("portal_package_id")))
        data.append(('Order.OrderHeader.OrderNumber', self.get("portal_order_number")))
        data.append(('OrderPayment[0].Amount', self.get("portal_order_price")))
        return data

    def __test__(self):
        self.response = self.session.post(self.get_url(self.api_urls.PostAction), data=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]

        doc_number = re.findall(',"InstrumentNumber":"(.*?)",', self.response.text)
        assert doc_number, "Doc number not found on the page"
        self.set("portal_doc_number", doc_number[0])


if __name__ == '__main__':
    run_test(__file__, browser="none")
