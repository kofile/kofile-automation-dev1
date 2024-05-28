"""Add Note"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
1. Navigate to CRS 
2. Add new OIT
3. Click Add Note
4. Add Description and click save
5. Click Edit and change description
6. Click Save
7. Click add to order
8. Finalize order
"""

tags = []


class test(TestParent):                                                                           # noqa
    datetime_format = "%m/%d/%Y %#H:%M"

    def __init__(self, data, user_index=0):
        self.user_index = user_index
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs(self.user_index)
        self.lib.CRS.crs.go_to_order_queue()
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.fill_order_header_name()

        note_tab_loc = self.lib.CRS.order_entry.tab_locator('Notes')
        self.lib.general_helper.find_and_click(note_tab_loc)
        self.lib.general_helper.find_and_click(self.pages.CRS.order_entry.add_note_btn)
        description_text = "Description for Payment on Accounts"
        self.lib.general_helper.find_and_send_keys(self.pages.CRS.order_entry.note_description, description_text)
        self.lib.general_helper.find_and_click(self.pages.CRS.order_entry.save_note)
        user_name = self.lib.CRS.crs.assign_user_name()
        date = self.lib.general_helper.get_current_date().strftime(self.datetime_format)
        desc_text = f"{user_name} {date}"
        self.lib.CRS.order_queue.check_note_description(desc_text)
        self.lib.CRS.order_queue.check_note_description(description_text)

        self.lib.general_helper.find_and_click(self.pages.CRS.order_entry.edit_note)
        self.lib.general_helper.find_and_click(self.pages.CRS.order_entry.save_note)
        date = self.lib.general_helper.get_current_date().strftime(self.datetime_format)
        desc_text_edit = f"\n{user_name} {date}"
        self.lib.CRS.order_queue.check_note_description(desc_text)
        self.lib.CRS.order_queue.check_note_description(desc_text_edit)
        self.lib.CRS.order_queue.check_note_description(description_text)

        self.lib.general_helper.find_and_click(self.pages.CRS.order_entry.edit_note)
        self.lib.general_helper.find_and_send_keys(self.pages.CRS.order_entry.note_description, "Edit")
        self.lib.general_helper.find_and_click(self.pages.CRS.order_entry.save_note)
        date_day = self.lib.general_helper.get_current_date().strftime(self.datetime_format)
        desc_text_edit = f"{user_name} {date_day}"
        self.lib.CRS.order_queue.check_note_description(desc_text_edit)
        self.lib.CRS.order_queue.check_note_description("Edit")
        self.lib.required_fields.crs_fill_required_fields()
        self.atom.CRS.order_entry.one_oit_to_summary()

        self.lib.general_helper.find_and_click(self.pages.CRS.order_queue.note_success_icon)
        desc_text_edit = f"{user_name} {date_day}"
        self.lib.CRS.order_queue.check_note_pop_up_text(desc_text_edit)
        self.lib.CRS.order_queue.check_note_pop_up_text("Edit")

        self.atom.CRS.add_payment.finalize_order()
        self.lib.general_helper.find_and_click(self.pages.CRS.order_queue.note_success_icon)
        self.lib.CRS.order_queue.check_note_pop_up_text(desc_text_edit)
        self.lib.CRS.order_queue.check_note_pop_up_text("Edit")


if __name__ == '__main__':
    run_test(__file__)
