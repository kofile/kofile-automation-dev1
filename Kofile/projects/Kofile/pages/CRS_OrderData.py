"""
Order Data tabs and elements (can be common for several tabs)
"""
from projects.Kofile.Lib.test_parent import PagesParent

"""
Order Item tab
"""


class CRSOrderData(PagesParent):
    def __init__(self):
        super(CRSOrderData, self).__init__()

    _ddl_doc_type = ('xpath',
                     '//select[@name="Order.OrderItems[%s].Document.DocumentTypeId"]',
                     'Document type dropdown')

    _inp_fee_parameter_criteria = ('xpath',
                                   '//input[@name="Order.OrderItems[%s].FeeParameterCriteria.%s"]',
                                   'Text input of Fee Parameter Criteria')

    _inp_properties_desc = ('xpath',
                            '//*[@name="Order.OrderItems[%s].Document.Properties[%s].LegalDescription.%s"]',
                            'Legal description inputs in Properties tab')
