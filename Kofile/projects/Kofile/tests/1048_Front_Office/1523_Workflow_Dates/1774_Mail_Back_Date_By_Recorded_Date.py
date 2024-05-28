from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Navigate to CRS ->
    Navigate to Front Office ->
    Click on the "Workflow Dates" sub-tab ->
    Select "Mail Back Date By Recorded Date" radio button ->
    Set recorded Date range current date and click on Search button ->
    Set mail back date today and save changes ->
    Create an RP order, set mail back date and finalize it. ->
    Again from Front Office/Workflow Dates/ Mail back menu search for today's documents ->
    Again set mail back end date today ->
    Changes saved. Mail back date is updated for the new recorded document too. Warning triangle disappeared.
        """

tags = []


class test(TestParent):

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.data_helper.get_front_office()
        self.atom.CRS.general.go_to_crs()
        # Navigate to Front Office
        self.actions.wait(1)
        self.lib.CRS.front_office.go_to_front_office()
        # Navigate to workflow dates sub
        self.lib.CRS.front_office.go_to_workflow_dates_sub()

        # set checkboxes
        self.lib.CRS.front_office.set_mail_back_date_by_recorded_date()
        self.lib.CRS.front_office.set_date_range()
        doc_count = self.lib.CRS.front_office.edit_mail_back_date()

        # create and finalize rp order
        self.lib.CRS.crs.go_to_order_queue()
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order, open_crs=False,
                                                               return_my_mail=True)

        # check mail back doc count
        self.atom.CRS.general.go_to_crs()
        self.actions.wait(1)
        self.lib.CRS.front_office.go_to_front_office()
        self.lib.CRS.front_office.go_to_workflow_dates_sub()
        self.lib.CRS.front_office.set_mail_back_date_by_recorded_date()
        self.lib.CRS.front_office.set_date_range()
        self.lib.CRS.front_office.verify_doc_count(doc_count)


if __name__ == '__main__':
    run_test(__file__)
