from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                                # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def schema(self):
        discount = self.api_test_data.discount
        return {
            "type": "object",
            "properties": {
                "isReceivedByMailVisible": {"type": "boolean", "value": True},
                "orderItemsForSummary": {"type": "array", "items": {
                    "type": "object",
                    "properties": {
                        "OrderItemType_Id": {"type": "number", "value": 1},
                        "OrderItemId": {"type": "number", "value": self.get("second_oit_id")},
                        "OrderItemType_Value": {"type": "string", "value": "Real Property Recordings"},
                        "Document_DocumentType": {"type": "string", "value": "AB"},
                        "FeeParameterCriteria_NoOfCopies": {"type": "string", "value": "0"},
                        "FeeParameterCriteria_NoOfAdditionCopy": {"type": "string", "value": "0"},
                        "FeeParameterCriteria_NoOfCertifications": {"type": "string", "value": "0"},
                        "FeeParameterCriteria_NoOfPageOrCopy": {"type": "number", "value": 1},
                        "Price": {"type": "number", "value": -10.01},
                        "Document_RecordedYear": {"type": "string"},
                        "Document_DocAndAppNum": {"type": "string"},
                        "Address": {"type": ["object", "null"]},
                        "GFNumber": {"type": "string"},
                        "OrderItemRoute": {"type": "string"},
                        "OrderItemRouteRejectionDesc": {"type": "string"},
                        "Document_InstrumentNumber": {"type": "string"},
                        "OrderItemStatusString": {"type": "string", "value": "Reviewed"},
                        "OrderItemDiscount": {"type": "string", "value": discount.get("code")},
                        "DiscountComment": {"type": "string", "value": discount.get("comment")},
                        "Document_CanCheckOut": {"type": "boolean", "value": False},
                        "IsOrderItemRouteActive": {"type": "boolean", "value": False},
                        "IsOrderItemRouteAprroved": {"type": "boolean", "value": False},
                        "IsOrderItemRouteRejected": {"type": "boolean", "value": False},
                        "HasPrintStamp": {"type": "boolean", "value": False},
                        "EnablePreviewViewerMargins": {"type": "boolean", "value": False},
                        "HasManualDiscount": {"type": "boolean", "value": False},
                        "IsSerialNumberVisible": {"type": "boolean", "value": False},
                        "ReturnByEmail": {"type": "boolean", "value": False},
                        "HaveNote": {"type": "boolean", "value": False},
                        "CanPrintApplication": {"type": "boolean", "value": False},
                        "CanPrintApplicationsSeamless": {"type": "boolean", "value": False},
                        "CanPrintApplicationsSeamlessSSNRedacted": {"type": "boolean", "value": False},
                        "CanPrintApplicationSSNRedacted": {"type": "boolean", "value": False},
                        "CanPrintCertificateForm": {"type": "boolean", "value": False},
                        "CanPrintCertificateVerification": {"type": "boolean", "value": False},
                        "CanPrintCommonApplication": {"type": "boolean", "value": False},
                        "CanReviewFromSummary": {"type": "boolean", "value": False},
                        "CanDeleteOrderItem": {"type": "boolean", "value": False},
                        "IsCertifiedCopy": {"type": "boolean", "value": False},
                        "IsCopyForPrior": {"type": "boolean", "value": False},
                        "IsDiscountVisible": {"type": "boolean", "value": True},
                        "ShowImageViewer": {"type": "boolean", "value": True},
                        "CanEditOrderItem": {"type": "boolean", "value": True},
                        "CanAddCopiesOrderItem": {"type": "boolean", "value": True},
                        "CanSetSerialNumber": {"type": "boolean", "value": True},
                        "CanPrioritizeOrderItems": {"type": "boolean", "value": True},
                        "IsCopyConsolidationEnabled": {"type": "boolean", "value": True},
                        "Duplicated_From": {"type": "number"},
                        "OrderItemCopyMaxCount": {"type": "number", "value": 50},
                        "ServiceTypeId": {"type": "number"},
                        "DocumentGroupId": {"type": "number"},
                        "AvalibleDiscounts": {"type": "array"},
                        "RouteOptions": {"type": "array"},
                        "RequiredActions": {"type": "array"},
                        "SerialNumberType": {"type": "string"},
                        "SerialNumber": {"type": "string"},
                        "EndSerialNumber": {"type": "string"},
                        "SerialNumberDefaultType": {"type": ["string", "null"]},
                    }
                }},
            }
        }

    @property
    def post_data(self):
        return self.api_test_data.duplicate_order_item_data

    def __before__(self):
        self.run_dependencies(("order_id", "first_oit_id", "second_oit_id"))

    def __test__(self):
        params = (
            ('orderId', self.get("order_id")),
            ('OrderItemId', self.get("first_oit_id")),
        )
        self.set_content_type('application/json')
        self.response = self.session.post(self.get_url(self.api_urls.DeleteOrderItem), params=params,
                                          json=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        self.validate(instance=self.response.json(), schema=self.schema)
        self.set("delete_oit", True)


if __name__ == '__main__':
    run_test(__file__, browser="none")
