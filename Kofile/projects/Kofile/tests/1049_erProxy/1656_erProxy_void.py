"""erProxy finalization"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """erProxy workflow, up to Archive, check in CS"""

tags = ['48999_location_2']


class test(TestParent):                                                                                  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: erProxy order voided
        """
        # submit erProxy and get created erProxy order number
        self.data["order_number"] = self.atom.ERProxy.general.create_er_proxy()[0][0]
        # go to CRS
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.crs.go_to_order_queue()
        self.atom.CRS.order_queue.assign_order()
        self.lib.general_helper.wait_for_spinner()
        # edit order
        self.lib.CRS.crs.click_running_man()
        self.actions.wait_for_element_displayed(self.pages.CRS.order_summary.lbl_order_number)
        self.atom.CRS.order_summary.edit_oit()
        # finalize order
        self.atom.CRS.add_payment.finalize_order()
        # void order
        self.atom.CRS.order_finalization.void_order()


if __name__ == '__main__':
    run_test(__file__)
