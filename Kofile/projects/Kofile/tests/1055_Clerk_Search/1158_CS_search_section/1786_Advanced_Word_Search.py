"""Advanced Word Search"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
              Search for documents in CS by more than one keyword in Advanced Word Search mode
              """

tags = ['48999_location_2']


class test(TestParent):                                                                                    # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CS.general.go_to_cs()
        column_data = {}
        self.lib.general_helper.find_and_click(self.pages.CS.main_page.rbn_advanced_word_search)
        self.lib.CS.general.click_on_search_button()
        if self.lib.PS.ps_main_page.is_search_successful():

            self.logging.info("ADVANCED SEARCH BY DOC DETAILS AND PARTY NAME--------------------------------")
            self.lib.CS.general.double_click_on_column_sort(2)
            for i in range(2, 10):
                column_name = self.lib.CS.general.get_column_name_by_index(i)
                dataset = self.pages.CS.main_page.column_data_by_row_and_column_index(1, i)
                column_data.update({column_name: dataset})
            for i in (
                    'Document Type',
                    'Recorded Date'):  # search by instrument date and book/page is not performed on UAT (8, 9)
                self.lib.general_helper.find_and_send_keys(self.pages.CS.main_page.txt_search_input, column_data[i])
                self.lib.general_helper.find_and_send_keys(
                    self.pages.CS.main_page.txt_name_search, f"{column_data['Grantor']}, {column_data['Grantee']}")
                self.lib.CS.general.click_on_search_button()
                self.lib.CS.general.double_click_on_column_sort(2)
                assert column_data['Document#'] in self.pages.CS.main_page.column_data_by_row_and_column_index(1, list(
                    column_data.keys()).index('Document#') + 2), \
                    f"Expected result missing for advanced search by column {i}"

            self.logging.info("ADVANCED SEARCH BY USING TYPE AHEAD --------------------------------------------")
            if len(column_data) > 2 and len(column_data['Grantor']) > 3:
                self.lib.general_helper.find_and_send_keys(self.pages.CS.main_page.txt_name_search,
                                                           column_data['Grantor'][:3])
                self.lib.general_helper.find_and_click(self.lib.general_helper.make_locator(
                    self.pages.CS.main_page.ddl_name_lookup_, column_data['Grantor'],
                    str(column_data['Grantor']).lower()))
                self.lib.CS.general.click_on_search_button()
                assert column_data['Grantor'] in self.pages.CS.main_page.column_data_by_row_and_column_index(1, list(
                    column_data.keys()).index('Grantor') + 2)

                self.logging.info("ADVANCED SEARCH BY KEYWORD CONTAINING WILD-CART CHARACTERS '?'= 1 SYMBOL,"
                                  " '*' = ANY NUMBER OF SYMBOLS -------------")

                self.lib.general_helper.find_and_send_keys(self.pages.CS.main_page.txt_name_search,
                                                           column_data['Grantor'].replace(column_data['Grantor'][1],
                                                                                          '?'))
                self.lib.CS.general.click_on_search_button()
                assert column_data['Grantor'] in self.pages.CS.main_page.column_data_by_row_and_column_index(1, list(
                    column_data.keys()).index('Grantor') + 2)
                self.lib.general_helper.find_and_send_keys(self.pages.CS.main_page.txt_name_search,
                                                           column_data['Grantor'].replace(column_data['Grantor'][1:3],
                                                                                          '*'))
                self.lib.CS.general.click_on_search_button()
                assert column_data['Grantor'] in self.pages.CS.main_page.column_data_by_row_and_column_index(1, list(
                    column_data.keys()).index('Grantor') + 2)

            else:
                self.actions.step("No search data with suitable party name found")

        else:
            self.actions.error("No search data found at all")


if __name__ == '__main__':
    run_test(__file__)
