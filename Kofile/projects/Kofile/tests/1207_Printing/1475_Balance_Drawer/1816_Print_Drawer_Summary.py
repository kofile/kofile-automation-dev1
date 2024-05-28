"""Print Drawer Summary"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Before drawer initialization navigate to Balance Drawer tab 
Navigate to " Initialize Drawer" tab, initialize the Drawer and navigate to Balance Drawer tab
Click the link
Navigate to DB: SELECT TOP 5 * FROM VG69999.DEVICE_JOB order by CREATED_DATE desc
Click "DEVICE_JOB_CONFIG" column
Copy FilePath and find the printed form in Azure in wf-content-tenant-code-print-folder
Now fill in Actual result fields and print Drawer Summary
Click "Yes"
Again click the link and in opened "Note" popup click "No"
Settle the balance and print the Drawer Summary
Find the new printed form in Azure
"""

tags = ['48999_location_2']


class test(TestParent):                                                                                   # noqa

    def __init__(self, data, user_index=3):
        self.user_index = user_index
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.actions.store('msg1', 'You have changed the actual amount. '
                                   'Are you sure you want to print the balance without settle?')
        self.actions.store('msg2', 'Drawer summary printing initiated')
        self.actions.store('actual_val', '15912.00')


        drawer_api = self.api.balance_drawer(self.data, self.user_index)
        self.lib.db_vpn.delete_drawer_session(drawer_id=drawer_api.get_drawer_id())

        self.atom.CRS.general.go_to_crs(self.user_index)
        self.atom.CRS.initialize_drawer.initialize_drawer()
        self.lib.CRS.balance_drawer.go_to_balance_drawer(user_index=self.user_index)
        self.actions.assert_element_present(self.pages.CRS.balance_drawer.lnk_print_drawer_sumamry)
        self.lib.CRS.balance_drawer.click_print_drawer_summary_lnk()
        self.actions.assert_element_text(self.pages.CRS.balance_drawer.pup_print_success_text, self.data.msg2)
        self.lib.general_helper.find_and_click(self.pages.CRS.balance_drawer.pup_success_btn_close)
        self.lib.files.download_and_compare_pdf_new(self.data, "drawer_summary")

        self.lib.CRS.balance_drawer.fill_actual_amount_from_expected("Cash", self.data.actual_val)
        self.lib.CRS.balance_drawer.click_print_drawer_summary_lnk("Note")
        self.actions.assert_element_text(self.pages.CRS.balance_drawer.pup_print_success_text, self.data.msg1)
        self.lib.general_helper.find_and_click(self.pages.CRS.balance_drawer.pup_print_warning_btn_yes)
        self.lib.general_helper.wait_for_spinner()
        self.actions.assert_element_text(self.pages.CRS.balance_drawer.pup_print_success_text, self.data.msg2)
        self.lib.general_helper.find_and_click(self.pages.CRS.balance_drawer.pup_success_btn_close)
        self.lib.files.download_and_compare_pdf_new(self.data, "drawer_summary")

        self.lib.CRS.balance_drawer.click_print_drawer_summary_lnk("Note")
        self.actions.assert_element_text(self.pages.CRS.balance_drawer.pup_print_success_text, self.data.msg1)
        self.lib.general_helper.find_and_click(self.pages.CRS.balance_drawer.pup_print_warning_btn_no)
        self.actions.assert_element_not_present(self.pages.CRS.balance_drawer.pup_success_print_drawer_summary)

        self.lib.CRS.balance_drawer.click_settle_button()
        self.lib.CRS.balance_drawer.click_print_drawer_summary_lnk()
        self.actions.assert_element_text(self.pages.CRS.balance_drawer.pup_print_success_text, self.data.msg2)
        self.lib.general_helper.find_and_click(self.pages.CRS.balance_drawer.pup_success_btn_close)
        self.lib.files.download_and_compare_pdf_new(self.data, "settle_drawer_summary")


if __name__ == '__main__':
    run_test(__file__)
