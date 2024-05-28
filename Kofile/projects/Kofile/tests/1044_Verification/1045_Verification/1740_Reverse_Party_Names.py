"""69871_Reverse_Party_Names"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
                Steps:
                1. Create order and process to Verification
                2. Clear and fill party names
                3. Click on the 'Reverse Parties' link
                4. Verify that entered party names are changed in places from Grantor to Grantee and vice versa 
              """

tags = ['48999_location_2']


class test(TestParent):                                                                               # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.general_helper.check_order_type()
        # Create and Finalize order
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        if self.data["OIT"] == "RP_Recordings":
            self.atom.CRS.general.go_to_crs()
        # Capture order
        self.lib.CRS.order_item_type.capture_step()
        # Indexing Queue
        self.lib.CRS.order_item_type.indexing_step()
        # Verification Queue
        self.lib.CRS.order_item_type.index_order(self.lib.CRS.crs.go_to_verification_queue)
        """In case of kerey revers parties are disabled.
            So still don't understand in which case re_key funcitonality should be used.
            Maybe after we just delete this line (self.lib.CRS.order_item_type.re_key_in_verification())
        """
        # self.lib.CRS.order_item_type.re_key_in_verification()
        # Reverse Parties
        self.lib.CRS.indexing_entry.revert_names()


if __name__ == '__main__':
    run_test(__file__)
