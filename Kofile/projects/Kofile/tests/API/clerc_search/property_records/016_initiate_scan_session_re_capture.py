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
        data = self.api_test_data.re_capture_initiate_scan_session_data.copy()
        data["ScannerTaskId"] = self.get("re_capture_scan_task_id")
        data["ScannerTaskConfiguration"]["DocumentId"] = self.get("re_capture_document_id")
        data["ScannerTaskConfiguration"]["IsInsertAction"] = True
        data["ScannerTaskConfiguration"]["InsertIndex"] = int(self.get("re_capture_scanned")) + 1
        return data

    def __before__(self):
        self.run_dependencies(("re_capture_scan_task_id", "re_capture_document_id", "re_capture_scanned"))

    def __test__(self):
        self.set_content_type('application/json')
        self.response = self.session.post(self.get_url(self.api_urls.InitiateScanSession), json=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)
        scanner_id = self.response.json()
        assert scanner_id != -1, "scanner app not running"
        self.set("re_capture_is_scanned", True)


if __name__ == '__main__':
    run_test(__file__, browser="none")
