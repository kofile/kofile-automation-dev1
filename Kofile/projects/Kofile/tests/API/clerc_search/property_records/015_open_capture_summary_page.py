from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test
import json
import re

description = """
"""

tags = ['API']


class test(ApiTestParent):  # noqa
    title = "<title>Capture Summary</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __before__(self):
        self.run_dependencies(("re_capture_capture_task_id",))

    @property
    def post_data(self):
        return {
            'captureTaskId': self.get("re_capture_capture_task_id"),
            'IsRecapture': 'true',
        }

    def __test__(self):
        self.set_content_type()
        self.response = self.session.get(self.get_url(self.api_urls.StartBatchScan), params=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]
        number = self.get("cs_re_capture_order_number")
        data = re.findall(r'(\[\{"DocumentGroup":[^\[]+:"%s"[^\[]+ScanTaskId":[^\[]+\])' % number,
                          self.response.text)
        assert data, f"Cant find order {number} in capture queue"
        json_data = json.loads(data[0])
        assert json_data, "Data is blank"
        json_data = json_data[0]
        self.set("re_capture_order_id", json_data["OrderId"])
        self.set("re_capture_document_id", json_data["DocumentId"])
        self.set("re_capture_order_item_id", json_data["OrderItemId"])
        self.set("re_capture_order_item_type_id", json_data["OrderItemTypeId"])
        self.set("re_capture_order_year", json_data["Year"])
        self.set("re_capture_doc_type", json_data["DocumentType"])
        self.set("re_capture_doc_group", json_data["DocumentGroup"])
        self.set("re_capture_pages", json_data["Pages"])
        self.set("re_capture_scanned", json_data["Scanned"])
        self.set("re_capture_scan_task_id", json_data["ScanTaskId"])
        self.set("re_capture_recorded_year", json_data["RecordedYear"])
        self.set("re_capture_initial_batch_items", json_data)


if __name__ == '__main__':
    run_test(__file__, browser="none")
