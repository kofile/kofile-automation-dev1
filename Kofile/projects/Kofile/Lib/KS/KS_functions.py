from projects.Kofile.Lib.test_parent import LibParent


class KS(LibParent):
    def __init__(self):
        super(KS, self).__init__()

    def click_on_search_button(self):
        self._general_helper.find_and_click(self._pages.KS.home_page.btn_search)
        self._general_helper.wait_for_spinner()

    def get_first_row_num_with_add_to_cart(self):
        return self._general_helper.find(self._pages.KS.home_page.all_rows_with_add_to_cart, get_attribute="data-value")

    def verify_row_icons_by_row_num(self, row_num):
        self._general_helper.find(
            self._general_helper.make_locator(self._pages.KS.home_page.icn_k_drive_by_row_num_, row_num))
        self._general_helper.find(
            self._general_helper.make_locator(self._pages.KS.home_page.icn_quick_doc_by_row_num_, row_num))
        self._general_helper.find(
            self._general_helper.make_locator(self._pages.KS.home_page.icn_add_to_cart_by_row_num_, row_num))

    def add_doc_to_cart_by_row_num(self, row_num):
        self._general_helper.find_and_click(
            self._general_helper.make_locator(self._pages.KS.home_page.icn_add_to_cart_by_row_num_, row_num))
        self._general_helper.wait_for_spinner()

    def click_on_quick_doc_by_row_num(self, row_num):
        self._general_helper.find_and_click(
            self._general_helper.make_locator(self._pages.KS.home_page.icn_quick_doc_by_row_num_, row_num))
        self._general_helper.find(self._pages.KS.home_page.pup_order_confirmation, wait_displayed=True, timeout=120)

    def go_to_cart(self):
        self._general_helper.scroll_and_click(self._pages.KS.home_page.lnk_cart)
        self._general_helper.find(self._pages.KS.home_page.lbl_cart, wait_displayed=True, timeout=60)

    def verify_delivery_method_by_text(self, option):
        self._general_helper.find(
            self._general_helper.make_locator(self._pages.KS.home_page.delivery_method_by_text_, option))

    def get_total_due(self):
        return float(self._general_helper.find(self._pages.KS.home_page.lbl_total_due, get_text=True))

    def get_available_balance(self):
        return float(
            self._general_helper.find(self._pages.KS.home_page.lbl_available_balance, get_text=True).split('$')[
                1].split(')')[
                0])

    def new_search(self):
        self._general_helper.find_and_click(self._pages.KS.home_page.btn_new_search)
        self.click_on_search_button()

    def get_order_total(self):
        return float(
            self._general_helper.find(self._pages.KS.home_page.lbl_total_price, get_text=True,
                                      wait_displayed=True).replace(
                '$', ''))

    def quick_doc_ca_payment(self, total_due, convenience_fee):
        self._general_helper.find_and_click(self._pages.KS.home_page.rbn_company_account)
        self._general_helper.find_and_click(self._pages.KS.home_page.btn_submit_pup)
        order_total = self.get_order_total()
        assert order_total == total_due + convenience_fee, \
            f"Order Total {order_total} is NOT equal to doc price {total_due}"

    def quick_doc_pay_at_counter(self):
        self._general_helper.find_and_click(self._pages.KS.home_page.rbn_pay_at_counter)
        self._general_helper.find_and_click(self._pages.KS.home_page.btn_submit_pup)
        total_due = self.get_total_due()
        self._general_helper.find_and_click(self._pages.KS.home_page.btn_submit_pay_at_counter)
        order_number = self._general_helper.find(self._pages.KS.home_page.lbl_order_number, get_text=True,
                                                 wait_displayed=True)
        self._general_helper.find_and_click(self._pages.KS.home_page.btn_close_pup)
        return order_number, total_due

    def search_for_doc_by_doc_number(self, doc_number):
        self._general_helper.find_and_send_keys(self._pages.KS.home_page.txt_search, doc_number)
        self.click_on_search_button()

    def click_on_cart_checkout(self):
        self._general_helper.find_and_click(self._pages.KS.home_page.btn_checkout)
        self._general_helper.find(self._pages.KS.home_page.pup_cart_payments, wait_displayed=True)

    def cart_ca_payment(self):
        self._general_helper.find_and_click(self._pages.KS.home_page.rbn_company_account)
        self._general_helper.find_and_click(self._pages.KS.home_page.btn_purchase_pup)
        return self.get_order_total()

    def cart_pay_at_counter(self):
        self._general_helper.find_and_click(self._pages.KS.home_page.rbn_pay_at_counter)
        self._general_helper.find_and_click(self._pages.KS.home_page.btn_purchase_pup)
        self._general_helper.find_and_click(self._pages.KS.home_page.btn_submit_pay_at_counter)
        total_due = self.get_total_due()
        order_number = self._general_helper.find(self._pages.KS.home_page.lbl_order_number, get_text=True,
                                                 wait_displayed=True)
        self._general_helper.find_and_click(self._pages.KS.home_page.btn_close_pup)
        return order_number, total_due

    def clear_cart(self):
        self.go_to_cart()
        self._general_helper.find_and_click(self._pages.KS.home_page.lnk_clear_cart)
        self._general_helper.find(self._pages.KS.home_page.lbl_no_items_in_cart, wait_displayed=True)
        self._general_helper.find_and_click(self._pages.KS.home_page.icn_home)
        self._general_helper.find(self._pages.KS.home_page.txt_search, wait_displayed=True)
