from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test
import re

description = """
        Open CRS ->
        Scan document ->
        Make search in image viewer 1 on image ->
        click more info button ->
        Check Title and content text in info window
        """

tags = ['48999_location_2']


class test(TestParent):                                                                                    # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs()

        self.lib.CRS.order_item_type.start_batch_scan()
        self.lib.CRS.capture.start_scan()
        self.lib.CRS.capture.open_image_in_image_viewer(timeout=60, retries=5)
        self.lib.image_recognition.verify_image_changes_on_viewer("1 origin")

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.image_information_button)

        self.actions.wait_for_element_present(self.pages.CRS.image_viewer.pup_print_dialog)
        self.actions.wait_for_element_text(self.pages.CRS.image_viewer.pup_print_dialog, "Document Image Info")
        content = self.lib.general_helper.find(self.pages.CRS.image_viewer.pup_print_dialog_content, get_text=True)
        assert re.match("""Width = \d{1,5} px
Height = \d{1,5} px
Resolution: \d{1,3} x \d{1,3} dpi""", content), "Unexpected info in modal window"

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.close_modal)
        self.actions.wait_for_element_not_present(self.pages.CRS.image_viewer.pup_print_dialog)


if __name__ == '__main__':
    run_test(__file__)
