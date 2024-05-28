from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CRS, create and finalize an order with 2 OITs (RP and ML)
    - Navigate to Capture Queue and scan and map 2 images
    - Click "Save & Exit" button
    - Go to Search and Search order 
        -> Order is moved to Indexing, contains 2 OITs and 2 doc numbers from 1-st step
    - Find the order in Indexing Queue -> Order contains the RP OIT
        """

tags = ["48999_location_2"]


class test(TestParent):                                                                         # noqa

    def __init__(self, data):
        data["OITs"] = [data["OIT_1"], data["OIT_2"]]
        data["OIT"] = data["OITs"][0]
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.order_queue.create_and_action_with_order(None)
        # Add 2-nd OIT to order
        self.lib.CRS.order_summary.click_new_order_item_icon()
        self.data["OIT"] = self.data["current_oit"] = self.data["OITs"][1]
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.one_oit_to_summary()
        self.atom.CRS.add_payment.finalize_order()
        self.atom.CRS.general.go_to_crs()

        # Scan and map 1-st OIT
        self.lib.CRS.order_item_type.scan_and_map()
        # Scan and map 2-nd OIT
        self.atom.CRS.capture.capture_and_map(oit_num=2)
        self.lib.CRS.order_item_type.save_order_in_capture_step()

        # Search and verify
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_status_indexing()
        self.lib.CRS.order_search.verify_count_of_oits_by_order_number(self.data["order_number"],
                                                                       len(self.data["OITs"]))
        self.lib.CRS.order_search.verify_doc_number_by_order_number(self.data["order_number"],
                                                                    self.data["doc_numbers"])

        # Index order
        self.lib.CRS.order_item_type.index_order()
        self.lib.CRS.order_item_type.save_order_in_index_entry()
        self.lib.CRS.order_item_type.next_order_in_index_summary()


if __name__ == '__main__':
    run_test(__file__)
