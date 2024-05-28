from selenium.common.exceptions import ElementClickInterceptedException
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
        Open CRS ->
        Scan document ->
        Make search in image viewer 1 on image ->
        Click multi-doc button ->
        Find image 1, 2, 3 and 4 in viewer ->
        Select page 3 ->
        Delete page 3 and check images 1,2 nad 4 displayed and 3 not displayed ->
        Click insert before and check doc count ->
        Click insert after and check doc count ->
        Pick first doc and click image details ->
        Check image 1 is displayed
        """

tags = ['48999_location_2']


class test(TestParent):                                                                                    # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def get_pages(self):
        return [i for i in self.lib.general_helper.find_elements(
            self.pages.CRS.image_viewer.thumbnail_pages) if i.is_displayed()]

    def __test__(self):
        self.atom.CRS.general.go_to_crs()

        _os = '{} origin small'
        self.lib.CRS.order_item_type.start_batch_scan()
        self.lib.CRS.capture.start_scan()
        self.lib.CRS.capture.open_image_in_image_viewer(timeout=60, retries=5)
        self.lib.image_recognition.verify_image_changes_on_viewer("1 origin")

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.multidoc_button)

        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(1), element=self.pages.CRS.image_viewer.image_viewer_container, quality=.9)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(2), element=self.pages.CRS.image_viewer.image_viewer_container)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(3), element=self.pages.CRS.image_viewer.image_viewer_container)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(4), element=self.pages.CRS.image_viewer.image_viewer_container)
        pages = self.get_pages()
        assert len(pages) == 4, f"Must be 4 page on thumbnail mode, but have {len(pages)}"
        pages[2].click()

        for _ in range(10):
            try:
                self.lib.general_helper.find_elements(self.pages.CRS.image_viewer.btn_thumb_delete_page)[2].click()
                break
            except ElementClickInterceptedException:
                self.actions.wait(1)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(1), element=self.pages.CRS.image_viewer.image_viewer_container, quality=.9)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(2), element=self.pages.CRS.image_viewer.image_viewer_container)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(4), element=self.pages.CRS.image_viewer.image_viewer_container)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(3), element=self.pages.CRS.image_viewer.image_viewer_container, should_exist=False)

        pages = self.get_pages()
        assert len(pages) == 3, f"Must be 3 page on thumbnail mode, but have {len(pages)}"
        pages[1].click()
        self.lib.general_helper.find_elements(self.pages.CRS.image_viewer.btn_insert_after)[1].click()
        self.lib.CRS.capture.start_scan(click=False)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.multidoc_button)

        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(1), element=self.pages.CRS.image_viewer.image_viewer_container, quality=.9)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(2), element=self.pages.CRS.image_viewer.image_viewer_container)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(3), element=self.pages.CRS.image_viewer.image_viewer_container)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(4), element=self.pages.CRS.image_viewer.image_viewer_container)

        pages = self.get_pages()
        assert len(pages) == 7, f"Must be 7 page on thumbnail mode, but have {len(pages)}"

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.btn_insert_before)
        self.lib.CRS.capture.start_scan(click=False)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.multidoc_button)

        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(1), element=self.pages.CRS.image_viewer.image_viewer_container, quality=.9)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(2), element=self.pages.CRS.image_viewer.image_viewer_container)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(3), element=self.pages.CRS.image_viewer.image_viewer_container)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(4), element=self.pages.CRS.image_viewer.image_viewer_container)

        pages = self.get_pages()
        assert len(pages) == 11, f"Must be 11 page on thumbnail mode, but have {len(pages)}"

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.multidoc_button)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.btn_switch_to_image_details)
        self.lib.image_recognition.verify_image_changes_on_viewer("1 origin")


if __name__ == '__main__':
    run_test(__file__)
