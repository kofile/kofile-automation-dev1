from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):  # noqa
    title = "<title>Order Queue</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        data = self.api_test_data.order_search_data.copy()
        payment_type = 'Cash'
        value = self.get('order_payment_type_ids').get(payment_type)
        assert value, f"Cant find {payment_type} in:\n{self.get('order_payment_type_ids')}"
        data["OrderPaymentTypeId"] = value
        return data

    def __before__(self):
        self.run_dependencies(("last_row_data", "order_payment_type_ids"))

    def __test__(self):
        self.set_content_type('application/x-www-form-urlencoded')
        self.response = self.session.post(self.get_url(self.api_urls.GetOrderSearchResult), data=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]

        self.api_lib.crs.get_search_result_content_by_index(self.response.content, None)


if __name__ == '__main__':
    run_test(__file__, browser="none")
