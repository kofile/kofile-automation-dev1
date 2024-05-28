from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to Public Search
    Click on search button in each department
    Check that results are found or "Sorry, no matches found." message is displayed
"""

tags = ['48999_location_2']


class test(TestParent):                                                                                 # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to Public Search
        self.atom.CS.general.go_to_cs(clerk=False, load_config=False, public_search=True)
        # Collect all department names
        departments = self.lib.PS.ps_main_page.department_list(return_names=True, return_all=True)
        # Search documents in each department
        for dep in departments:
            self.lib.PS.ps_main_page.click_on_department_tab(dep)
            self.lib.PS.ps_main_page.click_search_button()
            # Check "Sorry, no matches found." message
            if self.lib.PS.ps_main_page.is_search_successful():
                # Check result table
                assert self.lib.PS.ps_main_page.get_found_document_numbers(), \
                    f"Documents NOT found in PS department {dep} result table!"


if __name__ == '__main__':
    run_test(__file__)
