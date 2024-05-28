from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                                 # noqa
    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        now = self.datetime.now()
        item_data = self.api_test_data.save_batch_scan_item_data.copy()
        data = self.api_test_data.save_batch_scan_data.copy()
        item_data["DocumentId"] = self.get("portal_document_id")
        item_data["OrderId"] = self.get("portal_order_id")
        item_data["OrderNumber"] = self.get("portal_order_number")
        item_data["Number"] = self.get("portal_doc_number")
        item_data["Path"] = self.get("portal_azure_file_path")
        item_data["OrderItemId"] = self.get("portal_order_item_id")
        item_data["ScanDate"] = self.get("portal_scan_date")
        item_data["ScanTaskId"] = self.get("portal_scanner_id")
        item_data["Year"] = now.strftime("%Y")
        data["Documents"].append(item_data)
        return data

    @property
    def schema(self):
        return {
            "type": "object",
            "properties": {
                "sentToReview": {"type": "boolean", "value": False},
                "overAllSuccess": {"type": "boolean", "value": True}
            }
        }

    def __before__(self):
        self.run_dependencies(("portal_document_saved",))

    def __test__(self):
        self.set_content_type('application/json')
        self.response = self.session.post(self.get_url(self.api_urls.SaveBatchScan), json=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)
        self.set("portal_scan_complete", True)


if __name__ == '__main__':
    run_test(__file__, browser="none")
