from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test
import itertools
import re

description = """
1. Finalize RP OI, scan document in Mixed layout modes and map it to the created document, Check size of Image Viewer on print preview window
2. Change Paper Size select Margins from print preview window and check size of Image viewer
3. Open Image in Undock mode and click on print icon, check size of Image Viewer print preview window
                """

tags = ["48999_location_2"]


class test(TestParent):
    values = [0, 0.5, 1, 1.5]

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.lib.general_helper.check_order_type()
        self.locators = (self.pages.CRS.image_viewer.margin_top, self.pages.CRS.image_viewer.margin_left,
                         self.pages.CRS.image_viewer.margin_right, self.pages.CRS.image_viewer.margin_bottom)
        self.all_radiobuttons = self.make_locators()
        # Create and Finalize order
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        # Capture order
        self.lib.CRS.order_item_type.capture_step(save_after_scan=False)

        self.lib.CRS.capture.open_image_in_image_viewer(timeout=60, retries=5)
        self.actions.wait_for_element_displayed(self.pages.CRS.image_viewer.btn_print_icon)
        self.lib.general_helper.get_displayed_element(self.pages.CRS.image_viewer.btn_print_icon, click=True)
        self.lib.general_helper.wait_until(
            lambda: not self.lib.general_helper.find(self.pages.CRS.image_viewer.print_image,
                                                     get_attribute="src").endswith("for_print.gif"), 60)
        for loc in self.locators:
            self.lib.general_helper.find_and_click(self.lib.general_helper.make_locator(loc, 1))
        one_inch_size = self.get_size()
        for combo in itertools.product(*self.all_radiobuttons):
            values = list()
            for locator, val in combo:
                self.lib.general_helper.find_and_click(locator)
                values.append(val)
            tv, lv, rv, bv = values
            size = self.get_size()
            self.assert_size(size.get("padding_l"), one_inch_size.get("padding_l"), lv, "left")
            self.assert_size(size.get("padding_r"), one_inch_size.get("padding_r"), rv, "right")
            self.assert_size(size.get("padding_t"), one_inch_size.get("padding_t"), tv, "top")
            self.assert_size(size.get("padding_b"), one_inch_size.get("padding_b"), bv, "bottom")

    @staticmethod
    def assert_size(first, second, val, place):
        second_val = round(second * val, 4)
        values = (second_val, round(second_val + .0001, 4), round(second_val - .0001, 4))
        assert first in values, f"wrong margin {place} {val}. Expected: {second_val}, current: {first}"

    def make_locators(self):
        result = list()
        for loc in self.locators:
            locators = list()
            for val in self.values:
                locators.append((self.lib.general_helper.make_locator(loc, val), val))
            result.append(locators)
        return result

    def get_size(self):
        style = self.lib.general_helper.find(self.pages.CRS.image_viewer.print_image, get_attribute="style")
        width = re.findall("width: (.*?)px;", style)
        width = float(width[0]) if width else .0

        height = re.findall("height: (.*?)px;", style)
        height = float(height[0]) if height else .0

        padding = re.findall("padding: (.*?);", style)
        padding = padding[0] if padding else "0px"

        if padding == "0px":
            padding_l = .0
            padding_r = .0
            padding_t = .0
            padding_b = .0
        else:
            p = re.findall(" (.*?)px", f" {padding}")
            match p:
                case t, l:
                    padding_l = float(l)
                    padding_r = float(l)
                    padding_t = float(t)
                    padding_b = float(t)
                case t, l, b:
                    padding_l = float(l)
                    padding_r = float(l)
                    padding_t = float(t)
                    padding_b = float(b)
                case t, r, b, l:
                    padding_l = float(l)
                    padding_r = float(r)
                    padding_t = float(t)
                    padding_b = float(b)
                case _:
                    raise ValueError(f"Cant process padding: {padding}")
        return {"width": width, "height": height, "padding_l": padding_l, "padding_r": padding_r,
                "padding_t": padding_t, "padding_b": padding_b}


if __name__ == '__main__':
    run_test(__file__)
