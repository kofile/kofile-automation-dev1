from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):
    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def post_data(self, is_active):
        return [
            {
                'Id': self.get("type_and_head_record_id"),
                'IsActive': is_active,
            },
        ]

    @property
    def schema(self):
        return {
            "definitions": {},
            "title": "Root",
            "type": "object",
            "required": [
                "Success"
            ],
            "properties": {
                "Success": {
                    "$id": "#root/Success",
                    "title": "Success",
                    "type": "boolean",
                    "examples": [
                        True
                    ],
                    "default": True
                }
            }
        }

    def __before__(self):
        self.run_dependencies(("type_and_head_record_id",))

    def __test__(self):
        self.set_content_type('application/json; charset=UTF-8')
        self.response = self.session.post(self.get_url(self.api_urls.SetIndexedPartyStatus),
                                          json=self.post_data(False))
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)
        self.response = self.session.post(self.get_url(self.api_urls.SetIndexedPartyStatus),
                                          json=self.post_data(True))
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)


if __name__ == '__main__':
    run_test(__file__, browser="none")
