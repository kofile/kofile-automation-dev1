from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):
    place = "portal"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __before__(self):
        self.run_dependencies(("an_url",))

    @property
    def post_data(self):
        return self.api_test_data.portal_an_data.copy()

    @property
    def schema(self):
        return {
            "definitions": {},
            "title": "Root",
            "type": "object",
            "required": [
                "status",
                "OrderNumber",
                "IsInternet",
                "Message",
                "NavigationUrl"
            ],
            "properties": {
                "status": {
                    "$id": "#root/status",
                    "title": "Status",
                    "type": "boolean",
                    "examples": [
                        True
                    ],
                    "default": True
                },
                "OrderNumber": {
                    "$id": "#root/OrderNumber",
                    "title": "Ordernumber",
                    "type": "string",
                    "pattern": "^\d{14}$"
                },
                "IsInternet": {
                    "$id": "#root/IsInternet",
                    "title": "Isinternet",
                    "type": "boolean",
                    "examples": [
                        True
                    ],
                    "default": True
                },
                "Message": {
                    "$id": "#root/Message",
                    "title": "Message",
                    "type": "string",
                    "default": "",
                    "examples": [
                        ""
                    ],
                    "pattern": "^.*$"
                },
                "NavigationUrl": {
                    "$id": "#root/NavigationUrl",
                    "title": "Navigationurl",
                    "type": "null",
                    "default": None
                }
            }
        }

    def __test__(self):
        params = {'docType': 'ANUnincorporated'}
        self.set_content_type()
        self.response = self.session.post(self.get("an_url").replace("/ANUnincorporated/", self.api_urls.Submit),
                                          params=params, data=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)
        assert self.response.json()["status"], self.response.text
        self.set("portal_order_number", self.response.json()["OrderNumber"])
        self.logging.info(f"Order created {self.response.json()['OrderNumber']}")


if __name__ == '__main__':
    run_test(__file__, browser="none")

