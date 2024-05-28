"""smoke test"""

from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS, add Export OIT and save. .If run job flag is true, Run export job and verify \
        order status is finalized.
    Find order from order search. Verify order in archive. Click edit. Void order, go to order search and \
    verify status is Voided. If FTP flag is true go to FTP and check if order exist
    """

tags = ['48999_location_2']

class test(TestParent):  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: no
        Post-conditions: Order is processed from Order Queue to Archive
        """
        self.data["current_oit"] = self.data.OIT
        self.lib.general_helper.check_order_type()
        self.atom.CRS.order_queue.create_and_action_with_order(
            None, summary=self.atom.CRS.order_entry.order_summary_export_OIT)
        # verify status is Scheduled
        expected_status = self.data['config'].get_status('Order.Scheduled_status.value')
        self.actions.verify_element_text(self.pages.CRS.order_finalization.status_by_row_index(), expected_status)

        # execute scheduler job
        if self.data.jobrun == '1':
            self.lib.db_with_vpn.scheduler_job_update_for_export(scheduler_job_code=self.data.jobname)


if __name__ == '__main__':
    run_test(__file__)
