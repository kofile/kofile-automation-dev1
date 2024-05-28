from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test
from bs4 import BeautifulSoup

description = """
"""

tags = ['API']


class test(ApiTestParent):
    place = "cs"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __before__(self):
        self.run_dependencies(("cs_order_in_inbox", "cs_first_rp_order"))

    def __test__(self):
        self.set_content_type('application/json')
        self.response = self.session.get(self.get_url(self.api_urls.GetInboxItems, domain_key="cs_domain"))
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"

        soup = BeautifulSoup(self.response.content, "lxml")
        num = self.get("cs_first_rp_order")["Number"]
        assert soup.find("td", text=num), f"cant find doc with number {num} in inbox"
        count = len(soup.find_all("tr", class_="inboxItem"))
        assert count == 1, f"Inbox items count: {count}, but must be 1"


if __name__ == '__main__':
    run_test(__file__, browser="none")
