"""VA-10493_Alabama: Indexing/Verification/Re-Index - Plat Slide Field"""

from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    - Create a 'Map AL' order
    - In Order Item tab, enter as many number of pages as the wanted number of Slides (Pages) to enter
    - In Document tab, look up for pre-existing Slide values by typing a substring (ex. "001") 
    (please note that duplicate values are not allowed on the same document)
    - As the lookup list is displayed, verify that all values in lookup list contain the entered substring
    - Select the first value from lookup list and finalize the order
    - Process the order through Capture step to Indexing and check the Slide value in Indexing
    - Process the order to Verification and check the Slide value in Verification
    """

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: Order is processed from Order Queue to Archive
        """

        # create an order with OI from csv file
        self.lib.general_helper.check_order_type()
        no_of_pages = "1"
        slide_entered_value = "001"
        self.atom.CRS.general.go_to_crs()
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.fill_order_header_name()
        self.atom.CRS.order_entry.select_order_type()
        doc_type = self.data['config'].test_data(f"{self.data.OIT}.order_doc_type")
        self.lib.general_helper.select_by_text(self.pages.CRS.order_entry.ddl_order_item_tab_doc_type, doc_type)
        self.atom.CRS.order_entry.order_item_description()

        # enter as many number of pages as the wanted number of Slides to enter
        self.lib.general_helper.find_and_send_keys(self.pages.CRS.order_entry.txt_no_of_pages, no_of_pages)

        # navigate to Document tab and look up for a pre-existing Slide value
        self.lib.general_helper.find_and_click(self.lib.CRS.order_entry.tab_locator("Document"))
        self.lib.general_helper.find_and_send_keys(self.pages.CRS.order_entry.inp_slide_field,
                                                   slide_entered_value)

        # get the lookup list values displayed
        lookup_values = self.lib.general_helper.find_elements(
            self.pages.CRS.order_entry.lkp_slide_lookup_list_options, get_text=True)
        for value in lookup_values:
            assert slide_entered_value in value, f"Slide lookup value '{value}' does NOT contain " \
                                                 f"the entered substring '{slide_entered_value}'"

        # select the first value from lookup list
        self.lib.general_helper.find_and_click(self.pages.CRS.order_entry.lkp_slide_lookup_list_options)
        self.lib.general_helper.reset_focus()

        # get the selected value as it is populated (auto-formatted) in the field
        slide_selected_value = self.lib.general_helper.find(self.pages.CRS.order_entry.inp_slide_field,
                                                            get_attribute="value")

        # finalize the order
        self.atom.CRS.order_entry.one_oit_to_summary()
        self.atom.CRS.add_payment.finalize_order()

        # process through capture to indexing and check the Slide value in Indexing
        self.lib.CRS.order_item_type.capture_step()
        self.lib.CRS.crs.go_to_indexing_queue()
        self.lib.general_helper.find(self.pages.CRS.indexing_queue.btn_administrative, wait_displayed=True)
        self.lib.CRS.crs.click_all_show_all_action_links()
        self.atom.CRS.order_queue.assign_order()
        self.lib.CRS.crs.click_running_man()
        self.actions.wait_for_element_present(self.pages.CRS.indexing_entry.btn_save_and_advance)
        slide_indexing_value = self.lib.general_helper.find(self.pages.CRS.order_entry.inp_slide_field,
                                                            get_attribute="value")
        assert slide_indexing_value == slide_selected_value, \
            f"Slide value in Indexing '{slide_indexing_value}' does NOT equal to value " \
            f"'{slide_selected_value}' selected in Ordering"

        # process to Verification and check the Slide value in Verification
        self.lib.required_fields.crs_fill_required_fields()
        self.lib.CRS.order_item_type.save_order_in_index_entry()
        self.lib.CRS.order_item_type.next_order_in_index_summary()
        self.lib.CRS.crs.go_to_verification_queue()
        self.lib.general_helper.find(self.pages.CRS.indexing_queue.btn_administrative, wait_displayed=True)
        self.lib.CRS.crs.click_all_show_all_action_links()
        self.atom.CRS.order_queue.assign_order()
        self.lib.CRS.crs.click_running_man()
        self.actions.wait_for_element_present(self.pages.CRS.verification_entry.btn_save_and_advance)
        slide_verification_value = self.lib.general_helper.find(self.pages.CRS.order_entry.inp_slide_field,
                                                                get_attribute="value")
        assert slide_verification_value == slide_selected_value, \
            f"Slide value in Verification '{slide_verification_value}' does NOT equal to value " \
            f"'{slide_selected_value}' selected in Ordering"
        self.lib.CRS.order_item_type.save_order_in_verification_entry()
        self.lib.CRS.order_item_type.next_order_in_verification_summary(open_crs_in_end=False)


if __name__ == '__main__':
    run_test(__file__)
