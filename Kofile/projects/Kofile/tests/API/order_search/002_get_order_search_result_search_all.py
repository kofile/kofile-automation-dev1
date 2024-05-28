from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):
    title = "<title>Order Queue</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        data = self.api_test_data.order_search_data.copy()
        return data

    def __before__(self):
        self.run_dependencies(("last_row_data",))

    def __test__(self):
        self.set_content_type('application/x-www-form-urlencoded')
        self.response = self.session.post(self.get_url(self.api_urls.GetOrderSearchResult), data=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200]

        all_rows = self.api_lib.crs.get_search_result_content_by_index(self.response.content, None)
        assert len(all_rows) > 1, f"Search result count <= 1 without filters"

        data, department = None, None
        for row in all_rows:
            if row.get("document_number"):
                data = row
            if row.get("department"):
                department = row
            if data and department:
                break
        assert data, "Search result without filters not have any orders with document number"
        assert department, "Search result without filters not have any orders with department"
        self.set("row_with_doc_number", data)
        self.set("row_with_department", department)


if __name__ == '__main__':
    run_test(__file__, browser="none")
