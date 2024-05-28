from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test
from bs4 import BeautifulSoup
import re
import json

description = """
"""

tags = ['API']


class test(ApiTestParent):
    place, dep_id = "cs", 1
    title = ">Welcome to Vanguard"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.response = self.session.get(self.get_url(f"{self.api_urls.Index}/{self.dep_id}", domain_key="cs_domain"))
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]

        soup = BeautifulSoup(self.response.content, "lxml")
        documentgroups = soup.find("div", id="documentgroups")
        assert documentgroups, "documentgroups not found on the page"
        ng_init = documentgroups.get("ng-init")
        assert ng_init, "documentgroups not have attribute ng-init"
        json_str = re.findall(r'"DocumentGroups":(\[\{".*\}\]),"', ng_init)
        assert json_str, "regex error in ng-init in documentgroups"
        self.set("cs_rp_doc_groups", json.loads(json_str[0]))

        partytypes = soup.find("div", id="partytypes")
        assert partytypes, "partytypes filter not found on the page"
        ng_init = partytypes.get("ng-init")
        assert ng_init, "partytypes not have attribute ng-init"
        json_str = re.findall(r'"PartyTypes":(\[\{".*\}\]),"', ng_init)
        assert json_str, "regex error in ng-init in partytypes"
        self.set("cs_rp_party_names", json.loads(json_str[0]))

        searchfields = soup.find("div", id="searchfields")
        assert searchfields, "searchfields filter not found on the page"
        ng_init = searchfields.get("ng-init")
        assert ng_init, "searchfields not have attribute ng-init"
        json_str = re.findall(r'"SearchFields":(\[\{".*\}\]),"', ng_init)
        assert json_str, "regex error in ng-init in searchfields"
        self.set("cs_rp_search_fields", json.loads(json_str[0]))


if __name__ == '__main__':
    run_test(__file__, browser="none")
