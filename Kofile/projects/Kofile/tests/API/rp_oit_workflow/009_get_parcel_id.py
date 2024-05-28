from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                                # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def schema(self):
        return {
            "type": "object",
            "properties": {
                "Data": {"type": "object",
                         "properties": {
                             "Id": {"type": "number"},
                             "DocMasterId": {"type": "number"},
                             "SEQ": {"type": "number"},
                             "PropertyType": {"type": "number"},
                             "SequenceNumber": {"type": "number"},
                             "AddressType": {"type": "number"},
                             "TenantId": {"type": "number"},
                             "Address1": {"type": "string"},
                             "Address2": {"type": "string"},
                             "ZipCode": {"type": "string"},
                             "City": {"type": "string"},
                             "State": {"type": "string"},
                             "Document": {"type": ["string", 'null']},
                             "County": {"type": ["string", 'null']},
                             "ParcelId": {"type": ["number", 'null']},
                             "TenantCode": {"type": ["number", 'null']},
                         }},
            }
        }

    def __test__(self):
        params = (('parcelId', self.data.env.get("api_params", {}).get("parcel_id", self.api_test_data.parcel_id)),)
        self.response = self.session.get(self.get_url(self.api_urls.GetParcelId), params=params)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)


if __name__ == '__main__':
    run_test(__file__, browser="none", env="prod_ref")
