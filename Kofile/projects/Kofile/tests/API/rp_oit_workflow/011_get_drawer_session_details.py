from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                        # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def schema(self):
        return {
            "type": "object",
            "properties": {
                "RecordedDate": {"type": ["string", "null"]},
                "IsAdmin": {"type": "boolean"},
                "InitialBalance": {"type": "string"},
                "maxValue": {"type": "string"},
                "errorMessage": {"type": ["string", "null"]},
                "DrawerSessionDetails": {"type": "object",
                                         "properties": {
                                             "Id": {"type": "number"},
                                             "WorkstationId": {"type": "number"},
                                             "IsIndividual": {"type": "boolean"},
                                             "DrawerId": {"type": "number"},
                                             "BalancePostId": {"type": "number"},
                                             "DrawerName": {"type": ["string", "null"]},
                                             "DrawerDescription": {"type": ["string", "null"]},
                                             "TenantCode": {"type": ["string", "null"]},
                                             "InitAmount": {"type": "number"},
                                             "RecordedDate": {"type": ["string", "null"]},
                                             "InitailizeDateTime": {"type": "string"},
                                             "PostedDate": {"type": "string"},
                                             "DisplayName": {"type": "string"},
                                             "DisplayPostedDate": {"type": "string"},
                                             "DisplayInitailizeDateTime": {"type": "string"},
                                             "IsActive": {"type": "boolean"},
                                             "MaxValue": {"type": "number"},
                                             "TenantId": {"type": "number"},
                                             "ErrorMessage": {"type": ["string", "null"]},
                                             "AgentInfo": {"type": ["object", "null"],
                                                           "properties": {
                                                               "AgentId": {"type": "number"},
                                                               "AgentGuid": {"type": "string"},
                                                               "FirstName": {"type": ["string", "null"]},
                                                               "LastName": {"type": ["string", "null"]},
                                                               "MiddleName": {"type": ["string", "null"]},
                                                               "Suffix": {"type": ["string", "null"]},
                                                               "DomainName": {"type": ["string", "null"]},
                                                               "EmailId": {"type": ["number", "null"]},
                                                               "IsEnabled": {"type": "boolean"},
                                                               "IsSuperAdmin": {"type": "boolean"},
                                                               "UserGroupId": {"type": "number"},
                                                               "WorkstationId": {"type": "number"},
                                                               "LocationId": {"type": "number"},
                                                               "OriginId": {"type": "number"},
                                                               "TenantId": {"type": "number"},
                                                               "AdminGroupId": {"type": "number"},
                                                               "UserGroupName": {"type": ["string", "null"]},
                                                               "Workstation": {"type": ["string", "null"]},
                                                               "Location": {"type": ["string", "null"]},
                                                               "Origin": {"type": ["string", "null"]},
                                                               "TenantCode": {"type": ["string", "null"]},
                                                               "DefaultUrl": {"type": ["string", "null"]},
                                                               "UserName": {"type": "string"},
                                                               "ShortUserName": {"type": "string"},
                                                           }},
                                         }},
            }
        }

    def __test__(self):
        self.response = self.session.get(self.get_url(self.api_urls.GetDrawerSessionDetails))
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)


if __name__ == '__main__':
    run_test(__file__, browser="none")
