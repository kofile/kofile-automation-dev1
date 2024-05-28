"""Add a Second Document to Inbox"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
              Go to CS, add a document to Inbox and submit 'Copy' order to CRS
              Add a second document to Inbox and click on Inbox
              """

tags = ['48999_location_2']


class test(TestParent):                                                                                  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CS.general.go_to_cs()
        # get a random first doc number
        first_doc_num = self.api.clerc_search(self.data).get_document_number()
        self.atom.CS.general.submit_to_crs()
        first_order_number = self.data["order_number"]
        # get a random second doc number
        self.api.clerc_search(self.data).get_document_number()
        self.atom.CS.general.submit_to_crs()
        # finalize the second order
        self.atom.CS.general.finalize_cs_order()
        self.actions.store("prev_sum", {"doc_num": first_doc_num})
        self.actions.store("doc_num", first_doc_num)
        self.actions.store("order_number", first_order_number)
        # finalize the first order
        self.atom.CS.general.finalize_cs_order()


if __name__ == '__main__':
    run_test(__file__)
