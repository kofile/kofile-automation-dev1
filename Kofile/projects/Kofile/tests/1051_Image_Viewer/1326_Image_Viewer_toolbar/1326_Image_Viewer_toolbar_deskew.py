from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test
import xml.etree.ElementTree as ET

description = """
        Open CRS ->
        Scan document ->
        Make search that image isn't straight ->
        Click image maintenance tool button ->
        Click on deskew checkbox ->
        Click image maintenance tool button again->
        Check that image become straight after deskew
        """

tags = ['48999_location_2']


class test(TestParent):  # noqa

    def __init__(self, data):
        self.original_tiff = ''
        super(test, self).__init__(data, __name__, precondition=self._precondition)

    def __test__(self):
        self.atom.CRS.general.go_to_crs()

        self.lib.CRS.order_item_type.start_batch_scan()
        self.lib.CRS.capture.start_scan()
        self.lib.CRS.capture.open_image_in_image_viewer(timeout=60, retries=5)
        self.lib.image_recognition.verify_image_changes_on_viewer("[]_not_straight")

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.fit_height_button)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.image_maintenance_tool_button)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.deskew_checkbox)
        self.lib.general_helper.wait_for_spinner()
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.image_maintenance_tool_button)
        self.lib.general_helper.wait_for_spinner()
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.fit_height_button)
        self.lib.image_recognition.verify_image_changes_on_viewer("[]_straight")

    def _precondition(self):
        self.path_to_PredefinedImagesConfig_xml = self.names.path_to_PredefinedImagesConfig_xml
        tree = ET.parse(self.path_to_PredefinedImagesConfig_xml)
        root = tree.getroot()
        self.original_tiff = root.find('string').text
        root.find('string').text = self.names.filename_for_deskew_test
        tree.write(self.path_to_PredefinedImagesConfig_xml)

    def __del__(self):
        tree = ET.parse(self.path_to_PredefinedImagesConfig_xml)
        root = tree.getroot()
        root.find('string').text = self.original_tiff
        tree.write(self.path_to_PredefinedImagesConfig_xml)


if __name__ == '__main__':
    run_test(__file__)
