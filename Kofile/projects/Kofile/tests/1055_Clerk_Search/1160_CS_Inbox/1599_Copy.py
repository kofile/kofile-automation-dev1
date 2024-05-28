from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to CS, submit 'Copy' to CRS by DOC number, finalize and check order
        """

tags = ['48999_location_2']


class test(TestParent):                                                                              # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CS.general.go_to_cs()
        # Get random doc number for OIT
        self.api.clerc_search(self.data).get_document_number()
        # Submit document to CRS
        self.atom.CS.general.submit_to_crs()
        # Go to CRS
        self.atom.CRS.general.go_to_crs()
        # Check order and finalize
        self.atom.CS.general.finalize_and_check_in_crs()


if __name__ == '__main__':
    run_test(__file__)
