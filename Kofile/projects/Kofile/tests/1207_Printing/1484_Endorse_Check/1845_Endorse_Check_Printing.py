"""Endorse Check Printing"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Finalize an order with check payment method
                 On Order Finalization page, click on 'Endorse Checks' link
                 Verify that printing is successful and find the SlipPrinterConfig file in Azure
                 Find the order in Order Search and click on 'Endorse Checks' icon
                 Find the reprinted file in Azure"""

tags = ['48999_location_2']


# todo ShowOrderFinalization page not have a btn_void_order button and lnk_endorse_check button

class test(TestParent):                                                                                    # noqa

    def __init__(self, data):
        data["current_oit"] = data["OIT"]
        super(test, self).__init__(data, __name__)

    def __test__(self):
        if self.data["current_oit"] in self.data['config'].get_order_types():
            self.atom.CRS.order_queue.create_and_action_with_order(action=None, ind=1)
            self.lib.general_helper.scroll_and_click(self.pages.CRS.order_summary.btn_checkout)
            with_payment = self.data['config'].test_data(f"{self.data['current_oit']}.finalization.with_payment")
            if with_payment:
                self.atom.CRS.add_payment.add_payments("Check")
                self.lib.general_helper.find_and_click(self.pages.CRS.add_payment.btn_checkout)
            self.actions.wait_for_element_displayed(self.pages.CRS.order_finalization.btn_void_order)
            # click on Endorse Check link
            self.lib.general_helper.find_and_click(self.pages.CRS.order_finalization.lnk_endorse_check)
            self.actions.wait_for_element_displayed(self.pages.CRS.order_finalization.pup_endorse_stamp_printing)
            # get the filename from DEVICE_JOB -> DEVICE_JOB_CONFIG -> File path
            file_name = self.lib.db_with_vpn.get_file_name_from_xml()
            # find the printed SlipPrinterConfig file in Azure
            container = f"wfcontent-{self.data['env']['code']}-printfolder"
            self.lib.azure.check_blob_existence_in_container(file_name, container)
            # find the order in Order Search and reprint endorse checks
            self.atom.CRS.general.go_to_crs()
            self.lib.CRS.crs.go_to_order_search()
            self.atom.CRS.order_search.search_order_by_order_number()
            self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
            self.lib.CRS.order_search.click_on_endorse_check_icon(self.data["order_number"])
            self.actions.wait_for_element_displayed(self.pages.CRS.order_finalization.pup_endorse_stamp_printing)
            file_name = self.lib.db_with_vpn.get_file_name_from_xml()
            self.lib.azure.check_blob_existence_in_container(file_name, container)
        else:
            self.actions.step(f"{self.data['current_oit']} does not exist for current tenant")


if __name__ == '__main__':
    run_test(__file__)
