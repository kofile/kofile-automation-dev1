from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):
    place = "cs"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.set_content_type('application/json')
        self.response = self.session.post(self.get_url(self.api_urls.ClearInboxCart, domain_key="cs_domain"))
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.set("cs_inbox_clear", True)


if __name__ == '__main__':
    run_test(__file__, browser="none")
