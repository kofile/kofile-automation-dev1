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
        self.run_dependencies(("cs_first_rp_order", "cs_inbox_clear"))

    @property
    def post_data(self):
        data = self.api_test_data.cs_add_to_inbox_data.copy()
        order = self.get("cs_first_rp_order")
        data[0]["Document"] = {'Id': order["Id"]}
        data[0]['TotalPages'] = order["NumOfPages"]
        return data

    @property
    def schema(self):
        return {
            "definitions": {},
            "title": "Root",
            "type": "object",
            "required": [
                "Status",
                "Message",
                "TotalItem",
                "TotalPages"
            ],
            "properties": {
                "Status": {
                    "$id": "#root/Status",
                    "title": "Status",
                    "type": "boolean",
                    "enum": [True]
                },
                "Message": {
                    "$id": "#root/Message",
                    "title": "Message",
                    "type": "string",
                    "pattern": "^Item Saved Successfully.$"
                },
                "TotalItem": {
                    "$id": "#root/TotalItem",
                    "title": "Totalitem",
                    "type": "integer",
                    "enum": [1]
                },
                "TotalPages": {
                    "$id": "#root/TotalPages",
                    "title": "Totalpages",
                    "type": "integer",
                }
            }
        }

    def __test__(self):
        self.set_content_type('application/json')
        self.response = self.session.post(self.get_url(self.api_urls.SaveInboxDetails, domain_key="cs_domain"),
                                          json=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)
        self.set("cs_order_in_inbox", True)


if __name__ == '__main__':
    run_test(__file__, browser="none")
