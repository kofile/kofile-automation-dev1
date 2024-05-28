from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    - Go to CRS and create new order
    - Select RP OIT
    - Under Properties tab click add New Desc, New Subdivision, New Survey, New Property Address links
    - Click delete icon for each opened block
    - Click add New Desc, New Subdivision, New Survey, New Property Address links
    - Fill fields for each block
    - Change blocks ordering (via up/down icons)
    - Fill all required fields and finalize order"""


class test(TestParent):                                                                              # noqa
    user_index = 2

    def __init__(self, data):
        data["OIT"] = "RP_Recordings"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs(self.user_index)
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.fill_order_header_name()

        self.lib.general_helper.find_and_click(self.lib.CRS.order_entry.tab_locator("Properties"))
        blocks_before = len(self.lib.CRS.order_entry.get_property_blocks())
        # Add blocks
        self.lib.CRS.order_entry.click_properties__add_desc()
        self.lib.CRS.order_entry.click_properties__add_survey()
        self.lib.CRS.order_entry.click_properties__add_subdivision()
        self.lib.CRS.order_entry.click_properties__add_address()

        blocks = self.lib.CRS.order_entry.get_property_blocks()
        self.lib.CRS.order_entry.click_properties__up_button(2)  # move second block UP
        blocks_up = self.lib.CRS.order_entry.get_property_blocks()
        assert blocks_up[1] == blocks[2], "Second block is not moved UP"
        self.lib.CRS.order_entry.click_properties__down_button(1)  # move 1-st block DOWN
        blocks_down = self.lib.CRS.order_entry.get_property_blocks()
        assert blocks_down == blocks, "First block is not moved down"

        # Delete all added blocks
        self.lib.CRS.order_entry.click_properties__delete_button(blocks_before + 4)
        self.lib.CRS.order_entry.click_properties__delete_button(blocks_before + 3)
        self.lib.CRS.order_entry.click_properties__delete_button(blocks_before + 2)
        self.lib.CRS.order_entry.click_properties__delete_button(blocks_before + 1)
        blocks_del = self.lib.CRS.order_entry.get_property_blocks()
        assert len(blocks_del) == blocks_before, f"Incorrect block count after deletion"

        before_add = blocks_del.values()
        self.lib.CRS.order_entry.click_properties__add_desc()
        self.lib.CRS.order_entry.click_properties__add_desc(2 if "desc" not in before_add else 3)
        self.lib.CRS.order_entry.click_properties__add_survey()
        self.lib.CRS.order_entry.click_properties__add_survey(2 if "survey" not in before_add else 3)
        self.lib.CRS.order_entry.click_properties__add_subdivision()
        self.lib.CRS.order_entry.click_properties__add_subdivision(2 if "subdivision" not in before_add else 3)
        self.lib.CRS.order_entry.click_properties__add_address()
        self.lib.CRS.order_entry.click_properties__add_address(2 if "propaddress" not in before_add else 3)

        self.atom.CRS.order_entry.one_oit_to_summary()
        self.atom.CRS.add_payment.finalize_order()


if __name__ == '__main__':
    run_test(__file__)
