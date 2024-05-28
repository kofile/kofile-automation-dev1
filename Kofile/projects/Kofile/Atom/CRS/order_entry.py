from datetime import datetime

from selenium.webdriver.common.keys import Keys

from projects.Kofile.Atom.CRS.order_summary import OrderSummary
from projects.Kofile.Lib.test_parent import AtomParent


class OrderEntry(AtomParent):
    def __init__(self):
        super(OrderEntry, self).__init__()

    def check_order_data_after_origin_search(self, status):
        """
            Pre-conditions: Order Queue page is opened. Order is sent from CS to CRS
            Post-conditions: Order Queue page is displayed. Order Status and Assigned To are checked
            """
        from projects.Kofile.Atom.CRS.order_queue import OrderQueue
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        self._lib.general_helper.find(self._pages.CRS.general.lbl_order_count, wait_displayed=True)
        self._lib.CRS.crs.click_all_show_all_action_links()
        self._lib.general_helper.find(self._pages.CRS.general.lbl_order_count, wait_displayed=True)
        self._lib.CRS.crs.click_running_man()
        self._lib.general_helper.find(self._pages.CRS.order_summary.lbl_order_number, wait_displayed=True)
        # edit OIT
        OrderSummary().edit_oit(edit_all=True)
        # navigate to another queue and return to order queue
        self._lib.CRS.crs.go_to_indexing_queue()
        self._actions.wait(0.5)
        self._lib.general_helper.find(self._pages.CRS.indexing_queue.btn_add_new_indexing_task, wait_displayed=True)
        self._lib.CRS.crs.go_to_order_queue()
        OrderQueue().check_status_of_order(status=status)
        # verify that order is not assigned
        assigned_to_loc = self._pages.CRS.general.assigned_to_by_order_number_text(
            self._lib.general_helper.get_data()['order_number'])
        self._actions.verify_element_attribute(assigned_to_loc, 'value', '')

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def fill_order_header_name(self):
        """
           Pre-conditions: Order Header is displayed
           Post-conditions: Customer name is entered in Order Header
           """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        data = self._lib.general_helper.get_data()
        customer_type = data['config'].order_header_fill(f'{data.orderheader}.type')
        customer_name = data['config'].order_header_fill(f'{data.orderheader}.value')
        data["user_type"] = customer_type
        self._actions.step(f"customer type - '{customer_type}', customer name - '{customer_type}'")
        self._lib.CRS.order_header.fill_order_header_customer(customer_type, customer_name.lower())

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def many_oits_to_summary(self, order_item_quantity=None):
        """
            Pre-conditions: Order Entry page is opened on Order Item tab, Order Type (OIT) is selected
            Post-conditions: Order Summary page with several OI rows is displayed
            """
        self._actions.step(f"--- ATOM TEST --- {__name__} ---")

        data = self._lib.general_helper.get_data()
        # process the selected OIT to Order Summary
        self.one_oit_to_summary()
        # get the number of rows before copy
        row_numbers = self._lib.CRS.order_summary.get_number_of_rows()
        # copy the OIT
        order_item_quantity = self._lib.CRS.order_summary.copy_oit(order_item_quantity, row_index=1)
        # verify the number of rows after copy
        self._lib.general_helper.wait_for_elements_count(self._pages.CRS.order_summary.row_numbers,
                                                         (row_numbers + int(order_item_quantity)))
        self._actions.store("count_of_OITs", self._lib.CRS.order_summary.get_number_of_rows())
        # review the OITs
        for row in range(2, data["count_of_OITs"] + 1):
            self._lib.CRS.order_summary.click_edit_icon_by_row_index(row)
            # wait for Order Item tab to be displayed
            self._lib.general_helper.find(self._lib.CRS.order_entry.tab_locator("Order_Item"), wait_displayed=True)
            # fill required fields
            self._lib.required_fields.crs_fill_required_fields()
            # if OIT has document type dropdown, save the doc type in test data
            self._lib.CRS.order_entry.save_entered_doc_type()
            # click add to order
            self._lib.CRS.order_entry.click_add_to_order()
            # check that Order Summary screen is opened
            self._lib.general_helper.find(self._pages.CRS.order_summary.btn_checkout, wait_displayed=True)
            # save order number in data
            self._actions.store("order_number",
                                self._lib.general_helper.find(self._pages.CRS.order_summary.lbl_order_number,
                                                              get_text=True))
            # if OIT has serial number, fill it
            if data['config'].test_data(f"{data['current_oit']}.order_summary.serial_number"):
                self._lib.CRS.order_summary.enter_serial_number(row)

        self._actions.step(f"--- ATOMIC TEST END --- {__name__} ---")

    def one_oit_to_summary(self):
        """
            Pre-conditions: Order Entry page is opened on Order Item tab, Order Type (OIT) is selected
            Post-conditions: Order Summary page with one OI row is displayed
            """
        self._actions.step(f"--- ATOMIC TEST --- {__name__} ---")

        data = self._lib.general_helper.get_data()
        # wait for Order Item tab to be displayed
        self._lib.general_helper.find(self._lib.CRS.order_entry.tab_locator("Order_Item"), wait_displayed=True)
        # fill the required fields
        self._lib.required_fields.crs_fill_required_fields()
        # save the entered Property Address to test data
        self._lib.CRS.order_entry.save_entered_property()
        self._actions.step(data["prop_fields"])
        # save the entered doc type to test data
        self._lib.CRS.order_entry.save_entered_doc_type()
        # click add to order
        self._lib.CRS.order_entry.click_add_to_order()
        # if fee distribution popup is configured, click on fee distribution popup submit button
        self._lib.general_helper.find_and_click(self._pages.CRS.order_entry.btn_gov_fee_distribution_submit,
                                                should_exist=False, timeout=3,
                                                retries=1)
        # if OIT is Governmentals, click on fee distribution popup submit button
        if self._lib.general_helper.check_if_element_exists(
                self._pages.CRS.order_entry.ddl_gov_fee_distribution_copy_from):
            self._lib.general_helper.wait_for_spinner()
            self._actions.wait_for_element_displayed(self._pages.CRS.order_entry.ddl_gov_fee_distribution_copy_from)
            self._actions.select_option_by_text(self._pages.CRS.order_entry.ddl_gov_fee_distribution_copy_from,
                                                self._names.ANY_DATA['fee_distribution_oit'])
            self._lib.general_helper.wait_for_spinner()
            self._lib.general_helper.find_and_click(self._pages.CRS.order_entry.btn_gov_fee_distribution_submit,
                                                    should_exist=False, timeout=3,
                                                    retries=1)

        # wait for Order Summary page to open
        self._lib.general_helper.find(self._pages.CRS.order_summary.btn_checkout, wait_displayed=True)
        # save order number in test data
        self._actions.store("order_number",
                            self._lib.general_helper.find(self._pages.CRS.order_summary.lbl_order_number,
                                                          get_text=True))
        # if OIT has serial number, enter serial number
        if data['config'].test_data(f"{data['current_oit']}.order_summary.serial_number"):
            self._lib.CRS.order_summary.enter_serial_number()

        self._actions.wait_for_element_enabled(self._pages.CRS.order_summary.btn_checkout)

        self._actions.step(f"--- ATOMIC TEST END --- {__name__} ---")

    def order_item_description(self):
        """
            Pre-conditions: Order Entry page is displayed
            Post-conditions: Order Entry page is displayed, Order item description is verified
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        data = self._lib.general_helper.get_data()
        # get OIT description for current OIT from tenant config file
        oit_description = data['config'].test_data(f"{data['current_oit']}.order_item_description.value")
        self._actions.verify_element_text(self._pages.CRS.order_entry.lbl_oit_description, oit_description)

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def order_summary_export_OIT(self):
        """
           Pre-conditions: Order Queue page is opened at Order Item tab, drawer is initialized
           Post-conditions: Order Summary page is displayed, Checkout button is displayed
           """
        self._actions.step(f"--- ATOMIC TEST --- {__name__} ---")

        # wait for Order Item tab to be displayed
        self._lib.general_helper.find(self._lib.CRS.order_entry.tab_locator("Order_Item"), wait_displayed=True)
        # atom - fill required fields
        self._lib.required_fields.crs_fill_required_fields()
        # Recorded Date ranges if the field exists
        cur_date = datetime.now().strftime("%m%d%Y")
        if self._lib.general_helper.check_if_element_exists(self._pages.CRS.order_entry.recorded_date):
            self._lib.general_helper.find_and_send_keys(self._pages.CRS.order_entry.recorded_date_fromdate, cur_date)
            self._lib.general_helper.find_and_send_keys(self._pages.CRS.order_entry.recorded_date_todate, cur_date)
        # fill the Date Export Expires range if the field exists
        if self._lib.general_helper.check_if_element_exists(self._pages.CRS.order_entry.exp_date):
            self._lib.general_helper.find_and_send_keys(self._pages.CRS.order_entry.exp_date, cur_date)
            self._lib.general_helper.find_and_send_keys(self._pages.CRS.order_entry.exp_date, Keys.TAB)
        # click schedule order
        self._actions.wait_for_element_enabled(self._pages.CRS.order_entry.btn_schedule_order)
        self._lib.general_helper.scroll_and_click(self._pages.CRS.order_entry.btn_schedule_order)
        # submit opened popup if exists
        self._lib.general_helper.find_and_click(
            self._pages.CRS.order_entry.btn_onetimeexport_submit, should_exist=False)
        # check that Order Summary screen is opened
        self._lib.general_helper.find(self._pages.CRS.order_finalization.lbl_order_finalize_label, wait_displayed=True)
        # get order number and save in data
        self._actions.store("order_number",
                            self._lib.general_helper.find(self._pages.CRS.order_summary.lbl_order_number,
                                                          get_text=True))

        self._actions.step(f"--- ATOMIC TEST END --- {__name__} ---")

    def select_doc_type(self):
        """
           Pre-conditions: Order Entry page is open on Order Item tab
           Post-conditions: Order Entry page is open on Order Item tab, Doc type is selected
           """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        data = self._lib.general_helper.get_data()
        # get order type for current OIT from tenant config file
        order_type = data['config'].test_data(f"{data['current_oit']}.order_type")
        # get doc type for current OIT from tenant config file
        order_doc_type = data['config'].test_data(f"{data['current_oit']}.order_doc_type")
        # enter doc type
        self._lib.general_helper.find_and_send_keys(self._pages.CRS.order_entry.txt_order_doc_type, order_doc_type)
        # click on doc type option in dropdown list
        doc_type_locator = self._lib.general_helper.make_locator(
            self._pages.CRS.order_entry.ddl_order_doc_type_by_ordertype_by_doctype,
            order_type, order_doc_type)
        self._lib.general_helper.scroll_and_click(doc_type_locator)

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def select_order_type(self):
        """
            Pre-conditions: Order Entry page is open, Order Type dropdown displayed
            Post-conditions: Order Entry page is open on Order Item tab
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        data = self._lib.general_helper.get_data()
        # get order type for current OIT from tenant config file
        order_type = data['config'].test_data(f"{data['current_oit']}.order_type")
        # select order type option from dropdown list
        self._actions.select_option_by_text(self._pages.CRS.order_entry.ddl_order_type, order_type)
        # wait for Order Item tab to be displayed
        self._lib.general_helper.find(self._lib.CRS.order_entry.tab_locator("Order_Item"), wait_displayed=True)

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))


    def fill_order_header_address(self):
        """
        Pre-conditions: Order Header is displayed
        Post-conditions: Customer address is entered in Order Header
        """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        data = self._lib.general_helper.get_data()
        self._lib.CRS.order_entry.click_more_options()
        self._lib.general_helper.find_and_send_keys(self._pages.CRS.order_entry.new_user_email_field, data['config'].order_header_fill('email.value'))
        self._lib.general_helper.find_and_send_keys(self._pages.CRS.order_entry.inp_customer__addr1, data['config'].order_header_fill('address.address'))
        self._lib.general_helper.find_and_send_keys(self._pages.CRS.order_entry.inp_customer__zip, data['config'].order_header_fill('address.zip'))
        self._lib.general_helper.find_and_send_keys(self._pages.CRS.order_entry.inp_customer__city, data['config'].order_header_fill('address.city'))
        self._actions.select_option_by_text(self._pages.CRS.order_entry.ddl_customer_state, data['config'].order_header_fill('address.state'))

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))