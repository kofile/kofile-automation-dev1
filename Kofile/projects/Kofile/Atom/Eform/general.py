from projects.Kofile.Lib.general_helpers import EformHelpers
from projects.Kofile.Lib.test_parent import AtomParent


class General(AtomParent):
    def __init__(self):
        super(General, self).__init__()

    def add_to_cart(self):
        """
            Pre-conditions: eForm is opened with configured Cart Mode
            Post-conditions: Cart is opened with added eForm
            """
        self._actions.step(f"--- ATOME TEST --- {__name__} ---")
        self._lib.required_fields.eform_fill_required_fields()
        self._actions.wait_for_element_enabled(self._pages.eform.btn_submit_eform)
        self._actions.click(self._pages.eform.btn_submit_eform)
        self._actions.wait_for_element_displayed(self._pages.eform.txt_customer_name)
        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def create_and_submit_eform(self):
        """
            Pre-conditions: No
            Post-conditions: eForm order is submitted, order number saved in data
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        self.go_to_eform_portal()
        self.open_eform_document()
        self.submit_eform()

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def go_to_eform_portal(self):
        """
            Pre-conditions: No
            Post-conditions: eForm portal page is opened
            """
        # go to eform
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        self._actions.get_browser().set_window_size(1920, 1080)
        self._actions.get(EformHelpers.get_url())

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def open_eform_document(self):
        """
          Pre-conditions: Eform portal page is opened
          post-conditions: Selected e-OIT form is opened
          """
        # click on order type
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        # note: these two options only for headless browser
        data = self._lib.general_helper.get_data()
        order_type = data['config'].test_data(f"{data.OIT}.order_type").lower()
        order_tye_loc = self._lib.general_helper.make_locator(self._pages.eform.lnk_eform_order_type, order_type)
        self._actions.click(order_tye_loc)
        self._actions.wait_for_element_displayed(self._pages.eform.btn_submit_eform)

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def submit_eform(self):
        """
            Pre-conditions: eForm is opened
            Post-conditions: eForm is submitted, order number is saved
            """
        self._actions.step(f"--- ATOME TEST --- {__name__} ---")

        data = self._lib.general_helper.get_data()
        if data.OIT == 'Eform_Death_Certified_Copy':
            self._actions.click(self._pages.eform.rbt_death_certificate)
        self._lib.required_fields.eform_fill_required_fields()
        self._actions.wait_for_element_enabled(self._pages.eform.btn_submit_eform)
        # Check Cart Mode:
        if self._actions.get_element_value(self._pages.eform.btn_submit_eform) == "Add To Cart":
            # Cart Mode is "true" as submit button value is "Add To Cart"
            self._actions.click(self._pages.eform.btn_submit_eform)
            self._actions.wait_for_element_displayed(self._pages.eform.txt_customer_name)
            self._actions.send_keys(self._pages.eform.txt_customer_name, "Test Customer Name")
            self._actions.press_key(self._pages.eform.txt_customer_name, 'TAB')
            self._actions.wait_for_element_enabled(self._pages.eform.btn_checkout)
            self._actions.click(self._pages.eform.btn_checkout)
        else:
            # Cart Mode is "false" as submit button value is "Submit"
            self._actions.click(self._pages.eform.btn_submit_eform)
        self._actions.wait_for_element_displayed(self._pages.eform.pup_submission_txt_order)
        self._actions.store("order_number", self._actions.get_element_text(self._pages.eform.pup_submission_txt_order))

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))
