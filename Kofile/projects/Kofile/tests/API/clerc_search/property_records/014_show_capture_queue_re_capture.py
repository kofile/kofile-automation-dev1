from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test
import json
import re

description = """
"""

tags = ['API']


class test(ApiTestParent):  # noqa
    title = "<title>Capture Queue</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __before__(self):
        self.run_dependencies(("cs_re_capture_order_number",))

    def __test__(self):
        self.set_content_type()
        self.response = self.session.get(self.get_url(self.api_urls.ShowCaptureQueue))
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]
        number = self.get("cs_re_capture_order_number")
        data = re.findall(r'(\{"Id[^\{]+:"%s"[^\{]+\})' % number, self.response.text)
        assert data, f"Cant find order {number} in capture queue"
        json_data = json.loads(data[0])
        assert json_data["IsRecapture"] is True, f"IsRecapture must be True, but: {json_data['IsRecapture']}"
        self.set("re_capture_capture_task_id", json_data["Id"])
        self.set("re_capture_status", json_data["Status"])
        self.set("re_capture_doc_number", json_data["DocumentsNumber"])


if __name__ == '__main__':
    run_test(__file__, browser="none")
