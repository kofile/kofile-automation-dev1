from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):
    place, dep_id = "cs", 6

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        now = self.datetime.now()
        data = self.api_test_data.cs_search_ml_data.copy()
        data["DepartmentId"] = str(self.dep_id)
        data["DefaultEndDate"] = now.strftime('%m/%d/%Y 12:00:00 AM')
        data["Filters"]["RecordedDate"]["ToDate"] = now.strftime('%m/%d/%Y')
        data["Filters"]["PartyTypes"]["$values"] = [i['Code'] for i in self.get("cs_ml_party_names") if i['Id'] != 0]
        data["PartyTypesNames"] = ['All', ]
        data["SearchFields"] = [i['FieldName'] for i in self.get("cs_ml_search_fields") if i['FieldName'] != "All"]
        data["SearchFieldsNames"] = ['All', ]
        data["UseAnd"] = True
        data["SearchText"] = "test"
        return data

    @property
    def schema(self):
        return self.api_test_data.ml_search_schema

    def __before__(self):
        self.run_dependencies(("cs_ml_search_fields", "cs_ml_party_names"))

    def __test__(self):
        self.set_content_type('application/json')
        self.response = self.session.post(self.get_url(self.api_urls.DocumentSearch % self.dep_id,
                                                       domain_key="cs_domain"), json=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)


if __name__ == '__main__':
    run_test(__file__, browser="none")
