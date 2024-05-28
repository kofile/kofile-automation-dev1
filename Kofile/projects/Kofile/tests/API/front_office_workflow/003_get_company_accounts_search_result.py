from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):
    account_name, account_code = 'API tests account', '123123'

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        return {'accountName': self.account_name,
                'accountCode': '',
                'isActiveCompany': 'False'}

    @property
    def second_post_data(self):
        return {'accountName': '',
                'accountCode': self.account_code,
                'isActiveCompany': 'False'}

    @property
    def schema(self):
        return {
            "definitions": {},
            "title": "Root",
            "type": "array",
            "minItems": 1,
            "maxItems": 1,
            "default": [],
            "items": {
                "$id": "#root/items",
                "title": "Items",
                "type": "object",
                "required": [
                    "Id",
                    "AccountCode",
                    "IsEnabled",
                    "AccountName",
                    "AccountBalance",
                    "PsAccountBalance",
                    "OrganizationName",
                    "OrganizationFullName",
                    "OrganizationBalance",
                    "MinimumBalance",
                    "AllowCredit",
                    "LowBalanceLimit",
                    "PrimaryPhone",
                    "AllowOrdering",
                    "AllowERecording",
                    "AllowPublicSearch",
                    "UserName",
                    "Address",
                    "UserList",
                    "IsPanelHidden",
                    "AccountPaymentTotal",
                    "OrderNumber",
                    "OrderId",
                    "LastBalance",
                    "AllowDeactivate",
                    "Password",
                    "IsAllowExport",
                    "Departments",
                    "AchDetails",
                    "AccountDetails"
                ],
                "properties": {
                    "Id": {
                        "$id": "#root/items/Id",
                        "title": "Id",
                        "type": "integer",
                        "default": 0
                    },
                    "AccountCode": {
                        "$id": "#root/items/AccountCode",
                        "title": "Accountcode",
                        "type": "string",
                        "pattern": f"^{self.account_code}$"
                    },
                    "IsEnabled": {
                        "$id": "#root/items/IsEnabled",
                        "title": "Isenabled",
                        "type": "boolean",
                        "examples": [
                            False
                        ],
                        "default": True
                    },
                    "AccountName": {
                        "$id": "#root/items/AccountName",
                        "title": "Accountname",
                        "type": "string",
                        "default": "",
                        "pattern": f"^{self.account_name}$"
                    },
                    "AccountBalance": {
                        "$id": "#root/items/AccountBalance",
                        "title": "Accountbalance",
                        "type": "integer",
                        "examples": [
                            0
                        ],
                        "default": 0
                    },
                    "PsAccountBalance": {
                        "$id": "#root/items/PsAccountBalance",
                        "title": "Psaccountbalance",
                        "type": "integer",
                        "examples": [
                            0
                        ],
                        "default": 0
                    },
                    "OrganizationName": {
                        "$id": "#root/items/OrganizationName",
                        "title": "Organizationname",
                        "type": "null",
                        "default": None
                    },
                    "OrganizationFullName": {
                        "$id": "#root/items/OrganizationFullName",
                        "title": "Organizationfullname",
                        "type": "null",
                        "default": None
                    },
                    "OrganizationBalance": {
                        "$id": "#root/items/OrganizationBalance",
                        "title": "Organizationbalance",
                        "type": "integer",
                        "examples": [
                            0
                        ],
                        "default": 0
                    },
                    "MinimumBalance": {
                        "$id": "#root/items/MinimumBalance",
                        "title": "Minimumbalance",
                        "type": "integer",
                        "examples": [
                            0
                        ],
                        "default": 0
                    },
                    "AllowCredit": {
                        "$id": "#root/items/AllowCredit",
                        "title": "Allowcredit",
                        "type": "boolean",
                        "examples": [
                            False
                        ],
                        "default": True
                    },
                    "LowBalanceLimit": {
                        "$id": "#root/items/LowBalanceLimit",
                        "title": "Lowbalancelimit",
                        "type": "integer",
                        "examples": [
                            0
                        ],
                        "default": 0
                    },
                    "PrimaryPhone": {
                        "$id": "#root/items/PrimaryPhone",
                        "title": "Primaryphone",
                        "type": "null",
                        "default": None
                    },
                    "AllowOrdering": {
                        "$id": "#root/items/AllowOrdering",
                        "title": "Allowordering",
                        "type": "boolean",
                        "examples": [
                            False
                        ],
                        "default": True
                    },
                    "AllowERecording": {
                        "$id": "#root/items/AllowERecording",
                        "title": "Allowerecording",
                        "type": "boolean",
                        "examples": [
                            False
                        ],
                        "default": True
                    },
                    "AllowPublicSearch": {
                        "$id": "#root/items/AllowPublicSearch",
                        "title": "Allowpublicsearch",
                        "type": "boolean",
                        "examples": [
                            False
                        ],
                        "default": True
                    },
                    "UserName": {
                        "$id": "#root/items/UserName",
                        "title": "Username",
                        "type": "string",
                        "default": "",
                        "examples": [
                            ""
                        ],
                        "pattern": "^.*$"
                    },
                    "Address": {
                        "$id": "#root/items/Address",
                        "title": "Address",
                        "type": "null",
                        "default": None
                    },
                    "UserList": {
                        "$id": "#root/items/UserList",
                        "title": "Userlist",
                        "type": "null",
                        "default": None
                    },
                    "IsPanelHidden": {
                        "$id": "#root/items/IsPanelHidden",
                        "title": "Ispanelhidden",
                        "type": "boolean",
                        "examples": [
                            False
                        ],
                        "default": True
                    },
                    "AccountPaymentTotal": {
                        "$id": "#root/items/AccountPaymentTotal",
                        "title": "Accountpaymenttotal",
                        "type": "integer",
                        "examples": [
                            0
                        ],
                        "default": 0
                    },
                    "OrderNumber": {
                        "$id": "#root/items/OrderNumber",
                        "title": "Ordernumber",
                        "type": "null",
                        "default": None
                    },
                    "OrderId": {
                        "$id": "#root/items/OrderId",
                        "title": "Orderid",
                        "type": "integer",
                        "examples": [
                            0
                        ],
                        "default": 0
                    },
                    "LastBalance": {
                        "$id": "#root/items/LastBalance",
                        "title": "Lastbalance",
                        "type": "integer",
                        "examples": [
                            0
                        ],
                        "default": 0
                    },
                    "AllowDeactivate": {
                        "$id": "#root/items/AllowDeactivate",
                        "title": "Allowdeactivate",
                        "type": "boolean",
                        "examples": [
                            False
                        ],
                        "default": True
                    },
                    "Password": {
                        "$id": "#root/items/Password",
                        "title": "Password",
                        "type": "null",
                        "default": None
                    },
                    "IsAllowExport": {
                        "$id": "#root/items/IsAllowExport",
                        "title": "Isallowexport",
                        "type": "boolean",
                        "examples": [
                            False
                        ],
                        "default": True
                    },
                    "Departments": {
                        "$id": "#root/items/Departments",
                        "title": "Departments",
                        "type": "null",
                        "default": None
                    },
                    "AchDetails": {
                        "$id": "#root/items/AchDetails",
                        "title": "Achdetails",
                        "type": "null",
                        "default": None
                    },
                    "AccountDetails": {
                        "$id": "#root/items/AccountDetails",
                        "title": "Accountdetails",
                        "type": "null",
                        "default": None
                    }
                }
            }

        }

    def __test__(self):
        self.response = self.session.get(self.get_url(self.api_urls.GetCompanyAccountsSearchResult),
                                         params=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)
        self.response = self.session.get(self.get_url(self.api_urls.GetCompanyAccountsSearchResult),
                                         params=self.second_post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)

        self.set("company_account_id", self.response.json()[0]["Id"])
        self.set("company_account_name", self.account_name)
        self.set("company_account_code", self.account_code)


if __name__ == '__main__':
    run_test(__file__, browser="none")
