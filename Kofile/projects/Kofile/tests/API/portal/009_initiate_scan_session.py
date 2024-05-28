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
            "type": "number"
        }

    @property
    def post_data(self):
        return self.api_test_data.initiate_scan_session_data.copy()

    def __test__(self):
        self.set_content_type('application/json')
        self.response = self.session.post(self.get_url(self.api_urls.InitiateScanSession), json=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)
        scanner_id = self.response.json()
        assert scanner_id != -1, "scanner app not running"
        self.set("portal_scanner_id", scanner_id)


if __name__ == '__main__':
    run_test(__file__, browser="none")
