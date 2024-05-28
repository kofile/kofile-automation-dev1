from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):  # noqa
    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        data = self.api_test_data.save_batch_scan_data.copy()
        re_capture_initial_batch_items = self.get("re_capture_initial_batch_items")
        re_capture_initial_batch_items["Status"] = "Reviewed"
        data["Documents"].append(re_capture_initial_batch_items)
        data["CaptureTaskId"] = self.get("re_capture_capture_task_id")
        data["IsRecapture"] = True
        return data

    @property
    def schema(self):
        return {
            "type": "object",
            "properties": {
                "sentToReview": {"type": "boolean", "enum": [False]},
                "overAllSuccess": {"type": "boolean", "enum": [True]}
            }
        }

    def __before__(self):
        self.run_dependencies(("re_capture_document_saved", "re_capture_doc_group", "re_capture_initial_batch_items"))

    def __test__(self):
        self.set_content_type('application/json')
        self.response = self.session.post(self.get_url(self.api_urls.SaveBatchScan), json=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)
        self.call_module(self.data_mapping.get("search_by_order_number"),
                         order_number=self.get("cs_re_capture_order_number"), status="Archive")


if __name__ == '__main__':
    run_test(__file__, browser="none")
