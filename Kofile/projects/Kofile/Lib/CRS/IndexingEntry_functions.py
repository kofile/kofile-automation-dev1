from datetime import date as dt

import re
from projects.Kofile.Lib.Image_Recognition import ImageRecognition
from projects.Kofile.Lib.CRS.OrderEntry_functions import OrderEntry
from projects.Kofile.Lib.CRS.Capture_functions import Capture
from projects.Kofile.Lib.DB import DB, DataBaseWithVPN
from projects.Kofile.Lib.test_parent import LibParent

capture = Capture()
fill_reason_popup, get_order_status = capture.fill_reason_popup, capture.get_order_status
OrderEntry_functions = OrderEntry()


class IndexingEntry(LibParent):

    def __init__(self):
        super(IndexingEntry, self).__init__()

    def __48999__(self):
        self.get_parties_locators = self.get_parties_locators_loc_2

    def click_birth_death_record_save_button(self):
        self._general_helper.scroll_and_click(self._pages.CRS.indexing_entry.sumbit_block)
        # self._actions.wait_for_element_enabled(self._pages.CRS.indexing_queue.btn_birth_death_record_save)
        self._general_helper.wait_and_click(self._pages.CRS.indexing_entry.btn_birth_death_record_save, scroll=True,
                                            enabled=True)
        self._general_helper.wait_for_spinner()

    def fill_recorded_date(self, date=dt.today().strftime(r"%m/%d/%Y")):
        self._general_helper.find_and_send_keys(self._pages.CRS.indexing_entry.txt_recorded_date, date) \
            .send_keys(self._keys.TAB)

    def fill_doc_number(self, doc_number: str):
        self._general_helper.find_and_send_keys(self._pages.CRS.indexing_entry.txt_doc_number, doc_number)

    def check_exist_grantor_and_grantee_type_and_head(self, should_exist=True):
        data = self._general_helper.get_data()
        account_name = data.config.order_header_fill(f'{data.orderheader}.value').lower()
        self._general_helper.find_and_send_keys(self._pages.CRS.indexing_entry.grantor_name_input, account_name)
        status = self._general_helper.check_if_element_exists(
            self._pages.CRS.front_office.ddl_nta_party_name_lbl_by_name(account_name), 10)
        assert status if should_exist else not status, f"Grantor type and head{' not' if should_exist else ''} exist"
        self._general_helper.find_and_send_keys(self._pages.CRS.indexing_entry.grantor_name_input, 'test')
        self._actions.wait(1)
        self._actions.focus_element(self._pages.CRS.indexing_entry.grantee_name_input)
        if 'reenter_grantor' in data['config'].test_data(f"{data.OIT}.verification.reentry").keys():
            self._general_helper.scroll_and_click(
                self._pages.CRS.verification_entry.pup_ReKey_Verification_rdb_save_rekey_date)
            self._general_helper.scroll_and_click(
                self._pages.CRS.verification_entry.pup_ReKey_Verification_lnk_Save_Changes)
        self._general_helper.find_and_send_keys(self._pages.CRS.indexing_entry.grantee_name_input, account_name)
        status = self._general_helper.check_if_element_exists(
            self._pages.CRS.front_office.ddl_nta_party_name_lbl_by_name(account_name), 10)
        assert status if should_exist else not status, f"Grantee type and head{' not' if should_exist else ''} exist"
        self._general_helper.find_and_send_keys(self._pages.CRS.indexing_entry.grantee_name_input, 'test')

    def send_to_administrator(self, expected_status="AdminSuspend"):
        self._general_helper.scroll_and_click(self._pages.CRS.indexing_summary.lnk_Send_to_administrator)
        status = fill_reason_popup("/ShowIndexQueue")
        assert status == expected_status, f"Incorrect order[{self._general_helper.get_data()['order_number']}] status" \
                                          f" after 'Send to Administrator':\n" \
                                          f"Expected: '{expected_status}' but actual: '{status}'"

    def save_order(self, expected_status="Suspended"):
        self._general_helper.scroll_and_click(self._pages.CRS.indexing_summary.btn_save_order)
        status = fill_reason_popup("/ShowIndexQueue")
        assert status == expected_status, f"Incorrect order[{self._general_helper.get_data()['order_number']}] status" \
                                          f" after 'Send to Administrator':\n" \
                                          f"Expected: '{expected_status}' but actual: '{status}'"

    def return_to_indexing_queue(self, expected_status="In Process"):
        self._general_helper.find_and_click(self._pages.CRS.indexing_summary.lnk_Return_to_indexing_queue)
        data = self._general_helper.get_data()
        order_number = data["order_number"]
        status = get_order_status()
        assert status == expected_status, f"Incorrect order[{self._general_helper.get_data()['order_number']}] status" \
                                          f" after 'Send to Administrator':\n" \
                                          f"Expected: '{expected_status}' but actual: '{status}'"
        user = data.get("env").get("user")[data.get("user_index", 0)]
        username = f"{user} {user}".lower()
        assign_user = self._general_helper.find(
            self._pages.CRS.general.assigned_to_by_order_number_text_in_indexing(order_number)).get_attribute(
            "data-value").lower()
        assert assign_user == username, f"Assign user not equals, got {assign_user} but should be {username}"

    def copy_names_by_doc_num(self):
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_copy_names)
        self._actions.wait_for_element_displayed(self._pages.CRS.order_entry.copy_names_popup)
        data = self._general_helper.get_data()
        elements_count = len(self._general_helper.find_elements(self._pages.CRS.indexing_entry.grantor_name_input))
        doc_type = self._actions.get_element_text(self._pages.CRS.verification_entry.lbl_header_doc_type)
        # fill grantor name fields if they are empty
        for grantor_name_el in self._general_helper.find_elements(self._pages.CRS.indexing_entry.grantor_name_input):
            if grantor_name_el.get_attribute("value") == "":
                self._actions.send_keys(grantor_name_el, 'Test')
        with DB(data) as db:
            year, doc_num = db.get_exist_doc_number_and_year_by_department_with_parties(doc_type)
        self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.inp_copy_names__recorded_year, year)
        self._general_helper.find_and_send_keys(self._pages.CRS.order_entry.inp_copy_names__doc_number, doc_num)
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_copy_names__copy)
        new_elements = list()
        for _ in range(30):
            new_elements = self._general_helper.find_elements(self._pages.CRS.indexing_entry.grantor_name_input)
            if elements_count < len(new_elements):
                break
            self._actions.wait(1)
        assert elements_count < len(new_elements), "copy not add grantor"
        for element in new_elements:
            assert element.get_attribute("value").strip() != "", "blank grantor field"

    def copy_names_by_vol_page(self):
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_copy_names)
        self._actions.wait_for_element_displayed(self._pages.CRS.order_entry.copy_names_popup)
        data = self._general_helper.get_data()
        elements_count = len(self._general_helper.find_elements(self._pages.CRS.indexing_entry.grantor_name_input))
        with DB(data) as db:
            vol, page = db.get_exist_doc_vol_and_page_by_department()
        self._general_helper.find_and_send_keys(self._pages.CRS.indexing_entry.pup_copy_txt_volume, vol)
        self._general_helper.find_and_send_keys(self._pages.CRS.indexing_entry.pup_copy_txt_page, page)
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_copy_names__copy)
        if self._general_helper.check_if_element_exists(self._pages.CRS.verification_entry.pup_choose_document):
            self._actions.click(self._pages.CRS.verification_entry.pup_choose_document)
            self._actions.wait_for_element_enabled(self._pages.CRS.verification_entry.btn_choose_from_pup_choose_doc)
            self._general_helper.find_and_click(self._pages.CRS.verification_entry.btn_choose_from_pup_choose_doc)
        new_elements = list()
        for _ in range(30):
            new_elements = self._general_helper.find_elements(self._pages.CRS.indexing_entry.grantor_name_input)
            if elements_count < len(new_elements):
                break
            self._actions.wait(1)
        assert elements_count < len(new_elements), "copy not add grantor"
        for element in new_elements:
            assert element.get_attribute("value").strip() != "", "blank grantor field"

    def copy_names_from_prior_document(self, v):
        self._general_helper.scroll_and_click(self._pages.CRS.order_entry.btn_copy_names)
        self._actions.wait_for_element_displayed(self._pages.CRS.order_entry.copy_names_popup)
        self._general_helper.find_and_click(self._pages.CRS.indexing_entry.pup_copy_names_lnk_copy)
        for _ in range(30):
            value = self._actions.get_element_value(self._pages.CRS.indexing_entry.grantor_name_input)
            if value == v:
                break
            self._actions.wait(1)
        assert self._actions.get_element_value(
            self._pages.CRS.indexing_entry.grantor_name_input).lower() == v.lower()

    def revert_names(self):
        self._general_helper.find_and_send_keys(self._pages.CRS.indexing_entry.grantor_name_input, "TEST_1")
        self._general_helper.find_and_send_keys(self._pages.CRS.indexing_entry.grantee_name_input, "TEST_2")
        self._general_helper.find_and_click(self._pages.CRS.order_entry.btn_reverse_parties)
        self._actions.assert_element_value(self._pages.CRS.indexing_entry.grantor_name_input, "TEST_2")
        self._actions.assert_element_value(self._pages.CRS.indexing_entry.grantee_name_input, "TEST_1")

    def set_reference_document(self):
        data = self._general_helper.get_data()
        with DB(data) as db:
            year, doc_num = db.get_exist_doc_number_and_year_by_department()
        self._general_helper.find_and_send_keys(self._pages.CRS.indexing_entry.referer_year, year)
        self._general_helper.find_and_send_keys(self._pages.CRS.indexing_entry.referer_doc_num,
                                                doc_num + self._keys.TAB)
        self._actions.wait_for_element_present(self._pages.CRS.indexing_entry.ref_volpage_block)
        self._actions.wait_for_element_displayed(self._pages.CRS.indexing_entry.ref_volpage_block)
        self._actions.wait_for_element_text_contains(self._pages.CRS.indexing_entry.ref_volpage_block, "Vol/Page")
        data = self._general_helper.find(self._pages.CRS.indexing_entry.ref_volpage_block, get_text=True)
        assert re.findall(r"Vol/Page (\w|\d)+/(\w|\d)+", data), "cant find volume and page in result"

    def set_reference_document_by_vol_and_page(self):
        data = self._general_helper.get_data()
        with DB(data) as db:
            vol, page = db.get_exist_doc_vol_and_page_by_department()
        self._general_helper.find_and_send_keys(self._pages.CRS.indexing_entry.referer_volume, vol)
        self._general_helper.find_and_send_keys(self._pages.CRS.indexing_entry.referer_page, page + self._keys.TAB)
        if self._general_helper.check_if_element_exists(self._pages.CRS.verification_entry.pup_choose_document):
            self._actions.click(self._pages.CRS.verification_entry.pup_choose_document)
            self._actions.wait_for_element_enabled(self._pages.CRS.verification_entry.btn_choose_from_pup_choose_doc)
            self._general_helper.find_and_click(self._pages.CRS.verification_entry.btn_choose_from_pup_choose_doc)
        self._actions.wait_for_element_present(self._pages.CRS.indexing_entry.ref_doc_num_res)
        self._actions.wait_for_element_displayed(self._pages.CRS.indexing_entry.ref_doc_num_res)
        self._actions.wait_for_element_text_contains(self._pages.CRS.indexing_entry.ref_doc_num_res, "Doc#")
        data = self._general_helper.find(self._pages.CRS.indexing_entry.ref_doc_num_res, get_text=True)
        assert re.findall(r"Doc# \w+-\w+", data), "cant find doc number in result"

    def click_to_zoom(self):
        self._general_helper.find_and_click(self._pages.CRS.indexing_entry.zoom_btn)
        self._actions.wait_for_element_displayed(self._pages.CRS.indexing_entry.flip_names_first_grantor_cb)

    def flip_party_names(self, name="AUTOMATION TEST", flip_again=True):
        rev_name = " ".join(reversed(name.split(" ")))
        self.click_to_zoom()
        self._general_helper.find_and_send_keys(self._pages.CRS.indexing_entry.grantor_name_input, name)
        self._general_helper.find_and_check_uncheck_checkbox(self._pages.CRS.indexing_entry.flip_names_first_grantor_cb,
                                                             True)
        self._general_helper.wait_attribute_in_element(self._pages.CRS.indexing_entry.grantor_name_input, rev_name)
        if flip_again:
            self._general_helper.find_and_check_uncheck_checkbox(
                self._pages.CRS.indexing_entry.flip_names_first_grantor_cb,
                False)
            self._general_helper.wait_attribute_in_element(self._pages.CRS.indexing_entry.grantor_name_input, name)

        self._general_helper.find_and_send_keys(self._pages.CRS.indexing_entry.grantee_name_input, name)
        self._general_helper.find_and_check_uncheck_checkbox(self._pages.CRS.indexing_entry.flip_names_first_grantee_cb,
                                                             True)
        self._actions.assert_element_value(self._pages.CRS.indexing_entry.grantee_name_input, rev_name)
        self._general_helper.wait_attribute_in_element(self._pages.CRS.indexing_entry.grantee_name_input, rev_name)
        self._general_helper.find_and_check_uncheck_checkbox(self._pages.CRS.indexing_entry.flip_names_first_grantee_cb,
                                                             False)
        if flip_again:
            self._actions.assert_element_value(self._pages.CRS.indexing_entry.grantee_name_input, name)
            self._general_helper.wait_attribute_in_element(self._pages.CRS.indexing_entry.grantee_name_input, name)

    def check_names(self, name, separator="&", grantor=True):
        split_name = name.split(f" {separator} ")
        inp = self._pages.CRS.indexing_entry.grantor_name_input if \
            grantor else self._pages.CRS.indexing_entry.grantee_name_input
        cb = self._pages.CRS.indexing_entry.split_names_first_grantor_cb if \
            grantor else self._pages.CRS.indexing_entry.split_names_first_grantee_cb
        self._general_helper.find_and_send_keys(inp, name)
        self._general_helper.wait_attribute_in_element(inp, name)
        self._general_helper.find_and_check_uncheck_checkbox(cb, True)
        self._general_helper.wait_for_element_condition(inp, lambda el: len(el) > 1, many=True)
        for a, element in enumerate(self._general_helper.find_elements(inp)):
            if a < len(split_name):
                self._actions.assert_equals(element.get_attribute("value"), split_name[a])

    def split_party_names(self):
        name, name2 = "AUTOMATION & TEST", "AUTOMATION AND TEST"
        sep, sep2 = "&", "AND"
        self.click_to_zoom()
        self.check_names(name)
        self._general_helper.find_and_click(self._pages.CRS.indexing_entry.split_names_first_grantor_cb)
        self._general_helper.wait_attribute_in_element(self._pages.CRS.indexing_entry.grantor_name_input, name)
        self.check_names(name2, separator="AND")
        self._general_helper.find_and_click(self._pages.CRS.indexing_entry.split_names_first_grantor_cb)
        self._general_helper.wait_attribute_in_element(self._pages.CRS.indexing_entry.grantor_name_input,
                                                       name2.replace(sep2, sep))
        self.check_names(name, grantor=False)
        self._general_helper.find_and_click(self._pages.CRS.indexing_entry.split_names_first_grantee_cb)
        self._general_helper.wait_attribute_in_element(self._pages.CRS.indexing_entry.grantee_name_input, name)
        self.check_names(name2, separator="AND", grantor=False)
        self._general_helper.find_and_click(self._pages.CRS.indexing_entry.split_names_first_grantee_cb)
        self._general_helper.wait_attribute_in_element(self._pages.CRS.indexing_entry.grantee_name_input,
                                                       name2.replace(sep2, sep))

    def fill_property(self, step, add_spaces=False):
        """
        Fills indicated property, if count of indicated properties already added on the page, just
         fills property's fields,
        otherwise add a new one indicated property type.

        Required parameters is prop_type:str.
        By the prop_type the function takes data like as locators, or uniq functions from the _properties_dict
        and number of required properties. For example prop_type = 'subdivision-1|survey-2|description-3',
        so it will be added
        one subdivision two survey and three descriptions.
        """
        data = self._general_helper.get_data()
        prop_types = data['config'].test_data(f"{data.OIT}.indexing.property").keys()
        if step == 'indexing':
            # Add new property _types
            new_property_links = self._general_helper.find_elements(
                self._pages.CRS.indexing_entry.property_types_new_links)

            for new_property_link in new_property_links:
                self._general_helper.scroll_into_view(self._pages.CRS.indexing_entry.btn_save_and_advance)
                self._actions.click(new_property_link)
            # Delete default property row, for avoid duplication
            property_delete_icon = self._general_helper.make_locator(
                self._pages.CRS.indexing_entry.property_types_delete_icon_by_row, 1)
            self._general_helper.scroll_into_view(property_delete_icon)
            self._general_helper.find_and_click(property_delete_icon)

            # self._general_helper.scroll_and_click(new_property_link)
        for prop_type in prop_types:
            field_names = data['config'].test_data(f"{data.OIT}.indexing.property.{prop_type}")
            for field_name in field_names:
                field_loc = self._pages.CRS.indexing_entry.property_field_locator(prop_type, field_name)
                if field_name == 'Legal Description / Remarks':
                    field_name = 'LegalDescriptionRemarks'
                if field_name == 'Govt Lot':
                    field_name = 'GovtLot'
                field_content = data['config'].test_data(f"{data.OIT}.indexing.prop_values.{field_name}")
                if field_content:
                    self._general_helper.find_and_send_keys(field_loc,
                                                            f"  {field_content}   " if add_spaces else field_content)
                if prop_type == 'subdivision' and field_name == 'Subdivision':
                    self._actions.send_keys(field_loc, self._keys.TAB)
                    self._general_helper.find_and_click(
                        self._pages.CRS.indexing_entry.pup_returen_address_warning_btn_yes,
                        timeout=5,
                        should_exist=False)

    def upload_birth_death_image(self, data):
        """image folder is pre-stored in data['folder']"""
        self.click_on_upload_button()
        self._general_helper.scroll_and_click(
            self._general_helper.make_locator(self._pages.CRS.indexing_entry._pup_choose_image_folder_by_foldername,
                                              data["folder"]), wait_displayed=False)
        self._general_helper.scroll_and_click(
            self._general_helper.make_locator(self._pages.CRS.indexing_entry._pup_choose_image_by_foldername,
                                              data["folder"]))
        self._general_helper.wait_for_spinner()
        self._general_helper.scroll_and_click(self._pages.CRS.indexing_entry.pup_choose_image_btn_upload)
        self._general_helper.wait_for_spinner()

    def click_on_upload_button(self):
        self._general_helper.find_and_click(self._pages.CRS.indexing_entry.icn_birth_death_record_upload)
        self._actions.wait_for_element_displayed(self._pages.CRS.indexing_entry.pup_choose_image_btn_upload)

    def verify_attachment(self, expected_filename):
        self._general_helper.find_and_click(OrderEntry_functions.tab_locator('Attachments'))
        actual_filename = self._general_helper.find(self._pages.CRS.edit_order_item.lbl_attached_filename,
                                                    get_text=True)
        assert actual_filename == expected_filename, f"Attachment expected filename {expected_filename} is " \
                                                     f"NOT equal to actual {actual_filename}."

    def upload_birth_record_file(self, data):
        self._general_helper.find_and_click(self._pages.CRS.indexing_entry.icn_birth_death_record_upload)
        container = self._pages.CRS.indexing_entry.birth_folder(
            data.config.config_file.OITs[data["OIT"]]["indexing"]["birth_upload_image_folder"])
        if not self._general_helper.find(container, timeout=15, should_exist=False):
            self._general_helper.find_and_click(self._pages.CRS.indexing_entry.pup_choose_image_btn_cancel)
            DataBaseWithVPN(data).add_files_in_upload_folder()
            self._general_helper.find_and_click(self._pages.CRS.indexing_entry.icn_birth_death_record_upload)
        self._general_helper.find_and_click(self._pages.CRS.indexing_entry.birth_folder(
            data.config.config_file.OITs[data["OIT"]]["indexing"]["birth_upload_image_folder"]))
        self._general_helper.find_and_click(self._pages.CRS.indexing_entry.first_doc_in_search)
        ir = ImageRecognition()
        ir.check_uploaded_image(self._pages.CRS.indexing_entry.preview_content, "Preview not display image",
                                matrix="grey")
        self._general_helper.find_and_click(self._pages.CRS.indexing_entry.pup_choose_image_btn_upload)
        self._actions.wait_for_element_displayed(self._pages.CRS.image_viewer.single_image_viewer_container)
        ir.check_uploaded_image(self._pages.CRS.image_viewer.single_image_viewer_container,
                                "Uploaded file not display image", matrix="grey")

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

    def store_party_names(self, data):
        party_name = data['config'].test_data(f"{data.OIT}.indexing.party_name")
        self._actions.store('grantor_names',
                            {f_name: [_.get_attribute("value") for _ in self._general_helper.find_elements(
                                self.get_parties_locators(f_name)[0])] for f_name
                             in
                             party_name})
        self._actions.store('grantee_names',
                            {f_name: [_.get_attribute("value") for _ in self._general_helper.find_elements(
                                self.get_parties_locators(f_name)[1])] for f_name
                             in
                             party_name})

    def store_documents_grids(self):
        data = self._general_helper.get_data()
        if 'DOCUMENT' in data['config'].test_data(f"{data.OIT}.indexing.doc_fields"):
            self._actions.store('doc_type',
                                self._general_helper.find(
                                    self._pages.CRS.indexing_entry.doc_type_select).select.first_selected_option.text)
        if 'Volume' in data['config'].test_data(f"{data.OIT}.indexing.doc_fields"):
            self._actions.store('doc_liber',
                                self._actions.get_element_value(self._pages.CRS.indexing_entry.liber_input))
        if 'Page' in data['config'].test_data(f"{data.OIT}.indexing.doc_fields"):
            self._actions.store('doc_page', self._actions.get_element_value(self._pages.CRS.indexing_entry.page_input))
        if 'Consideration Amount' in data['config'].test_data(f"{data.OIT}.indexing.doc_fields"):
            self._actions.store('consideration',
                                self._actions.get_element_value(self._pages.CRS.indexing_entry.consideration_input))
