from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                                  # noqa
    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        now = self.datetime.now()
        data = self.api_test_data.validate_documentItem_details_data.copy()
        data["DocumentItem"]["documentItem"]["DocumentId"] = self.get("document_id")
        data["DocumentItem"]["documentItem"]["ScanTaskId"] = self.get("scanner_id")
        data["DocumentItem"]["documentItem"]["Year"] = now.strftime("%Y")
        data["DocumentItem"]["documentItem"]["Scanned"] = self.api_test_data.pages
        data["DocumentItem"]["documentItem"]["ScanDate"] = self.get("scan_date")
        data["DocumentItem"]["documentItem"]["Path"] = self.get("azure_file_path")
        data["DocumentItem"]["documentItem"]["RecordedYear"] = now.strftime("%Y-01-01T00:00:00")
        data["DocumentItem"]["DocumentId"] = self.get("document_id")
        data["DocumentItem"]["ScanTaskId"] = self.get("scanner_id")
        data["DocumentItem"]["OrderNumber"] = self.get("order_number")
        data["DocumentItem"]["Number"] = self.get("instrument_number")
        data["DocumentItem"]["Year"] = now.strftime("%Y")
        data["DocumentItem"]["Pages"] = self.api_test_data.pages
        data["DocumentItem"]["Scanned"] = self.api_test_data.pages
        data["DocumentItem"]["Path"] = self.get("azure_file_path")
        data["DocumentItem"]["ScanDate"] = self.get("scan_date")
        data["DocumentItem"]["DocumentGroup"]["Id"] = self.api_test_data.doc_group["id"]
        data["DocumentItem"]["DocumentGroup"]["Name"] = self.api_test_data.doc_group["name"]
        data["DocumentItem"]["DocumentType"]["Key"] = self.api_test_data.doc_type["id"]
        data["DocumentItem"]["DocumentType"]["Value"] = self.api_test_data.doc_type["name"]
        return data

    @property
    def schema(self):
        return {
            "type": "object",
            "properties": {
                "success": {"type": "boolean", "value": True},
                "validationResult": {"type": "number", "value": 1},
                "OrderItemId": {"type": "null"}
            }
        }

    def __before__(self):
        self.run_dependencies(("order_number", "instrument_number", "document_id", "azure_file_path", "scan_date"))

    def __test__(self):
        self.set_content_type('application/json')
        self.response = self.session.post(self.get_url(self.api_urls.ValidateDocumentItemDetails), json=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)


if __name__ == '__main__':
    run_test(__file__, browser="none")
