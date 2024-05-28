from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
   Log in to CS as a Clerk -> Property Records Search default page with clerk name is displayed
   Search for documents by any search criteria in any department -> Search results are found and displayed
   Export search results to Excel -> Search results are downloaded in Excel format
   Open the downloaded Excel doc and check the column data -> All columns are correctly filled with corresponding data

        """

tags = ['48999_location_2']


class test(TestParent):                                                                                    # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CS.general.go_to_cs(clerk=True)

        # search document
        self.api.clerc_search(self.data).get_document_number()
        self.lib.PS.general.search_document_by_number()
        if self.lib.PS.ps_main_page.is_search_successful():
            file_path = self.lib.CS.general.export_search_result("exel")
            self.lib.CS.general.check_exported_file(file_path, "exel", self.data["doc_num"])
        else:
            raise ValueError("Search failed!")


if __name__ == '__main__':
    run_test(__file__)
