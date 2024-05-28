from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                              # noqa
    title = "<title>Indexing Summary</title>"

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        data = self.api_test_data.cs_order_actions_indexing_data.copy()
        data["Order.OrderId"] = self.get("cs_re_index_order_id")
        data["Order.OrderItems[0].OrderItemId"] = self.get("re_index_order_item_id")
        data["orderItemId"] = self.get("re_index_order_item_id")
        data["indexingTaskId"] = self.get("cs_re_index_indexing_task_id")
        data['Order.OrderItems[0].OrderItemType.Id'] = self.get("re_index_order_item_type_id")
        data['orderTypeId'] = self.get("re_index_order_type_id")
        data["orderNum"] = self.get("cs_re_index_order_number")
        data["dmId"] = self.get("re_index_order_dm_id")
        data['docTypeId'] = self.get("re_index_order_doc_type_id")
        data['Order.OrderItems[0].Document.DocumentTypeId'] = self.get("re_index_order_doc_type_id")
        data['Order.OrderItems[0].Document.VitalIndexExtras.EventDate'] = self.datetime.now().strftime("%m/%d/%Y")
        return data

    def __before__(self):
        self.run_dependencies(("re_index_order_dm_id", "re_index_order_item_id", "re_index_order_item_type_id",
                               "re_index_order_type_id", "cs_re_index_order_id", "cs_re_index_order_number",
                               "re_index_order_doc_type_id", "cs_re_index_indexing_task_id"))

    def __test__(self):
        self.set_content_type()
        self.response = self.session.post(self.get_url(self.api_urls.IndexingOrderActions), data=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert self.title in self.response.text[:200], self.response.text[:200]
        self.set("re_index_order_item_saved_in_indexing", True)


if __name__ == '__main__':
    run_test(__file__, browser="none")
