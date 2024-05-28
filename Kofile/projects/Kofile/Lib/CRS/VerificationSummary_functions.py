from projects.Kofile.Lib.test_parent import LibParent


class VerificationSummary(LibParent):
    def __init__(self):
        super(VerificationSummary, self).__init__()

    def click_next_order_button(self):
        self._general_helper.find_and_click(self._pages.CRS.verification_summary.btn_next_order)
        self._general_helper.wait_for_spinner()

    def send_order_to_indexing(self, reason='Test'):
        self._general_helper.find_and_click(self._pages.CRS.verification_summary.lnk_send_order_to_indexing_queue)
        self._actions.send_keys(self._pages.CRS.verification_summary.pup_send_order_to_admin_txt_reason, reason)
        cur_url = self._actions.get_current_url()
        self._general_helper.find_and_click(self._pages.CRS.verification_summary.pup_send_order_to_admin_lnk_submit)
        self._general_helper.wait_url_change(cur_url)

    def click_edit_order_item(self):
        self._general_helper.find_and_click(self._pages.CRS.verification_summary.editicon_by_row())
