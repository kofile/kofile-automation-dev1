import re
from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                          # noqa
    title = "<title>Order Finalization</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __before__(self):
        self.run_dependencies(("finalize_order",))

    def __test__(self):
        params = (('orderId', self.get("order_id")),)
        self.response = self.session.get(self.get_url(self.api_urls.ShowOrderFinalization), params=params)
        order_item_id = re.findall('"OrderItemId":(.*?),', self.response.text)
        instrument_number = re.findall(',"InstrumentNumber":"(.*?)",', self.response.text)
        assert order_item_id, "Cant find OrderItemId on page"
        assert instrument_number, "Cant find InstrumentNumber on page"
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]
        self.set("final_order_item_id", order_item_id[0])
        self.set("instrument_number", instrument_number[0])


if __name__ == '__main__':
    run_test(__file__, browser="none")
