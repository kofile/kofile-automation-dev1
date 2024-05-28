from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    - Go to CRS and create new order
    - Select RP OIT
    - Fill Properties and other required fields and click 'Add to Order'
    - Click 'add new order item' and select OIT with properties tab
    - In properties tab click 'Copy Property' link - Click 'Copy From Prior Order Item' link
    -> Property information from previous OIt is filled correspondingly
    - Fill all required fields and finalize Order - Get One of finalized Order's OIT document number
    
    - Go to Order queue and add OIT with Properties
    - In Properties tab click 'Copy Property' link
    - Input 'year and document number' from previous steps
    -> Properties information is filled correspondingly"""


class test(TestParent):                                                                              # noqa
    user_index = 2

    def __init__(self, data):
        data["OIT"] = "RP_Recordings"
        super(test, self).__init__(data, __name__)

    def check_copied_properties(self, blocks, properties):
        copied_blocks = self.lib.CRS.order_entry.get_property_blocks()
        assert copied_blocks == blocks, f"Expected copied property blocks: '{blocks}'. Actual: '{copied_blocks}'"
        desc_copy = self.lib.CRS.order_entry.get_properties_desc_values()
        survey_copy = self.lib.CRS.order_entry.get_properties_survey_values()
        subdivision_copy = self.lib.CRS.order_entry.get_properties_subdivision_values()
        address_copy = self.lib.CRS.order_entry.get_properties_address_values()
        desc2_copy = self.lib.CRS.order_entry.get_properties_desc_values(
            self.lib.CRS.order_entry.get_property_block_index("newdesc", 2, all_blocks=copied_blocks))
        survey2_copy = self.lib.CRS.order_entry.get_properties_survey_values(
            self.lib.CRS.order_entry.get_property_block_index("survey", 2, all_blocks=copied_blocks))
        subdivision2_copy = self.lib.CRS.order_entry.get_properties_subdivision_values(
            self.lib.CRS.order_entry.get_property_block_index("subdivision", 2, all_blocks=copied_blocks))
        address2_copy = self.lib.CRS.order_entry.get_properties_address_values(
            self.lib.CRS.order_entry.get_property_block_index("propaddress", 2, all_blocks=copied_blocks))
        properties_copy = {"desc": desc_copy, "survey": survey_copy, "subdivision": subdivision_copy,
                           "address": address_copy, "desc2": desc2_copy, "survey2": survey2_copy,
                           "subdivision2": subdivision2_copy, "address2": address2_copy}
        assert properties_copy == properties, f"Expected properties: '{properties}'. Actual: '{properties_copy}'"

    def __test__(self):
        self.atom.CRS.general.go_to_crs(self.user_index)
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.fill_order_header_name()
        self.lib.general_helper.find_and_click(self.lib.CRS.order_entry.tab_locator("Properties"))
        # add blocks
        before_add = self.lib.CRS.order_entry.get_property_blocks().values()
        self.lib.CRS.order_entry.click_properties__add_desc() if "desc" not in before_add else None
        self.lib.CRS.order_entry.click_properties__add_survey() if "survey" not in before_add else None
        self.lib.CRS.order_entry.click_properties__add_subdivision() if "subdivision" not in before_add else None
        self.lib.CRS.order_entry.click_properties__add_address() if "propaddress" not in before_add else None
        # fill blocks
        desc = self.lib.CRS.order_entry.fill_properties_desc(return_values=True)
        survey = self.lib.CRS.order_entry.fill_properties_survey(return_values=True)
        subdivision = self.lib.CRS.order_entry.fill_properties_subdivision(return_values=True)
        address = self.lib.CRS.order_entry.fill_properties_address(return_values=True)
        # add and fill additional blocks
        desc2 = self.lib.CRS.order_entry.click_properties__add_desc(2)
        survey2 = self.lib.CRS.order_entry.click_properties__add_survey(2)
        subdivision2 = self.lib.CRS.order_entry.click_properties__add_subdivision(2)
        address2 = self.lib.CRS.order_entry.click_properties__add_address(2)
        properties = {"desc": desc, "survey": survey, "subdivision": subdivision, "address": address,
                      "desc2": desc2, "survey2": survey2, "subdivision2": subdivision2, "address2": address2}
        blocks = self.lib.CRS.order_entry.get_property_blocks()
        self.atom.CRS.order_entry.one_oit_to_summary()

        # Add OIT, copy properties and verify
        self.lib.CRS.order_summary.click_new_order_item_icon()
        self.atom.CRS.order_entry.select_order_type()
        self.lib.general_helper.find_and_click(self.lib.CRS.order_entry.tab_locator("Properties"))
        self.lib.CRS.order_entry.copy_properties()
        self.check_copied_properties(blocks, properties)
        self.atom.CRS.order_entry.one_oit_to_summary()
        self.atom.CRS.add_payment.finalize_order()

        # Create new order, copy properties from previous document and verify
        self.atom.CRS.general.go_to_crs(self.user_index)
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.fill_order_header_name()
        self.lib.general_helper.find_and_click(self.lib.CRS.order_entry.tab_locator("Properties"))
        self.lib.CRS.order_entry.copy_properties(self.data["doc_year"], self.data["doc_number"])
        # TODO 'propaddress' blocks are not copied. BUG or feature? Wait clarification from Stella
        self.check_copied_properties(blocks, properties)
        self.atom.CRS.order_entry.one_oit_to_summary()
        self.atom.CRS.add_payment.finalize_order()


if __name__ == '__main__':
    run_test(__file__)
