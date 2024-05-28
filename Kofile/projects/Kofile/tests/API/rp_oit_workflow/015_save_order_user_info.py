from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                             # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def schema(self):
        return {
            "type": "object",
            "properties": {
                "OrderId": {"type": "number", "value": self.get("order_id")},
                "AssignedAgentId": {"type": "number"},
                "AgentId": {"type": "number"},
                "WorkstationId": {"type": "number"},
                "OrderStatus": {"type": "number"},
                "PrintTicketCount": {"type": "number"},
                "CreatedWorkstationId": {"type": "number"},
                "CreatedAduserId": {"type": "number"},
                "OrderQueueStatus": {"type": "number"},
                "ReviewStatus": {"type": "number"},
                "TenantId": {"type": "number"},
                "WorkflowStep": {"type": "number"},
                "OrderSearchStatus": {"type": "number"},
                "Priority": {"type": "number"},
                "OrderStatusId": {"type": "number"},
                "FinalizeWorkstationId": {"type": "number"},
                "ContainingItemsCount": {"type": "number"},
                "AgentAdminGroupId": {"type": "number"},
                "PrecedingWorkingDays": {"type": "number"},
                "ProcessAduserId": {"type": "number"},
                "ProcessWorkstationId": {"type": "number"},
                "NoOfDocuments": {"type": "number"},
                "NoOfItems": {"type": "number"},
                "AgentIdHold": {"type": "number"},
                "DocumentWithTaxNumber": {"type": "string"},
                "OrderDate": {"type": ["string", "null"]},
                "AssignedTo": {"type": ["string", "null"]},
                "DisableEditActions": {"type": ["string", "null"]},
                "AgentName": {"type": ["string", "null"]},
                "TenantCode": {"type": ["string", "null"]},
                "DisableEditingPurchasedOrder": {"type": ["string", "null"]},
                "PaymentComment": {"type": ["string", "null"]},
                "WorkstationName": {"type": ["string", "null"]},
                "CapturingTaskStatus": {"type": ["string", "null"]},
                "VerificationTaskStatus": {"type": ["string", "null"]},
                "IndexingTaskStatus": {"type": ["string", "null"]},
                "FinalizeAgentName": {"type": ["string", "null"]},
                "FinalizeShortAgentName": {"type": ["string", "null"]},
                "ShortUserName": {"type": ["string", "null"]},
                "FinalizeWorkstationName": {"type": ["string", "null"]},
                "OrderStatusGroupName": {"type": ["string", "null"]},
                "OrderEvent": {"type": ["string", "null"]},
                "OrderDetails": {"type": ["string", "null"]},
                "ErOrigin": {"type": ["string", "null"]},
                "DocumentNumber": {"type": ["string", "null"]},
                "Comment": {"type": ["string", "null"]},
                "CreatedLocation": {"type": ["string", "null"]},
                "Discount": {"type": ["string", "null"]},
                "GFNumberRange": {"type": ["string", "null"]},
                "TaxNumber": {"type": ["string", "null"]},
                "ErCustomerName": {"type": ["string", "null"]},
                "PackageIdWithoutOrganizationName": {"type": ["string", "null"]},
                "OrderTotal": {"type": ["number", "null"]},
                "FinalizeDate": {"type": "string"},
                "OrderCancellationTime": {"type": "string"},
                "IsReroute": {"type": "boolean", "value": False},
                "IsPSCopyOrCertifiedCopy": {"type": "boolean", "value": False},
                "IsSplitted": {"type": "boolean", "value": False},
                "IsMerged": {"type": "boolean", "value": False},
                "ContainsTodayAdjustment": {"type": "boolean", "value": False},
                "IsAutoCreated": {"type": "boolean", "value": False},
                "IsReviewFinished": {"type": "boolean", "value": False},
                "IsCompanyPayment": {"type": "boolean", "value": False},
                "IsRestore": {"type": "boolean", "value": False},
                "IsReview": {"type": "boolean", "value": False},
                "IsOCRPending": {"type": "boolean", "value": False},
                "IsReceiptPrint": {"type": "boolean", "value": False},
                "IsLocked": {"type": "boolean", "value": False},
                "IsFromLaterCheckout": {"type": "boolean", "value": False},
                "HasCheckPaymentMethod": {"type": "boolean", "value": False},
                "IsFullVoid": {"type": "boolean", "value": False},
                "isPartialVoided": {"type": "boolean", "value": False},
                "IsRecorded": {"type": "boolean", "value": False},
                "IsPaymentIncomplete": {"type": "boolean", "value": False},
                "IsPaidOnClient": {"type": "boolean", "value": False},
                "IsReEntryOrderExpired": {"type": "boolean", "value": False},
                "HaveNote": {"type": "boolean", "value": False},
                "IsAccepted": {"type": "boolean", "value": False},
                "ShowReportDateOption": {"type": "boolean", "value": False},
                "AllowEditPayment": {"type": "boolean", "value": True},
                "AllowEditPaymentNonFinancial": {"type": "boolean", "value": True},
                "AllowOrderVoid": {"type": "boolean", "value": True},
                "IsOrderSaveAvailable": {"type": "boolean", "value": True},
                "OrderItems": {"type": ["object", "null"]},
                "OrderPayments": {"type": ["object", "null"]},
                "OrderHistories": {"type": ["object", "null"]},
                "OrderHeader": {"type": "object",
                                "properties": {
                                    "LocationId": {"type": "number"},
                                    "WorkstationId": {"type": "number"},
                                    "OriginId": {"type": "number"},
                                    "TenantId": {"type": "number"},
                                    "SubmitionDate": {"type": "string"},
                                    "OrderDate": {"type": "string"},
                                    "HeaderModified": {"type": "boolean", "value": True},
                                    "SendEmailReciept": {"type": "boolean", "value": True},
                                    "ReceivedByMail": {"type": "boolean", "value": False},
                                    "IsEditNonFinancialHeader": {"type": "boolean", "value": False},
                                    "IsReceivedByMailVisible": {"type": "boolean", "value": False},
                                    "CanEditReceiveDateByUserGroup": {"type": "boolean", "value": False},
                                    "AllowEditReceiveDateByOrigin": {"type": "boolean", "value": False},
                                    "AllowHardcodedReceiveTimeByOrigin": {"type": "boolean", "value": False},
                                    "OrderNumber": {"type": ["string", "null"]},
                                    "PackageId": {"type": ["string", "null"]},
                                    "Origin": {"type": ["string", "null"]},
                                    "ProcessingOrigin": {"type": ["string", "null"]},
                                    "TrackingId": {"type": ["string", "null"]},
                                    "Location": {"type": ["string", "null"]},
                                    "UpdateOriginal": {"type": ["string", "null"]},
                                    "DepartmentInfo": {"type": ["string", "null"]},
                                    "ReceiveDateTime": {"type": ["string", "null"]},
                                    "HardcodedReceiveTimeByOrigin": {"type": ["string", "null"]},
                                    "LastReceiveDate": {"type": ["string", "null"]},
                                    "ERecording": {"type": ["string", "null"]},
                                    "Refundee": {"type": ["string", "null"]},
                                    "TenantCode": {"type": ["string", "null"]},
                                    "OrderPaymentTypeDesc": {"type": ["string", "null"]},
                                    "CompanyAccount": {"type": ["object", "null"]},
                                    "PackageIdWithoutOrganizationName": {"type": ["object", "null"]},
                                    "OrderUser": {"type": "object",
                                                  "properties": {
                                                      "UserType": {"type": "number"},
                                                      "User": {"type": ["object", "null"]},
                                                      "AccountDetails": {"type": ["object", "null"]},
                                                      "PersonalUserId": {"type": "number"},
                                                      "IsOrganization": {"type": "boolean", "value": False},
                                                  }},
                                }}
            }
        }

    def __before__(self):
        self.run_dependencies(("user_id", "address_id", "order_id"))

    @property
    def post_data(self):
        data = self.api_test_data.save_order_user_info_data.copy()
        data["PersonalUserId"] = self.get("user_id")
        data["User[Address][AddressId]"] = self.get("address_id")
        data["User[Address][Email]"] = self.data.env.email_user
        return data

    def __test__(self):
        params = (('orderId', self.get("order_id")), ('isEmailReplesment', 'true'),)
        self.response = self.session.post(self.get_url(self.api_urls.SaveOrderUserInfo), params=params, data=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)


if __name__ == '__main__':
    run_test(__file__, browser="none")
