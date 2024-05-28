from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test
import itertools

description = """
"""

tags = ['API']


class test(ApiTestParent):
    place, dep_id = "cs", 9

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def post_data(self, party_name, search_field, use_and):
        now = self.datetime.now()
        data = self.api_test_data.cs_search_dr_data.copy()
        data["DepartmentId"] = str(self.dep_id)
        data["DefaultEndDate"] = now.strftime('%m/%d/%Y 12:00:00 AM')
        data["Filters"]["RecordedDate"]["ToDate"] = now.strftime('%m/%d/%Y')
        data["Filters"]["PartyTypes"]["$values"] = [party_name["Code"], ]
        data["PartyTypesNames"] = [party_name["Description"], ]
        data["SearchFields"] = [search_field['FieldName'], ]
        data["SearchFieldsNames"] = [search_field["Name"], ]
        data["UseAnd"] = use_and
        return data

    @property
    def schema(self):
        return self.api_test_data.dr_search_schema

    def __before__(self):
        self.run_dependencies(("cs_dr_search_fields", "cs_dr_party_names"))

    def __test__(self):
        errors_count = 0
        self.set_content_type('application/json')
        for party_name, search_field in itertools.product(
                *[[i for i in self.get("cs_dr_party_names") if i['Id'] != 0],
                  [i for i in self.get("cs_dr_search_fields") if i['FieldName'] != "All"]]):
            try:
                self.response = self.session.post(
                    self.get_url(self.api_urls.DocumentSearch % self.dep_id, domain_key="cs_domain"),
                    json=self.post_data(party_name, search_field, bool(self.random.getrandbits(1))))
                assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
                self.validate(instance=self.response.json(), schema=self.schema)
            except Exception as e:
                self.logging.error(e, exc_info=True)
                self.logging.info(f"{party_name=}")
                self.logging.info(f"{search_field=}")
                errors_count += 1
        assert not errors_count, f"Test have {errors_count} errors, check logs"


if __name__ == '__main__':
    run_test(__file__, browser="none")
