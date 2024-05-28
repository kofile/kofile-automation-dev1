from projects.Kofile.Lib.test_parent import AtomParent


class OrderFinalization(AtomParent):
    def __init__(self):
        super(OrderFinalization, self).__init__()

    def get_year_doc_number(self, index=1):
        """
           Pre-conditions: Order Finalization is displayed, index - order item index, starts from 1
           Post-conditions: Order Finalization is displayed, data['doc_year'] and data['doc_number'] are returned
           """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        self._lib.general_helper.wait_for_page_load()
        self._actions.take_screenshot("- - - Order Finalization page - - -")
        doc_numbers = self._lib.general_helper.find_elements(
            self._pages.CRS.order_finalization.txt_table_data_doc_number, get_text=True)
        self._actions.store("doc_numbers", doc_numbers)  # for tests with several OITs
        self._actions.store("doc_number", doc_numbers[index - 1])
        self._actions.store("doc_year", self._lib.general_helper.find_elements(
            self._pages.CRS.order_finalization.txt_table_data_doc_year, get_text=True)[index - 1])

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def re_finalize_order(self):
        """
            Pre-conditions: Edit Order Item (post-finalization) page is displayed, order total is changed
            Post-conditions:  Order Finalization page is displayed, order is re-finalized
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        # save the change
        self._lib.general_helper.scroll_and_click(self._pages.CRS.order_finalization.btn_save_order)
        # wait for "outstanding balance" popup and click ok
        self._lib.general_helper.scroll_and_click(self._pages.CRS.order_finalization.pup_outstanding_btn_ok)
        self._lib.general_helper.find(self._pages.CRS.add_payment.btn_checkout, wait_displayed=True)
        # if refund to address is required, fill it
        if self._lib.general_helper.find(self._pages.CRS.order_header.lbl_address_is_required, timeout=3,
                                         should_exist=False, wait_displayed=True):
            self._lib.general_helper.scroll_and_click(self._pages.CRS.order_header.lnk_more_option)
            self._actions.wait(1.5)
            self._lib.CRS.order_header.fill_required_fields()
        else:
            self._actions.step("Refund address is not required")
        self._lib.CRS.add_payment.fill_in_payment_method_comment(2, "Refund comment")  # required for REF tenant
        # fill comment
        self._lib.general_helper.scroll_and_click(self._pages.CRS.add_payment.btn_checkout)
        self._lib.CRS.admin_payments.add_checkout_comment()
        # re-finalize the edited order
        self._lib.general_helper.find(self._pages.CRS.order_finalization.btn_void_order, wait_displayed=True)

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def void_order(self):
        """
           Pre-conditions: Order Finalization page is displayed, order is finalized
           Post-conditions: Order Finalization is displayed, order is voided
           """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        data = self._lib.general_helper.get_data()
        self._lib.CRS.order_finalization.process_void_order(voidable=True, void_oit="ALL", expected_error=None)
        # if OIT has payment, edit the transaction ids and finalize void
        if data['config'].test_data(f"{data['current_oit']}.finalization.void_with_payment"):
            self._lib.CRS.order_finalization.edit_transaction_ids()
            self._lib.CRS.order_finalization.click_finalize_void_button()
            self._lib.general_helper.find(self._pages.CRS.order_finalization.lbl_order_finalize_label,
                                          wait_displayed=True)

        # Check status is voided
        self._lib.CRS.order_finalization.check_order_finalization__order_status(expected_status='Voided')

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))
