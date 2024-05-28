from projects.Kofile.Lib.general_helpers import GeneralHelpers
from projects.Kofile.Lib.test_parent import PagesParent
from projects.Kofile.pages.CRS_OrderData import CRSOrderData

"""
all kind of fields throughout the entire CRS
"""
CRS_OrderData = CRSOrderData()


class CRSFields(PagesParent):
    def __init__(self):
        super(CRSFields, self).__init__()

    @staticmethod
    def page_input_by_oi_index_by_property_index(order_item_index=0, property_index=0):
        """
        returns Page input field locator by order item index,
        by property index,
        if error returns None

        order item index starts from 0
        """
        return GeneralHelpers.make_locator(CRS_OrderData._inp_properties_desc, order_item_index, property_index, "Page")

    @staticmethod
    def volume_input_by_oi_index_by_property_index(order_item_index=0, property_index=0):
        """
        returns Volume input field locator by order item index,
        by property index,
        if error returns None

        order item index starts from 0
        """
        return GeneralHelpers.make_locator(CRS_OrderData._inp_properties_desc, order_item_index, property_index,
                                           "Volume")

    @staticmethod
    def subdivision_input_by_oi_index_by_property_index(order_item_index=0, property_index=0):
        """
        returns Subdivision input field locator by order item index,
        by property index,
        if error returns None

        order item index starts from 0
        """
        return GeneralHelpers.make_locator(CRS_OrderData._inp_properties_desc, order_item_index, property_index,
                                           "Subdivision")

    @staticmethod
    def ncb_input_by_oi_index_by_property_index(order_item_index=0, property_index=0):
        """
        returns NCB input field locator by order item index,
        by property index,
        if error returns None

        order item index starts from 0
        """
        return GeneralHelpers.make_locator(CRS_OrderData._inp_properties_desc, order_item_index, property_index,
                                           "Block2")

    @staticmethod
    def block_input_by_oi_index_by_property_index(order_item_index=0, property_index=0):
        """
        returns Block input field locator by order item index,
        by property index,
        if error returns None

        order item index starts from 0
        """
        return GeneralHelpers.make_locator(CRS_OrderData._inp_properties_desc, order_item_index, property_index,
                                           "Block")

    @staticmethod
    def lot_input_by_oi_index_by_property_index(order_item_index=0, property_index=0):
        """
        returns Lot input field locator by order item index,
        by property index,
        if error returns None

        order item index starts from 0
        """
        return GeneralHelpers.make_locator(CRS_OrderData._inp_properties_desc, order_item_index, property_index, "Lot")

    @staticmethod
    def county_block_input_by_oi_index_by_property_index(order_item_index=0, property_index=0):
        """
        returns County Block input field locator by order item index,
        by property index,
        if error returns None

        order item index starts from 0
        """
        return GeneralHelpers.make_locator(CRS_OrderData._inp_properties_desc, order_item_index, property_index,
                                           "Block3")

    @staticmethod
    def no_of_pages_input_by_oi_index(order_item_index=0):
        """
        returns Number of Pages input field locator by order item index,
        if error returns None

        order item index starts from 0
        """
        return GeneralHelpers.make_locator(CRS_OrderData._inp_fee_parameter_criteria, order_item_index, "NoOfPage")

    @staticmethod
    def document_type_ddl_by_oi_index(order_item_index=0):
        """
        returns Document Type dropdown locator by order item index,
        if error returns None

        order item index starts from 0
        """
        return GeneralHelpers.make_locator(CRS_OrderData._ddl_doc_type, order_item_index)
