from projects.Kofile.Lib.test_parent import LibParent


class PackageSearch(LibParent):
    def __init__(self):
        super(PackageSearch, self).__init__()

    def get_result_table_all_rows(self):
        return self._actions.get_browser().find_all(self._pages.CRS.package_search.result_table_all_rows)

    def verify_to_date(self, to_date_):
        self._actions.verify_element_value(self._pages.CRS.package_search.txt_to_date, to_date_)

    def verify_from_date(self, from_date):
        self._actions.verify_element_value(self._pages.CRS.package_search.txt_from_date, from_date)

    def click_reset_search(self):
        self._general_helper.scroll_and_click(self._pages.CRS.package_search.lnk_reset_search)

    def verify_no_matches_found(self):
        self._actions.verify_element_present(self._pages.CRS.package_search.lbl_no_matches_found)
        self._actions.verify_element_text(self._pages.CRS.package_search.lbl_no_matches_found, "No match found")

    def search_packages_by_date_range(self, from_date, to_date):
        self._general_helper.find_and_send_keys(self._pages.CRS.package_search.txt_from_date, from_date)
        self._general_helper.find_and_send_keys(self._pages.CRS.package_search.txt_to_date, to_date)
        self.click_search_button()

    def click_search_button(self):
        self._general_helper.wait_and_click(self._pages.CRS.package_search.btn_search)

    def fill_package_id(self, package_id):
        self._general_helper.find_and_send_keys(self._pages.CRS.package_search.txt_package_id, package_id)

    def get_order_number(self, row_index=1):
        return self._actions.get_element_text(self._pages.CRS.package_search.order_number_by_row_index(row_index))

    def wait_and_click_search_lookup(self, package_id):
        lookup = self._general_helper.make_locator(self._pages.CRS.package_search.ddl_package_id_lookup, package_id)
        self._general_helper.wait_and_click(lookup)
