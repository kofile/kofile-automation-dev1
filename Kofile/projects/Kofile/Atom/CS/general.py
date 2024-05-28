from projects.Kofile.Atom.CRS.order_summary import OrderSummary
from projects.Kofile.Atom.CRS.general import General as GeneralAtom
from projects.Kofile.Lib.general_helpers import ClerkSearchGeneralHelpers as CSHelper
from projects.Kofile.Lib.test_parent import AtomParent


class General(AtomParent):
    def __init__(self):
        super(General, self).__init__()

    def finalize_and_check_in_crs(self):
        """
           Check order in CRS and finalize
           """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        self._lib.CRS.crs.click_running_man()
        self._lib.PS.general.check_doc_number_in_order_summary()
        self._lib.PS.general.calculate_fee()
        self._lib.PS.general.check_status_and_type_in_order_summary()
        self._lib.PS.general.check_doc_type_in_order_summary()
        self._lib.PS.general.edit_order_and_save()
        self._lib.PS.general.checkout_order()
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def finalize_cs_order(self):
        general = GeneralAtom()
        """
            Pre-conditions: No
            Post-conditions: Order summary is displayed
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        general.go_to_crs()
        self._lib.CRS.crs.click_running_man()
        self._lib.general_helper.wait_for_spinner()
        self._lib.PS.general.edit_order_and_save()
        self._lib.PS.general.checkout_order()

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def go_to_cs(self, clerk=True, load_config=True, oit=None, public_search=False):
        """
           Pre-conditions:
           start - no
           finish - CS page opened
           CRS: clerk=True, public_search=False
           KS: clerk=False, public_search=False
           PS: clerk=False, public_search=True
           """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        if load_config:
            self._actions.step("--- *Load CS test config* ---")
            self._lib.data_helper.test_config(oit)
            self._actions.step("--- *CS test config loaded successfully* ---")
        # note: these two options only for headless browser
        self._actions.get_browser().set_window_size(1920, 1080)
        self._actions.get_browser().maximize_window()
        # go to CS
        self._actions.get(CSHelper.get_url(clerk=clerk, public_search=public_search))
        # Wait till page loaded
        self._lib.general_helper.find(self._pages.PS.main_page.logo, 60)
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def process_order_from_cs_to_order_summary(self):
        """
           Pre-conditions: None
           Post-conditions: Order summary is displayed
           """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        general = GeneralAtom()
        # Atom
        self.go_to_cs()
        # Get random doc number for OIT
        self._api.clerc_search(self._lib.general_helper.get_data()).get_document_number()
        self.submit_to_crs()
        general.go_to_crs()
        self._lib.CRS.crs.click_running_man()

        self._actions.wait(1)
        OrderSummary().edit_oit()
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def submit_to_crs(self, clear_inbox=True):
        """
          Adds single document specified by doc_num from req_dept_tab tab to Inbox
          and submit new order to CRS. Returns order number as string if
          operation was successful, empty string otherwise
          """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))
        data = self._lib.general_helper.get_data()
        order_type = data.get("test_config").get("order_type")
        req_dept_tab = data.get("test_config").get("dept")
        doc_num = data.get("doc_num")
        if clear_inbox:
            self._api.clerc_search(data).clear_inbox()
        # dept list
        self._lib.PS.ps_main_page.click_on_department_tab(req_dept_tab)
        # enter doc number to search field
        self._lib.PS.ps_main_page.search_field(doc_num)
        # narrow search
        self._lib.PS.ps_main_page.click_more_options_button()
        # set recorded date range 'to' date
        self._lib.PS.ps_main_page.date_to_set(req_dept_tab)
        if "Doc#" in self._lib.PS.ps_main_page.get_checkbox_names():
            self._lib.PS.ps_main_page.click_checkbox("Doc#")
        self._lib.PS.ps_main_page.select_document_group()
        self._lib.PS.ps_main_page.click_search_button()
        if self._lib.PS.ps_main_page.is_search_successful():
            self._lib.PS.ps_main_page.click_row_with_doc_number(
                doc_num, not_in_workflow=True if order_type in ["Re-Index", "Re-Capture"] else False)
            self._lib.PS.ps_preview.click_tab("Summary")
            self._lib.PS.ps_summary_tab.document_preview_summary()
            self._lib.PS.ps_preview.click_add_to_inbox(1)
            self._lib.PS.ps_preview.click_close()
            self._lib.PS.ps_main_page.click_inbox()
            # set order type
            self._lib.PS.ps_inbox.select_order_type(order_type)
            # add customer name
            if order_type not in ["Re-Index", "Re-Capture"]:
                self._lib.PS.ps_inbox.customer_name("TEST CUSTOMER NAME")
            if order_type == "Copy":
                data["current_oit"] = "Copies"
            self._lib.PS.ps_inbox.click_submit()
            conf_num = self._lib.PS.ps_inbox.confirmation_order_number()
            self._actions.store("order_number", conf_num)
            self._actions.take_screenshot("Confirmation pop-up")
            self._lib.PS.ps_inbox.confirmation_close()
        else:
            raise ValueError("Search failed!")
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))
