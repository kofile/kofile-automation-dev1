from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):
    payment_name, dep = 'test', 'RealPropertyRecords'

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def post_data(self):
        self.set("type_and_head_search_text", self.payment_name)
        self.set("type_and_head_dep", self.dep)
        return {
            'searchText': self.payment_name,
            'departmentType': self.dep,
        }

    @property
    def schema(self):
        return {
            "definitions": {},
            "title": "Root",
            "type": "array",
            "minItems": 1,
            "default": [],
            "items": {
                "$id": "#root/items",
                "title": "Items",
                "type": "object",
                "required": [
                    "Id",
                    "CurrentId",
                    "TypeId",
                    "TypeCode",
                    "SequenceNumber",
                    "Description",
                    "FirstName",
                    "LastName",
                    "MiddleName",
                    "CombinedName",
                    "LastFirstName",
                    "FirstLastName",
                    "CombinedNameWithSuffix",
                    "FullName",
                    "FullNameWithSuffix",
                    "Prefix",
                    "CoupleName",
                    "LastFirstMiddleNameWithSuffix",
                    "Suffix",
                    "UnparsedName",
                    "MaidenSurname",
                    "NonPersonIndicator",
                    "Addresses",
                    "Extras",
                    "MarriageExtras",
                    "Principal",
                    "Surety",
                    "ResourceId",
                    "IsProxyMarriage",
                    "Is30DayWaiver",
                    "AffidavitApplicantName",
                    "PartyAddress",
                    "HasBeenFlipped",
                    "ParcelId",
                    "IsActive",
                    "IsDirect",
                    "TenantId",
                    "TenantCode"
                ],
                "properties": {
                    "Id": {
                        "$id": "#root/items/Id",
                        "title": "Id",
                        "type": "integer",
                        "default": 0
                    },
                    "CurrentId": {
                        "$id": "#root/items/CurrentId",
                        "title": "Currentid",
                        "type": "string",
                        "pattern": "^\d{1,10}$"
                    },
                    "TypeId": {
                        "$id": "#root/items/TypeId",
                        "title": "Typeid",
                        "type": "integer",
                        "examples": [
                            0
                        ],
                        "default": 0
                    },
                    "TypeCode": {
                        "$id": "#root/items/TypeCode",
                        "title": "Typecode",
                        "type": "null",
                        "default": None
                    },
                    "SequenceNumber": {
                        "$id": "#root/items/SequenceNumber",
                        "title": "Sequencenumber",
                        "type": "integer",
                        "examples": [
                            0
                        ],
                        "default": 0
                    },
                    "Description": {
                        "$id": "#root/items/Description",
                        "title": "Description",
                        "type": "null",
                        "default": None
                    },
                    "FirstName": {
                        "$id": "#root/items/FirstName",
                        "title": "Firstname",
                        "type": "string",
                        "default": "",
                        "examples": [
                            ""
                        ],
                        "pattern": "^.*$"
                    },
                    "LastName": {
                        "$id": "#root/items/LastName",
                        "title": "Lastname",
                        "type": "string",
                        "pattern": f"^{self.payment_name}$"
                    },
                    "MiddleName": {
                        "$id": "#root/items/MiddleName",
                        "title": "Middlename",
                        "type": "null",
                        "default": None
                    },
                    "CombinedName": {
                        "$id": "#root/items/CombinedName",
                        "title": "Combinedname",
                        "type": "null",
                        "default": None
                    },
                    "LastFirstName": {
                        "$id": "#root/items/LastFirstName",
                        "title": "Lastfirstname",
                        "type": "null",
                        "default": None
                    },
                    "FirstLastName": {
                        "$id": "#root/items/FirstLastName",
                        "title": "Firstlastname",
                        "type": "string",
                        "default": "",
                        "pattern": f"^.*$"
                    },
                    "CombinedNameWithSuffix": {
                        "$id": "#root/items/CombinedNameWithSuffix",
                        "title": "Combinednamewithsuffix",
                        "type": "string",
                        "default": "",
                        "pattern": "^.*$"
                    },
                    "FullName": {
                        "$id": "#root/items/FullName",
                        "title": "Fullname",
                        "type": "string",
                        "default": "",
                        "pattern": "^.*$"
                    },
                    "FullNameWithSuffix": {
                        "$id": "#root/items/FullNameWithSuffix",
                        "title": "Fullnamewithsuffix",
                        "type": "string",
                        "default": "",
                        "pattern": "^.*$"
                    },
                    "Prefix": {
                        "$id": "#root/items/Prefix",
                        "title": "Prefix",
                        "type": "string",
                        "default": "",
                        "examples": [
                            "iss"
                        ],
                        "pattern": "^.*$"
                    },
                    "CoupleName": {
                        "$id": "#root/items/CoupleName",
                        "title": "Couplename",
                        "type": "string",
                        "default": "",
                        "pattern": "^.*$"
                    },
                    "LastFirstMiddleNameWithSuffix": {
                        "$id": "#root/items/LastFirstMiddleNameWithSuffix",
                        "title": "Lastfirstmiddlenamewithsuffix",
                        "type": "string",
                        "default": "",
                        "pattern": "^.*$"
                    },
                    "Suffix": {
                        "$id": "#root/items/Suffix",
                        "title": "Suffix",
                        "type": "string",
                        "default": "",
                        "examples": [
                            ""
                        ],
                        "pattern": "^.*$"
                    },
                    "UnparsedName": {
                        "$id": "#root/items/UnparsedName",
                        "title": "Unparsedname",
                        "type": "null",
                        "default": None
                    },
                    "MaidenSurname": {
                        "$id": "#root/items/MaidenSurname",
                        "title": "Maidensurname",
                        "type": "null",
                        "default": None
                    },
                    "NonPersonIndicator": {
                        "$id": "#root/items/NonPersonIndicator",
                        "title": "Nonpersonindicator",
                        "type": "integer",
                        "examples": [
                            0
                        ],
                        "default": 0
                    },
                    "Addresses": {
                        "$id": "#root/items/Addresses",
                        "title": "Addresses",
                        "type": "null",
                        "default": None
                    },
                    "Extras": {
                        "$id": "#root/items/Extras",
                        "title": "Extras",
                        "type": "null",
                        "default": None
                    },
                    "MarriageExtras": {
                        "$id": "#root/items/MarriageExtras",
                        "title": "Marriageextras",
                        "type": "null",
                        "default": None
                    },
                    "Principal": {
                        "$id": "#root/items/Principal",
                        "title": "Principal",
                        "type": "boolean",
                        "examples": [
                            False
                        ],
                        "default": True
                    },
                    "Surety": {
                        "$id": "#root/items/Surety",
                        "title": "Surety",
                        "type": "boolean",
                        "examples": [
                            False
                        ],
                        "default": True
                    },
                    "ResourceId": {
                        "$id": "#root/items/ResourceId",
                        "title": "Resourceid",
                        "type": "integer",
                        "examples": [
                            0
                        ],
                        "default": 0
                    },
                    "IsProxyMarriage": {
                        "$id": "#root/items/IsProxyMarriage",
                        "title": "Isproxymarriage",
                        "type": "boolean",
                        "examples": [
                            False
                        ],
                        "default": True
                    },
                    "Is30DayWaiver": {
                        "$id": "#root/items/Is30DayWaiver",
                        "title": "Is30daywaiver",
                        "type": "boolean",
                        "examples": [
                            False
                        ],
                        "default": True
                    },
                    "AffidavitApplicantName": {
                        "$id": "#root/items/AffidavitApplicantName",
                        "title": "Affidavitapplicantname",
                        "type": "null",
                        "default": None
                    },
                    "PartyAddress": {
                        "$id": "#root/items/PartyAddress",
                        "title": "Partyaddress",
                        "type": "null",
                        "default": None
                    },
                    "HasBeenFlipped": {
                        "$id": "#root/items/HasBeenFlipped",
                        "title": "Hasbeenflipped",
                        "type": "boolean",
                        "examples": [
                            False
                        ],
                        "default": True
                    },
                    "ParcelId": {
                        "$id": "#root/items/ParcelId",
                        "title": "Parcelid",
                        "type": "null",
                        "default": None
                    },
                    "IsActive": {
                        "$id": "#root/items/IsActive",
                        "title": "Isactive",
                        "type": "boolean",
                        "examples": [
                            True
                        ],
                        "default": True
                    },
                    "IsDirect": {
                        "$id": "#root/items/IsDirect",
                        "title": "Isdirect",
                        "type": "boolean",
                        "examples": [
                            False
                        ],
                        "default": True
                    },
                    "TenantId": {
                        "$id": "#root/items/TenantId",
                        "title": "Tenantid",
                        "type": "integer",
                        "examples": [
                            0
                        ],
                        "default": 0
                    },
                    "TenantCode": {
                        "$id": "#root/items/TenantCode",
                        "title": "Tenantcode",
                        "type": "null",
                        "default": None
                    }
                }
            }

        }

    def __test__(self):
        self.response = self.session.get(self.get_url(self.api_urls.GetAllPartyNames),
                                         params=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)
        self.set("type_and_head_record_id", self.response.json()[0]["Id"])


if __name__ == '__main__':
    run_test(__file__, browser="none")
