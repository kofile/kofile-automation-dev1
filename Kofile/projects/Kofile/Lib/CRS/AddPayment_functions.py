from projects.Kofile.Lib.CRS.OrderFinalization_functions import OrderFinalization
from projects.Kofile.Lib.test_parent import LibParent

order_finalization = OrderFinalization()


class AddPayment(LibParent):

    def __init__(self):
        self.prepare_payments = lambda s: True
        super(AddPayment, self).__init__()

    def __48999__(self):
        self.prepare_payments = lambda s: s.remove("Credit Card") if "Credit Card" in s else None

    def check_add_payment_checkout_button(self, should_be_enabled=True, retries=2):
        # Check 'Add payment' Checkout button enabled/disabled
        checkout = self._general_helper.find(self._pages.CRS.add_payment.btn_checkout, 60, get_attribute="disabled")
        if (should_be_enabled and checkout) or (not should_be_enabled and not checkout):
            if retries:
                retries -= 1
                self._actions.wait(1)
                return self.check_add_payment_checkout_button(should_be_enabled, retries)
            raise ValueError(
                "Add payment 'Checkout' button unexpectedly {}".format("disabled" if should_be_enabled else "enabled"))
        return checkout

    def click_add_payment_checkout_button(self, expected_status="Finalized", expected_total=None, timeout=30):
        # Click 'Add payment' Checkout button
        self.check_add_payment_checkout_button(retries=4)
        self._general_helper.scroll_and_click(self._pages.CRS.add_payment.btn_checkout)
        if self._general_helper.find(self._pages.CRS.add_payment.pup_checkout_txt_comment, 2, False):
            self._general_helper.find_and_send_keys(self._pages.CRS.add_payment.pup_checkout_txt_comment,
                                                    "Some checkout comment")
            self._general_helper.find_and_click(self._pages.CRS.add_payment.pup_checkout_btn_submit)
            self._actions.wait(0.5)
            self._general_helper.find_and_click(self._pages.CRS.add_payment.btn_checkout)
        if self._general_helper.find(self._pages.CRS.add_payment.pup_save_header_btn_yes, timeout=10,
                                     should_exist=False):
            self._general_helper.find_and_click(self._pages.CRS.add_payment.pup_save_header_btn_yes)
        self._general_helper.find(self._pages.CRS.order_finalization.lbl_order_finalize_label, timeout=timeout)
        order_finalization.check_order_finalization__order_status(expected_status)
        order_finalization.check_order_finalization__order_total_amount(expected_total)

    def add_payment_method(self):
        # Add payment
        self._general_helper.scroll_and_click(self._pages.CRS.add_payment.btn_new_payment_method)

    def delete_payment_method(self, row=1):
        # Delete payment
        self._general_helper.scroll_and_click(
            self._general_helper.make_locator(self._pages.CRS.add_payment.btn_paymethod_delete_by_row, row))

    def get_all_payment_methods(self, row=1, remove_credit_card=True):
        # Get ALL payment methods from row
        locator = self._general_helper.make_locator(self._pages.CRS.add_payment.ddl_paymethod_payment_method_by_row,
                                                    row)
        all_payments = self._general_helper.find_elements(
            self._general_helper.remake_locator(locator, "/option[not(text()='Select')]"),
            get_text=True)
        if remove_credit_card:
            self.prepare_payments(all_payments)
        # Move Credit Card payment method to the end of the list
        if 'Credit Card' in all_payments:
            all_payments.append(all_payments.pop(all_payments.index('Credit Card')))
        return all_payments

    def get_payment_method(self, row=1):
        # Get payment method from row
        payment = self._general_helper.find(
            self._general_helper.make_locator(self._pages.CRS.add_payment.ddl_paymethod_payment_method_by_row, row),
            get_attribute="value")
        return payment

    def get_payment_method_enabled(self, row=1):
        # Get payment method field status from row
        field = self._general_helper.find(
            self._general_helper.make_locator(self._pages.CRS.add_payment.ddl_paymethod_payment_method_by_row, row))
        return field.is_enabled()

    def get_payment_method_amount(self, row=1):
        # Get amount from payment method row
        amount_str = self._general_helper.find(self._general_helper.make_locator(
            self._pages.CRS.add_payment.txt_paymethod_amount_by_row, row), get_attribute="value")
        self._logging.info(f'{amount_str=}')
        amount = float(amount_str)
        return amount

    def get_payment_method_amount_enabled(self, row=1):
        # Get amount from payment method field status row
        field = self._general_helper.find(
            self._general_helper.make_locator(self._pages.CRS.add_payment.txt_paymethod_amount_by_row, row),
            get_attribute="readonly")
        return not bool(field)

    def get_cash_change_due_amount(self):
        # Get CASH change due amount
        amount = self._general_helper.find(self._pages.CRS.add_payment.txt_cash_change_due_amount, should_exist=False,
                                           timeout=1)
        return float(amount.value) if amount else 0

    def get_payment_method_comment(self, row=1):
        # Get comment from payment method row
        comment = self._general_helper.find(self._general_helper.make_locator(
            self._pages.CRS.add_payment.txt_paymethod_comment_by_row, row), get_attribute="value")
        return comment

    def get_payment_method_comment_enabled(self, row=1):
        # Get comment from payment method field status row
        field = self._general_helper.find(
            self._general_helper.make_locator(self._pages.CRS.add_payment.txt_paymethod_comment_by_row, row),
            get_attribute="readonly")
        return not bool(field)

    def get_payment_method_transaction_id(self, row=1):
        # Get transaction ID from payment method row
        tr_id = self._general_helper.find(self._general_helper.make_locator(
            self._pages.CRS.add_payment.txt_paymethod_transaction_id_by_row, row), get_attribute="value")
        return tr_id

    def get_payment_method_transaction_id_enabled(self, row=1):
        # Get transaction ID from payment method field status row
        field = self._general_helper.find(
            self._general_helper.make_locator(self._pages.CRS.add_payment.txt_paymethod_transaction_id_by_row, row),
            get_attribute="readonly")
        return not bool(field)

    def fill_in_payment_method(self, row=1, method="1"):
        """method='Cash' - select 'Cash' from list
        method='1' - Select first payment method from list"""
        locator = self._general_helper.make_locator(self._pages.CRS.add_payment.ddl_paymethod_payment_method_by_row,
                                                    row)
        if method.isdigit():
            self._actions.select_by_index(locator, method)
        else:
            self._actions.select_option_by_text(locator, method)

    def fill_in_payment_method_amount(self, row=1, amount=1):
        self._actions.wait(1)
        self._general_helper.find_and_send_keys(self._general_helper.make_locator(
            self._pages.CRS.add_payment.txt_paymethod_amount_by_row, row), amount)

    def fill_in_payment_method_comment(self, row=1, comment="comment"):
        el = self._general_helper.find_and_send_keys(self._general_helper.make_locator(
            self._pages.CRS.add_payment.txt_paymethod_comment_by_row, row), comment)
        el.send_keys(self._keys.TAB)

    def fill_in_payment_method_transaction_id(self, row=1, tr_id="TRID"):                       # noqa
        el = self._general_helper.find_and_send_keys(self._general_helper.make_locator(
            self._pages.CRS.add_payment.txt_paymethod_transaction_id_by_row, row), tr_id)
        el.send_keys(self._keys.TAB)

    def get_balance_due_amount(self):
        # Get 'Balance due' amount
        balance_due = float(
            self._general_helper.find(self._pages.CRS.add_payment.lbl_paygrid_balance_due_amount, get_text=True)[1:])
        return balance_due

    def get_total_amount(self):
        # Get 'Total' amount
        total = float(
            self._general_helper.find(self._pages.CRS.add_payment.lbl_paygrid_subtotal_amount, get_text=True)[1:])
        return total

    def get_processing_fee(self):
        # Get 'Balance due' amount
        try:
            processing_fee = float(
                self._general_helper.find(
                    self._pages.CRS.add_payment.lbl_processing_fee_amount, get_text=True)[1:])
            return processing_fee
        except Exception as e:
            print(e)
            return 0

    def void_order__copy_transaction_id(self, from_row=1, to_row=2):
        to_ = ("xpath", "//li[@class='showError']/input[contains(@name,'TransactionId')]",
               "Required transaction ID field")
        if self._general_helper.find(to_, should_exist=False, timeout=2):
            tr_id = self.get_payment_method_transaction_id(from_row)
            self.fill_in_payment_method_transaction_id(to_row, tr_id)

    def check_all_payment_methods_count(self, min_count=3, retry_count=30, wait_per_tick=1):
        all_payment_methods = list()
        for _ in range(retry_count):
            all_payment_methods = self.get_all_payment_methods()
            if len(all_payment_methods) >= min_count:
                break
            self._actions.wait(wait_per_tick)
        assert len(all_payment_methods) >= min_count, f"Total payment methods count < {min_count}"

    def get_expected_processing_fee(self, payed_amount):
        data = self._general_helper.get_data()
        credit_card_amount = self.get_balance_due_amount() - payed_amount
        if data['config'].test_data(f"{data.OIT}.payment_methods.processing_fee.by_range"):
            ranges = data['config'].test_data(f"{data.OIT}.payment_methods.processing_fee.ranges")
            list_ranges = list(ranges)
            for r in list_ranges:
                min_v, max_v = r.split('-')
                if float(min_v) <= credit_card_amount <= float(max_v):
                    return ranges[r]
        elif data['config'].test_data(f"{data.OIT}.payment_methods.processing_fee.fix_amount"):
            return data['config'].test_data(f"{data.OIT}.payment_methods.processing_fee.amount")
        elif data['config'].test_data(f"{data.OIT}.payment_methods.processing_fee.by_percentage"):
            percent = data['config'].test_data(f"{data.OIT}.payment_methods.processing_fee.percent")
            fee_amount = (credit_card_amount * (percent / 100))
            return round(fee_amount, 2)
        elif data['config'].test_data(f"{data.OIT}.payment_methods.processing_fee.no_fee"):
            return 0
        else:
            self._logging.error(f"No processing fee configured for {data.OIT}")
