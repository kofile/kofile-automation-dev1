"""New Indexing Birth Death Task Workflow"""
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
- Upload images to Birth/Death sub-folder
- Create a new Birth/Death record from Indexing New Task, upload image and save
- Process order to Archive
- Find the created document in CS
- Find the created document in Indexing search form
"""

tags = ["48999_location_2"]


class test(TestParent):                                                                                # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: Birth/Death Order is found in Indexing search
        """
        self.lib.data_helper.test_config()
        oit = str(self.data["OIT"]).lower()
        self.atom.CRS.indexing.OCR_Image_Upload(birth_count=1 if "birth" in oit else 0,
                                                death_count=1 if "death" in oit else 0)
        self.atom.CRS.indexing.create_new_indexing_task(self.data)
        self.atom.CRS.indexing.birth_death_verification_step(self.data)
        self.actions.step(type(self.data["dept_id"]).__name__)
        self.lib.CS.general.export_and_find_created_doc_in_cs(self.data, self.data["dept_id"])
        self.atom.CRS.indexing.search_birth_death_in_indexing(self.data)


if __name__ == '__main__':
    run_test(__file__)
