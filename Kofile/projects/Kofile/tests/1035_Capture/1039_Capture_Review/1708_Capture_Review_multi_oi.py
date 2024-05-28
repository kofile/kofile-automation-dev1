"""Capture Review"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """Create, finalize, capture a RP order with several OIs in Dallas 
                 and process it through Capture Review step"""

tags = ["dallas"]


class test(TestParent):                                                                                  # noqa

    def __init__(self, data):
        data["OIT"] = "RP_Recordings"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.order_queue.create_and_action_with_order(None, open_crs=True,
                                                               summary=self.atom.CRS.order_entry.many_oits_to_summary)
        self.atom.CRS.add_payment.finalize_order()
        self.lib.CRS.order_item_type.capture_step(oi_count=self.data["count_of_OITs"])
        self.lib.CRS.crs.go_to_order_search()
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
        self.lib.CRS.order_search.verify_order_status_indexing()
        # order moves to scheduled-KDI on Dallas, and will be auto-processed to Archive


if __name__ == '__main__':
    run_test(__file__, env="qa_dallas")
