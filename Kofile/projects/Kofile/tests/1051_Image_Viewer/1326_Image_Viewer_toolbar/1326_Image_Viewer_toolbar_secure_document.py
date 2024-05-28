from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
        Open CRS ->
        Scan document ->
        Make search in image viewer 1 on image ->
        Click secure document and check status ->
        Click unsecure document and check status ->
        """

tags = ['48999_location_2']


class test(TestParent):                                                                                 # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs()

        self.lib.CRS.order_item_type.start_batch_scan()
        self.lib.CRS.capture.start_scan()
        self.lib.CRS.capture.open_image_in_image_viewer(timeout=60, retries=5)
        self.lib.image_recognition.verify_image_changes_on_viewer("1 origin")

        self.lib.CRS.capture.check_secure_doc_button_title("Image Is Viewable")
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.set_secured_document_content_button)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.infobox_yes_button)

        self.lib.CRS.capture.check_secure_doc_button_title("Image Is Private")
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.set_secured_document_content_button)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.infobox_yes_button)
        self.lib.CRS.capture.check_secure_doc_button_title("Image Is Viewable")


if __name__ == '__main__':
    run_test(__file__)
