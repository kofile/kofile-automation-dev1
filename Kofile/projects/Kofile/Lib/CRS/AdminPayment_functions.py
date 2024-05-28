from projects.Kofile.Lib.test_parent import LibParent


class AdminPayment(LibParent):

    def __init__(self):
        super(AdminPayment, self).__init__()

    def add_checkout_comment(self):
        if self._general_helper.find(self._pages.CRS.add_payment.pup_checkout_txt_comment, timeout=10,
                                     should_exist=False):

            self._general_helper.find_and_click(self._pages.CRS.add_payment.pup_checkout_btn_submit)
            self._general_helper.scroll_and_click(self._pages.CRS.add_payment.btn_checkout)
            self._actions.wait(1)
        else:
            self._actions.step("There is no comment field on checkout")

    def get_processing_fee_label(self):
        self._general_helper.find(self._pages.CRS.admin_payment.lbl_processing_fee)

    def get_processing_fee_amount(self):
        return float(self._general_helper.find(self._pages.CRS.admin_payment.lbl_processing_fee_amount,
                     get_text=True).replace('$', ''))
