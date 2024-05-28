import logging

import pytesseract
import requests
from PIL import Image
from fuzzywuzzy import fuzz
import io
import cv2
import numpy as np
import imutils
from selenium.common.exceptions import WebDriverException
from golem.webdriver.extended_webelement import ExtendedRemoteWebElement
from projects.Kofile.Lib.test_parent import LibParent


class ImageRecognition(LibParent):
    def __init__(self):
        super(ImageRecognition, self).__init__()
        self.pytesseract_config = getattr(self._names, "pytesseract_config") if hasattr(
            self._names, "pytesseract_config") else ''
        pytesseract.pytesseract.tesseract_cmd = self._names.pytesseract_path

    def load_image(self, image_url):
        headers = self._names.headers
        headers["User-Agent"] = self._actions.get_browser().execute_script("return navigator.userAgent;")
        cookies = dict()
        for i in self._actions.get_browser().get_cookies():
            cookies[i["name"]] = i["value"]
        response = requests.get(image_url, stream=True, verify=False, headers=headers, cookies=cookies)
        assert response.status_code == 200, "Request for image returned {}".format(response.status_code)
        return response

    def get_black_pixel_count(self, image_url, rgb=False, matrix=(0, 0, 0, 255), not_matrix=False):
        if isinstance(image_url, str):
            image = Image.open(self.load_image(image_url).raw)
        else:
            image = Image.open(image_url)
        pixels = image.load()
        counter = 0
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                if rgb:
                    if not_matrix:
                        if pixels[x, y] != matrix:
                            counter += 1
                    else:
                        if matrix == "grey":
                            r, g, b, _ = pixels[x, y]
                            if r < 100 and g < 100 and b < 100:
                                counter += 1
                        else:
                            if pixels[x, y] == matrix:
                                counter += 1
                else:
                    if not_matrix:
                        if pixels[x, y] == 0:
                            counter += 1
                    else:
                        if pixels[x, y] == 1:
                            counter += 1
        return counter

    def recognize_image_text(self, image_url, step, crop, offset=0):
        response = self.load_image(image_url)
        image = Image.open(response.raw)
        if crop:
            image = image.crop(crop if isinstance(crop, tuple) else (0, offset, image.height, offset + 100))
        result = pytesseract.image_to_string(image, lang='eng', config=self.pytesseract_config).strip()
        logging.info(f"Image text in {step}: {result}")
        return result.replace("¥", "Y")

    @staticmethod
    def string_matching_rate(str1, str2):
        ratio = fuzz.partial_ratio(str1.lower(), str2.lower())
        return ratio

    def load_screenshot(self, element=None):
        f = None
        for _ in range(10):
            try:
                if element:
                    f = io.BytesIO(element.screenshot_as_png)
                else:
                    f = io.BytesIO(self._actions.get_browser().get_screenshot_as_png())
                break
            except WebDriverException:
                self._actions.wait(5)
        assert f, "Fail to get screenshot"
        return f

    def verify_image_changes_on_viewer(self, mode: str, element=None, should_exist=True, quality=.8, debug=False, retry=10,
                                       place="site", click_fit=True):
        """
        The function compares the element with mode and finds the equality of images.
        If 'should exist' parameter == True raises ValueError in case of not founding

        Parameters:
        mode: type: string value: name of file without extension
        element: type: tuple, list, str, ExtendedRemoteWebElement, np array, bytes
        should_exist: type: bool
        quality: type: float value: from .0 to 1.0
        debug: type: bool value: displaying image and marking found comparison with red
        retry: type: int value: retry count
        place: type; string value: if sent indicates where the process worked, othervice equal site
        click_fit: type: bool value: clicking fit by height in image viewer

        return: None
        """
        counter = 1
        if element is None:
            element = self._pages.CRS.image_viewer.single_image_viewer_container
        template = cv2.imread(self._names.path.join(self._names.scanned_images_path, f"{mode}.png"))
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        (t_h, t_w) = template.shape[:2]
        for _ in range(retry if should_exist else 1):
            try:
                if isinstance(element, (tuple, list, str)):
                    img = cv2.imdecode(np.frombuffer(
                        self._general_helper.find(element).screenshot_as_png, dtype=np.uint8), cv2.IMREAD_COLOR)
                elif isinstance(element, ExtendedRemoteWebElement):
                    img = cv2.imdecode(np.frombuffer(element.screenshot_as_png, dtype=np.uint8), cv2.IMREAD_COLOR)
                else:
                    img = cv2.cvtColor(np.array(element), cv2.COLOR_RGB2BGR)
            except WebDriverException:
                self._actions.wait(5)
                continue
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            for scale in np.linspace(0.2, 1.0, 20)[::-1]:
                resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
                if resized.shape[0] < t_h or resized.shape[1] < t_w:
                    break
                result = cv2.matchTemplate(resized, template, cv2.TM_CCOEFF_NORMED)
                loc = np.where(result >= quality)
                if debug:
                    self._logging.info(loc)
                    for pt in zip(*loc[::-1]):
                        cv2.rectangle(resized, pt, (pt[0] + t_w, pt[1] + t_h), (0, 0, 255), 2)
                    cv2.imshow('result', resized)
                    cv2.waitKey(0)
                if loc[0].size != 0:
                    if should_exist:
                        return
                    else:
                        raise ValueError(f"Image {mode} found in image viewer on {place}")
            self._actions.wait(3)
            if click_fit:
                self._general_helper.find_and_click(self._pages.CRS.image_viewer.fit_height_button)
        if should_exist:
            raise ValueError(f"Image {mode} not found in image viewer on site")

    def check_fit(self, pos):
        """
        pos:
        h - height
        w - width
        n - none, x and y no fit
        """
        self._actions.wait(3)
        f = self.load_screenshot(self._general_helper.find(self._pages.CRS.image_viewer.single_image_viewer_container))
        image = Image.open(f)
        x, y = image.size
        pixels = image.load()
        if pos == "h":
            assert pixels[int(x / 2), 20] == (255, 255, 255, 255), f"Hit by height error, {pixels[int(x / 2), 20]}"
            assert pixels[20, int(y / 2)] == (237, 237, 237, 255), f"Hit by height error, {pixels[20, int(y / 2)]}"
        elif pos == "w":
            assert pixels[20, int(y / 2)] == (255, 255, 255, 255), f"Hit by width error, {pixels[20, int(y / 2)]}"
        elif pos == "n":
            assert pixels[int(x / 2), 20] == (
                237, 237, 237, 255), f"Displayed with fit, but must displayed without fit, {pixels[int(x / 2), 20]}"
            assert pixels[20, int(y / 2)] == (
                237, 237, 237, 255), f"Displayed with fit, but must displayed without fit, {pixels[20, int(y / 2)]}"
        else:
            raise ValueError("Wrong pos argument")
        f.close()

    def check_uploaded_image(self, container, ms, px_c=0, bigger=True, matrix=(0, 0, 0, 255), not_matrix=False):
        pixel_count, condition = 0, None
        self._general_helper.find_and_click(self._pages.CRS.image_viewer.fit_height_button)
        self._actions.wait(1)
        for _ in range(10):
            f = self.load_screenshot(self._general_helper.find(container))
            pixel_count = self.get_black_pixel_count(f, rgb=True, matrix=matrix, not_matrix=not_matrix)
            f.close()
            if bigger:
                condition = pixel_count - (pixel_count * .1) > px_c
            else:
                condition = pixel_count + (pixel_count * .1) < px_c
            if condition:
                break
            self._general_helper.find_and_click(self._pages.CRS.image_viewer.fit_height_button)
            self._actions.wait(3)
        assert condition, ms
        return pixel_count
