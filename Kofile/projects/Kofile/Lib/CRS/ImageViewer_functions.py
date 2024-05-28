from selenium.webdriver import ActionChains
from projects.Kofile.Lib.Image_Recognition import ImageRecognition
from projects.Kofile.Lib.test_parent import LibParent

"""Precondition: image is open in Image Viewer"""
ir = ImageRecognition()


# REDACTION----------------------------------------------------------------------------------------------------------

class ImageViewer(LibParent):

    def __init__(self):
        super(ImageViewer, self).__init__()

    def add_redaction(self, step, width=104, height=104, close_second_window=False):
        """adds redaction on image and returns redaction coordinates"""
        if close_second_window:
            try:
                self._actions.close_window_by_index(1)
            except Exception as e:
                print(e)
                self._actions.step("second window not fount")
        self._general_helper.wait_for_spinner(spinner_in=5, spinner_out=30)
        self._actions.wait(1)
        self._general_helper.wait_for_spinner()
        self._general_helper.scroll_and_click(self._pages.CRS.image_viewer.icn_redaction)
        # double click on image and drag to draw the redaction area
        container = self._general_helper.find(self._pages.CRS.image_viewer.image_container)
        ac = ActionChains(self._actions.get_browser())
        ac.double_click(container)
        ac.move_by_offset(width, height).click().perform()
        self._actions.wait(1)
        # get redaction coordinates
        redaction_coordinates = self.get_redaction_coordinates(step)
        # save redaction
        self._general_helper.scroll_and_click(self._pages.CRS.image_viewer.icn_redaction)
        self._general_helper.wait_for_spinner(spinner_in=5, spinner_out=45)
        assert not len(redaction_coordinates) < 4, "Redaction area is NOT drawn"
        return redaction_coordinates

    def verify_redaction(self, data, original_redaction_coordinates, last_page, step, pixel_count):
        redaction_coordinates_step = self.find_redaction(data, last_page, step)
        if redaction_coordinates_step is not None:
            self.compare_redaction_coordinates(original_redaction_coordinates, redaction_coordinates_step, step)
            self.find_redaction_on_image(data, False, pixel_count)

    def find_redaction_on_image(self, data, last_page, pixel_count):
        if last_page:
            self.move_to_last_page(data)
        self._actions.wait(5)
        image_url = self._general_helper.find(self._pages.CRS.image_viewer.image, get_attribute='src')
        count = ir.get_black_pixel_count(image_url)
        self._logging.info(f"find {count} black pixels")
        self._actions.wait(2)
        assert count > pixel_count, "Redaction not found"

    def find_redaction(self, data, last_page, step):
        """finds previously added redaction on a given step"""
        if self._general_helper.find(self._pages.CRS.image_viewer.icn_redaction).is_displayed():
            if last_page:
                self.move_to_last_page(data)
            self._general_helper.scroll_and_click(self._pages.CRS.image_viewer.icn_redaction)
            self._actions.wait(1)
            redaction_coordinates = self.get_redaction_coordinates(step)
            return redaction_coordinates
        else:
            self._logging.info(f"Redaction icon is absent in {step} step")
            return None

    def move_to_last_page(self, data, step="indexing"):
        if data['config'].test_data(f"{data.OIT}.{step}.first_page_to_last_page"):
            self._general_helper.find_and_click(self._pages.CRS.image_viewer.btn_move_to_last_page)
            self._actions.wait(10)

    def get_redaction_coordinates(self, step):
        redaction_coord_string = self._general_helper.find(self._pages.CRS.image_viewer.redaction_box,
                                                           get_attribute="style",
                                                           wait_displayed=True).split(';')
        redaction_coordinates = [float(redaction_coord_string[1].split(': ')[1].split('px')[0]),  # x
                                 float(redaction_coord_string[0].split(': ')[1].split('px')[0]),  # y
                                 float(redaction_coord_string[2].split(': ')[1].split('px')[0]),  # width
                                 float(redaction_coord_string[3].split(': ')[1].split('px')[0])]  # length
        self._logging.info(f"Redaction coordinates in {step}: {redaction_coordinates}")
        return redaction_coordinates

    def compare_redaction_coordinates(self, coord_1, coord_2, step, absolute_accuracy=25):
        for i in range(len(coord_1)):
            assert abs(coord_1[i] - coord_2[i]) <= absolute_accuracy, "Redaction position is NOT correct!"
        self._logging.info(f"Redaction position is correct in {step}")

    # ROTATION---------------------------------------------------------------------------------------------------------

    def rotate_image(self, step):
        """rotates image and saves rotated image parameters"""
        self._general_helper.scroll_and_click(self._pages.CRS.image_viewer.icn_page_edit)
        self._actions.wait(1)
        self._general_helper.find_and_click(self._pages.CRS.image_viewer.icn_rotate_right)
        self._actions.wait(3)
        # save rotation
        self._general_helper.scroll_and_click(self._pages.CRS.image_viewer.icn_page_edit)
        self._general_helper.wait_for_spinner()
        self._actions.wait(5)
        # get rotation degree
        rotation_parameters = self.get_rotated_image_parameters(step)
        assert not rotation_parameters[0] == 90.0, "Image is NOT rotated"
        self._general_helper.wait_for_spinner()
        self._actions.wait(3)
        return rotation_parameters

    def get_rotated_image_parameters(self, step):
        self._general_helper.find_and_click(self._pages.CRS.image_viewer.fit_width_button)
        self._actions.wait(1)
        rotation_degree_string = self._general_helper.find(self._pages.CRS.image_viewer.image, get_attribute="style",
                                                           wait_displayed=True).split(';')
        rotation_degree = rotation_degree_string[4].split('(')[1].split('deg')[0] if step == "Capture" else None
        rotation_parameters = [rotation_degree,
                               rotation_degree_string[0].split(': ')[1].split('px')[0],  # width
                               rotation_degree_string[1].split(': ')[1].split('px')[0]]  # height
        self._logging.info(f"Rotated image parameters in {step}: {rotation_parameters}")
        return rotation_parameters

    def verify_rotation(self, data, original_rotation_parameters, last_page, step):
        if last_page:
            self.move_to_last_page(data)
        rotation_parameters_step = self.get_rotated_image_parameters(step)
        self.compare_rotation_parameters(original_rotation_parameters, rotation_parameters_step, step)

    def compare_rotation_parameters(self, parameters_1, parameters_2, step):
        self._actions.step(
            f"rotation {parameters_1[1]} == {parameters_2[1]} and {parameters_1[2]} == {parameters_2[1]}")
        state_1 = parameters_1[1] <= parameters_1[2]
        state_2 = parameters_2[1] <= parameters_2[2]
        assert state_1 == state_2, f"Image is NOT rotated in {step}, {state_1} " \
                                   f"({parameters_1[1]}, {parameters_1[2]}) != {state_2} ({parameters_2[1]}, " \
                                   f"{parameters_2[2]})"

    # STAMPS-------------------------------------------------------------------------------------------------

    def add_custom_stamp(self, custom_stamp_locator, step):
        assert self._general_helper.find(
            custom_stamp_locator).is_displayed(), f"Custom stamp icon is absent in {step} step"
        self._general_helper.scroll_and_click(custom_stamp_locator)
        self._general_helper.wait_for_spinner(spinner_out=35)
        # save stamp
        self._general_helper.scroll_and_click(custom_stamp_locator)
        self._general_helper.wait_for_spinner(spinner_in=5, spinner_out=45)
        self._actions.wait(1)
        self._general_helper.wait_for_spinner()

    def verify_text_on_image(self, data, text, last_page, step, accuracy=60, crop=False, should_exist=True, offset=0):
        if last_page:
            self.move_to_last_page(data, step)
        self._actions.wait(5)
        image_url = self._general_helper.find(self._pages.CRS.image_viewer.image, get_attribute='src')
        image_text = ir.recognize_image_text(image_url, step, crop, offset)
        matching_rate = ir.string_matching_rate(f"{image_text}{'@' * 100}", text)
        self._logging.info(f"String matching rate in {step} is {matching_rate}%")
        assert matching_rate > accuracy if should_exist else matching_rate < 30, \
            f"{text} is{' NOT' if should_exist else ''} found on image in {step}"
        # -----------------------------------------------------------------------------------------------------------------

    def dock_image(self, total_images):
        self._actions.click(self._pages.CRS.image_viewer.icn_dock_viewer)
        self._actions.switch_to_last_window()
        self._general_helper.wait_for_spinner()
        self._actions.wait_for_element_displayed(self._pages.CRS.image_viewer.lbl_total_images, timeout=120)
        self._actions.wait(6)
        current_count = self._actions.get_element_text(self._pages.CRS.image_viewer.lbl_total_images)
        assert total_images == current_count, \
            f"Total Images number is different, must be {total_images} but have {current_count}"

    def undock_image(self, text='The Image Viewer has been returned to Main Window'):
        self._actions.click(self._pages.CRS.image_viewer.icn_dock_viewer)
        self._actions.wait_for_element_displayed(self._pages.CRS.image_viewer.txt_docked_img_text)
        self._actions.verify_element_text(self._pages.CRS.image_viewer.txt_docked_img_text, text)
        self._actions.close_window()
        self._actions.switch_to_first_window()

    def check_dock_undock_func_with_redaction(self, data, original_redaction_coordinates, total_images, pixel_count,
                                              last_page=True):
        self.dock_image(total_images)
        if original_redaction_coordinates:
            self.find_redaction_on_image(data, last_page, pixel_count)
        else:
            self._actions.step("No redaction is added")
        self.undock_image()
