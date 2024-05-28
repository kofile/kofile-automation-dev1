from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
        Open CRS ->
        Go to indexing queue ->
        Add new indexing order birth record ->
        Click upload button ->
        pick document ->
        Check document in image viewer
        """

tags = ['48999_location_2']


class test(TestParent):                                                                                   # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.crs.go_to_indexing_queue()

        self.lib.CRS.indexing_queue.add_birth_indexing_order()
        self.actions.assert_element_not_displayed(self.pages.CRS.image_viewer.single_image_viewer_container)
        self.lib.CRS.indexing_entry.upload_birth_record_file(self.data)


if __name__ == '__main__':
    run_test(__file__)
