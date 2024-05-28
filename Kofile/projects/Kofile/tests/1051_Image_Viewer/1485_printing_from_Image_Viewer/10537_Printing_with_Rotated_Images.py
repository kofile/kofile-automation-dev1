from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
1. Send Birth Certificate Copy from CS
2. Open Order in CRS, Open Image Viewer
3. Click on Print Rotated Image icon.
4. Click on Select All/DeSelect All action link
5. Select some pages, click on Rotate left icon
6. Click on Rotate Right Icon
7. Click on Print Rotated Image icon to turn off
8. Apply some Stamps/redactions/crops on images and Turn Print Rotated Image on
9. Click on Print Rotated Image icon, select and rotate some pages.
10. Click on Print action link in Print preview popup
    """

tags = ['48999_location_2']


class test(TestParent):

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to Clerk Search
        self.atom.CS.general.go_to_cs()
        # Get random doc number for OIT
        self.api.clerc_search(self.data).get_document_number(not_in_workflow=True)
        # Submit document to CRS
        self.atom.CS.general.submit_to_crs()
        # Go to CRS
        self.atom.CRS.general.go_to_crs()
        # Go to Indexing Queue
        self.lib.general_helper.scroll_and_click(self.pages.CRS.general.lnk_go_to_orders)
        # Process order
        self.lib.CRS.crs.click_running_man()
        self.lib.general_helper.find_and_click(self.pages.CRS.order_entry.image_row)
        self.actions.wait_for_element_displayed(self.pages.CRS.image_viewer.print_rotated_image)
        self.actions.assert_element_attribute(
            self.pages.CRS.image_viewer.print_rotated_image, "title", "Print Rotated Image")
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.print_rotated_image)
        self.lib.general_helper.assert_class_contain(self.pages.CRS.image_viewer.print_rotated_image, "btnselected")
        self.lib.general_helper.assert_class_contain(self.pages.CRS.capture_queue.rotate_left_button, "disabled")
        self.lib.general_helper.assert_class_contain(self.pages.CRS.capture_queue.rotate_right_button, "disabled")
        self.lib.general_helper.assert_class_contain(self.pages.CRS.capture_queue.rotate_left_button, "disabled",
                                                     el_index=-1)
        self.lib.general_helper.assert_class_contain(self.pages.CRS.capture_queue.rotate_right_button, "disabled",
                                                     el_index=-1)

        self.lib.general_helper.get_displayed_element(self.pages.CRS.image_viewer.select_all_button, click=True)
        self.lib.general_helper.assert_class_contain(self.pages.CRS.capture_queue.rotate_left_button, "disabled",
                                                     el_index=-1, is_not=True)
        self.lib.general_helper.assert_class_contain(self.pages.CRS.capture_queue.rotate_right_button, "disabled",
                                                     el_index=-1, is_not=True)
        for el in self.get_all_tumbs():
            assert "checkBoxOn" in el.get_attribute("class")

        self.lib.general_helper.get_displayed_element(self.pages.CRS.image_viewer.de_select_all_button, click=True)
        self.lib.general_helper.assert_class_contain(self.pages.CRS.capture_queue.rotate_left_button, "disabled",
                                                     el_index=-1)
        self.lib.general_helper.assert_class_contain(self.pages.CRS.capture_queue.rotate_right_button, "disabled",
                                                     el_index=-1)

        for el in self.get_all_tumbs():
            assert "checkBoxOn" not in el.get_attribute("class")
            el.click()

        self.lib.general_helper.assert_class_contain(self.pages.CRS.capture_queue.rotate_left_button, "disabled",
                                                     el_index=-1, is_not=True)
        self.lib.general_helper.assert_class_contain(self.pages.CRS.capture_queue.rotate_right_button, "disabled",
                                                     el_index=-1, is_not=True)

        self.lib.general_helper.assert_class_contain(self.pages.CRS.capture_queue.pup_upload_btn_first_page, "disabled")
        self.lib.general_helper.assert_class_contain(self.pages.CRS.capture_queue.pup_upload_btn_previous_page,
                                                     "disabled")
        self.lib.general_helper.assert_class_contain(self.pages.CRS.capture_queue.pup_upload_btn_next_page, "disabled")
        self.lib.general_helper.assert_class_contain(self.pages.CRS.capture_queue.pup_upload_btn_last_page, "disabled")
        self.lib.general_helper.assert_class_contain(self.pages.CRS.image_viewer.zoom_in_button, "disabled")
        self.lib.general_helper.assert_class_contain(self.pages.CRS.image_viewer.zoom_out_button, "disabled")
        self.lib.general_helper.assert_class_contain(self.pages.CRS.image_viewer.fit_width_button, "disabled")
        self.lib.general_helper.assert_class_contain(self.pages.CRS.image_viewer.fit_height_button, "disabled")
        self.lib.general_helper.assert_class_contain(self.pages.CRS.image_viewer.fit_best_button, "disabled")
        self.lib.general_helper.assert_class_contain(self.pages.CRS.image_viewer.icn_crop, "disabled")
        self.lib.general_helper.assert_class_contain(self.pages.CRS.image_viewer.icn_restore_crop, "disabled")
        self.lib.general_helper.assert_class_contain(self.pages.CRS.image_viewer.icn_redaction, "disabled")
        self.lib.general_helper.assert_class_contain(self.pages.CRS.image_viewer.icn_restore_redaction, "disabled")

        self.lib.general_helper.get_displayed_element(self.pages.CRS.image_viewer.de_select_all_button, click=True)
        self.first_tumb_img = self.get_first_tumb_img()
        self.first_tumb_img.click()
        assert "transform: rotate(0deg)" in self.first_tumb_img.get_attribute("style")
        rotate_left_button = self.lib.general_helper.get_displayed_element(
            self.pages.CRS.capture_queue.rotate_left_button, many=True)[-1]
        rotate_right_button = self.lib.general_helper.get_displayed_element(
            self.pages.CRS.capture_queue.rotate_right_button, many=True)[-1]
        self.change_rotate(rotate_left_button, "270")
        self.change_rotate(rotate_left_button, "180")
        self.change_rotate(rotate_left_button, "90")
        self.change_rotate(rotate_left_button, "0")
        self.change_rotate(rotate_left_button, "270")
        self.change_rotate(rotate_right_button, "360")
        self.change_rotate(rotate_right_button, "90")
        self.change_rotate(rotate_right_button, "180")
        self.change_rotate(rotate_right_button, "270")
        self.change_rotate(rotate_right_button, "360")
        self.change_rotate(rotate_right_button, "90")
        self.change_rotate(rotate_left_button, "0")

        self.change_rotate(rotate_left_button, "270")
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.print_rotated_image)
        self.lib.general_helper.assert_class_contain(self.pages.CRS.image_viewer.icn_crop, "disabled", is_not=True)
        self.lib.general_helper.find_and_click(self.pages.CRS.image_viewer.print_rotated_image)
        self.lib.general_helper.assert_class_contain(self.pages.CRS.image_viewer.icn_crop, "disabled")
        self.first_tumb_img = self.get_first_tumb_img()
        self.check_first_img("0")
        self.actions.wait(2)

        self.lib.general_helper.get_displayed_element(self.pages.CRS.image_viewer.btn_print_icon, click=True)
        self.lib.general_helper.wait_until(
            lambda: not self.lib.general_helper.find(self.pages.CRS.image_viewer.print_image,
                                                     get_attribute="src").endswith("for_print.gif"), 60)
        start_size = self.get_size()
        self.lib.general_helper.find_and_click(self.pages.CRS.capture_queue.pup_order_cancel_btn_cancel)
        self.first_tumb_img.click()
        self.change_rotate(rotate_left_button, "270")
        self.lib.general_helper.get_displayed_element(self.pages.CRS.image_viewer.btn_print_icon, click=True)
        self.lib.general_helper.wait_until(
            lambda: not self.lib.general_helper.find(self.pages.CRS.image_viewer.print_image,
                                                     get_attribute="src").endswith("for_print.gif"), 60)
        second_size = self.get_size()
        assert start_size != second_size, f"size without rotation: {start_size}\nwith rotation: {second_size}"

    def get_size(self):
        return [self.lib.general_helper.find(self.pages.CRS.image_viewer.print_width, get_text=True),
                self.lib.general_helper.find(self.pages.CRS.image_viewer.print_height, get_text=True)]

    def get_first_tumb_img(self):
        return self.lib.general_helper.get_displayed_element(
            self.pages.CRS.image_viewer.thumbnail_pages, parent=self.lib.general_helper.get_displayed_element(
                self.pages.CRS.image_viewer.print_image_container))

    def change_rotate(self, btn, expect):
        btn.click()
        self.actions.wait(.2)
        self.check_first_img(expect)

    def check_first_img(self, expect):
        style = self.first_tumb_img.get_attribute("style")
        assert f"transform: rotate({expect}deg)" in style, f"actual: {style}\nexpect: transform: rotate({expect}deg)"
        assert expect == self.first_tumb_img.get_attribute("rotate"), f"actual: {style}\nexpect: {expect}"

    def get_all_tumbs(self):
        els = self.lib.general_helper.find_elements(self.pages.CRS.image_viewer.multi_selectdoc_checkbox,
                                                    parent=self.lib.general_helper.find(
                                                        self.pages.CRS.image_viewer.print_image_container))
        return [i for i in els if i.is_displayed()]


if __name__ == '__main__':
    run_test(__file__)
