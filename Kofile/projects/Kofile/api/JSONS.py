from datetime import datetime, timedelta


class ClerkSearchJsons:

    @staticmethod
    def document_search(department_id=1, doc_group_name=None, doc_group_id=None, page_num=1, doc_type_in_cs=None,
                        search_text=None):
        search_text = search_text if search_text else doc_type_in_cs
        dg_names = [doc_group_name] if doc_group_name else doc_group_name
        if doc_group_id:
            doc_group_id = doc_group_id if isinstance(doc_group_id, list) else [doc_group_id]
        else:
            doc_group_id = []
        party_types = {"1": ["D", "I"], "2": ["D", "I"], "3": ["D", "I"], "4": ["BN", "OW"], "5": ["C", "M", "F"],
                       "6": ["G", "B"], "7": ["DT", "IT"], "8": [], "9": ["DE", "F"], "11": ["O", "R"], "12": ["S"],
                       "13": [], "15": ["DT", "IT"]}
        # If document dot found on first 3 pages - change year in 'search from date' to 1901
        from_year = "2000" if page_num <= 5 else "1901"
        # Set 'search to date' to yesterday date| today is search_text
        to_date = (datetime.now() - timedelta(0 if search_text else 1)).strftime("%m/%d/%Y")
        type_key = "$type"
        data = {
            "DefaultEndDate": f"{datetime.now().strftime('%m/%d/%Y')}",
            "DefaultStartDate": "1/1/1800 12:00:00 AM",
            "DepartmentId": department_id,
            "DocGroupsNames": [],
            "ExportRowsLimit": "100",
            "Filters": {
                type_key: "System.Collections.Generic.Dictionary`2[[System.String, "
                         "mscorlib],[System.Object, mscorlib]], mscorlib",
                "PartyTypes": {
                    type_key: "System.Collections.Generic.List`1[[System.String, mscorlib]], mscorlib",
                    "$values": party_types.get(department_id)
                },
                "RecordedDate": {
                    type_key: "System.Collections.Generic.Dictionary`2[[System.String, "
                             "mscorlib],[System.DateTime, mscorlib]], mscorlib",
                    "FromDate": f"1/1/{from_year}",
                    "ToDate": f"{to_date}"
                }
            },
            "IsAdvancedSearch": False,
            "IsRowPresentationMode": "0",
            "NameSearchText": "",
            "Pagination": {
                "PageNo": str(page_num),
                "PageSize": "400"
            },
            "PartyTypesNames": ["All"],
            "SearchFields": [
                "DOC#",
                "DocType"
            ],
            "SearchFieldsNames": ["All"],
            "SearchMode": "Doc",
            "SortColumns": [],
            "SortOrder": "ASC",
            "UseAnd": True,
            "UseTypeAhead": "on"
        }
        if dg_names:
            data.update({"DocGroupsNames": dg_names})
            data["Filters"].update({"DocumentGroups": {type_key: "System.Collections.Generic.List`1"
                                                                "[[System.Int16, mscorlib]], mscorlib",
                                                       "$values": doc_group_id}})
        if department_id in [6, "6"]:
            data.update({"SortColumns": [{"ColumnName": "Applicant2", "SortDirection": "ASC"}]})
        if search_text:
            data.update({"SearchText": search_text})
        return data
