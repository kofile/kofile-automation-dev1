from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):
    place = "portal"
    title = "<title>Unincorporated Assumed Name</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __before__(self):
        self.run_dependencies(("an_url",))

    def __test__(self):
        self.response = self.session.get(self.get("an_url"))
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]


if __name__ == '__main__':
    run_test(__file__, browser="none")
