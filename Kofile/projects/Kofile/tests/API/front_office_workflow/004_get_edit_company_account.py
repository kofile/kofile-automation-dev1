from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):
    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        return {'accountId': self.get("company_account_id")}

    @property
    def schema(self):
        return {
            "definitions": {},
            "title": "Root",
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
                    "$id": "#root/Id",
                    "title": "Id",
                    "type": "integer",
                    "examples": [
                        self.get("company_account_id")
                    ],
                    "default": 0
                },
                "AccountCode": {
                    "$id": "#root/AccountCode",
                    "title": "Accountcode",
                    "type": "string",
                    "default": "",
                    "examples": [
                        ""
                    ],
                    "pattern": f"^{self.get('company_account_code')}$"
                },
                "IsEnabled": {
                    "$id": "#root/IsEnabled",
                    "title": "Isenabled",
                    "type": "boolean",
                    "examples": [
                        False
                    ],
                    "default": True
                },
                "AccountName": {
                    "$id": "#root/AccountName",
                    "title": "Accountname",
                    "type": "string",
                    "default": "",
                    "pattern": f"^{self.get('company_account_name')}$"
                },
                "AccountBalance": {
                    "$id": "#root/AccountBalance",
                    "title": "Accountbalance",
                    "type": "integer",
                    "examples": [
                        0
                    ],
                    "default": 0
                },
                "PsAccountBalance": {
                    "$id": "#root/PsAccountBalance",
                    "title": "Psaccountbalance",
                    "type": "integer",
                    "examples": [
                        0
                    ],
                    "default": 0
                },
                "OrganizationName": {
                    "$id": "#root/OrganizationName",
                    "title": "Organizationname",
                    "type": "null",
                    "default": None
                },
                "OrganizationFullName": {
                    "$id": "#root/OrganizationFullName",
                    "title": "Organizationfullname",
                    "type": "null",
                    "default": None
                },
                "OrganizationBalance": {
                    "$id": "#root/OrganizationBalance",
                    "title": "Organizationbalance",
                    "type": "integer",
                    "examples": [
                        0
                    ],
                    "default": 0
                },
                "MinimumBalance": {
                    "$id": "#root/MinimumBalance",
                    "title": "Minimumbalance",
                    "type": "integer",
                    "examples": [
                        0
                    ],
                    "default": 0
                },
                "AllowCredit": {
                    "$id": "#root/AllowCredit",
                    "title": "Allowcredit",
                    "type": "boolean",
                    "examples": [
                        False
                    ],
                    "default": True
                },
                "LowBalanceLimit": {
                    "$id": "#root/LowBalanceLimit",
                    "title": "Lowbalancelimit",
                    "type": "integer",
                    "examples": [
                        0
                    ],
                    "default": 0
                },
                "PrimaryPhone": {
                    "$id": "#root/PrimaryPhone",
                    "title": "Primaryphone",
                    "type": "string",
                    "default": "",
                    "pattern": "^.*$"
                },
                "AllowOrdering": {
                    "$id": "#root/AllowOrdering",
                    "title": "Allowordering",
                    "type": "boolean",
                    "examples": [
                        False
                    ],
                    "default": True
                },
                "AllowERecording": {
                    "$id": "#root/AllowERecording",
                    "title": "Allowerecording",
                    "type": "boolean",
                    "examples": [
                        False
                    ],
                    "default": True
                },
                "AllowPublicSearch": {
                    "$id": "#root/AllowPublicSearch",
                    "title": "Allowpublicsearch",
                    "type": "boolean",
                    "examples": [
                        False
                    ],
                    "default": True
                },
                "UserName": {
                    "$id": "#root/UserName",
                    "title": "Username",
                    "type": "string",
                    "default": "",
                    "examples": [
                        ""
                    ],
                    "pattern": "^.*$"
                },
                "Address": {
                    "$id": "#root/Address",
                    "title": "Address",
                    "type": "object",
                    "required": [
                        "AddressId",
                        "AddressCode",
                        "AddressName",
                        "AddressLine1",
                        "AddressLine2",
                        "Email",
                        "City",
                        "StateCode",
                        "ZipCode",
                        "County",
                        "Country",
                        "CountryCode",
                        "CountryName",
                        "StateProvince",
                        "StateName",
                        "DMAddressTypeID",
                        "PhoneNumber",
                        "StateOrCountryName",
                        "UnparsedAddress",
                        "StateAndCountry",
                        "FullAddress",
                        "FullAddressWithoutZip",
                        "MailingFullAddress",
                        "CityStateZip"
                    ],
                    "properties": {
                        "AddressId": {
                            "$id": "#root/Address/AddressId",
                            "title": "Addressid",
                            "type": "integer",
                            "default": 0
                        },
                        "AddressCode": {
                            "$id": "#root/Address/AddressCode",
                            "title": "Addresscode",
                            "type": "null",
                            "default": None
                        },
                        "AddressName": {
                            "$id": "#root/Address/AddressName",
                            "title": "Addressname",
                            "type": "string",
                            "default": "",
                            "pattern": f"^{self.get('company_account_name')}$"
                        },
                        "AddressLine1": {
                            "$id": "#root/Address/AddressLine1",
                            "title": "Addressline1",
                            "type": "string",
                            "default": "",
                            "examples": [
                                ""
                            ],
                            "pattern": "^.*$"
                        },
                        "AddressLine2": {
                            "$id": "#root/Address/AddressLine2",
                            "title": "Addressline2",
                            "type": "string",
                            "default": "",
                            "examples": [
                                ""
                            ],
                            "pattern": "^.*$"
                        },
                        "Email": {
                            "$id": "#root/Address/Email",
                            "title": "Email",
                            "type": "null",
                            "default": None
                        },
                        "City": {
                            "$id": "#root/Address/City",
                            "title": "City",
                            "type": "string",
                            "default": "",
                            "examples": [
                                ""
                            ],
                            "pattern": "^.*$"
                        },
                        "StateCode": {
                            "$id": "#root/Address/StateCode",
                            "title": "Statecode",
                            "type": "integer",
                            "examples": [
                                0
                            ],
                            "default": 0
                        },
                        "ZipCode": {
                            "$id": "#root/Address/ZipCode",
                            "title": "Zipcode",
                            "type": "string",
                            "default": "",
                            "examples": [
                                ""
                            ],
                            "pattern": "^.*$"
                        },
                        "County": {
                            "$id": "#root/Address/County",
                            "title": "County",
                            "type": "null",
                            "default": None
                        },
                        "Country": {
                            "$id": "#root/Address/Country",
                            "title": "Country",
                            "type": "null",
                            "default": None
                        },
                        "CountryCode": {
                            "$id": "#root/Address/CountryCode",
                            "title": "Countrycode",
                            "type": "null",
                            "default": None
                        },
                        "CountryName": {
                            "$id": "#root/Address/CountryName",
                            "title": "Countryname",
                            "type": "null",
                            "default": None
                        },
                        "StateProvince": {
                            "$id": "#root/Address/StateProvince",
                            "title": "Stateprovince",
                            "type": "null",
                            "default": None
                        },
                        "StateName": {
                            "$id": "#root/Address/StateName",
                            "title": "Statename",
                            "type": "string",
                            "default": "",
                            "examples": [
                                ""
                            ],
                            "pattern": "^.*$"
                        },
                        "DMAddressTypeID": {
                            "$id": "#root/Address/DMAddressTypeID",
                            "title": "Dmaddresstypeid",
                            "type": "integer",
                            "examples": [
                                0
                            ],
                            "default": 0
                        },
                        "PhoneNumber": {
                            "$id": "#root/Address/PhoneNumber",
                            "title": "Phonenumber",
                            "type": "null",
                            "default": None
                        },
                        "StateOrCountryName": {
                            "$id": "#root/Address/StateOrCountryName",
                            "title": "Stateorcountryname",
                            "type": "null",
                            "default": None
                        },
                        "UnparsedAddress": {
                            "$id": "#root/Address/UnparsedAddress",
                            "title": "Unparsedaddress",
                            "type": "string",
                            "default": "",
                            "examples": [
                                ""
                            ],
                            "pattern": "^.*$"
                        },
                        "StateAndCountry": {
                            "$id": "#root/Address/StateAndCountry",
                            "title": "Stateandcountry",
                            "type": "string",
                            "default": "",
                            "examples": [
                                ""
                            ],
                            "pattern": "^.*$"
                        },
                        "FullAddress": {
                            "$id": "#root/Address/FullAddress",
                            "title": "Fulladdress",
                            "type": "string",
                            "default": "",
                            "pattern": f"^{self.get('company_account_name')} test str new$"
                        },
                        "FullAddressWithoutZip": {
                            "$id": "#root/Address/FullAddressWithoutZip",
                            "title": "Fulladdresswithoutzip",
                            "type": "string",
                            "default": "",
                            "pattern": f"^{self.get('company_account_name')} test str new$"
                        },
                        "MailingFullAddress": {
                            "$id": "#root/Address/MailingFullAddress",
                            "title": "Mailingfulladdress",
                            "type": "string",
                            "default": "",
                            "examples": [
                                ""
                            ],
                            "pattern": "^.*$"
                        },
                        "CityStateZip": {
                            "$id": "#root/Address/CityStateZip",
                            "title": "Citystatezip",
                            "type": "string",
                            "default": "",
                            "examples": [
                                ""
                            ],
                            "pattern": "^.*$"
                        }
                    }
                }
                ,
                "UserList": {
                    "$id": "#root/UserList",
                    "title": "Userlist",
                    "type": "array",
                    "default": []
                },
                "IsPanelHidden": {
                    "$id": "#root/IsPanelHidden",
                    "title": "Ispanelhidden",
                    "type": "boolean",
                    "examples": [
                        False
                    ],
                    "default": True
                },
                "AccountPaymentTotal": {
                    "$id": "#root/AccountPaymentTotal",
                    "title": "Accountpaymenttotal",
                    "type": "integer",
                    "examples": [
                        0
                    ],
                    "default": 0
                },
                "OrderNumber": {
                    "$id": "#root/OrderNumber",
                    "title": "Ordernumber",
                    "type": "null",
                    "default": None
                },
                "OrderId": {
                    "$id": "#root/OrderId",
                    "title": "Orderid",
                    "type": "integer",
                    "examples": [
                        0
                    ],
                    "default": 0
                },
                "LastBalance": {
                    "$id": "#root/LastBalance",
                    "title": "Lastbalance",
                    "type": "integer",
                    "examples": [
                        0
                    ],
                    "default": 0
                },
                "AllowDeactivate": {
                    "$id": "#root/AllowDeactivate",
                    "title": "Allowdeactivate",
                    "type": "boolean",
                    "examples": [
                        True
                    ],
                    "default": True
                },
                "Password": {
                    "$id": "#root/Password",
                    "title": "Password",
                    "type": "null",
                    "default": None
                },
                "IsAllowExport": {
                    "$id": "#root/IsAllowExport",
                    "title": "Isallowexport",
                    "type": "boolean",
                    "examples": [
                        False
                    ],
                    "default": True
                },
                "Departments": {
                    "$id": "#root/Departments",
                    "title": "Departments",
                    "type": "null",
                    "default": None
                },
                "AchDetails": {
                    "$id": "#root/AchDetails",
                    "title": "Achdetails",
                    "type": "null",
                    "default": None
                },
                "AccountDetails": {
                    "$id": "#root/AccountDetails",
                    "title": "Accountdetails",
                    "type": "object",
                    "required": [
                        "Id",
                        "AccountId",
                        "OrderItemTypeId",
                        "ProcFeeTypes"
                    ],
                    "properties": {
                        "Id": {
                            "$id": "#root/AccountDetails/Id",
                            "title": "Id",
                            "type": "integer",
                            "examples": [
                                1
                            ],
                            "default": 0
                        },
                        "AccountId": {
                            "$id": "#root/AccountDetails/AccountId",
                            "title": "Accountid",
                            "type": "integer",
                            "examples": [
                                23
                            ],
                            "default": 0
                        },
                        "OrderItemTypeId": {
                            "$id": "#root/AccountDetails/OrderItemTypeId",
                            "title": "Orderitemtypeid",
                            "type": "integer",
                            "examples": [
                                -1
                            ],
                            "default": 0
                        },
                        "ProcFeeTypes": {
                            "$id": "#root/AccountDetails/ProcFeeTypes",
                            "title": "Procfeetypes",
                            "type": "array",
                            "default": []
                        }
                    }
                }

            }
        }

    def __before__(self):
        self.run_dependencies(("company_account_id",))

    def __test__(self):
        self.response = self.session.get(self.get_url(self.api_urls.EditCompanyAccount),
                                         params=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)


if __name__ == '__main__':
    run_test(__file__, browser="none")
