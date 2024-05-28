from datetime import datetime
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Log in to Clerk Search as a Clerk -> Property Records Search default page with clerk name is displayed
    Verify actions on the row -> Actions available on the row are "Print", "Quick Doc"(=FREE DOWNLOAD) and "Add to Inbox
    Click on "Print" icon on any row -> Infinite spinner appears upon the action
    Update the last DEVICE_JOB record for your printer in DB
    Printing success message appears.
    The printed document is found in Azure
    https://vgdevimages.blob.core.windows.net:443/wfcontent-psexchange-69999/Printing folder
    Click on "Quick Doc" icon on any row -> The image is immediately downloaded (free download)
    Click on Add to Inbox icon on any row -> The document is added to clerk's Inbox
    """

tags = ['48999_location_2']


class test(TestParent):                                                                                   # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CS.general.go_to_cs(clerk=True)

        # search document
        self.api.clerc_search(self.data).get_document_number()
        self.lib.PS.general.search_document_by_number()
        if self.lib.PS.ps_main_page.is_search_successful():
            printing_time = datetime.utcnow()
            self.lib.CS.general.print_doc(self.data)

            # check do in azure
            azure = self.lib.azure
            correct_file = None
            now = datetime.utcnow()
            all_files_generator = azure.get_all_files_in_folder(f"wfcontent-psexchange-{self.data['env']['code']}",
                                                                folder="Printing/")
            while filename := next(all_files_generator, None):
                if printing_time < filename.last_modified.replace(tzinfo=None) < now:
                    correct_file = filename
                    break
            assert correct_file, "File not found in azure"

            # download file
            self.lib.CS.general.download_file()

            # add to inbox
            self.lib.PS.ps_main_page.clear_inbox_()
            self.actions.wait_for_element_present(self.pages.PS.main_page.add_to_inbox_button)
            self.lib.general_helper.find_and_click(self.pages.PS.main_page.add_to_inbox_button)
            self.actions.wait_for_element_text(self.pages.PS.main_page.inbox_item_count, "1")
        else:
            raise ValueError("Search failed!")


if __name__ == '__main__':
    run_test(__file__)
