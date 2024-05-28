from projects.Kofile.Atom.CRS.order_entry import OrderEntry
from projects.Kofile.Atom.CRS.general import General

from projects.Kofile.Lib.test_parent import AtomParent


class OrderQueue(AtomParent):
    def __init__(self):
        super(OrderQueue, self).__init__()

    def add_new_order(self):
        """
            Pre-conditions: Order Queue page is opened
            Post-conditions: Order Queue page is opened, Order type dropdown is displayed
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        self._lib.CRS.order_queue.add_new_order()
        self._actions.wait_for_element_displayed(self._pages.CRS.order_entry.ddl_order_type)

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def assign_order(self, ind=None):
        """
            Pre-conditions: Order Queue page is displayed
            Post-conditions: Order Queue page is displayed, order is assigned
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        # order should already be in order queue according to preconditions
        self._lib.CRS.crs.click_all_show_all_action_links()
        self._lib.CRS.crs.click_admin_key()
        user_index = ind if ind is not None else self._actions.execution.data["user_index"]
        self._lib.CRS.crs.assign_order_by_user_name(self._actions.execution.data["order_number"], user_index)

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def check_status_of_order(self, status):
        """
            Pre-conditions: Order Queue page is displayed
            Post-conditions: Order Queue page is displayed, order status is checked
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        self._actions.wait_for_element_displayed(self._pages.CRS.general.lbl_order_count)
        self._lib.CRS.crs.click_all_show_all_action_links()
        self._actions.wait_for_element_displayed(self._pages.CRS.general.lbl_order_count)
        self._lib.CRS.crs.verify_order_status(status)

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def create_and_action_with_order(self, action, ind=0, summary=None, open_crs=True, return_my_mail=False,
                                     oi_count=1):
        """
            Pre-conditions: CRS is opened, Order Queue is displayed
            Post-conditions: Order Summary is displayed. All OITs are reviewed
            """
        order_entry_atom, general = OrderEntry(), General()
        summary = summary if summary else order_entry_atom.one_oit_to_summary
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        if open_crs:
            general.go_to_crs(ind)
        # atom
        self.add_new_order()
        order_entry_atom.fill_order_header_name()
        for _ in range(oi_count):
            if _ != 0:
                self._lib.CRS.order_summary.click_new_order_item_icon()
            order_entry_atom.select_order_type()
            order_entry_atom.order_item_description()
            if return_my_mail:
                self._lib.CRS.order_entry.click_return_by_mail_checkbox()
                self._lib.CRS.order_entry.click_copy_from_order_header_link()
                self._lib.CRS.order_entry.get_return_by_mail_values()
            summary.__call__()
        if action:
            action.__call__()

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def fill_order_entry_tabs(self):
        """
            Pre-conditions: No
            Post-conditions: Order Entry page is opened on Order Item tab
            """
        order_entry_atom, general = OrderEntry(), General()
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        general.go_to_crs()
        self.add_new_order()
        order_entry_atom.fill_order_header_name()
        order_entry_atom.select_order_type()
        order_entry_atom.order_item_description()
        self._lib.general_helper.find(self._lib.CRS.order_entry.tab_locator("Order_Item"), wait_displayed=True)
        self._lib.required_fields.crs_fill_required_fields()
        self._lib.general_helper.find_and_click(self._lib.CRS.order_entry.tab_locator("Order_Item"))

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def get_next_order(self):
        """
           Pre-conditions: Order Queue page is displayed
           Post-conditions: Order Summary page is displayed
           """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        self._lib.general_helper.wait_and_click(self._pages.CRS.order_queue.btn_next_order)
        self._lib.general_helper.find_and_click(self._pages.CRS.order_queue.pup_drawer_initialize_btn_initialize,
                                                should_exist=False,
                                                timeout=5)

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def add_order_with_scan_first_flow(self, order_types):
        order_entry_atom, general = OrderEntry(), General()
        general.go_to_crs()
        self.add_new_order()
        order_entry_atom.fill_order_header_name()
        self._lib.CRS.order_entry.click_start_batch_scan_button()
        if not isinstance(order_types, list):
            order_types = [order_types]
        for i, oit in enumerate(order_types, 1):
            if oit and oit.lower() !='none':
                self._lib.CRS.capture.start_scan()
                self._actions.wait_for_element_not_enabled(self._pages.CRS.capture_summary.btn_save_and_exit)
                if oit in self._data['config'].get_order_types():
                    self._lib.CRS.capture.select_order_type(
                        self._data['config'].test_data(f"{oit}.order_type"), row_num=i)
                else:
                    self._lib.CRS.capture.select_order_type(oit, row_num=i)
        self._lib.CRS.order_item_type.save_order_in_capture_step(e_file=True)

