from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                            # noqa
    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def schema(self):
        return {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "Id": {"type": "number"},
                    "UnparsedName": {"type": ["string", "null"]},
                    "FirstName": {"type": "string"},
                    "LastName": {"type": "string"},
                    "MiddleName": {"type": ["string", "null"]},
                    "Phone": {"type": ["string", "null"]},
                    "Address": {"type": ["string", "null"]},
                    "CompanyUser": {"type": ["string", "null"]},
                    "Email": {"type": "string"},
                }
            },
        }

    def __test__(self):
        params = (('emailId', self.data.env.email_user),)
        self.response = self.session.get(self.get_url(self.api_urls.GetCustomersByEmail), params=params)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)
        self.set("user_id", self.response.json()[0].get("Id"))


if __name__ == '__main__':
    run_test(__file__, browser="none")
