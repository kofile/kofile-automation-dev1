from projects.Kofile.Lib.test_parent import AtomParent


class General(AtomParent):
    def __init__(self):
        super(General, self).__init__()

    def go_to_crs(self, ind=0):
        """
        Pre-conditions: No
        Post-conditions: CRS homepage is displayed
        """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        # note: these two options are only for headless browser
        self._actions.get_browser().set_window_size(1920, 1080)
        # self._actions.get_browser().maximize_window()
        self._actions.get(self._lib.general_helper.get_url(ind))
        self._actions.store("user_index", ind)

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

        try:
            return self._actions.get_cookie("ASP.NET_SessionId").get("value")
        except Exception as e:
            self._logging.info(type(e).__name__)