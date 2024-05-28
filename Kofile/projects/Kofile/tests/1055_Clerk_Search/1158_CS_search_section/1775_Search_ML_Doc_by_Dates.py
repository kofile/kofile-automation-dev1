"""Search ML Doc by Dates"""
from datetime import date, timedelta
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
              Finalize an ML order.
              Find the created ML doc in CS by Application Date = Finalization Date.
              Find the ML doc in Capture step, scan and map, enter Recording Date = Finalization Date and save. 
              Find the ML document in CS by Recording Date
              """

tags = ['48999_location_2']


class test(TestParent):                                                                                # noqa

    def __init__(self, data):
        data["OIT"] = "Marriage_License"
        super(test, self).__init__(data, __name__, precondition=self._precondition)

    def __test__(self):
        cs_config = self.lib.data_helper.test_config(oit=self.data["OIT"])
        dept_id = cs_config["dept_id"]
        date_from = (date.today() - timedelta(days=1)).strftime(self.lib.general_helper.DATE_PATTERN)
        date_to = (date.today() - timedelta(hours=9)).strftime(self.lib.general_helper.DATE_PATTERN)

        self.lib.db_with_vpn.scheduler_job_update_for_set_export_document(dept_id)
        self.atom.CS.general.go_to_cs()
        self.lib.CS.general.go_to_department_by_dept_id(dept_id)
        self.lib.CS.general.search_ml_docs_by_date(date_from, date_to)
        self.lib.CS.general.verify_doc_number_in_results(self.data["doc_year-doc_num"], should_exist=True)
        self.lib.CS.general.clear_dates()
        self.lib.CS.general.search_ml_docs_by_date(date_from, date_to)
        self.lib.CS.general.verify_doc_number_in_results(self.data["doc_year-doc_num"], should_exist=False)
        self.atom.CS.api_helper.capture_document()
        self.lib.db_with_vpn.scheduler_job_update_for_set_export_document(dept_id)
        self.atom.CS.general.go_to_cs()
        self.lib.CS.general.go_to_department_by_dept_id(dept_id)
        self.lib.CS.general.search_ml_docs_by_date(date_from, date_to, date_name="recording")
        self.lib.CS.general.verify_doc_number_in_results(self.data["doc_year-doc_num"], should_exist=True)

    def _precondition(self):
        self.atom.CS.api_helper.initialize_drawer()
        self.atom.CS.api_helper.create_order()


if __name__ == '__main__':
    run_test(__file__)
