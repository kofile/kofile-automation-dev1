from projects.Kofile.Lib.CRS.CRS_functions import CRS
from projects.Kofile.Lib.test_parent import LibParent

CRS_functions = CRS()


class IndexingQueue(LibParent):
    def __init__(self):
        super(IndexingQueue, self).__init__()

    def verify_order_status(self, status):
        """Verify status of order in Indexing Queue"""
        data = self._general_helper.get_data()
        self._actions.verify_element_text(self._pages.CRS.general.status_by_order_number(data["order_number"]),
                                          data['config'].get_status(f'Indexing.{status}.value'))

    def select_new_indexing_task(self, data):
        """Birth or Death option is stored in data['OIT']"""
        CRS_functions.go_to_indexing_queue()
        self._general_helper.find_and_click(self._pages.CRS.indexing_queue.btn_add_new_indexing_task)
        self._general_helper.find_and_click(
            self._general_helper.make_locator(self._pages.CRS.indexing_queue.pup_nit_ddl_select_doc_group,
                                              ' '.join(data["OIT"].split('_'))))
        self._general_helper.find_and_click(self._pages.CRS.indexing_queue.pup_nit_btn_submit)
        self._actions.wait_for_element_displayed(self._pages.CRS.indexing_entry.txt_doc_number)

    def add_birth_indexing_order(self):
        self._general_helper.find_and_click(self._pages.CRS.indexing_queue.add_new_order_btn)
        self._actions.wait_for_element_present(self._pages.CRS.indexing_queue.pup_nit_ddl_doc_group)
        self._general_helper.select_by_text(self._pages.CRS.indexing_queue.pup_nit_ddl_doc_group, "Birth Record")
        self._general_helper.find_and_click(self._pages.CRS.indexing_queue.pup_nit_btn_submit)
        self._actions.wait_for_element_displayed(self._pages.CRS.indexing_entry.icn_birth_death_record_upload)
