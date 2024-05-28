from projects.Kofile.Lib.test_parent import AtomParent


class OrderSearch(AtomParent):
    def __init__(self):
        super(OrderSearch, self).__init__()

    def search_order_by_assigned_to(self):
        """
           Pre-conditions: Any queue is opened, Order is created and assigned to env.user_first,
           Post-conditions: Order Search page with search results is displayed
           """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        self._lib.CRS.crs.go_to_order_search()
        self._lib.CRS.order_search.search_by_more_options(field_locator=self._pages.CRS.order_search.ddl_assigned_to,
                                                          dropdown=True,
                                                          search_data=self._lib.general_helper.get_data()["env"][
                                                              "user_first"])
        self._lib.CRS.order_search.verify_not_empty_result_or_no_matches_found()

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def search_order_by_doc_number(self):
        """
           Pre-conditions: Any queue is opened, Order is created, doc number is saved in data['doc_number']
           Post-conditions: Order Search page with search results is displayed
           """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        self._lib.CRS.crs.go_to_order_search()
        # self._pages.CRS.order_search.txt_doc_number_to is not used because this field
        # is automatically filled with txt_doc_number_from value after click search button
        self._lib.CRS.order_search.search_by_more_options(self._pages.CRS.order_search.txt_doc_number_from, False,
                                                          self._lib.general_helper.get_data()["doc_number"])
        self._lib.CRS.order_search.verify_not_empty_result_or_no_matches_found()

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def search_order_by_order_number(self):
        """
            Pre-conditions: Any queue is opened, Order is created, order number is saved in data['order_number']
            Post-conditions: Order Search page with search results is displayed
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        self._lib.CRS.crs.go_to_order_search()
        self._lib.CRS.order_search.search_by_order_number(self._lib.general_helper.get_data()['order_number'])
        self._lib.CRS.order_search.verify_not_empty_result_or_no_matches_found()

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def search_order_by_serial_number(self):
        """
           Pre-conditions: Any queue is opened, Order with SN is created, SN is saved in data['serial_number']
           Post-conditions: Order Search page with search results is displayed
           """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        self._lib.CRS.crs.go_to_order_search()
        self._lib.CRS.order_search.search_by_more_options(self._pages.CRS.order_search.txt_serial_number,
                                                          dropdown=False,
                                                          search_data=self._lib.general_helper.get_data()[
                                                              'serial_number'])
        # verify search results
        self._lib.CRS.order_search.verify_not_empty_result_or_no_matches_found()

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def search_order_by_tracking_id(self):
        """
           Pre-conditions: Any queue is opened, Order with TrID is created, TrID is saved in data['tracking_id']
           Post-conditions: Order Search page with search results is displayed
           """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        self._lib.CRS.crs.go_to_order_search()
        self._lib.CRS.order_search.search_by_more_options(self._pages.CRS.order_search.txt_tracking_id, dropdown=False,
                                                          search_data=self._lib.general_helper.get_data()[
                                                              'tracking_id'])
        # verify search result
        self._lib.CRS.order_search.verify_not_empty_result_or_no_matches_found()

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def search_orders_by_account_code(self):
        """
        Pre-conditions: Any queue is opened Order with account user is created, account is saved in data['account_code']
        Post-conditions: Order Search page with search results is displayed
        """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        self._lib.CRS.crs.go_to_order_search()
        self._lib.CRS.order_search.search_by_account_code(self._lib.general_helper.get_data()['account_code'])
        self._lib.CRS.order_search.verify_not_empty_result_or_no_matches_found()

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def search_orders_by_date_range(self):
        """
            Pre-conditions: Any queue is opened, search dates are stored in data['from_date'] and data['to_date']
            Post-conditions: Order Search page with search results is displayed
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        data = self._lib.general_helper.get_data()
        self._lib.CRS.crs.go_to_order_search()
        self._lib.CRS.order_search.fill_date_and_search(data['from_date'], data['to_date'])
        self._lib.CRS.order_search.verify_not_empty_result_or_no_matches_found()

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def search_orders_by_email(self):
        """
            Pre-conditions: Any queue is opened, Order with email user is created, email is saved in data['email']
            Post-conditions: Order Search page with search results is displayed
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        self._lib.CRS.crs.go_to_order_search()
        self._lib.CRS.order_search.search_by_email(self._lib.general_helper.get_data()['email'])
        self._lib.CRS.order_search.verify_not_empty_result_or_no_matches_found()

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def search_orders_by_name(self):
        """
           Pre-conditions: Any queue is opened, Order is created, customer name is saved in data['name']
           Post-conditions: Order Search page with search results is displayed
           """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        self._lib.CRS.crs.go_to_order_search()
        self._lib.CRS.order_search.search_by_more_options(field_locator=self._pages.CRS.order_search.txt_name,
                                                          dropdown=False,
                                                          search_data=self._lib.general_helper.get_data()['name'])
        self._lib.CRS.order_search.verify_not_empty_result_or_no_matches_found()

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def verify_order_status(self, expected_status):
        """
            Pre-conditions: Any queue is opened, Order is created, doc number is saved in test data
            Post-conditions: Order Search page with search results is displayed
            """
        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        data = self._lib.general_helper.get_data()
        self._lib.CRS.crs.go_to_order_search()
        doc_number = data.prev_sum["doc_number"] if data.get("prev_sum") else data["doc_number"]
        self._lib.CRS.order_search.search_by_more_options(
            field_locator=self._pages.CRS.order_search.txt_doc_number_from, dropdown=False,
            search_data=doc_number)
        # verify search results
        results = self._lib.general_helper.find_elements(self._pages.CRS.order_search.order_search_results,
                                                         get_text=True)
        assert "No match found" not in results, "No match found"
        # check last order status
        status = \
            self._lib.general_helper.find_elements(self._pages.CRS.order_search.results_status_column, get_text=True)[
                -1]
        assert status == expected_status, f"Expected 'Order search status': '{expected_status}' " \
                                          f"not equal to actual: '{status}'"

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))
