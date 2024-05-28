from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
"""

tags = ['API']


class test(ApiTestParent):                                                                               # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    @property
    def schema(self):
        discount = self.api_test_data.discount
        return {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "OrderItemType_Id": {"type": "number", "value": 1},
                    "OrderItemId": {"type": "number"},
                    "OrderItemType_Value": {"type": "string", "value": "Real Property Recordings"},
                    "Document_DocumentType": {"type": "string", "value": "AJ"},
                    "FeeParameterCriteria_NoOfPageOrCopy": {"type": "number"},
                    "FeeParameterCriteria_NoOfCopies": {"type": "string"},
                    "FeeParameterCriteria_NoOfAdditionCopy": {"type": "string"},
                    "FeeParameterCriteria_NoOfCertifications": {"type": "string"},
                    "Price": {"type": "number", "value": 93.0},
                    "Document_RecordedYear": {"type": "string"},
                    "Document_DocAndAppNum": {"type": "string"},
                    "Document_InstrumentNumber": {"type": "string"},
                    "OrderItemStatusString": {"type": "string", "value": "Reviewed"},
                    "Document_CanCheckOut": {"type": "boolean", "value": False},
                    "Duplicated_From": {"type": "number"},
                    "AvalibleDiscounts": {"type": "array"},
                    "IsDiscountVisible": {"type": "boolean", "value": True},
                    "OrderItemDiscount": {"type": "string", "value": discount.get("cade")},
                    "DiscountComment": {"type": "string", "value": discount.get("comment")},
                    "ShowImageViewer": {"type": "boolean", "value": True},
                    "RequiredActions": {"type": "array"},
                    "SerialNumberType": {"type": "string"},
                    "SerialNumberDefaultType": {"type": ["string", "null"]},
                    "SerialNumber": {"type": "string"},
                    "EndSerialNumber": {"type": "string"},
                    "OrderItemCopyMaxCount": {"type": "number", "value": 50},
                    "IsSerialNumberVisible": {"type": "boolean", "value": False},
                    "HaveNote": {"type": "boolean", "value": False},
                    "CanEditOrderItem": {"type": "boolean", "value": True},
                    "CanAddCopiesOrderItem": {"type": "boolean", "value": True},
                    "CanSetSerialNumber": {"type": "boolean", "value": True},
                    "CanPrintApplication": {"type": "boolean", "value": False},
                    "CanPrintApplicationsSeamless": {"type": "boolean", "value": False},
                    "CanPrintApplicationsSeamlessSSNRedacted": {"type": "boolean", "value": False},
                    "CanPrintApplicationSSNRedacted": {"type": "boolean", "value": False},
                    "CanPrintCertificateForm": {"type": "boolean", "value": False},
                    "CanPrintCertificateVerification": {"type": "boolean", "value": False},
                    "CanPrintCommonApplication": {"type": "boolean", "value": False},
                    "CanDeleteOrderItem": {"type": "boolean", "value": True},
                    "CanPrioritizeOrderItems": {"type": "boolean", "value": True},
                    "IsCertifiedCopy": {"type": "boolean", "value": False},
                    "IsCopyForPrior": {"type": "boolean", "value": False},
                    "IsCopyConsolidationEnabled": {"type": "boolean", "value": True},
                    "CanReviewFromSummary": {"type": "boolean", "value": False},
                    "DocumentGroupId": {"type": "number"},
                    "ServiceTypeId": {"type": "number"},
                    "GFNumber": {"type": "string"},
                    "ReturnByEmail": {"type": "boolean"},
                    "Address": {"type": ["object", "null"]},
                    "HasManualDiscount": {"type": "boolean", "value": False},
                    "RouteOptions": {"type": "array"},
                    "OrderItemRoute": {"type": "string"},
                    "OrderItemRouteRejectionDesc": {"type": "string"},
                    "IsOrderItemRouteActive": {"type": "boolean", "value": False},
                    "IsOrderItemRouteAprroved": {"type": "boolean", "value": False},
                    "IsOrderItemRouteRejected": {"type": "boolean", "value": False},
                    "HasPrintStamp": {"type": "boolean", "value": False},
                    "EnablePreviewViewerMargins": {"type": "boolean", "value": False},
                }
            }
        }

    @property
    def post_data(self):
        return self.api_test_data.duplicate_order_item_data

    def __before__(self):
        self.run_dependencies(("order_id", "order_item_id"))

    def __test__(self):
        params = (('orderId', self.get("order_id")), ('OrderItemId', self.get("order_item_id")),
                  ('orderItemTypeId', '1'), ('noOfCopies', "1"), ('docGroupId', '1'), ('serviceTypeId', '1'),)
        self.set_content_type('application/json')
        self.response = self.session.post(self.get_url(self.api_urls.DuplicateOrderItem), params=params,
                                          json=self.post_data)
        assert self.response.status_code == 200, f"Actual response status: {self.response.status_code}"
        assert len(self.response.json()) == 2
        self.validate(instance=self.response.json(), schema=self.schema)
        first_oit, second_oit = self.response.json()
        self.set("first_oit_id", first_oit.get("OrderItemId"))
        self.set("second_oit_id", second_oit.get("OrderItemId"))


if __name__ == '__main__':
    run_test(__file__, browser="none")
