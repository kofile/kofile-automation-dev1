from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                            # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.set_content_type()
        self.response = self.session.post(self.get_url(self.api_urls.SetAdUserConfig),
                                          data=self.api_test_data.set_ad_user_config_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"


if __name__ == '__main__':
    run_test(__file__, browser="none")
