from time import sleep, time
from golem.webdriver.extended_webelement import Select
from datetime import datetime
from projects.Kofile.Lib.Required_fields import RequiredFields
from projects.Kofile.Lib.test_parent import LibParent


class PS(LibParent):
    status_column = 12

    def __init__(self):
        super(PS, self).__init__()

    def __48999__(self):
        self.status_column = 14

    def wait_until_order_summary_is_loaded(self, timeout=90):
        # wait for Order Summary page to be loaded
        max_wait = time() + timeout
        while max_wait > time():
            curl = self._actions.get_browser().current_url
            if "Order/OrderSummary?orderId" in curl:
                return self._general_helper.find(self._pages.PS.summary_tab.new_order_item)
            else:
                sleep(1)
        raise ValueError(f"Order summary page isn't loaded in {timeout} seconds")

    def check_doc_number_in_order_summary(self, row_index=1):
        cs_doc_num = self._general_helper.get_data().prev_sum.doc_num
        self.wait_until_order_summary_is_loaded()
        r1 = self._general_helper.find(self._general_helper.remake_locator(
            self._pages.PS.summary_tab.doc_year_oq, f"{row_index}{self._pages.PS.summary_tab.doc_year_2}"),
            get_text=True)
        r2 = self._general_helper.find(self._pages.PS.summary_tab.doc_num_id_oq, get_text=True).lstrip('/')
        os_doc_num = f"{r1}-{r2}"
        assert cs_doc_num == os_doc_num, f"Expected document number from CS: {cs_doc_num} " \
                                         f"not equal to: {os_doc_num} in CRS"

    def check_doc_type_in_order_summary(self):
        doc_type_cs = self._general_helper.get_data().prev_sum.doc_type
        doc_type_os = self._general_helper.find(self._pages.PS.summary_tab.doc_type_os, get_text=True)
        doc_type_list = [x.strip() for x in doc_type_os.lower().split("-")]
        doc_type_cs_list = [x.strip() for x in doc_type_cs.lower().split("-")]
        if len(doc_type_cs_list) == 1:
            assert doc_type_cs.lower() in doc_type_list, "Incorrect doc type"
        else:
            assert doc_type_cs.lower() == doc_type_os.lower(), "Incorrect doc type"

    def check_fee_description(self, tconf):
        fee_desc_os = self._general_helper.find(self._pages.PS.summary_tab.fee_desc, get_text=True)
        fee_desc_cs = tconf.get("fee_description")
        assert fee_desc_cs == fee_desc_os, f"Expected Fee Description: {fee_desc_cs} not equal to actual: {fee_desc_os}"

    def check_status_and_type_in_order_summary(self):
        test_config = self._general_helper.get_data().test_config
        stat = self._general_helper.find(self._pages.PS.summary_tab.oit_status, get_text=True)
        type_ = self._general_helper.find(self._pages.PS.summary_tab.oit_type, get_text=True)
        exp_stat = test_config.get("order_status_before")
        exp_type = test_config.get("oit_type_before")
        assert exp_stat == stat, f'Expected order status: {exp_stat} not equal to actual: {stat}'
        assert exp_type == type_, f'Expected order type: {exp_type} not equal to actual: {type_}'

    def calculate_fee(self):
        data = self._general_helper.get_data()
        tconf = data.test_config
        num_p_cs = int(data.prev_sum.num_of_pages)  # if tconf.get("is_package") else 1
        no_of_cert = 1 if "Certified" in tconf.get("order_type") else 0
        no_of_addtl_copies = 0
        no_of_contr = 0
        num_p_os = self._general_helper.find(self._pages.PS.summary_tab.number_of, get_text=True)
        self._actions.step(
            f"\nnum_p_cs: {num_p_cs}\nno_of_cert: {no_of_cert}\nno_of_addtl_copies: {no_of_addtl_copies}\n"
            f"no_of_contr: {no_of_contr}\nnum_p_os:{num_p_os}\n\nfee_calc: {tconf.get('fee_calc')}")
        prc_calc = str("{:.2f}".format(eval(tconf.get("fee_calc"))))
        data.prc_calc = prc_calc
        return prc_calc

    def go_to_finalization(self, payment_method="", transaction_id="trID", comment_text="comment"):
        """If 'payment_method' is '', then tries to choose Cash payment method, if fails - chooses Company Account,
        otherwise uses given payment method
        """
        el = self._general_helper.find(self._pages.PS.summary_tab.payment_methods_field)
        payment_method = payment_method if payment_method else "Cash"
        Select(el).select_by_visible_text(payment_method)
        # set transaction ID
        self._general_helper.find_and_send_keys(self._pages.PS.summary_tab.tr_id_field, transaction_id)
        self._general_helper.find_and_send_keys(self._pages.PS.summary_tab.comment_field, comment_text)
        # add amount
        balance = self._general_helper.find(self._pages.PS.summary_tab.balance_field, get_text=True)
        self._general_helper.find_and_send_keys(self._pages.PS.summary_tab.amount_field, balance)
        self._general_helper.scroll_and_click(self._pages.PS.summary_tab.checkout_field)

    def finalization_check(self, row=1):

        data = self._general_helper.get_data()
        prc_calc = data.prc_calc
        tconf = data.test_config
        doc_num_cs = data.prev_sum.doc_num
        fin_oit_type = self._general_helper.find(self._pages.PS.summary_tab.oit_type_fin, get_text=True)
        fin_stat = self._general_helper.find(self._general_helper.remake_locator(
            self._pages.PS.summary_tab.order_status, f"[{row}]/td[{self.status_column}]"), get_text=True)
        r1 = self._general_helper.find(self._general_helper.remake_locator(
            self._pages.PS.summary_tab.doc_year_os, f"{row}{self._pages.PS.summary_tab.doc_year_2}"), get_text=True)
        r2 = self._general_helper.find(self._pages.PS.summary_tab.doc_num_id_os, get_text=True).lstrip('/')
        fin_doc_num = f"{r1}-{r2}"
        fin_total = str(
            "{:.2f}".format(float(self._general_helper.find(self._pages.PS.summary_tab.total_amount, get_text=True))))
        total_price = str(
            "{:.2f}".format(
                float(self._general_helper.find(self._pages.PS.summary_tab.total_price, get_text=True)[1:])))
        exp_oit_type = tconf.get("oit_type_after")
        exp_order_status = tconf.get("order_status_after")
        assert exp_oit_type == fin_oit_type, f'Expected oit type: {exp_oit_type} not equal to actual: {fin_oit_type}'
        assert exp_order_status == fin_stat, f'Expected order status: {exp_order_status} ' \
                                             f'not equal to actual: {fin_stat}'
        assert doc_num_cs == fin_doc_num, f"Expected doc number: {doc_num_cs} not equal to actual: {fin_doc_num}"
        if prc_calc != fin_total:
            print(50 * "*")
            print(f"Expected PRICE '{prc_calc}' not equal to actual total amount '{fin_total}'")
            print(50 * "*")
        if prc_calc != total_price:
            print(50 * "*")
            print(f"Expected PRICE '{prc_calc}' not equal to actual total price '{total_price}'")
            print(50 * "*")

    def edit_order_and_save(self):
        tconf = self._general_helper.get_data().test_config
        self._general_helper.find_and_click(self._pages.PS.summary_tab.edit_button)
        self.check_fee_description(tconf)
        RequiredFields().crs_fill_required_fields()
        self._general_helper.scroll_and_click(self._pages.PS.summary_tab.save_order_btn)
        if tconf.get("number_certifications_popup"):
            has_button = self._general_helper.find(self._pages.PS.summary_tab.popup_yes_btn, timeout=5,
                                                   should_exist=False)
            if has_button:
                self._general_helper.find_and_click(self._pages.PS.summary_tab.popup_yes_btn)
        if tconf.get("is_serial_number"):
            self._general_helper.find_and_click(self._pages.PS.summary_tab.serial_number_btn)
            self._general_helper.find(self._pages.PS.summary_tab.serial_number_popup)
            self._actions.wait(1)
            self._general_helper.find_and_click(self._pages.PS.summary_tab.serial_number_end_field)
            self._actions.wait(1)
            retries = 10
            while retries:
                now = datetime.now()
                sn = f"{now.month}{now.year}{now.day}{now.second}{now.microsecond}"[:15]
                field = self._general_helper.find_and_send_keys(self._pages.PS.summary_tab.serial_number_start_field,
                                                                sn)
                self._actions.wait(1)
                if self._general_helper.find(self._pages.PS.summary_tab.small_loader, timeout=1, should_exist=False):
                    self._actions.wait(1)
                if "koValidationError" in field.get_attribute("class"):
                    self._actions.step("koValidationError")
                    retries -= 1
                else:
                    break
            self._general_helper.find_and_click(self._pages.PS.summary_tab.serial_number_submit_btn)
            self._actions.wait_for_element_not_present(self._pages.PS.summary_tab.serial_number_popup)

    def checkout_order(self):
        self._general_helper.find_and_click(self._pages.PS.summary_tab.checkout_button)
        if self._general_helper.get_data().test_config.get("fee_calc") != "0":
            self.go_to_finalization()
        self.finalization_check()

    def auth(self, email, password):
        self._general_helper.find_and_click(self._pages.PS.pprint.login_button)
        self._actions.wait_for_element_not_present(self._pages.PS.pprint.si_popup_header, 30)
        self._general_helper.find_and_send_keys(self._pages.PS.pprint.si_email, email)
        self._general_helper.find_and_send_keys(self._pages.PS.pprint.si_pass, password)
        self._general_helper.find_and_click(self._pages.PS.pprint.si_signin_btn)
        self._actions.wait_for_element_displayed(self._pages.PS.pprint.logout_button, 60)

    def go_to_marriage_license_tab(self):
        self._general_helper.find_and_click(self._pages.PS.pprint.marriage_license_tab)
        self._actions.wait_for_element_displayed(self._pages.PS.pprint.marriage_date_range)

    def search_document_by_number(self, with_year=False):
        if with_year:
            search_str = f"{self._general_helper.get_data().doc_year}-{self._general_helper.get_data().doc_num}"
        else:
            search_str = self._general_helper.get_data().doc_num
        self._general_helper.find_and_send_keys(self._pages.PS.main_page.search_input, search_str)
        self._general_helper.find_and_click(self._pages.PS.main_page.doc_num_checkbox)
        self._general_helper.find_and_click(self._pages.PS.main_page.search_button)
        self._general_helper.wait_for_spinner()

    def purchase_first_document(self):
        self._general_helper.find_and_click(self._pages.PS.main_page.print_icon)
        self._actions.wait_for_element_displayed(self._pages.PS.main_page.company_acc_purchase)
        self._general_helper.find_and_click(self._pages.PS.main_page.company_acc_purchase)
        self._actions.wait_for_element_not_present(self._pages.PS.payment.payment_status_block, 120)
        self._actions.wait_for_element_displayed(self._pages.PS.payment.wrapper_page_content)
        self._actions.assert_element_text_contains(self._pages.PS.payment.wrapper_page_content, "Success!")

    def verify_certificate_date(self, date=None):
        self._actions.assert_element_text_contains(self._pages.CS.main_page.certification_date_range,
                                                   date if date else datetime.now().strftime("%#m/%#d/%Y"))
