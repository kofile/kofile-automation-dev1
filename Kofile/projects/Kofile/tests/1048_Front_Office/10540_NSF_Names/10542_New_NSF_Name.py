"""+ New NSF Name"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test
from datetime import datetime

description = """
              Go to CRS -> Front Office -> Financial -> NSF Names
              Click on + New Row
              Enter a unique (non-existing) NSF Name and Check Number, Check Amount, Check Datetime, Order #, 
              Active values and save
              Search for the newly added NSF Name and verify that the new name is found in search results
              """

tags = ["48999_location_2"]


class test(TestParent):                                                                     # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # test data
        datetime_now = datetime.now()
        unique_number = datetime_now.strftime("%Y%m%d%H%M%S")           # uuid.uuid4().hex
        nsf_name, check_number, check_amount, active = f"Auto_NSF_{unique_number}", f"Check_{unique_number}", 100, False
        check_date = datetime_now.strftime("%m/%d/%Y")
        order_number = f"{datetime_now.strftime('%Y%m%d')}00001"
        new_nsf_name_values = {"txt_nsf_name": nsf_name, "txt_check_number": check_number,
                               "txt_check_amount": check_amount, "txt_check_date": check_date,
                               "txt_order_number": order_number, "chx_active": active}
        # go to front office and create a new unique nsf_name with the above test data
        self.lib.data_helper.get_front_office()
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.front_office.go_to_front_office()
        self.lib.CRS.front_office.go_to_nsf_names_submenu()
        self.lib.CRS.front_office.create_new_nsf_name(new_nsf_name_values)
        # search for the newly created nsf_name and verify that name is found in search results
        self.lib.CRS.front_office.search_for_nsf_name(new_nsf_name_values.get("txt_nsf_name"))
        nsf_names_in_results = self.lib.CRS.front_office.get_nsf_names_in_search_results()
        assert len(nsf_names_in_results) == 1, \
            f"{len(nsf_names_in_results)} results are found for searched NSF Name instead of one"
        assert nsf_names_in_results[0] == new_nsf_name_values.get("txt_nsf_name"), \
            f"Actual NSF Name '{nsf_names_in_results[0]}' found does NOT match " \
            f"the expected '{new_nsf_name_values.get('txt_nsf_name')}'"


if __name__ == '__main__':
    run_test(__file__)
