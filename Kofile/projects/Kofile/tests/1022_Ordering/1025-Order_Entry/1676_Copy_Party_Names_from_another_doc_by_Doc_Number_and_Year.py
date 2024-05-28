from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    - Find RP doc with filled 'Party' fields by API
    - Go to CRS and create new order
    - Select RP OIT, fill order header
    - Navigate to Party tab and click 'Copy Names' -> Pop-up is opened
    - Enter year and doc# from 1 step and click 'Copy' 
    -> Parties information from previous document correspondingly filled in current doc"""


class test(TestParent):                                                                                # noqa
    user_index = 2

    def __init__(self, data):
        data["OIT"] = "RP_Recordings"
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # Search RP document with filled PARTIES
        self.atom.CS.general.go_to_cs(self.user_index)
        docs = self.api.clerc_search(self.data).document_search()["ResultSet"]
        doc = {}
        for i in docs:
            if i.get("Grantor") and i.get("Grantee"):
                doc = i
                break
        year, doc_num = doc["Number"].split("-")
        parties = {"Grantor": doc["Grantor"], "Grantee": doc["Grantee"]}

        self.atom.CRS.general.go_to_crs()
        self.atom.CRS.order_queue.add_new_order()
        self.atom.CRS.order_entry.select_order_type()

        # Copy names from found document and check values
        self.lib.CRS.order_entry.copy_parties_names(year, doc_num)
        copied_parties = self.lib.CRS.order_entry.get_parties_values()

        assert parties == copied_parties, f"Expected values '{parties}' is not equal to {copied_parties}"


if __name__ == '__main__':
    run_test(__file__)
