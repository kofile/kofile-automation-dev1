"""Basic Word Search"""
from projects.Kofile.Lib.test_parent import TestParent

from runner import run_test

description = """
              Search for documents by search options in CS in Basic Word Search mode
              """

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data):
        # This is the sequence of rows in search
        self.search_options_by_column_order = \
            ["Names", "Names", "Doc Type", "Recorded Date", "Doc#", "Legal", None]
        super(test, self).__init__(data, __name__)

    def __48999__(self):
        self.search_options_by_column_order = \
            ["Parcel ID", "Names", "Names", "Doc Type", "Recorded Date", "Doc#", "Legal", None]

    def __test__(self):
        self.atom.CS.general.go_to_cs()
        self.lib.CS.general.click_on_search_button()
        if self.lib.PS.ps_main_page.is_search_successful():

            self.logging.info("BASIC SEARCH BY SEARCH OPTIONS --------------------------------")
            bvp = "Book/Liber/Page" if "dev" in self.data.env.config_name else "Book/Vol/Page"
            self.search_options_by_column_order.append(bvp)
            # Indexing by default starts from 0 and the first column in UI is '+'
            for index, i in enumerate(self.search_options_by_column_order, start=2):
                if i:
                    for _ in range(10):
                        self.lib.CS.general.click_on_search_button()
                        if table := self.lib.general_helper.find(self.pages.CS.main_page.result_table, timeout=3,
                                                                 should_exist=False):
                            if table.is_displayed():
                                self.actions.take_screenshot("result has been find")
                                break
                        self.actions.wait(1)
                    self.lib.CS.general.double_click_on_column_sort(column_index=index)
                    column_data = self.pages.CS.main_page.column_data_by_row_and_column_index(1, index)
                    if column_data:
                        self.lib.CS.general.click_on_search_option(i)
                        self.lib.CS.general.search_by_keyword(column_data)
                        assert column_data in self.pages.CS.main_page.column_data_by_row_and_column_index(
                            1, index), f"Search by {i} option failed!"
                        self.lib.CS.general.reset_search()

            self.logging.info("BASIC SEARCH BY DOC_GROUP OPTIONS ----------------------------")
            if self.data.get("env").get("code") == "69999":
                doc_group_options = ["FEDERAL TAX LIENS", "PERSONAL PROPERTY", "STATE TAX LIENS"]
                expected_texts = ["FEDERAL TAX LIEN", "PERSONAL PROPERTY", "STATE TAX LIEN"]
                for i in doc_group_options:
                    index = doc_group_options.index(i)
                    self.lib.CS.general.click_on_search_option(i)
                    self.lib.CS.general.click_on_search_button()
                    if self.lib.PS.ps_main_page.is_search_successful():
                        assert expected_texts[index] in self.pages.CS.main_page.column_data_by_row_and_column_index(
                            1, 4), f"Search by {i} doc group option failed!"
                    self.lib.CS.general.reset_search()

            self.logging.info("BASIC SEARCH BY AND/OR OPTION WITH SEVERAL KEYWORDS ----------------------------")
            self.lib.CS.general.click_on_search_button()
            self.lib.CS.general.double_click_on_column_sort(column_index=2)
            grantor = self.pages.CS.main_page.column_data_by_row_and_column_index(1, 2)
            grantee = self.pages.CS.main_page.column_data_by_row_and_column_index(1, 3)
            if grantor and grantee:
                self.actions.click(self.lib.general_helper.find_elements(self.pages.CS.main_page.rbns_and_or_)[0])
                self.lib.CS.general.search_by_keyword(f"{grantor}, {grantee}")
                assert grantor in self.pages.CS.main_page.column_data_by_row_and_column_index(1, 2) and \
                       grantee in self.pages.CS.main_page.column_data_by_row_and_column_index(1, 3), \
                    f"Search by grantor AND grantee with '{grantor} {grantee}' data failed!"
            elif grantor:
                self.lib.CS.general.click_on_search_option("GRANTOR")
                self.actions.click(self.lib.general_helper.find_elements(self.pages.CS.main_page.rbns_and_or_)[1])
                self.lib.CS.general.search_by_keyword(f"{grantor}, {grantee}")
                assert grantor in self.pages.CS.main_page.column_data_by_row_and_column_index(1, 2), \
                    f"Search by grantor OR grantee with '{grantor} {grantee}' data failed!"

        else:
            self.logging.info("No search data found at all")


if __name__ == '__main__':
    run_test(__file__)
