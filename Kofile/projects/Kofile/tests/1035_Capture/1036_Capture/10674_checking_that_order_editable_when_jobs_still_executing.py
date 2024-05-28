from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

import re

CHECK_POS = True

description = """
    Create Scan First - Real Property OH
    Finalize order
    Execute Autoredaction jobs (AutoRedactionExport , AutoRedactionListenner, AutoRedactionImport ) - during jobs execution check that order is editable in verification queue 
    After Autoredaction jobs executed, find order in Verificationqueue, assign and edit. Check image viewer 
    All candidates are autoredacted (On Attached file autoredaction candidates exists in page 2, 15, 16)
        """

tags = ["48999_location_2"]


class test(TestParent):  # noqa
    oit = "Real Property OH"
    stamps = {
        "2": {
            "top": (700, 900),
            "left": (200, 400),
            "width": (60, 80),
            "height": (5, 20),
        },
        "15": {
            "top": (800, 1000),
            "left": (250, 450),
            "width": (60, 80),
            "height": (5, 20),
        },
        "16": {
            "top": (150, 350),
            "left": (250, 450),
            "width": (60, 80),
            "height": (5, 20),
        }
    }

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.order_queue.add_order_with_scan_first_flow(self.oit)
        self.lib.general_helper.find_and_click(self.pages.PS.summary_tab.edit_button)
        self.lib.required_fields.crs_fill_required_fields()
        self.lib.general_helper.scroll_and_click(self.pages.CRS.order_entry.btn_add_to_order)
        self.actions.wait_for_element_displayed(self.pages.CRS.order_summary.lnk_return_to_order_queue)
        self.atom.CRS.add_payment.finalize_order()
        order_number = self.lib.CRS.order_header.get_order_number()
        with self.lib.db as db:
            if db.get_status_auto_redaction_job(order_number) == 10:
                db.scheduler_job_update_for_export("AutoRedactionExport")
                assert self.lib.general_helper.wait_until(
                    lambda m=order_number: db.get_status_auto_redaction_job(m) == 20, timeout=2 * 60, period=3)
            if db.get_status_auto_redaction_job(order_number) == 20:
                db.scheduler_job_update_for_export("AutoRedactionExport")
                assert self.lib.general_helper.wait_until(
                    lambda m=order_number: db.get_status_auto_redaction_job(m) == 30, timeout=2 * 60, period=3)
            if db.get_status_auto_redaction_job(order_number) == 30:
                db.scheduler_job_update_for_export("AutoRedactionExport")
                assert self.lib.general_helper.wait_until(
                    lambda m=order_number: db.get_status_auto_redaction_job(m) == 100, timeout=10 * 60, period=10)
        self.lib.general_helper.find_and_click(self.pages.CRS.order_finalization.row_numbers)
        self.lib.general_helper.wait_and_click(self.pages.CRS.image_viewer.icn_redaction)

        for key, value in self.stamps.items():
            self.actions.wait_for_element_displayed(self.pages.CRS.image_viewer.page_number_input)
            self.lib.general_helper.wait_for_element_clickable(self.pages.CRS.image_viewer.page_number_input, 10)
            self.actions.clear_element(self.pages.CRS.image_viewer.page_number_input)
            self.actions.send_keys(self.pages.CRS.image_viewer.page_number_input, (key, self.keys.ENTER))
            self.actions.wait(3)
            box = self.lib.general_helper.find(self.pages.CRS.image_viewer.redaction_box)
            style = box.get_attribute("style")
            for k, v in value.items():
                val = re.findall(rf"{k}: (\d+(?:\.\d+)?)px;", style)
                assert val, f"{style=} {k=}"
                if CHECK_POS:
                    assert v[0] < float(val[0]) < v[1], f"{val=}, {v=}, {k=}, {key=}"


if __name__ == '__main__':
    run_test(__file__)
