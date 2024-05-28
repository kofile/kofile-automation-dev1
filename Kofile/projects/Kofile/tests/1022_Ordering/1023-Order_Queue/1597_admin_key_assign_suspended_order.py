"""cancel order test"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Create order with user1, save order.
                Find Order from Order Queue. Assign order to user4. Verify name after assignment"""

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data, ind=1):
        self.ind = ind
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: Order Queue
        Post-conditions: Order is in  suspended status and assigned to another clerk
        """
        self.data["current_oit"] = self.data.OIT
        self.lib.general_helper.check_order_type()
        # atom test
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.order_summary.save_order)
        # assign order
        self.lib.CRS.crs.go_to_order_queue()
        self.atom.CRS.order_queue.assign_order(ind=self.ind)
        assign_name_el = (self.pages.CRS.general.assigned_to_by_order_number_text(self.data["order_number"]))
        self.actions.verify_element_attribute(assign_name_el, 'value',
                                              self.lib.CRS.crs.assign_user_name(ind=self.ind))


if __name__ == '__main__':
    run_test(__file__)
