"""Upload Attachment"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
1. Navigate to CRS add any OIT 
2. Click attachments tab
3. Click Upload button, choose different files (word, pdf, png) and upload
4. Finalize order
5. Check attachment in Indexing/Verification attachment tab
"""

tags = []


class test(TestParent):                                                                           # noqa
    doc_file, png_file, pdf_file = "Word_file.docx", "Image.png", "PDF_file.pdf"
    doc_file_tiff, png_file_tiff, pdf_file_tiff = "Word_file.tiff", "Image.tiff", "PDF_file.tiff"

    def __init__(self, data, user_index=0):
        self.user_index = user_index
        super(test, self).__init__(data, __name__)

    def check_files(self, ms, attachment_tab_loc, doc_file_tiff, png_file_tiff, pdf_file_tiff):
        if self.lib.general_helper.check_if_element_exists(attachment_tab_loc):
            self.lib.general_helper.find_and_click(attachment_tab_loc)
            self.lib.CRS.crs.verify_file_present(doc_file_tiff)
            self.lib.CRS.crs.verify_file_present(png_file_tiff)
            self.lib.CRS.crs.verify_file_present(pdf_file_tiff)
        else:
            self.actions.step(ms)

    def __test__(self):
        self.atom.CRS.general.go_to_crs(self.user_index)
        self.lib.CRS.crs.go_to_order_queue()
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.select_order_type()
        self.atom.CRS.order_entry.fill_order_header_name()
        self.lib.required_fields.crs_fill_required_fields()

        attachment_tab_loc = self.lib.CRS.order_entry.tab_locator('Attachments')
        self.lib.general_helper.find_and_click(attachment_tab_loc)
        self.lib.CRS.order_entry.attach_and_verify_file(self.doc_file)
        self.lib.CRS.order_entry.attach_and_verify_file(self.png_file)
        self.lib.CRS.order_entry.attach_and_verify_file(self.pdf_file)
        self.atom.CRS.order_entry.one_oit_to_summary()
        self.atom.CRS.add_payment.finalize_order()

        # go to Capture
        self.lib.CRS.order_item_type.capture_step()

        # check order in Indexing queue

        self.lib.CRS.order_item_type.index_order()
        self.check_files('Indexing step does not have attachment tab', attachment_tab_loc, self.doc_file_tiff,
                         self.png_file_tiff, self.pdf_file_tiff)
        self.lib.CRS.order_item_type.save_order_in_index_entry()
        self.lib.CRS.order_item_type.next_order_in_index_summary()

        # check orders in Verification queue
        self.lib.CRS.crs.go_to_verification_queue()
        self.atom.CRS.order_queue.assign_order(self.user_index)
        self.lib.CRS.crs.click_running_man()
        self.check_files('Verification step does not have attachment tab', attachment_tab_loc, self.doc_file_tiff,
                         self.png_file_tiff, self.pdf_file_tiff)


if __name__ == '__main__':
    run_test(__file__)
