from projects.Kofile.Lib.test_parent import AtomParent

from projects.Kofile.Atom.CS.general import General as CSGeneral

general = CSGeneral()


class General(AtomParent):
    def __init__(self):
        super(General, self).__init__()

    def login_to_KS(self):
        """
            Pre-conditions: No
            Post-conditions: Kiosk Search homepage is displayed, user is logged in
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        env = self._actions.execution.data["env"]
        general.go_to_cs(clerk=False, public_search=False)
        if not self._lib.general_helper.find(self._pages.KS.home_page.lnk_sign_out, should_exist=False, timeout=5):
            self._lib.general_helper.find_and_click(self._pages.KS.home_page.lnk_sign_in)
            self._lib.general_helper.find_and_send_keys(self._pages.KS.home_page.txt_email_pup_sign_in,
                                                        env["kiosk_user_email"])
            self._lib.general_helper.find_and_send_keys(self._pages.KS.home_page.txt_password_pup_sign_in,
                                                        env["kiosk_user_password"])
            self._lib.general_helper.find_and_click(self._pages.KS.home_page.btn_sign_in_pup_sign_in)
            self._lib.general_helper.find(self._pages.KS.home_page.lnk_sign_out, wait_displayed=True)
        general.go_to_cs(clerk=False, public_search=False)

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))
