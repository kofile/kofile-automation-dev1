from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                                  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def schema(self):
        return {
            "type": "object",
            "properties": {
                "AddressId": {"type": "number"},
                "AddressCode": {"type": "string"},
                "AddressName": {"type": "string"},
                "AddressLine1": {"type": "string"},
                "AddressLine2": {"type": "string"},
                "Email": {"type": "string"},
                "City": {"type": "string"},
                "StateCode": {"type": "number"},
                "ZipCode": {"type": "string"},
                "County": {"type": ["string", "null"]},
                "Country": {"type": ["string", "null"]},
                "CountryCode": {"type": ["string", "null"]},
                "CountryName": {"type": ["string", "null"]},
                "StateProvince": {"type": ["string", "null"]},
                "StateName": {"type": ["string", "null"]},
                "DMAddressTypeID": {"type": "number"},
                "PhoneNumber": {"type": "string"},
                "StateOrCountryName": {"type": ["string", "null"]},
                "UnparsedAddress": {"type": "string"},
                "StateAndCountry": {"type": "string"},
                "FullAddress": {"type": "string"},
                "FullAddressWithoutZip": {"type": "string"},
                "MailingFullAddress": {"type": "string"},
                "CityStateZip": {"type": "string"},
            }
        }

    def __before__(self):
        self.run_dependencies(("user_id",))

    def __test__(self):
        user_id = self.get("user_id")
        params = (('userId', user_id),)
        self.response = self.session.get(self.get_url(self.api_urls.GetUserAddressByUserId), params=params)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)
        self.set("address_id", self.response.json().get("AddressId"))


if __name__ == '__main__':
    run_test(__file__, browser="none", env="qa_dev")
