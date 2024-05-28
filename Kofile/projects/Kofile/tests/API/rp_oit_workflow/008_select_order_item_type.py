from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                               # noqa
    title = "<title>New Order</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        data = self.api_test_data.select_order_item_type_data.copy()
        data.append(('Order.OrderHeader.OrderUser.PersonalUserId', self.get("user_id")))
        data.append(('Order.OrderHeader.OrderUser.User.Email', self.data.env.email_user))
        data.append(('Order.OrderHeader.OrderUser.User.Address.AddressId', self.get("address_id")))
        data.append(('Order.OrderHeader.OrderUser.User.Address.Email', self.data.env.email_user))
        return data

    def __before__(self):
        self.run_dependencies(("user_id", "address_id"))

    def __test__(self):
        self.response = self.session.post(self.get_url(self.api_urls.SelectOrderItemType), data=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]


if __name__ == '__main__':
    run_test(__file__, browser="none")
