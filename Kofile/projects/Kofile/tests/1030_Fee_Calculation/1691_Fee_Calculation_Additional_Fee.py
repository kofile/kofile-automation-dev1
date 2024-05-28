"""Fee Calculation: Additional Fee"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Check 'Additional Fee' calculation"""

tags = []            # additional fees are missing for RP both in ref and PT


class test(TestParent):                                                                              # no qa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        if self.data.OIT in self.data['config'].get_order_types() and \
                self.data['config'].test_data(f"{self.data['OIT']}.additional_fee_labels"):
            self.atom.CRS.order_queue.fill_order_entry_tabs()
            self.lib.CRS.order_entry.enter_and_verify_additional_fees()
        else:
            self.actions.error(f"{self.data.OIT} does not exist for current tenant or OIT has no additional fees")


if __name__ == '__main__':
    run_test(__file__)
