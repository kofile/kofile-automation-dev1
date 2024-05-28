from projects.Kofile.Lib.test_parent import LibParent


class IndexingSummary(LibParent):
    def __init__(self):
        super(IndexingSummary, self).__init__()

    def click_next_order_button(self):
        self._general_helper.find_and_click(self._pages.CRS.indexing_summary.btn_next_order)
        self._general_helper.wait_for_spinner()

