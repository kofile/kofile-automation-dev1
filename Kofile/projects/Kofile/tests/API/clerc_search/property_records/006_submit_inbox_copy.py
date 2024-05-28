from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):
    place = "cs"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __before__(self):
        self.set("cs_inbox_clear", None)
        self.set("cs_order_in_inbox", None)
        self.run_dependencies(("cs_first_rp_order", "copy_first_rp_order"))
        self.set("cs_first_rp_order", self.get("copy_first_rp_order"))
        self.run_dependencies(("cs_order_in_inbox", ))

    @property
    def post_data(self):
        data = self.api_test_data.cs_submit_data.copy()
        order = self.get("cs_first_rp_order")
        data["InboxCartItems"][0]["CartItem"]["Document"] = {'Id': order["Id"]}
        data["InboxCartItems"][0]["OrderType"] = {'Id': '3', 'Desc': 'Copy'}
        data["InboxCartItems"][0]["Comment"] = "Copy api test"
        return data

    @property
    def schema(self):
        data = self.api_test_data.submit_schema.copy()
        data["properties"]["Orders"]["items"]["properties"]["Documents"]["items"][
            "pattern"] = f'^{self.get("cs_first_rp_order")["Number"]}$'
        return data

    def __test__(self):
        self.set_content_type('application/json')
        self.response = self.session.post(self.get_url(self.api_urls.SubmitInbox, domain_key="cs_domain"),
                                          json=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)
        num = self.response.json()["Orders"][0]["OrderNumber"]
        self.set("cs_copy_order_number", num)
        self.logging.info(f"COPY ORDER {num}")
        self.set("cs_order_in_inbox", None)


if __name__ == '__main__':
    run_test(__file__, browser="none")
