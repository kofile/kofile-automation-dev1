from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS -> Front Office, search all company accounts by clicking 'List All', 
    Check result table
        """
        
tags = ["48999_location_2"]


class test(TestParent):                                                                              # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs()
        # Navigate to Front Office
        self.lib.CRS.front_office.go_to_front_office()
        self.actions.click(self.pages.CRS.front_office.lnk_sub_menu_company_accounts)
        # Click 'List All' link and check result table
        self.lib.CRS.front_office.click_list_all_button()
        # Click 'Reset Search'
        self.lib.CRS.front_office.click_reset_search_button()


if __name__ == '__main__':
    run_test(__file__)
