from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
        Log in to CS as a Clerk -> Property Records Search default page with clerk name is displayed
        Search for documents by any search criteria in any department -> Search results are found and displayed
        Sort the results by any column data (recorded date and doc number) ->
        Sorting in ascending order displays the data in a given column in ascending order
        Sorting in descending order displays the data in a given column by descending order
        """

tags = ['48999_location_2']


class test(TestParent):                                                                                     # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CS.general.go_to_cs(clerk=True)
        # search document
        self.lib.general_helper.find_and_click(self.pages.PS.main_page.search_button)
        self.lib.general_helper.wait_for_spinner()
        if self.lib.PS.ps_main_page.is_search_successful():
            self.lib.CS.general.check_sort(self.pages.PS.main_page.date_in_result_filter,
                                           self.pages.PS.main_page.date_in_result)
            self.lib.CS.general.check_sort(self.pages.PS.main_page.doc_num_in_result_filter,
                                           self.pages.PS.main_page.doc_num_in_result)
            self.lib.CS.general.check_sort(self.pages.PS.main_page.grantor_in_result_filter,
                                           self.pages.PS.main_page.grantor_in_result)
            self.lib.CS.general.check_sort(self.pages.PS.main_page.grantee_in_result_filter,
                                           self.pages.PS.main_page.grantee_in_result)
            self.lib.CS.general.check_sort(self.pages.PS.main_page.doc_type_in_result_filter,
                                           self.pages.PS.main_page.doc_type_in_result)
            self.lib.CS.general.check_sort(self.pages.PS.main_page.legal_dept_in_result_filter,
                                           self.pages.PS.main_page.legal_dept_in_result)
            self.lib.CS.general.check_sort(self.pages.PS.main_page.instrument_date_in_result_filter,
                                           self.pages.PS.main_page.instrument_date_in_result)
            self.lib.CS.general.check_sort(self.pages.PS.main_page.book_vol_page_in_result_filter,
                                           self.pages.PS.main_page.book_vol_page_in_result)
        else:
            raise ValueError("Search failed!")


if __name__ == '__main__':
    run_test(__file__)
