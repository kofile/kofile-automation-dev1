import re
from urllib.parse import urlparse, parse_qs

from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                           # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        data = self.api_test_data.order_actions_data.copy()
        data.append(('Order.OrderHeader.OrderUser.User.Email', self.data.env.email_user))
        data.append(('Order.OrderHeader.OrderUser.PersonalUserId', self.get("user_id")))
        data.append(('Order.OrderHeader.OrderUser.User.Address.AddressId', self.get("address_id")))
        data.append(('Order.OrderHeader.OrderUser.User.Address.Email', self.data.env.email_user))
        return data

    def __before__(self):
        self.run_dependencies(("user_id", "address_id"))

    def __test__(self):
        self.response = self.session.post(self.get_url(self.api_urls.OrderActions), data=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert " <title>Order Summary</title>" in self.response.text
        order_id = parse_qs(urlparse(self.response.url).query).get("orderId")
        assert order_id, "Cant find order_id in redirect url"
        self.set("order_id", order_id[0])
        order_item_id = re.findall('"OrderItemId":(.*?),"', self.response.text)
        assert order_item_id, "Cant find order_item_id on page"
        self.set("order_item_id", order_item_id[0])
        order_number = re.findall('"OrderNumber":"(.*?)","', self.response.text)
        assert order_number, "Cant find order_number on page"
        self.set("order_number", order_number[0])


if __name__ == '__main__':
    run_test(__file__, browser="none")
