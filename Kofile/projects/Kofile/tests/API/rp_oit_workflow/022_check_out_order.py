from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test
import re

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                             # noqa
    title = "<title>Add Payment</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        now = self.datetime.now()
        data = self.api_test_data.check_out_order_data.copy()
        data.append(('Order.OrderId', self.get("order_id")))
        data.append(('Order.OrderHeader.OrderUser.PersonalUserId', self.get("user_id")))
        data.append(('Order.OrderHeader.OrderUser.User.Email', self.data.env.email_user))
        data.append(('Order.OrderHeader.OrderUser.User.Address.AddressId', self.get("address_id")))
        data.append(('Order.OrderHeader.OrderUser.User.Address.Email', self.data.env.email_user))
        data.append(('receiveDateInput', now.strftime("%m/%d/%Y")))
        data.append(('receiveTimeInput', now.strftime('%H:%M %p')))
        data.append(('Order.OrderHeader.OrderNumber', self.get("order_number")))
        return data

    def __before__(self):
        self.run_dependencies(("order_id", "user_id", "address_id", "order_number"))

    def __test__(self):
        self.set_content_type()
        self.response = self.session.post(self.get_url(self.api_urls.CheckOutOrder), data=self.post_data,
                                          allow_redirects=True)
        price = re.findall('<span id="orderTotalAmt" class="hidden">(.*?)</span>', self.response.text)
        assert price
        self.set("price", price[0])
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]


if __name__ == '__main__':
    run_test(__file__, browser="none", env="qa_dev")
