from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                                # noqa
    title = "<title>Verification Summary</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        data = self.api_test_data.order_actions_verification_data.copy()
        data["Order.OrderId"] = self.get("order_id")
        data["Order.OrderItems[0].OrderItemId"] = self.get("second_oit_id")
        data["orderItemId"] = self.get("second_oit_id")
        data["verificationTaskId"] = self.get("verification_task_id")
        data["orderNum"] = self.get("order_number")
        data['Order.OrderItems[0].Document.VitalIndexExtras.EventDate'] = self.datetime.now().strftime("%m/%d/%Y")
        data["dmId"] = self.get("dm_id")
        return data

    def __before__(self):
        self.run_dependencies(("verification_task_id",))

    def __test__(self):
        self.set_headers(self.api_test_data.indexing_headers)
        self.response = self.session.post(self.get_url(self.api_urls.VerificationOrderActions), data=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]
        self.set("order_item_saved_in_verification", True)


if __name__ == '__main__':
    run_test(__file__, browser="none")
