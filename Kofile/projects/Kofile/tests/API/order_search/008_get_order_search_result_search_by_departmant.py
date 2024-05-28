from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):  # noqa
    title = "<title>Order Queue</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        data = self.api_test_data.order_search_data.copy()
        department = self.get("row_with_department")["department"] or "Property Records"
        value = self.get('department_ids').get(department)
        assert value, f"Cant find {self.get('row_with_department')['department']} in:\n{self.get('department_ids')}"
        data["DepartmentId"] = value
        return data

    def __before__(self):
        self.run_dependencies(("row_with_department", "department_ids"))

    def __test__(self):
        self.set_content_type('application/x-www-form-urlencoded')
        self.response = self.session.post(self.get_url(self.api_urls.GetOrderSearchResult), data=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]

        row_data = None
        row_with_department = self.get("row_with_department")
        for row in self.api_lib.crs.get_search_result_content_by_index(self.response.content, None):
            if row.get("order_id") == row_with_department.get("order_id"):
                row_data = row
                break
        assert row_data, f'Cant find order with id {row_with_department["order_id"]} and order number ' \
                         f'{row_with_department["order_number"]} in result by ' \
                         f'department {row_with_department["department"]}'
        assert row_with_department == row_data, f"Expected result on first row:\n {row_with_department}\n" \
                                          f"Actual result:\n {row_data}"


if __name__ == '__main__':
    run_test(__file__, browser="none")
