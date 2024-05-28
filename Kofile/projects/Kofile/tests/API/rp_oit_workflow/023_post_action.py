from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                         # noqa
    title = "<title>Order Finalization</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        now = self.datetime.now()
        data = self.api_test_data.post_action_data.copy()
        data.append(('Order.OrderHeader.OrderUser.PersonalUserId', self.get("user_id")))
        data.append(('Order.OrderHeader.OrderNumber', self.get("order_number")))
        data.append(('Order.OrderHeader.OrderUser.User.Email', self.data.env.email_user))
        data.append(('Order.OrderHeader.OrderUser.User.Address.AddressId', self.get("address_id")))
        data.append(('Order.OrderHeader.OrderUser.User.Address.Email', self.data.env.email_user))
        data.append(('receiveDateInput', now.strftime("%m/%d/%Y")))
        data.append(('receiveTimeInput', now.strftime('%H:%M %p')))
        data.append(('Order.OrderId', self.get("order_id")))
        data.append(('orderId', self.get("order_id")))
        inner_data = [
            '{"orderItemId":%s,"orderItemTypeId":1,"orderItemTypeDesc":"Real Property Recordings","orderItemSequence":%s}' % (
                self.get("second_oit_id"), 1)]
        data.append(('receivedByMailList',
                     '{"orderId":%s,"orderItems":[%s]}' % (self.get("order_id"), ",".join(inner_data))))
        data.append(('OrderPayment[0].Amount', self.get("price")))
        return data

    def __before__(self):
        self.run_dependencies(
            ("user_id", "order_number", "address_id", "order_id", "second_oit_id", "delete_oit", "price"))

    def __test__(self):
        self.response = self.session.post(self.get_url(self.api_urls.PostAction), data=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]
        self.set("finalize_order", True)


if __name__ == '__main__':
    run_test(__file__, browser="none", env="qa_dev")
