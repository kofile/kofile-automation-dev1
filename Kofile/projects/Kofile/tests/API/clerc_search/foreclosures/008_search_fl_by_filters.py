from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):
    place, dep_id = "cs", 13

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def post_data(self, search_field, use_and):
        now = self.datetime.now()
        data = self.api_test_data.cs_search_fl_data.copy()
        data["DepartmentId"] = str(self.dep_id)
        data["DefaultEndDate"] = now.strftime('%m/%d/%Y 12:00:00 AM')
        data["Filters"]["RecordedDate"]["ToDate"] = now.strftime('%m/%d/%Y')
        data["SearchFields"] = [search_field['FieldName'], ]
        data["SearchFieldsNames"] = [search_field["Name"], ]
        data["UseAnd"] = use_and
        return data

    @property
    def schema(self):
        return self.api_test_data.cs_search_schema

    def __before__(self):
        self.run_dependencies(("cs_fl_search_fields", ))

    def __test__(self):
        errors_count = 0
        self.set_content_type('application/json')
        for search_field in [i for i in self.get("cs_fl_search_fields") if i['FieldName'] != "All"]:
            try:
                self.response = self.session.post(
                    self.get_url(self.api_urls.DocumentSearch % self.dep_id, domain_key="cs_domain"),
                    json=self.post_data(search_field, bool(self.random.getrandbits(1))))
                assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
                self.validate(instance=self.response.json(), schema=self.schema)
            except Exception as e:
                self.logging.error(e, exc_info=True)
                self.logging.info(f"{search_field=}")
                errors_count += 1
        assert not errors_count, f"Test have {errors_count} errors, check logs"


if __name__ == '__main__':
    run_test(__file__, browser="none")
