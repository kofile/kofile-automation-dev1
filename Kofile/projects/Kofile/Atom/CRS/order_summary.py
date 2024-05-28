from projects.Kofile.Lib.test_parent import AtomParent


class OrderSummary(AtomParent):
    def __init__(self):
        super(OrderSummary, self).__init__()

    def add_tracking_id(self):
        """
            Pre-conditions: Order Summary is opened
            Post-conditions: Tracking ID added to order and saved in data.tracking_id
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        self._lib.CRS.order_summary.click_add_tracking_id_button()
        self._actions.store("tracking_id", self._lib.CRS.order_summary.fill_in_tracking_id())
        self._lib.CRS.order_summary.submit_tracking_id()

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def cancel_order(self):
        """
           Pre-conditions: Order Summary is opened
           Post-conditions: Order is cancelled, Order Queue is opened
           """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        self._lib.CRS.order_summary.click_cancel_entire_order()
        self._lib.CRS.crs.fill_reason(self._pages.CRS.order_summary.pup_Cancel_entire_order_reason)

        self._actions.wait_for_element_displayed(self._pages.CRS.order_queue.btn_add_new_order)
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def edit_oit(self, edit_all=False):
        """
           Pre-conditions: Order Summary is displayed,
           Post-conditions: Order Summary is displayed. All OITs are reviewed
           """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        data = self._lib.general_helper.get_data()
        use_row_checkbox = data['config'].test_data(f"{data.OIT}.order_summary.use_row_checkbox")
        # wait order summary is displayed
        self._actions.wait_for_element_present(self._pages.CRS.order_summary.lbl_order_number)
        rows_number = self._lib.CRS.order_summary.get_number_of_rows()
        for row in range(1, rows_number + 1):
            status = self._lib.CRS.order_summary.get_status_by_row_index(row)
            # check if status of oit is pending, edit oit
            if status == 'Pending' or edit_all:
                #  if checkbox is configured, check on checkbox, else edit oit
                if use_row_checkbox:
                    checkbox = self._pages.CRS.order_summary.checkbox_by_row_index(row)
                    self._lib.general_helper.wait_and_click(checkbox)
                else:
                    self._lib.CRS.order_summary.click_edit_icon_by_row_index(row)
                    self._lib.CRS.order_entry.wait_order_item_tab_displayed()

                    self._lib.required_fields.crs_fill_required_fields()

                    # check if OIT has document type dropdown, pass it to data
                    doc_type_config = data['config'].test_data(f"{data.OIT}.doc_type")
                    if doc_type_config and data.get("order_type") != "Copy":
                        self._lib.CRS.order_entry.select_doctype()

                    self._lib.CRS.order_entry.click_add_to_order()

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def reject_order(self):
        """
           Pre-conditions: Order Summary is opened
           Post-conditions: Order is rejected, Order Queue is opened
           """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        # fill tracking id
        self.add_tracking_id()
        self._lib.general_helper.wait_and_click(self._pages.CRS.order_summary.lnk_reject_entire_order, scroll=True)
        self._lib.CRS.crs.reject_erproxy_order()
        self._actions.wait_for_element_displayed(self._pages.CRS.order_queue.btn_add_new_order)
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def save_order(self):
        """
          Pre-conditions: Order Summary is opened
          Post-conditions: Order is saved, Order Queue is opened
          """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        # click save order button
        self._lib.general_helper.wait_and_click(self._pages.CRS.order_summary.btn_save_order, scroll=True)
        self._lib.CRS.crs.fill_reason(self._pages.CRS.order_summary.pup_Cancel_entire_order_reason)
        # wait for add new order button in order queue
        self._actions.wait_for_element_displayed(self._pages.CRS.order_queue.btn_add_new_order)
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def send_to_admin(self):
        """
           Pre-conditions: Order Summary is opened
           Post-conditions: Order is sent to admin, Order Queue is opened
           """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        # click Send To Administrator action link
        self._lib.general_helper.wait_and_click(self._pages.CRS.order_summary.lnk_send_to_admin, scroll=True)
        self._lib.CRS.crs.fill_reason(self._pages.CRS.order_summary.pup_Cancel_entire_order_reason)
        # wait for add new order button in order queue
        self._actions.wait_for_element_displayed(self._pages.CRS.order_queue.btn_add_new_order)
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))
