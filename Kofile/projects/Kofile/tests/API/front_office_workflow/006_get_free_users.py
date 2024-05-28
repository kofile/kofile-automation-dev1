from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):
    email = "test@test.com"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        return {"email": self.email, "accountId": self.get('company_account_id')}

    @property
    def schema(self):
        return {
            "definitions": {},
            "title": "Root",
            "minItems": 1,
            "maxItems": 5,
            "type": "array",
            "default": [],
            "items": {
                "$id": "#root/items",
                "title": "Items",
                "type": "object",
                "required": [
                    "Id",
                    "UnparsedName",
                    "FirstName",
                    "LastName",
                    "MiddleName",
                    "Email",
                    "Phone",
                    "Address",
                    "CompanyUser"
                ],
                "properties": {
                    "Id": {
                        "$id": "#root/items/Id",
                        "title": "Id",
                        "type": "integer",
                        "default": 0
                    },
                    "UnparsedName": {
                        "$id": "#root/items/UnparsedName",
                        "title": "Unparsedname",
                        "type": "null",
                        "default": None
                    },
                    "FirstName": {
                        "$id": "#root/items/FirstName",
                        "title": "Firstname",
                        "type": "string",
                        "default": "",
                        "examples": [
                            "$"
                        ],
                        "pattern": "^.*$"
                    },
                    "LastName": {
                        "$id": "#root/items/LastName",
                        "title": "Lastname",
                        "type": "string",
                        "default": "",
                        "examples": [
                            "%"
                        ],
                        "pattern": "^.*$"
                    },
                    "MiddleName": {
                        "$id": "#root/items/MiddleName",
                        "title": "Middlename",
                        "type": "null",
                        "default": None
                    },
                    "Email": {
                        "$id": "#root/items/Email",
                        "title": "Email",
                        "type": "string",
                        "default": "",
                        "examples": [
                            "test@test.com"
                        ],
                        "pattern": "^.*$"
                    },
                    "Phone": {
                        "$id": "#root/items/Phone",
                        "title": "Phone",
                        "type": "null",
                        "default": None
                    },
                    "Address": {
                        "$id": "#root/items/Address",
                        "title": "Address",
                        "type": "null",
                        "default": None
                    },
                    "CompanyUser": {
                        "$id": "#root/items/CompanyUser",
                        "title": "Companyuser",
                        "type": "null",
                        "default": None
                    }
                }
            }

        }

    def __before__(self):
        self.run_dependencies(("company_account_id", "company_account_user_removed"))

    def __test__(self):
        self.response = self.session.get(self.get_url(self.api_urls.GetFreeUsers),
                                         params=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)
        self.set("company_account_user_id", self.response.json()[0]["Id"])
        self.set("company_account_user_email", self.email)


if __name__ == '__main__':
    run_test(__file__, browser="none")
