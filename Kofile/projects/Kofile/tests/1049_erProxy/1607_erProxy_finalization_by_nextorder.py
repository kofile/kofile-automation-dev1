"""erProxy finalization via Next Order"""

import configparser
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """erProxy Finalization via Next Order button"""

# This test is skipped, since clicking on Next Order from order queue
# may take any other non-erProxy order.

configparser.ConfigParser()


class test(TestParent):                                                                              # noqa
    count = 0

    def __init__(self, data, cycle_count=None):
        self.cycle_count = cycle_count
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: er-proxy order(s) is(are) finalized
        cycle_count shows how many times the test will be repeated
        if cycle_count=None, all orders will be processed until 'No Order to Process'
        """

        # check if there are orders to process via Next Order
        self.atom.CRS.general.go_to_crs()
        self.atom.CRS.order_queue.get_next_order()
        if 'No Order To Process.' not in self.actions.get_browser().page_source:
            while 'Order Summary' in self.actions.get_browser().page_source and self.count != self.cycle_count:
                self.atom.CRS.order_summary.edit_oit()
                self.actions.click(self.pages.CRS.order_summary.btn_checkout)
                self.actions.wait_for_element_displayed(self.pages.CRS.order_finalization.lbl_order_finalize_label)

                # check thumbnails after finalization
                row_number = self.actions.get_browser().find_all(self.pages.CRS.order_finalization.row_numbers)
                for row in row_number:
                    self.actions.click(row)
                    self.atom.CRS.image_viewer.thumbnail_checking()

                # get next order
                self.actions.click(self.pages.CRS.order_finalization.btn_get_next)
                self.actions.step("Created {}".format(self.count))
                self.count += 1
                if 'Error' in self.actions.get_browser().find_element_by_tag_name('body').text:
                    self.actions.fail("Error occurs.")
                    self.actions.take_screenshot()
                self.lib.general_helper.wait_for_spinner()
        else:
            self.actions.step(" 'There is no  order to process' popup is displayed")


if __name__ == '__main__':
    run_test(__file__)
