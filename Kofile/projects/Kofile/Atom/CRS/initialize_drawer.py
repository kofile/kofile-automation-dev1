from projects.Kofile.Lib.test_parent import AtomParent


class InitializeDrawer(AtomParent):
    def __init__(self):
        super(InitializeDrawer, self).__init__()

    def initialize_drawer(self):
        """
            Pre-conditions: CRS is Opened
            Post-conditions: Drawer Initialized
            """
        self._actions.step(f"--- ATOMIC TEST --- {__name__} ---")

        # click on initialize drawer tab
        self._lib.CRS.balance_drawer.go_to_initialize_drawer()
        # wait for drawer initialization screen to open
        self._lib.general_helper.find(self._pages.CRS.initialize_drawer.btn_cancel, wait_displayed=True)
        # Check if submit is enabled click submit
        if self._lib.general_helper.find_and_click(self._pages.CRS.initialize_drawer.btn_submit, timeout=5,
                                                   should_exist=False):
            self._actions.wait(2)
            self._actions.refresh_page()
            self._lib.general_helper.find(self._pages.CRS.initialize_drawer.btn_submit_inactive_id, timeout=5,
                                          wait_displayed=True)
            self._lib.CRS.crs.go_to_order_queue()
        else:
            self._lib.CRS.crs.go_to_order_queue()

        self._actions.step(f"--- ATOMIC TEST END --- {__name__} ---")
