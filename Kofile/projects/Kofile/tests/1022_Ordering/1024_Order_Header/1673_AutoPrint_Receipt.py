from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
Go to CRS Order Queue and click on Add New Order button
In Order Header, select the "Yes" option for AutoPrint Receipt 
Create and finalize any OIT with generic receipt printing (not erProxy)
Find the printed receipt in Azure
"""


class test(TestParent):                                                                            # noqa

    def __init__(self, data):
        data["OIT"] = "Copies"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.order_queue.add_new_order()
        self.lib.CRS.order_header.select_auto_print_option()
        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order)
        # get printed filename from url
        file_name = str(self.actions.get_current_url().split('=')[-1])
        self.logging.info(f"Generic receipt filename: {file_name}")
        # find the printed receipt in Azure
        container = f"wfcontent-{self.data['env']['code']}-printfolder"
        self.lib.azure.check_blob_existence_in_container(file_name, container)


if __name__ == '__main__':
    run_test(__file__)
