from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
        Open CRS ->
        Scan document ->
        Make search in image viewer 1 on image ->
        Click multi select ->
        Find small 1, 2, 3 and 4 on images -> 
        Verify checkbox all checkbox not checked ->
        Click select all ->
        Verify checkbox all checkbox checked ->
        Click unselect all ->
        Verify checkbox all checkbox not checked ->
        Select page 1 nad 2 ->
        Click rotate right ->
        Find 1 and 2 rotate to right nad 2, 3 origin ->
        Verify checkbox all checkbox on image 1 nad 2 checked and 3, 4 not checked ->
        Unselect image 1 and 2 ->
        Select image 3 ->
        Click rotate to left ->
        Find image 1 and 2 rotated to right and 3 rotated to left ->
        Click delete button ->
        Verify image 1,2 and 4 displayed and 3 not displayed ->
        Select image 1 nad click split doc ->
        Verify img capture summary is 2 ->
        Check image 2 and 4 displayed and 1 and 3 not displayed in image viewer ->
        Change rotation for image 2 and 4 ->
        Click rollback button ->
        Check image 2 and 4 rotation has been rollback
        """

tags = ['48999_location_2']


class test(TestParent):                                                                                  # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs()

        _os, _rs, _ls = "{} origin small", "{} right small", "{} left small"
        self.lib.CRS.order_item_type.start_batch_scan()
        self.lib.CRS.capture.start_scan()
        self.lib.CRS.capture.open_image_in_image_viewer(timeout=60, retries=5)
        self.lib.image_recognition.verify_image_changes_on_viewer("1 origin")

        self.lib.CRS.capture.click_multi_select()

        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(1), element=self.pages.CRS.image_viewer.image_viewer_container, quality=.9)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(2), element=self.pages.CRS.image_viewer.image_viewer_container)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(3), element=self.pages.CRS.image_viewer.image_viewer_container)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(4), element=self.pages.CRS.image_viewer.image_viewer_container)

        for a, i in enumerate(self.lib.CRS.capture.get_all_multiselect_checkbox()):
            assert "checkBoxOn" not in i.get_attribute("class"), f"Checkbox {a + 1} is checked"

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.select_all_button)
        for a, i in enumerate(self.lib.CRS.capture.get_all_multiselect_checkbox()):
            assert "checkBoxOn" in i.get_attribute("class"), f"Checkbox {a + 1} is not checked"

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.de_select_all_button)
        for a, i in enumerate(self.lib.CRS.capture.get_all_multiselect_checkbox()):
            assert "checkBoxOn" not in i.get_attribute("class"), f"Checkbox {a + 1} is checked"
            if a in (0, 1):
                i.click()

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.icn_rotate_right)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _rs.format(1), element=self.pages.CRS.image_viewer.image_viewer_container, quality=.9)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _rs.format(2), element=self.pages.CRS.image_viewer.image_viewer_container)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(3), element=self.pages.CRS.image_viewer.image_viewer_container)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(4), element=self.pages.CRS.image_viewer.image_viewer_container)

        for a, i in enumerate(self.lib.CRS.capture.get_all_multiselect_checkbox()):
            if a in (0, 1):
                assert "checkBoxOn" in i.get_attribute("class"), f"Checkbox {a + 1} is not checked"
            else:
                assert "checkBoxOn" not in i.get_attribute("class"), f"Checkbox {a + 1} is checked"
            if a < 3:
                i.click()

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.icn_rotate_left)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _rs.format(1), element=self.pages.CRS.image_viewer.image_viewer_container, quality=.9)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _rs.format(2), element=self.pages.CRS.image_viewer.image_viewer_container)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _ls.format(3), element=self.pages.CRS.image_viewer.image_viewer_container)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(4), element=self.pages.CRS.image_viewer.image_viewer_container)

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.multi_selectdoc_delete_button)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _rs.format(1), element=self.pages.CRS.image_viewer.image_viewer_container, quality=.9)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _rs.format(2), element=self.pages.CRS.image_viewer.image_viewer_container)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _ls.format(3), element=self.pages.CRS.image_viewer.image_viewer_container, should_exist=False)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(4), element=self.pages.CRS.image_viewer.image_viewer_container)

        self.lib.CRS.capture.get_all_multiselect_checkbox(3)[0].click()
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.multi_selectdoc_split_button)
        doc_count = 0
        for _ in range(5):
            doc_count = len(self.lib.general_helper.find_elements(self.pages.CRS.capture_summary.img_capture_summary))
            if doc_count == 2:
                break
            self.actions.wait(3)
        assert doc_count == 2, f"Split make {doc_count} documents but should be 2"
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _rs.format(1), element=self.pages.CRS.image_viewer.image_viewer_container, quality=.9, should_exist=False)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _rs.format(2), element=self.pages.CRS.image_viewer.image_viewer_container)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _ls.format(3), element=self.pages.CRS.image_viewer.image_viewer_container, should_exist=False)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(4), element=self.pages.CRS.image_viewer.image_viewer_container)

        self.lib.CRS.capture.click_multi_select()
        cb_2, cb_4 = self.lib.CRS.capture.get_all_multiselect_checkbox(2)
        cb_2.click()
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.icn_rotate_right)
        cb_2.click()
        cb_4.click()
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.icn_rotate_left)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            "2 flip small", element=self.pages.CRS.image_viewer.image_viewer_container)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _ls.format(4), element=self.pages.CRS.image_viewer.image_viewer_container)

        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.multi_selectdoc_rollback_button)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _rs.format(2), element=self.pages.CRS.image_viewer.image_viewer_container)
        self.lib.image_recognition.verify_image_changes_on_viewer(
            _os.format(4), element=self.pages.CRS.image_viewer.image_viewer_container)


if __name__ == '__main__':
    run_test(__file__)
