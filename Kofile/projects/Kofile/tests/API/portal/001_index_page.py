from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test
from bs4 import BeautifulSoup

description = """
"""

tags = ['API']


class test(ApiTestParent):
    place = "portal"
    title = "<title>Kiosk Home</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.response = self.session.get(self.get_url(self.api_urls.Index, domain_key="portal_domain"))
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]

        soup = BeautifulSoup(self.response.content, "lxml")
        ml_a = soup.find("a", string="Assumed Names")

        self.set("an_url", ml_a.get("href"))


if __name__ == '__main__':
    run_test(__file__, browser="none")
