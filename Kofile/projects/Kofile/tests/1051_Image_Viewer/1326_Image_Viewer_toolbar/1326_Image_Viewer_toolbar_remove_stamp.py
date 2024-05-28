from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
        Open CRS ->
        Go to indexing queue ->
        Add new indexing order birth record ->
        Click upload button ->
        pick document ->
        Check document in image viewer ->
        Add c3 stamp and get pixel count->
        Remove stamp and get pixel count ->
        assert pixel count with stamp > pixel count without stamp
        """

tags = ['48999_location_2']


class test(TestParent):                                                                                  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.crs.go_to_indexing_queue()

        self.lib.CRS.indexing_queue.add_birth_indexing_order()
        self.actions.assert_element_not_displayed(self.pages.CRS.image_viewer.single_image_viewer_container)
        self.lib.CRS.indexing_entry.upload_birth_record_file(self.data)

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.icn_C3)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.infobox_yes_button)
        self.lib.general_helper.wait_for_spinner()

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.icn_C3)
        self.lib.general_helper.wait_for_spinner()

        self.actions.wait(5)
        pixels_with_stamp = self.lib.image_recognition.check_uploaded_image(
            self.pages.CRS.image_viewer.single_image_viewer_container, "Stamp not added")

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.eStamp_button)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.remove_stamp_button)
        self.lib.general_helper.wait_for_spinner()
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.eStamp_button)
        self.actions.wait(5)
        self.lib.image_recognition.check_uploaded_image(self.pages.CRS.image_viewer.single_image_viewer_container,
                                                        "Stamp not removed", bigger=False, px_c=pixels_with_stamp)


if __name__ == '__main__':
    run_test(__file__)
