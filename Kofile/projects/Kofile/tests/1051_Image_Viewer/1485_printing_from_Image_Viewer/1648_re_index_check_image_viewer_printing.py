from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Go to CS, submit 'Re-Index', find order from indexing queue, open,
click print icon on image viewer (if configured) and verify that success popup is opened, 
save doc, click on indexing summary row,
again click print icon on image viewer (if configured) and verify that success popup is opened
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
        self.lib.general_helper.scroll_and_click(self.pages.CRS.indexing_queue.lnk_go_to_indexing)
        # Wait loading page
        self.lib.general_helper.find(self.pages.CRS.indexing_queue.btn_add_new_indexing_task)
        # Process order
        self.lib.CRS.crs.click_running_man()
        # Wait loading page
        self.lib.general_helper.find(self.pages.CRS.indexing_entry.btn_cancel)
        # Fill required fields if needed
        self.lib.required_fields.crs_fill_required_fields()
        # Check printing from image viewer
        self.atom.CRS.image_viewer.print_checking()
        # Save order
        self.lib.general_helper.scroll_and_click(self.pages.CRS.indexing_entry.btn_save_and_advance)
        # Click on indexing summary row
        self.actions.click(self.pages.CRS.indexing_summary.image())
        # Check printing from image viewer
        self.atom.CRS.image_viewer.print_checking()
        # Click Next order button
        self.lib.general_helper.find_and_click(self.pages.CRS.indexing_summary.btn_next_order)


if __name__ == '__main__':
    run_test(__file__)
