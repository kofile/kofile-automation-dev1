from projects.Kofile.Lib.test_parent import LibParent


class VoidOrderSummary(LibParent):
    def __init__(self):
        super(VoidOrderSummary, self).__init__()

    def get_row_numbers(self):
        return self._actions.get_browser().find_all(
            self._pages.CRS.void_order_summary.void_row_numbers)

    def get_last_row_number(self):
        row_numbers = self.get_row_numbers()
        return len(row_numbers)

    def submit_fee_distribution_popup(self):
        data = self._general_helper.get_data()
        self._actions.wait_for_element_displayed(self._pages.CRS.void_order_summary.pup_fee_desc_btn_submit)
        self._general_helper.scroll_into_view(self._pages.CRS.void_order_summary.pup_fee_desc_btn_submit)
        # check if Void Reports radio-buttons exists on Fee Distribution popup
        report_radio_button = data['config'].test_data(f"{data.OIT}.finalization.void_report_radiobutton")
        if report_radio_button:
            self._general_helper.find_and_click(self._pages.CRS.void_order_summary.pup_fee_desc_rdb_void_today,
                                                should_exist=False)
        self._actions.wait_for_element_enabled(self._pages.CRS.void_order_summary.pup_fee_desc_btn_submit)
        self._actions.click(self._pages.CRS.void_order_summary.pup_fee_desc_btn_submit)

    def click_void_button(self):
        self._general_helper.find_and_click(self._pages.CRS.void_order_summary.btn_void)

    def uncheck_last_oit_checkbox(self, with_payment):
        last_row_index = self.get_last_row_number()
        total_voids_amount = self._actions.get_element_text(
            self._pages.CRS.void_order_summary.lbl_feegrid_total_voids_amount)
        checkbox_element = self._pages.CRS.void_order_summary.checkbox_by_row_index(row_num=last_row_index)
        self._actions.uncheck_element(checkbox_element)
        # Wait until total amount is changed
        if with_payment:
            self._actions.wait_for_element_text_is_not(
                self._pages.CRS.void_order_summary.lbl_feegrid_total_voids_amount, total_voids_amount)
