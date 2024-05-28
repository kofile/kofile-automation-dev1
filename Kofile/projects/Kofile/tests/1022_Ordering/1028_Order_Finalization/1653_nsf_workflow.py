"""NFS workflow"""
import re
from random import randint
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Steps:

                 1. Add new order e.g. Plats and finalize with 'Check' payment method
                 2. Add new order with 'NSF' OIT
                 3. Input order number from 1 step (order with 'Check' payment method)
                 4. Verify Amount in popup (compare with price of order from step 1)  
                 5. Select 'NSF' checkbox and click 'Submit' button
                 6. Verify Total in fee box (compare with Amount from step 4) 
                 7. Enter random 'Number Of' (from 1 to 10)
                 8. Verify NSF Fee (compare with configured nsf fee * 'Number Of')
                 9. Verify Total in fee box (compare with order price + NSF Fee)
                 10. Finalize Order
                 11. Verify that 'Number Of' is read only
                 12. Navigate to Order Search
                 13. Check 'NSF' checkbox
                 14. Verify that order search results contains order finalized with 'Check' payment method

              """

tags = ['48999_location_2']

"""Anna - NSF OIT Is not exists in 48999. So skip test for 48999"""
class test(TestParent):                                                                            # noqa

    def __init__(self, data, ind=1):
        self.ind = ind
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.data["current_oit"] = self.data.OIT
        self.lib.general_helper.check_order_type()
        # Note: use User1, NSF is not available for User4
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        # -----------------------------------------order_summary_page-------------------------------------
        one_oit = self.data["current_oit"]
        self.actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        self.lib.general_helper.scroll_and_click(self.pages.CRS.order_summary.btn_checkout)

        # -----------------------------------------admin_payment_page--------------------------------------
        with_payment = self.data['config'].test_data("{}.finalization.with_payment".format(one_oit))
        if with_payment:
            self.atom.CRS.add_payment.add_payments("Check")
            self.actions.click(self.pages.CRS.add_payment.btn_checkout)

        self.actions.wait_for_element_displayed(self.pages.CRS.order_finalization.btn_void_order)

        # ----------------------------------------order_finalization_page-------------------------------------

        # get order price
        order_price = self.actions.get_element_text(self.pages.CRS.order_finalization.price_by_row_index())
        # go to Order Queue
        self.lib.CRS.crs.go_to_order_queue()
        # ----------------------------------------add_new_order_with_NSF_OIT-----------------------------------
        self.data["current_oit"] = self.data.nsf_oit
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.fill_order_header_name()

        # input order number from previous order finalized with Check payment method
        self.actions.send_keys(self.pages.CRS.order_entry.inp_nsf_order_num, self.data["order_number"])
        nsf_order_num = self.lib.general_helper.make_locator(
            self.pages.CRS.order_entry._ddl_nsf_lookup_by_order_num,
            self.data["order_number"])
        # wait for dropdown to be displayed
        self.lib.general_helper.wait_and_click(nsf_order_num)

        # verify that popup is shown
        self.actions.wait_for_element_displayed(self.pages.CRS.order_entry.pup_nsf)
        self.actions.assert_element_present(self.pages.CRS.order_entry.pup_nsf)

        # verify Amount in popup (compare with price of order finalized with 'Check' payment method)
        self.actions.assert_element_text(self.pages.CRS.order_entry.txt_nsf_amount, order_price)

        # verify Total in fee box (compare with Amount in popup)
        self.actions.click(self.pages.CRS.order_entry.chk_nsf)
        self.lib.general_helper.wait_and_click(self.pages.CRS.order_entry.btn_nsf_submit)
        self.actions.wait(2)
        self.actions.assert_element_text(self.pages.CRS.order_entry.txt_total_amount, order_price)

        # verify NSF Fee in fee box (compare with configured nsf fee * Number Of)
        no_of = randint(1, 10)
        self.actions.send_keys(self.pages.CRS.order_entry.inp_no_of, no_of)
        config_nsf_fee = self.actions.get_element_text(self.pages.CRS.order_entry.lbl_oit_description)
        # cut price from OIT description and convert to float
        pattern = r"[\d.|,]+"
        config_nsf_fee = float((re.search(pattern, config_nsf_fee)).group())
        # multiply configured nsf fee and NoOf
        config_nsf_fee_with_no_of = config_nsf_fee * no_of
        self.actions.wait(2)
        # get NSF Fee from fee box
        nsf_fee = self.actions.get_element_text(
            self.lib.general_helper.make_locator(self.pages.CRS.order_entry._txt_fee_amount_less, 1))
        nsf_fee = float((re.search(pattern, nsf_fee)).group())
        self.actions.assert_equals(nsf_fee, config_nsf_fee_with_no_of)

        # verify Total in fee box (compare with order price + NSF Fee)
        total = self.actions.get_element_text(self.pages.CRS.order_entry.txt_total_amount)
        total = float((re.search(pattern, total)).group())
        order_price = float((re.search(pattern, order_price)).group())
        self.actions.assert_equals(total, order_price + nsf_fee)

        self.actions.click(self.pages.CRS.order_entry.btn_add_to_order)
        self.actions.wait_for_element_displayed(self.pages.CRS.order_summary.btn_checkout)

        # -------------------------------order_summary_page-----------------------------------------------
        self.atom.CRS.add_payment.finalize_order()
        self.actions.wait_for_element_displayed(self.pages.CRS.order_finalization.btn_void_order)

        # -------------------------------order_finalization_page-----------------------------------------------
        self.lib.general_helper.find_and_click(
            self.lib.general_helper.make_locator(self.pages.CRS.order_finalization.icn_edit_order, self.ind))
        # verify that NoOf field is read only
        self.actions.assert_element_attribute(self.pages.CRS.order_entry.inp_no_of, 'readonly', 'true')
        self.lib.general_helper.scroll_and_click(self.pages.CRS.order_finalization.btn_save_order)
        self.lib.general_helper.wait_and_click(self.pages.CRS.order_entry.btn_nsf_submit)
        self.actions.click(self.pages.CRS.order_finalization.btn_order_queue)

        # go to Order Search page
        self.lib.CRS.crs.go_to_order_search()

        # -------------------------------order_search_page-----------------------------------------------

        self.actions.click(self.pages.CRS.order_search.lnk_more_options)
        self.lib.general_helper.wait_and_click(self.pages.CRS.order_search.cbx_nsf)
        self.actions.click(self.pages.CRS.order_search.btn_search)
        self.actions.wait_for_element_displayed(self.pages.CRS.order_search.order_search_results)

        self.actions.assert_page_contains_text(self.data["order_number"])
        self.actions.wait(1)


if __name__ == '__main__':
    run_test(__file__)
