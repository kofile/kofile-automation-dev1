from projects.Kofile.Lib.test_parent import TestParent
from datetime import datetime, timezone
from runner import run_test


description = """
    Go to CRS -> Balance Drawer
    -> In Balance Drawer click 'Settle' button
    -> Click 'Print drawer summary' > Success pop-up 'Drawer summary printing initialized' appeared
    -> Go to Azure Blob > Check that printed document exist in 'wf-content-[TENANT_CODE]-print-folder' folder
    """

tags = ["48999_location_2"]


class test(TestParent):                                                                  # noqa
    user_index = 0

    def __init__(self, data):
        data["orderheader"] = "guest"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Go to CRS
        self.atom.CRS.general.go_to_crs(self.user_index)
        # Go to Balance drawer
        self.lib.CRS.balance_drawer.go_to_balance_drawer(initialize=True, user_index=self.user_index)
        self.lib.CRS.balance_drawer.click_settle_button()
        self.lib.CRS.balance_drawer.click_print_drawer_summary_lnk()
        # Wait until document printed
        self.actions.wait(5)
        # Search document in Azure
        now_timestamp = int(datetime.now().astimezone(timezone.utc).timestamp())
        container = f"wfcontent-{self.data['env']['code']}-printfolder"
        files = self.lib.azure.get_blobs_list_in_container(container, name_starts_with="DrawerSummary_")
        found = False
        for i in files:
            file_timestamp = int(i["creation_time"].timestamp())
            if now_timestamp - file_timestamp <= 30:
                self.logging.info(f"File found: {i}")
                found = True
                break
        assert found, f"Drawer Summary pdf file not found in '{container}' after click 'Print drawer summary' link"


if __name__ == '__main__':
    run_test(__file__)
