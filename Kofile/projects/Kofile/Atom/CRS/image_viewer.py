from projects.Kofile.Lib.test_parent import AtomParent


class ImageViewer(AtomParent):
    def __init__(self):
        super(ImageViewer, self).__init__()

    def print_checking(self):
        """
            Pre-conditions: Image viewer opened on any screen
            Post-conditions: Image viewer is opened, Image printing is checked
            """

        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        # wait image viewer is opened
        self._lib.general_helper.wait_for_spinner(spinner_in=10, spinner_out=150,
                                                  locator_spinner=self._pages.CRS.image_viewer.image_viewer_spinner[1])
        # if print icon is configured click on print
        style = self._actions.get_element_attribute(self._pages.CRS.image_viewer.btn_print_style, 'style')
        if style != "display: none;":
            self._lib.general_helper.find_and_click(self._pages.CRS.image_viewer.btn_print_icon)
            self._lib.general_helper.find_and_click(self._pages.CRS.image_viewer.lnk_print)
            # wait popup appear
            self._actions.wait_for_element_displayed(self._pages.CRS.image_viewer.pup_print_dialog)
            # verify popup text
            self._actions.verify_element_text(self._pages.CRS.image_viewer.pup_print_dialog, "Success")
            #  close popup
            self._actions.click(self._pages.CRS.image_viewer.btn_close_pup_print)
        else:
            self._actions.step("Print icon is not configured for this step")

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))

    def thumbnail_checking(self):
        """
            Pre-conditions: Any screen with thumbnails is opened
            Post-conditions: Any screen with thumbnails is opened. Thumbnails number is compared with page number
            """

        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        # wait image viewer is opened
        self._lib.general_helper.wait_for_spinner(spinner_in=10, spinner_out=150,
                                                  locator_spinner=self._pages.CRS.image_viewer.image_viewer_spinner[1])
        self._actions.wait_for_element_displayed(self._pages.CRS.general.btn_last_page)
        # If last page icon is enabled go to last page and then check thumbnails
        disabled = self._actions.get_element_attribute(self._pages.CRS.general.btn_last_page, 'disabled')

        if disabled is None:
            self._actions.click(self._pages.CRS.general.btn_last_page)
            self._lib.general_helper.wait_for_spinner(spinner_in=10, spinner_out=150,
                                                      locator_spinner=self._pages.CRS.image_viewer.image_viewer_spinner[
                                                          1])
        self._actions.wait_for_element_visible(self._pages.CRS.general.total_images)
        # get generated thumbnails
        thumbnails = self._actions.get_browser().find_all(self._pages.CRS.general.thumbnails)
        generated_thumbnails_count = str(len(thumbnails))
        # verify thumbnails = total images
        self._actions.verify_element_text(self._pages.CRS.general.total_images, generated_thumbnails_count)

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))
