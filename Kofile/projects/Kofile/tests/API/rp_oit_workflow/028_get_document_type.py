from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                                # noqa
    oit, term = 'REAL PROPERTY', 'ABANDONMENT'

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def schema(self):
        return {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "Key": {"type": "number"},
                    "Value": {"type": "string", "pattern": f"^.*?{self.term}.*?$"},
                }
            }
        }

    def __test__(self):
        params = (('term', self.term), ('docGroupDesc', self.oit),)
        self.response = self.session.get(self.get_url(self.api_urls.GetDocumentType), params=params)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)


if __name__ == '__main__':
    run_test(__file__, browser="none")
