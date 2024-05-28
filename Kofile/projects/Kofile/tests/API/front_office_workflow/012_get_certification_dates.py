from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):
    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def schema(self):
        return {
            "definitions": {},
            "title": "Root",
            "type": "array",
            "default": [],
            "items": {
                "$id": "#root/items",
                "title": "Items",
                "type": "object",
                "required": [
                    "TenantId",
                    "DeptId",
                    "DeptDesc",
                    "BeginDate",
                    "BeginDateString",
                    "EndDate",
                    "EndDateString",
                    "InterXId",
                    "IntraXId",
                    "AllowSearchAll",
                    "Sequence"
                ],
                "properties": {
                    "TenantId": {
                        "$id": "#root/items/TenantId",
                        "title": "Tenantid",
                        "type": "integer",
                        "examples": [
                            2
                        ],
                        "default": 0
                    },
                    "DeptId": {
                        "$id": "#root/items/DeptId",
                        "title": "Deptid",
                        "type": "integer",
                        "examples": [
                            1
                        ],
                        "default": 0
                    },
                    "DeptDesc": {
                        "$id": "#root/items/DeptDesc",
                        "title": "Deptdesc",
                        "type": "string",
                        "default": "",
                        "examples": [
                            "Property Records"
                        ],
                        "pattern": "^.*$"
                    },
                    "BeginDate": {
                        "$id": "#root/items/BeginDate",
                        "title": "Begindate",
                        "type": "string",
                        "default": "",
                        "examples": [
                            "1975-05-06T00:00:00"
                        ],
                        "pattern": "^.*$"
                    },
                    "BeginDateString": {
                        "$id": "#root/items/BeginDateString",
                        "title": "Begindatestring",
                        "type": "string",
                        "default": "",
                        "examples": [
                            "05/06/1975"
                        ],
                        "pattern": "^.*$"
                    },
                    "EndDate": {
                        "$id": "#root/items/EndDate",
                        "title": "Enddate",
                        "type": "string",
                        "default": "",
                        "examples": [
                            "2023-04-12T00:00:00"
                        ],
                        "pattern": "^.*$"
                    },
                    "EndDateString": {
                        "$id": "#root/items/EndDateString",
                        "title": "Enddatestring",
                        "type": "string",
                        "default": "",
                        "examples": [
                            "04/12/2023"
                        ],
                        "pattern": "^.*$"
                    },
                    "InterXId": {
                        "$id": "#root/items/InterXId",
                        "title": "Interxid",
                        "type": "integer",
                        "examples": [
                            0
                        ],
                        "default": 0
                    },
                    "IntraXId": {
                        "$id": "#root/items/IntraXId",
                        "title": "Intraxid",
                        "type": "integer",
                        "examples": [
                            0
                        ],
                        "default": 0
                    },
                    "AllowSearchAll": {
                        "$id": "#root/items/AllowSearchAll",
                        "title": "Allowsearchall",
                        "type": "boolean",
                        "examples": [
                            False
                        ],
                        "default": True
                    },
                    "Sequence": {
                        "$id": "#root/items/Sequence",
                        "title": "Sequence",
                        "type": "integer",
                        "examples": [
                            0
                        ],
                        "default": 0
                    }
                }
            }

        }

    def __test__(self):
        self.response = self.session.get(self.get_url(self.api_urls.GetCertificationDates))
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)


if __name__ == '__main__':
    run_test(__file__, browser="none")
