from projects.Kofile.Lib.test_parent import AtomParent

from projects.Kofile.Atom.CRS.general import General
from projects.Kofile.Atom.CRS.order_search import OrderSearch
from projects.Kofile.Atom.CRS.order_finalization import OrderFinalization


class AddPayment(AtomParent):
    def __init__(self):
        super(AddPayment, self).__init__()

    def add_payments(self, payments="", tr_id="", comment="", amount="", start_from=1, forbidden_payments=None,
                     edit_payment=False):
        """
            ['Cash', 'Cashiers Check', 'Check', 'Credit Card', 'LegalEase', 'Money Order', 'VitalCheck']

            Pre-conditions: Add Payment is displayed
            Post-conditions: Payment(s) is added, Add Payment is displayed
            If payments not provided - select first available payment from list
            If payments = 'ALL' - add all available payment methods
            If amount not provided - split Balance due between payments
            """

        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        all_payments = self._lib.CRS.add_payment.get_all_payment_methods()
        if forbidden_payments:
            forbidden_payments = forbidden_payments if isinstance(forbidden_payments, list) else [forbidden_payments]
            # Check forbidden payments in drop-down list
            if len(all_payments) < 3:
                self._actions.wait(3)
                new_all_payments = None
                for _ in range(20):
                    new_all_payments = self._lib.CRS.add_payment.get_all_payment_methods()
                    self._actions.log(new_all_payments)
                    if new_all_payments and (new_all_payments != all_payments):
                        break
                    self._actions.wait(1)
                all_payments = new_all_payments if new_all_payments else all_payments
            errors = [i for i in forbidden_payments if i in all_payments]
            assert not errors, f"Forbidden payment method(s): '{errors}' found " \
                               f"in payments dropdown list: '{all_payments}'"
        payments = all_payments if payments == "ALL" else ["1"] if not payments \
            else [payments] if not isinstance(payments, list) else payments
        if not amount and not edit_payment:
            # Split 'Balance due' between payments
            balance_due_amount = self._lib.CRS.add_payment.get_balance_due_amount()
            # payments_count = len(payments)
            # amount_per_payment = round(balance_due_amount / payments_count + 0.004, 2)
            amount_per_payment = self._lib.general_helper.create_amounts(payments, balance_due_amount)
        else:
            amount_per_payment = amount
        # Add payment methods and fill payment fields
        for n, i in enumerate(payments, start_from):
            if n > 1 and not edit_payment:
                # Add payment
                self._lib.CRS.add_payment.add_payment_method()
            self._lib.CRS.add_payment.get_all_payment_methods(n)
            # Select payment method
            self._lib.CRS.add_payment.fill_in_payment_method(n, i)
            # Fill in Transaction ID
            if tr_id is not None:
                if i in ["Check"]:
                    # Transaction ID should be required for some payment methods
                    required = self._lib.general_helper.find(
                        self._lib.general_helper.remake_locator(self._lib.general_helper.make_locator(
                            self._pages.CRS.add_payment.txt_paymethod_transaction_id_by_row, n), "/../../li[2]",
                            "Required Transaction ID field"), get_attribute="class")
                    assert required == "showError", f"Transaction ID field for '{i}' payment method is not required!"
                self._lib.CRS.add_payment.fill_in_payment_method_transaction_id(
                    n, tr_id if tr_id else f"TRID{n}{i}")         # noqa
            # Fill in Amount
            if amount is not None and i != 'Credit Card':
                payment_amount = amount_per_payment[n - 1] if isinstance(amount_per_payment,
                                                                         list) else amount_per_payment
                self._lib.CRS.add_payment.fill_in_payment_method_amount(n, payment_amount)
            # Fill in Comment
            if comment is not None:
                self._lib.CRS.add_payment.fill_in_payment_method_comment(n, comment if comment else f"comment_{n}_{i}")
            if i == 'Credit Card':
                break
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))
        return payments

    def finalize_and_process_to_archive(self):
        """
            Pre-conditions: Order Summary page is displayed
            Post-conditions: Order is processed to Archive
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        data = self._lib.general_helper.get_data()
        # finalize the order
        self.finalize_order(print_doc_number=True)
        # if OI is RP, scan documents button will not allow to go to other menu
        if data["OIT"] == "RP_Recordings":
            General().go_to_crs()
        # process order to Archive
        self._lib.CRS.order_item_type.capture_step()
        self._lib.CRS.order_item_type.indexing_step()
        self._lib.CRS.order_item_type.verification_step(False)
        # verify order is in Archive
        OrderSearch().search_order_by_order_number()
        self._lib.CRS.order_search.verify_order_present_in_result(data["order_number"])
        index_type = data['config'].test_data(f"{data.OIT}.indexing.indexing_type")
        self._lib.CRS.order_search.verify_order_status(
            "indexing_status" if index_type == 'scheduled_kdi' else "archive_status")

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def finalize_order(self, payments="", tr_id="", comment="", amount="", start_from=1, forbidden_payments=None,
                       edit_payment=False, expected_status=None, expected_total=None, print_doc_number=False):
        """
            Pre-conditions: Order Summary is displayed
            Post-conditions: Payment is added, Order Finalization is displayed
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        data = self._lib.general_helper.get_data()
        # click Order Summary Checkout button
        self._lib.CRS.order_summary.click_order_summary_checkout_button()
        if data['config'].test_data(f"{data['current_oit']}.finalization.with_payment"):
            # add payment
            self.add_payments(payments=payments, tr_id=tr_id, comment=comment, amount=amount,
                              start_from=start_from, forbidden_payments=forbidden_payments, edit_payment=edit_payment)
            # click Checkout
            self._lib.CRS.add_payment.click_add_payment_checkout_button(expected_status, expected_total)

        self._actions.wait_for_element_displayed(self._pages.CRS.order_finalization.lbl_order_finalize_label)

        # get doc number and recorded year
        OrderFinalization().get_year_doc_number()

        if print_doc_number:
            self._actions.step("Doc year - '{}'".format(data["doc_year"]))
            self._actions.step("Doc number - '{}'".format(data["doc_number"]))

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))
