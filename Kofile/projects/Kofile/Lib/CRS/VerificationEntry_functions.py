import re

from projects.Kofile.Lib.CRS.IndexingEntry_functions import IndexingEntry
from projects.Kofile.Lib.test_parent import LibParent

IndexingEntry_functions = IndexingEntry()


class VerificationEntry(LibParent):
    prop_sfx = list()

    def __init__(self):
        super(VerificationEntry, self).__init__()
        self._properties_dict = {
            "subdivision": {'elm_to_check_rekey': self._pages.CRS.indexing_entry.property_subdivision},
            "survey": {'elm_to_check_rekey': self._pages.CRS.indexing_entry.survey_name_input},
            "newdesc": {'elm_to_check_rekey': self._pages.CRS.indexing_entry.description_property_input},
            "condominium": {'elm_to_check_rekey': self._pages.CRS.indexing_entry.property_condominium},
            "unplatted": {'elm_to_check_rekey': self._pages.CRS.indexing_entry.unplatted_section_input}
        }

    def __48999__(self):
        self.prop_sfx = ["0-Condominium", "0-Unplatted"]
        self.get_parties_locators = self.get_parties_locators_loc_2

    def click_save_and_advance_button(self):
        self._general_helper.find_and_click(self._pages.CRS.verification_entry.btn_save_and_advance)
        self._general_helper.wait_for_spinner()

    def check_property_re_key_n_rows(self):
        IndexingEntry_functions.fill_property(step='verification')
        self._actions.focus_element(self._pages.CRS.indexing_entry.grantee_name_input)
        self._actions.wait_for_element_enabled(
            self._pages.CRS.verification_entry.btn_save_and_advance_verification_entry)
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_add_new_desc)
        self._actions.focus_element(self._pages.CRS.indexing_entry.grantee_name_input)
        self._actions.wait_for_element_displayed(self._pages.CRS.verification_entry.confirm_popup)
        self._general_helper.find_and_click(self._pages.CRS.verification_entry.pup_return_address_warning_btn_yes)
        self._actions.wait_for_element_not_enabled(
            self._pages.CRS.verification_entry.btn_save_and_advance_verification_entry)
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_add_new_desc)
        self._actions.focus_element(self._pages.CRS.indexing_entry.grantee_name_input)
        self._actions.wait_for_element_displayed(self._pages.CRS.verification_entry.confirm_popup)
        self._general_helper.find_and_click(self._pages.CRS.verification_entry.pup_return_address_warning_btn_no)
        self._actions.wait_for_element_not_enabled(
            self._pages.CRS.verification_entry.btn_save_and_advance_verification_entry)
        self._general_helper.find_and_click(
            self._pages.CRS.verification_entry.pup_ReKey_Verification_lnk_Return_to_Rekey)

    def return_to_rekey_property(self):
        data = self._general_helper.get_data()
        prop_types = data['config'].test_data(f"{data.OIT}.indexing.property").keys()
        # checking empty row case
        for p in prop_types:
            self._check_re_key_for_field(self._properties_dict[p]['elm_to_check_rekey'],
                                         self._pages.CRS.indexing_entry.grantee_name_input,
                                         return_to_re_key=True)
        # checking mismatch data in row case
        for p in prop_types:
            if p == 'subdivision' or p == 'condominium':
                data_for_input = 'TEST'
            else:
                data_for_input = self._general_helper.random_string(5, 4)
            self._check_re_key_for_field(self._properties_dict[p]['elm_to_check_rekey'],
                                         self._pages.CRS.indexing_entry.grantee_name_input,
                                         data_for_input=data_for_input, return_to_re_key=True)
            self._actions.clear_element(self._properties_dict[p]['elm_to_check_rekey'])

    def update_re_key_data_property(self):
        data = self._general_helper.get_data()
        prop_types = data['config'].test_data(f"{data.OIT}.indexing.property").keys()
        # checking empty row case
        for p in prop_types:
            self._check_re_key_for_field(self._properties_dict[p]['elm_to_check_rekey'],
                                         self._pages.CRS.indexing_entry.grantee_name_input,
                                         save_re_key=True)
        # checking mismatch data in row case
        for p in prop_types:
            if p == 'subdivision' or p == 'condominium':
                data_for_input = 'TEST'
            elif p == 'unplatted':
                data_for_input = '5'
            else:
                data_for_input = self._general_helper.random_string(5, 4)
            self._check_re_key_for_field(self._properties_dict[p]['elm_to_check_rekey'],
                                         self._pages.CRS.indexing_entry.grantee_name_input,
                                         data_for_input=data_for_input, save_re_key=True)

    def _select_property_section_and_value(self):
        data = self._general_helper.get_data()
        property_type = list(data['config'].test_data(f"{data.OIT}.indexing.property").keys())[0]
        field_name = data['config'].test_data(f"{data.OIT}.indexing.property.{property_type}")[0]
        loc = self._pages.CRS.indexing_entry.property_field_locator(property_type, field_name)
        if field_name == 'Legal Description / Remarks':
            field_name = 'LegalDescriptionRemarks'
        if field_name == 'Govt Lot':
            field_name = 'GovtLot'
        value = data['config'].test_data(f"{data.OIT}.indexing.prop_values.{field_name}")
        return loc, value

    def restore_re_key_data_property(self):
        # checking empty row case
        loc_and_value = self._select_property_section_and_value()
        self._check_re_key_for_field(loc_and_value[0], self._pages.CRS.indexing_entry.grantee_name_input,
                                     indexed_data=loc_and_value[1],
                                     restore_indexed=True)
        # checking mismatch data in row case
        loc_and_value = self._select_property_section_and_value()
        self._check_re_key_for_field(loc_and_value[0], self._pages.CRS.indexing_entry.grantee_name_input,
                                     data_for_input=self._general_helper.random_string(5, 4),
                                     indexed_data=loc_and_value[1], restore_indexed=True)

    def return_to_rekey_parties(self, section_to_check, section_to_move_out):
        party_fields = self._actions.execution.data['config'].test_data(
            f"{self._actions.execution.data.OIT}.indexing.party_name")
        for _ in party_fields:
            self._check_re_key_for_field(self._pages.CRS.indexing_entry.party_name_locator(section_to_check, _),
                                         self._pages.CRS.indexing_entry.party_name_locator(section_to_move_out, _),
                                         data_for_input=self._general_helper.random_string(5, 4), return_to_re_key=True)
            self._actions.clear_element(self._pages.CRS.indexing_entry.party_name_locator(section_to_check, _))

    def update_re_key_data_parties(self, data):
        default_prop_type_name = data.config.config_file.OITs[f'{data.OIT}']['indexing']['default_ptop_type']
        party_fields = data['config'].test_data(f"{data.OIT}.indexing.party_name")
        self.fill_party_names(data, grantee_section=True)
        self._check_re_key_for_field(self._pages.CRS.indexing_entry.party_name_locator('Grantor Name', party_fields[0]),
                                     self._pages.CRS.indexing_entry.party_name_locator('Grantee Name', party_fields[0]),
                                     data_for_input=self._general_helper.random_string(5, 4), save_re_key=True,
                                     default_prop_type_name=default_prop_type_name)
        self._check_re_key_for_field(self._pages.CRS.indexing_entry.party_name_locator('Grantee Name', party_fields[0]),
                                     self._pages.CRS.indexing_entry.party_name_locator('Grantor Name', party_fields[0]),
                                     data_for_input=self._general_helper.random_string(5, 4), save_re_key=True,
                                     default_prop_type_name=default_prop_type_name)

    def restore_re_key_data_parties(self, data):
        default_prop_type_name = data.config.config_file.OITs[f'{data.OIT}']['indexing']['default_ptop_type']
        party_fields = data['config'].test_data(f"{data.OIT}.indexing.party_name")
        self.fill_party_names(data, grantee_section=True)
        self._check_re_key_for_field(self._pages.CRS.indexing_entry.party_name_locator('Grantor Name', party_fields[0]),
                                     self._pages.CRS.indexing_entry.party_name_locator('Grantee Name', party_fields[0]),
                                     data_for_input=self._general_helper.random_string(5, 4),
                                     indexed_data=self._actions.execution.data.grantor_names[party_fields[0]][0],
                                     restore_indexed=True,
                                     default_prop_type_name=default_prop_type_name)
        self._check_re_key_for_field(self._pages.CRS.indexing_entry.party_name_locator('Grantee Name', party_fields[0]),
                                     self._pages.CRS.indexing_entry.party_name_locator('Grantor Name', party_fields[0]),
                                     data_for_input=self._general_helper.random_string(5, 4),
                                     indexed_data=self._actions.execution.data.grantee_names[party_fields[0]][0],
                                     restore_indexed=True,
                                     default_prop_type_name=default_prop_type_name)

    def send_document_to_indexing(self, reason):
        self._general_helper.find_and_click(self._pages.CRS.verification_entry.send_document_to_index_checkbox)
        self._actions.wait_for_element_displayed(
            self._pages.CRS.verification_entry.send_document_to_indexing_queue_input)
        self._general_helper.find_and_send_keys(
            self._pages.CRS.verification_entry.send_document_to_indexing_queue_input,
            reason)
        self._general_helper.find_and_click(self._pages.CRS.order_summary.pup_discount_btn_submit)
        self._actions.wait(1)

    def cancel_verification(self, reason, desc):
        self._general_helper.find_and_click(self._pages.CRS.verification_entry.btn_cancel)
        self._general_helper.find_and_click(self._pages.CRS.verification_entry.send_order_to_indexing_queue_button)
        self._general_helper.find_and_click(self._pages.CRS.order_summary.pup_btn_cancel_entire_order_submit)
        self._general_helper.find_and_send_keys(self._pages.CRS.order_summary.pup_Cancel_entire_order_reason, reason)
        self._general_helper.find_and_send_keys(self._pages.CRS.order_summary.pup_Cancel_Entire_Order_description, desc)
        self._general_helper.find_and_click(self._pages.CRS.order_summary.pup_btn_cancel_entire_order_submit)
        self._actions.wait_for_window_present_by_partial_url("/VerificationTaskEntry?")

    def check_prop_rekey_grid_header(self):
        """
        Function compares typed during indexing prop types with their
        count and preconfigured tenants prop types and check
        prop grid header on the verification entry page.
        """
        data = self._general_helper.get_data()
        typed_prop_types = data['config'].test_data(f"{data.OIT}.indexing.property").keys()
        result = [f"1-{i.capitalize()}" if i != 'newdesc' else "1 -Desc" for i in typed_prop_types]
        result = ', '.join(result + self.prop_sfx)
        self._actions.assert_element_text(self._pages.CRS.verification_entry.lbl_property_grid_text, result)

    def check_prop_rows_count_and_seq(self):
        pr_blocks = list(map(lambda i: re.sub(r"^.*-|\s.*$", "", i),
                             self._general_helper.find_elements(self._pages.CRS.verification_entry.abstract_prop_block,
                                                                get_attribute='class')))
        data = self._general_helper.get_data()
        assert pr_blocks == list(data['config'].test_data(f"{data.OIT}.indexing.property").keys())

    def check_prop_rekey_fields_are_empty(self):
        data = self._general_helper.get_data()
        typed_prop_types = data['config'].test_data(f"{data.OIT}.indexing.property").keys()
        for p in typed_prop_types:
            field_names = data['config'].test_data(f"{data.OIT}.indexing.property.{p}")
            for field_name in field_names:
                self._actions.assert_element_value(self._pages.CRS.indexing_entry.property_field_locator(p, field_name),
                                                   "")

    def check_party_names_count(self, data):
        grantor_names = data.grantor_names[data.config.config_file.OITs[f'{data.OIT}']['indexing']['party_name'][0]]
        grantee_names = data.grantee_names[data.config.config_file.OITs[f'{data.OIT}']['indexing']['party_name'][0]]
        assert len(self._general_helper.find_elements(
            self._pages.CRS.indexing_entry.party_name_locator(
                'Grantor Name', data.config.config_file.OITs[f'{data.OIT}']['indexing']['party_name'][0]))
        ) == len(grantor_names)
        assert len(self._general_helper.find_elements(
            self._pages.CRS.indexing_entry.party_name_locator(
                'Grantee Name', data.config.config_file.OITs[f'{data.OIT}']['indexing']['party_name'][0]))
        ) == len(grantee_names)

    def check_party_names_are_empty(self):
        for i in self._general_helper.find_elements(
                self._pages.CRS.indexing_entry.grantor_name_input):
            self._actions.assert_element_value(i, "")

        for i in self._general_helper.find_elements(
                self._pages.CRS.indexing_entry.grantee_name_input):
            self._actions.assert_element_value(i, "")

    def check_party_names_are_not_empty(self, data):
        party_fields = data['config'].test_data(f"{data.OIT}.indexing.party_name")
        for _ in party_fields:
            stored_grantor_values = data.grantor_names[_]
            stored_grantee_values = data.grantee_names[_]
            grantor_inputs = self._general_helper.find_elements(
                self._pages.CRS.indexing_entry.party_name_locator('Grantor Name', _))
            grantee_inputs = self._general_helper.find_elements(
                self._pages.CRS.indexing_entry.party_name_locator('Grantee Name', _))
            for i in stored_grantor_values:
                self._actions.assert_element_value(grantor_inputs[stored_grantor_values.index(i)], i)
            for i in stored_grantee_values:
                self._actions.assert_element_value(grantee_inputs[stored_grantee_values.index(i)], i)

    def get_parties_locators(self, f_name):
        return (
            self._pages.CRS.indexing_entry.party_name_locator("Grantor Name", f_name),
            self._pages.CRS.indexing_entry.party_name_locator("Grantee Name", f_name)
        )

    def get_parties_locators_loc_2(self, f_name):
        return (
            self._pages.CRS.indexing_entry.grantor_name_input,
            self._pages.CRS.indexing_entry.grantee_name_input
        )

    def fill_party_names(self, data, grantor_section=False, grantee_section=False):
        party_fields = data['config'].test_data(f"{data.OIT}.indexing.party_name")
        if grantor_section:
            for _ in party_fields:
                stored_values = data.grantor_names[_]
                inputs = self._general_helper.find_elements(self.get_parties_locators(_)[0])
                for a, value in enumerate(stored_values):
                    if value:
                        inp = inputs[a]
                        self._actions.clear(inp)
                        self._actions.send_keys(inp, value)
        if grantee_section:
            for _ in party_fields:
                stored_values = data.grantee_names[_]
                inputs = self._general_helper.find_elements(self.get_parties_locators(_)[1])
                for a, value in enumerate(stored_values):
                    if value:
                        inp = inputs[a]
                        self._actions.clear(inp)
                        self._actions.send_keys(inp, value)

    def check_doc_fields_are_empty(self, data):
        if 'DOCUMENT' in data['config'].test_data(f"{data.OIT}.indexing.doc_fields"):
            self._actions.assert_element_value(self._pages.CRS.verification_entry.doc_type_select, "")
        if 'Book' in data['config'].test_data(f"{data.OIT}.indexing.doc_fields"):
            self._actions.assert_element_value(self._pages.CRS.verification_entry.book_input, "")
        if 'Volume' in data['config'].test_data(f"{data.OIT}.indexing.doc_fields"):
            self._actions.assert_element_value(self._pages.CRS.verification_entry.volume_input, "")
        if 'Page' in data['config'].test_data(f"{data.OIT}.indexing.doc_fields"):
            self._actions.assert_element_value(self._pages.CRS.verification_entry.page_input, "")
        if 'Consideration Amount' in data['config'].test_data(f"{data.OIT}.indexing.doc_fields"):
            self._actions.assert_element_value(self._pages.CRS.verification_entry.consideration_input, "")

    def fill_doc_fields(self, data):
        if 'DOCUMENT' in data['config'].test_data(f"{data.OIT}.indexing.doc_fields"):
            self._actions.select_option_by_text(self._pages.CRS.verification_entry.doc_type_select, data.doc_type)
        if 'Volume' in data['config'].test_data(f"{data.OIT}.indexing.doc_fields"):
            self._actions.send_keys(self._pages.CRS.verification_entry.volume_input, data.doc_liber)
        if 'Page' in data['config'].test_data(f"{data.OIT}.indexing.doc_fields"):
            self._actions.send_keys(self._pages.CRS.verification_entry.page_input, data.doc_page)
        if 'Consideration Amount' in data['config'].test_data(f"{data.OIT}.indexing.doc_fields"):
            self._actions.send_keys(self._pages.CRS.verification_entry.consideration_input, data.consideration)

    def _check_re_key_for_field(self, checking_elem, move_cursor_to_elem, indexed_data='', data_for_input='',
                                return_to_re_key=False, save_re_key=False, restore_indexed=False,
                                default_prop_type_name=''):
        """
        Function for checking re-Key for indicated fields.

        :param checking_elem: The web element that will be checked.
        :param move_cursor_to_elem: The cursor will be moved to this web element.
        :param indexed_data: The data that was typed in the corresponded field during indexing.
        :param data_for_input: The data that will be typed in the corresponded field,
         should be not same as indexed_data.
        :param return_to_re_key: Set True if you want to check this re-Key behaviour.
        :param save_re_key: Set True if you want to check this re-Key behaviour.
        :param restore_indexed: Set True if you want to check this re-Key behaviour.
        :param default_prop_type_name: Set it in case of checking party name fields for focusing in property section.
        """
        self._actions.clear_element(checking_elem)
        self._actions.focus_element(checking_elem)
        if data_for_input:
            self._actions.send_keys(checking_elem, data_for_input)
        self._actions.wait(0.3)
        self._actions.focus_element(move_cursor_to_elem)
        self._actions.wait_for_element_displayed(
            self._pages.CRS.verification_entry.pup_ReKey_Verification_lnk_Return_to_Rekey)
        self._actions.wait(0.5)

        if data_for_input:
            assert self._general_helper.find_elements(checking_elem)[0].value_of_css_property(
                'color') == 'rgba(228, 0, 0, 1)', "Element {} text's color isn't red".format(checking_elem[1])
        else:
            assert self._general_helper.find_elements(checking_elem)[0].value_of_css_property(
                'border-color') == 'rgb(228, 0, 0)', "Element's {} border color isn't red".format(checking_elem[1])
        if return_to_re_key:
            self._general_helper.find_and_click(
                self._pages.CRS.verification_entry.pup_ReKey_Verification_lnk_Return_to_Rekey)
            self._actions.wait_for_element_not_present(
                self._pages.CRS.verification_entry.pup_ReKey_Verification_lnk_Return_to_Rekey)
            self._actions.wait_for_element_not_enabled(
                self._pages.CRS.verification_entry.btn_save_and_advance_verification_entry)
        elif save_re_key or restore_indexed:
            if save_re_key:
                self._general_helper.find_and_click(
                    self._pages.CRS.verification_entry.pup_ReKey_Verification_rdb_save_rekey_date)
            elif restore_indexed:
                self._general_helper.find_and_click(
                    self._pages.CRS.verification_entry.pup_ReKey_Verification_rdb_restore_date)
            self._general_helper.find_and_click(
                self._pages.CRS.verification_entry.pup_ReKey_Verification_lnk_Save_Changes)
            self._actions.wait_for_element_not_present(
                self._pages.CRS.verification_entry.pup_ReKey_Verification_lnk_Return_to_Rekey)
            if 'Grantor' in checking_elem[1] or 'Grantee' in checking_elem[1]:
                self._actions.focus_element(self._properties_dict[default_prop_type_name]['elm_to_check_rekey'])
                self._actions.wait(1)
                self._actions.focus_element(checking_elem)
            self._actions.wait_for_element_enabled(
                self._pages.CRS.verification_entry.btn_save_and_advance_verification_entry)
            if save_re_key:
                data = data_for_input
            else:
                data = indexed_data
            self._actions.wait_for_element_displayed(checking_elem)
            self._general_helper.wait_attribute_in_element(checking_elem, data)

    def check_party_re_key_n_rows(self):
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_add_grantor)
        self._actions.focus_element(self._pages.CRS.verification_entry.page_input)
        self._actions.wait_for_element_displayed(self._pages.CRS.verification_entry.confirm_popup)
        self._general_helper.find_and_click(self._pages.CRS.verification_entry.pup_return_address_warning_btn_yes)
        self._actions.wait_for_element_not_enabled(
            self._pages.CRS.verification_entry.btn_save_and_advance_verification_entry)
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_add_grantor)
        self._actions.focus_element(self._pages.CRS.verification_entry.page_input)
        self._actions.wait_for_element_displayed(self._pages.CRS.verification_entry.confirm_popup)
        self._general_helper.find_and_click(self._pages.CRS.verification_entry.pup_return_address_warning_btn_no)
        self._actions.focus_element(self._pages.CRS.verification_entry.page_input)
        self._actions.wait_for_element_displayed(
            self._pages.CRS.verification_entry.pup_ReKey_Verification_lnk_Return_to_Rekey)
        self._actions.wait_for_element_not_enabled(
            self._pages.CRS.verification_entry.btn_save_and_advance_verification_entry)

    def check_view_indexing_data(self, section, elm_to_moving_out):
        links = {
            "property": self._pages.CRS.verification_entry.lnk_view_indexing_data,
            "document": self._pages.CRS.verification_entry.lnk_view_indexing_document_data,
            "grantor": self._pages.CRS.verification_entry.lnk_view_indexing_grantor_data,
            "grantee": self._pages.CRS.verification_entry.lnk_view_indexing_grantee_data
        }
        self._actions.wait_for_element_displayed(links[section])
        self._general_helper.find_and_click(links[section])
        if section == 'property':
            self._actions.wait_for_element_displayed(
                self._general_helper.make_locator(self._pages.CRS.verification_entry.view_indexed_section_title,
                                                  'PROPERTY'))
            data = self._general_helper.get_data()
            prop_types = data['config'].test_data(f"{data.OIT}.indexing.property").keys()
            for p in prop_types:
                self._check_rows_in_view_indexed_data_block('prop-' + p)
        elif section == 'document':
            doc_fields = self._actions.execution.data['config'].test_data(
                f"{self._actions.execution.data.OIT}.indexing.doc_fields")
            if 'DOCUMENT' in doc_fields:
                self._actions.wait_for_element_displayed(
                    self._general_helper.make_locator(self._pages.CRS.verification_entry.view_indexed_section_title,
                                                      'DOCUMENT'))
                self._actions.assert_element_displayed(
                    self._pages.CRS.verification_entry.doc_type_select_in_view_indexed_data)
            book_page_block = [_ for _ in doc_fields if _ != 'DOCUMENT' and _ != 'Consideration Amount']
            for _ in book_page_block:
                self._actions.assert_element_displayed(
                    self._general_helper.make_locator(
                        self._pages.CRS.verification_entry.book_vol_page_input_in_view_indexed_data, _))
            self._actions.assert_element_displayed(
                self._pages.CRS.verification_entry.cons_amount_input_in_view_indexed_data)
        elif section == 'grantor':
            self._actions.wait_for_element_displayed(
                self._general_helper.make_locator(self._pages.CRS.verification_entry.view_indexed_section_title,
                                                  'GRANTOR'))
            grantor_names = self._actions.execution.data.grantor_names[
                self._actions.execution.data.config.config_file.OITs[f'{self._actions.execution.data.OIT}']['indexing'][
                    'party_name'][
                    0]]
            self._check_rows_in_view_indexed_data_block('party-block', len(grantor_names))
        elif section == 'grantee':
            self._actions.wait_for_element_displayed(
                self._general_helper.make_locator(self._pages.CRS.verification_entry.view_indexed_section_title,
                                                  'GRANTEE'))
            grantee_names = self._actions.execution.data.grantee_names[
                self._actions.execution.data.config.config_file.OITs[f'{self._actions.execution.data.OIT}']['indexing'][
                    'party_name'][
                    0]]
            self._check_rows_in_view_indexed_data_block('party-block', len(grantee_names))
        # Moving out cursor for checking that the viewed section is closed
        self._actions.focus_element(elm_to_moving_out)
        if section == 'property':
            self._general_helper.wait_disappear_element(
                self._general_helper.make_locator(self._pages.CRS.verification_entry.view_indexed_section_title,
                                                  'PROPERTY'))
        elif section == 'document':
            self._general_helper.wait_disappear_element(
                self._general_helper.make_locator(self._pages.CRS.verification_entry.view_indexed_section_title,
                                                  'DOCUMENT'))
        elif section == 'grantor':
            self._general_helper.wait_disappear_element(
                self._general_helper.make_locator(self._pages.CRS.verification_entry.view_indexed_section_title,
                                                  'GRANTOR'))
        elif section == 'grantee':
            self._general_helper.wait_disappear_element(
                self._general_helper.make_locator(self._pages.CRS.verification_entry.view_indexed_section_title,
                                                  'GRANTEE'))

    def _check_rows_in_view_indexed_data_block(self, row_name, row_count=1):
        elms_in_block = self._general_helper.find_elements(
            self._general_helper.make_locator(self._pages.CRS.verification_entry.rekey_row_in_view_indexed_data,
                                              row_name))
        assert len(elms_in_block) == row_count, "Count of {} rows isn't equal {}, it is {}".format(row_name, row_count,
                                                                                                   len(elms_in_block))

    def copy_names(self, doc_year, doc_number, section):
        self._actions.click(
            self._general_helper.make_locator(self._pages.CRS.verification_entry.copy_names_link, section))
        self._actions.send_keys(self._pages.CRS.verification_entry.pup_copy_txt_recorded_year, doc_year)
        self._actions.send_keys(self._pages.CRS.verification_entry.pup_copy_txt_document_number, doc_number)
        self._actions.click(self._pages.CRS.verification_entry.copy_btn_in_copy_names_popup)

    def check_rekey_after_copy_names(self, data, section):
        doc_year = data['doc_year_for_copy_names']
        doc_number = data['doc_numb_for_copy_names']
        default_prop_type_name = data['config'].test_data(f"{data.OIT}.indexing.default_ptop_type")
        if section == 'Grantor':
            self.fill_party_names(data=data, grantee_section=True)
            self.copy_names(doc_year, doc_number, section)
            self._actions.wait(1)
            self._actions.focus_element(self._pages.CRS.indexing_entry.grantee_name_input)
        elif section == 'Grantee':
            self.fill_party_names(data=data, grantor_section=True)
            self.copy_names(doc_year, doc_number, section)
            self._actions.wait(1)
            self._actions.focus_element(self._pages.CRS.indexing_entry.grantor_name_input)
        else:
            assert 'Section name is incorrect, it should be as Grantor or Grantee'
        self._actions.wait_for_element_enabled(self._pages.CRS.verification_entry.pup_ReKey_warning_btn_no)
        self._actions.click(self._pages.CRS.verification_entry.pup_ReKey_warning_btn_no)
        self._actions.click(self._pages.CRS.verification_entry.pup_ReKey_Verification_rdb_restore_date)
        self._actions.click(self._pages.CRS.verification_entry.pup_ReKey_Verification_lnk_Save_Changes)
        self._actions.wait_for_element_not_present(
            self._pages.CRS.verification_entry.pup_ReKey_Verification_lnk_Return_to_Rekey)
        self._actions.focus_element(self._properties_dict[default_prop_type_name]['elm_to_check_rekey'])
        self._actions.focus_element(self._pages.CRS.indexing_entry.grantee_name_input)
        self._actions.wait(1)

    def process_rekey_and_send_to_indexing(self, data):
        self._actions.focus_element(self._pages.CRS.verification_entry.consideration_input)
        self._actions.wait(0.3)
        self._actions.focus_element(self._pages.CRS.indexing_entry.grantor_name_input)
        self._actions.wait(0.3)
        self._actions.focus_element(self._pages.CRS.indexing_entry.grantee_name_input)
        self._actions.wait(0.3)
        self._actions.focus_element(
            self._properties_dict[data['config'].test_data(f"{data.OIT}.indexing.default_ptop_type")][
                'elm_to_check_rekey'])
        self._actions.wait(0.3)
        self._actions.focus_element(self._pages.CRS.indexing_entry.grantee_name_input)
        self._actions.wait(0.3)
        self.send_document_to_indexing(reason='Re-Key test')
        self._actions.click(self._pages.CRS.verification_entry.btn_save_and_advance_verification_entry)

    def process_order_item_trough_verification_entry(self, data, fill_properties=False):
        if data.OIT == 'RP_Recordings':
            self.fill_doc_fields(data)
            self.fill_party_names(data, grantor_section=True, grantee_section=True)
            if fill_properties:
                IndexingEntry_functions.fill_property(step='verification')
            self._actions.focus_element(
                self._properties_dict[data['config'].test_data(f"{data.OIT}.indexing.default_ptop_type")][
                    'elm_to_check_rekey'])
            self._actions.focus_element(self._pages.CRS.indexing_entry.grantee_name_input)
        self.click_save_and_advance_button()
