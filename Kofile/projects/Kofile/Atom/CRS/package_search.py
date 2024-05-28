from projects.Kofile.Lib.test_parent import AtomParent


class PackageSearch(AtomParent):
    def __init__(self):
        super(PackageSearch, self).__init__()

    def search_order_by_package_id(self):
        """
            Pre-conditions: Package is submitted, browser is in any queue
            Post-conditions: Package search is executed, result row or 'No match found' is displayed
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        data = self._lib.general_helper.get_data()
        PACKAGE_ID = data['package_id']
        try:
            # go to Package Search
            self._lib.CRS.crs.go_to_package_search()

            self._lib.CRS.package_search.fill_package_id(PACKAGE_ID)
            self._lib.CRS.package_search.click_search_button()

            try:
                data['order_number'] = self._lib.CRS.package_search.get_order_number()
                self._actions.step(f"Search result found. Order number of the package is {data['order_number']}")
            except Exception:
                # if no search results are found, verify "No match found" text
                self._lib.CRS.package_search.verify_no_matches_found()
        except Exception:
            self._actions.error("Could not search for results")

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def search_packages_by_date_range(self):
        """
            Pre-conditions: No
            Post-conditions: Package search by date is performed, results or 'No match found' are displayed
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        data = self._lib.general_helper.get_data()

        try:
            # go to Package Search and search by dates from data
            self._lib.CRS.crs.go_to_package_search()
            # search packages by date
            self._lib.CRS.package_search.search_packages_by_date_range(data['from_date'], data['to_date'])
            # wait for results or No match found to display
            result_rows = self._lib.CRS.package_search.get_result_table_all_rows()
            if result_rows:
                data['result_rows'] = result_rows
                self._actions.step(f"{len(result_rows)} results are found for the given date range")

            else:
                data['result_rows'] = None
                self._lib.CRS.package_search.verify_no_matches_found()
        except Exception:
            self._actions.error("Could not search for results")

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))
