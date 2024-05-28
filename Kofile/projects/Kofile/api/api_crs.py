from bs4 import BeautifulSoup


class CRS:

    @staticmethod
    def parse_search_result(content, table_id="orderSearchBlock"):
        soup = BeautifulSoup(content, "lxml")
        table = soup.find("table", id=table_id)
        assert table, "Table with results not found"
        tbody = table.find("tbody")
        assert tbody, "Table with results not found"
        all_rows = tbody.find_all("tr")
        assert all_rows, "No search result"
        return all_rows

    def _get_search_result_content_by_index(self, row, index, package_can_be_blank=True):
        result = dict()

        result["order_id"] = self.get_column_value(row, index, "OrderId")
        result["package_id"] = self.get_column_value(row, index, "PackageId", is_blank=package_can_be_blank)
        result["agent_id"] = self.get_column_value(row, index, "AgentId", is_blank=True)
        result["order_number"] = self.get_column_value(row, index, "OrderHeader.OrderNumber")
        result["location"] = self.get_column_value(row, index, "OrderHeader.Location")
        result["department"] = self.get_column_value(row, index, "OrderHeader.DepartmentInfo.Description",
                                                     is_blank=True)
        result["origin"] = self.get_column_value(row, index, "OrderHeader.Origin")
        result["order_date"] = self.get_column_value(row, index, "OrderHeader.OrderDate")
        result["no_of_items"] = self.get_column_value(row, index, "NoOfItems")
        result["order_total"] = self.get_column_value(row, index, "OrderTotal")
        result["no_of_documents"] = self.get_column_value(row, index, "NoOfDocuments")
        result["order_search_status"] = self.get_column_value(row, index, "OrderSearchStatus")
        result["recorded_date"] = self.get_column_value(row, index, "RecordedDate", is_blank=True)
        result["finalize_agent_name"] = self.get_column_value(row, index, "FinalizeAgentName", is_blank=True)
        result["first_name"] = self.get_column_value(row, index, "OrderHeader.OrderUser.User.FirstName", is_blank=True)
        result["gf_number_range"] = self.get_column_value(row, index, "GFNumberRange", is_blank=True)
        result["document_number"] = self.get_column_value(row, index, "DocumentNumber", is_blank=True)
        result["order_status_id"] = self.get_column_value(row, index, "OrderStatusId", is_blank=True)
        result["num_of_pages"] = self.get_column_value(row, index, "NumOfPages", is_blank=True)

        return result

    def _get_package_search_result_content_by_index(self, row, index):
        result = dict()

        result["order_id"] = self.get_column_value(row, index, "OrderId")
        result["order_number"] = self.get_column_value(row, index, "OrderNumber")
        result["department_desc"] = self.get_column_value(row, index, "DepartmentDesc", is_blank=True)
        result["submitter_name"] = self.get_column_value(row, index, "SubmitterName", is_blank=True)
        result["customer_name"] = self.get_column_value(row, index, "CustomerName", is_blank=True)
        result["order_received_on"] = self.get_column_value(row, index, "OrderReceivedOn", is_blank=True)
        result["order_recorded_on"] = self.get_column_value(row, index, "OrderRecordedOn", is_blank=True)
        result["ad_user_name"] = self.get_column_value(row, index, "AdUserName", is_blank=True)
        result["no_of_documents"] = self.get_column_value(row, index, "NoOfDocuments")
        result["document_number"] = self.get_column_value(row, index, "DocumentNo", is_blank=True)
        result["origin"] = self.get_column_value(row, index, "Origin")
        result["package_id"] = self.get_column_value(row, index, "PackageId")

        return result

    def get_search_result_content_by_index(self, content, index=0, package_can_be_blank=True):
        if index is None:
            return [self._get_search_result_content_by_index(row, a, package_can_be_blank) for a, row in
                    enumerate(self.parse_search_result(content))]
        else:
            row = self.parse_search_result(content)[index]
            return self._get_search_result_content_by_index(row, index, package_can_be_blank)

    def get_package_search_result_content_by_index(self, content, index=0):
        if index is None:
            return [self._get_package_search_result_content_by_index(row, a) for a, row in
                    enumerate(self.parse_search_result(content, table_id="OrderQueue"))]
        else:
            row = self.parse_search_result(content, table_id="OrderQueue")[index]
            return self._get_package_search_result_content_by_index(row, index)

    @staticmethod
    def get_column_value(row, index, data_column, is_blank=False):
        data = row.find("td", {"data-column": data_column})
        assert data, f"{data_column} not found in result row with index: {index}"
        data_text = data.text.strip()
        if not is_blank:
            assert data_text, f"{data_column} not found in result row with index: {index}"
        return data_text

    @staticmethod
    def get_drop_down_values(content, _id):
        soup = BeautifulSoup(content, "lxml")
        select = soup.find("select", id=_id)
        assert select, f"Cant find select with id {_id}"
        options = select.find_all("option")
        assert options, f"Select with id {_id} not have options"
        return {i.text: i.get("value") for i in options if i.get("value")}
