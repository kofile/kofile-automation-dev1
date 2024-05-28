from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                               # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def schema(self):
        return {
            "type": "object",
            "properties": {
                "Price": {"type": "number"},
                "IsPaymentAvalible": {"type": "boolean"},
            }
        }

    def __before__(self):
        self.run_dependencies(("order_id", "second_oit_id"))

    def __test__(self):
        params = (('orderId', self.get("order_id")), ('orderItemId', self.get("second_oit_id")), ('discountCode', ''),
                  ('discountValue', '0'), ('discountComment', ''))
        self.response = self.session.get(self.get_url(self.api_urls.UpdateOrderItemDiscount), params=params)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)


if __name__ == '__main__':
    run_test(__file__, browser="none")
