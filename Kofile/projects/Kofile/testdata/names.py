from random import randint
from datetime import datetime, timedelta
from os import path

from projects.Kofile.Lib.general_helpers import GeneralHelpers
from projects.Kofile.testdata.printing_data import PrintData


class Names:
    printing_data = PrintData()

    def __init__(self, data):
        self.path = path
        mode_name = f"__{data['env']['code']}__"
        if hasattr(self, mode_name):
            getattr(self, mode_name).__call__()

    date_now = datetime.now()
    stamp = date_now.strftime("%d%m%Y_%S")

    OITNAMES = {
        "default": ["Acc_Payment"],
        "Order_header_account": ["Acc_Payment", "RP_Recordings_guest", "Acc_Payment"],
        "Add_to_order": ["Acc_Payment", "RP_Recordings_guest"],
        # "CS_CC_GOV": ["Certified Copy - GOV"],
        "rp": ["RP_Recordings_guest"],
        "ml": ["ML"],
        # "test": ["CCM"],
        "mb": ["MB"],
        "bcc": ["BCC"],
        "acc_payment": ["Acc_Payment"],
        "alc_Permit": ["Alc_Permit"],
        "manual_load_test": ["RP_Recordings_guest", "ML"],
        "an": ["AN"],
        "bcs": ["BCS"],
    }

    FIELDS_VALUE = {
        "Numbers": {
            "NoOfPage": [1, 5],
            'Payment': [1, 10],
            'NoOfCopies': [1, 5],
            'NoOfBrandLocations': [1, 5],
            'NoOfPassports': [1, 5],
            'NoOfPhotos': [1, 5],
            'NoOfLots': [1, 5],
            'No. Of Searches': [1, 5],
            'No. Of Pages': [1, 5],
            'NoOfNames': [1, 5],
            'ConsiderationAmount': [1, 10],
            'NumberOf': [1, 10]
        },

        "Strings": {
            'FirstName': [f'FName_{stamp}'],
            'Address1': ['Northern Ave'],
            'ZipCode': ['75424-2542'],
            'City': ['New York'],
            'DeathCity': ['New York'],
            'UnIncorporatedBusinessName': [f'TBusinessName_{stamp}'],
            'AddressName': ['TestAvenue'],
            'Name': ['TestOwnerName'],
            'LastName': [f'LName_{stamp}'],
            'DeathDate': ['01011910'],
            'IssueDate': ['01152020'],
            'DocNumber': ['150'],
            'AddressLine1': ['TestAddress1'],
            'BirthCity': ['TestCity'],
            'BirthDate': ['01151988'],
            'BirthCounty': ['TestCounty'],
            'DeathCounty': ['TestCounty'],
            'MarriageIDType': ['Test'],
            'ExpectedMarriageDate': ['01152020'],
            'RanchName': ['TestRanchName'],
            'DocRecordedYear': ['2019'],
            'IdentificationExpiry': [(date_now + timedelta(1)).strftime("%m%d%Y")],
            'Penalty': [],
            'AddressLine2': ['TestAddress2'],
            'IsCopyAddress': [],
            'ProtestFee': [],
            'ReturnByEmail': [],
            'MilitaryVeteranDiscount': [],
            'DateOfOriginalRecording': [],
            'RelationToDocumentApplicant': ['Test'],
            'Value': ['564878-7878'],
            'UnparsedProperty': ['Test'],
            'DischargeDate': ['01152020'],
            'RecordedDocNumber': ['150'],
            'UnparsedName': ['Test'],
            'InstrumentNumber': ['350'],
            'AmountOfBond': ['150'],
            'AmountOfClaim': ['100'],
            "EventDate": [(date_now - timedelta(1)).strftime("%m/%d/%Y")],
            "AnticipatedDate": [(date_now + timedelta(days=0)).strftime("%m/%d/%Y")],
            "EffectiveDate": [(date_now + timedelta(days=0)).strftime("%m/%d/%Y")],
            "ExpirationDate": [(date_now + timedelta(days=2)).strftime("%m/%d/%Y")],
            "DocRecordedDate": [GeneralHelpers.random_date(2020, 4, 10, True)],
            "MLApplicantsRelationship": ['ML Applicants Relationship'],
            "RecordedDate": [GeneralHelpers.random_date(2020, 4, 10, True)],
            "MarriedBy": ["MARRIAGE PERFORMED BY"],
            "CountyOfMarriage": ["COUNTY OF MARRIAGE"],
            "Email": ['test@volo.global'],
            'ParcelId': [f"{randint(100, 999)}-{randint(100, 999)}-{randint(100, 999)}-{randint(1000, 9999)}"],
            "DivorceCourtCaseNum": ["12"],
            "OwnerName": ["TestOwnerName"],
            "Number Of": "1",

            # PlaceHolder
            'SSN': ['654-54-5454'],
            'ID Type': ['test'],
            'Id Type and #': ['test'],
            'Amount': ['100A'],
            'Recorder Year': ['2019'],
            'Document Number': ['111'],
            'AffidavitApplicantName': ['AffidavitApplicantName'],
            "Unparsed": [GeneralHelpers.random_string(15)],
            "Volume": ["vol1"],
            "Book": ["12345"],
            "Page": ["678"],
            "County": ["County"],
            "CityTownZip": ["CityTownZip"],
            "DeathRecordBirthDate": ["01011900"],
            "CauseOfDeathA": ["Cause of Death A"],
            "MLApplicantsRelationship": ["Relationship"],
            # 'Refund to' fields
            "Phone": ["1234567890"],
            "Address": ["Refund to Address"],
            "Zip": ["789456123"],
            "NoOfLabels": ["5"],
            "NoOfPlusFree": ["1"],
            "eForm": {
                "email": "applicant{}@example.com",
                "phone": "{}000000000",
                "county": "county {}",
                "country": "country {}",
                "first_name": "applicant {} first name",
                "last_name": "applicant {} last name",
                "ssn": "{}00-00-0000",
                "ended_county": "Ended County {}",
                "ended_country": "Ended Country {}",
                "education": "{}0",
                "college": "{}+",
                "race": "Hispanic",
                "parent_name": "parent name {} {}",
                "surname_at_birth": "Surname at Birth {} {}",
                "parent_city": "city {} {}",
                "parent_county": "county {} {}",
                "parent_county_of_birth": "county of birth {} {}",
                "end_date": "04/00/2017"
            }
        }
    }

    ANY_DATA = {
        "void_comment_popup": "Automation test",
        "order_item_quantity": "1",
        "transaction_id": "1",
        "edit_no_of_pages": "1",
        "any_text": "Test",
        "package_id": "VoloAutoTest_2020-8-13-20-57-53-647",
        "fee_distribution_oit": "Account Payment"
    }

    KS_Cart_options = {
        "option_1": "Copy"
    }

    # image recognition
    # pytesseract_config = r"--oem 3 --psm 6"
    pytesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;\
            q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    # -----------------------------
    # note: this might be a solution for random values
    # to be further discussed
    # -----------------------------

    # TEST = {
    #     "my_random_value": randint,
    #     "my_random_min": 1,
    #     "my_random_max": 10
    # }
    # # demo code
    # print(names.TEST["my_random_value"](
    #     names.TEST["my_random_min"],
    #     names.TEST["my_random_max"]))

    internal_db = path.join(path.dirname(__file__), "internal.db")
    test_data_path = path.dirname(__file__)

    file_path = path.join(test_data_path, "Attachment_files")
    erProxy_file_path = path.join(test_data_path, "erProxy_Package")
    ocr_templates = path.join(test_data_path, "OCR_TEMPLATES")
    ocr_images = path.join(test_data_path, "OCR_IMAGES")
    scanned_images_path = path.join(test_data_path, "scanned_images")
    print_files = path.join(test_data_path, "Print_files")

    print_golden_files = path.join(print_files, "XXXXX_DrawerSummary_golden.pdf")
    print_rejection_golden_file = path.join(print_files, "XXXXX_RejectionRecording_golden.pdf")
    print_application_golden_file = path.join(print_files, "XXXXX_Marriage_License_Application_golden.pdf")
    print_certificate_golden_file = path.join(print_files, "XXXXX_Marriage_License_Certificate_golden.pdf")
    print_CoverPage_guest_golden_file = path.join(print_files, "XXXXX_CoverPage_guest_golden.pdf")
    print_CS_file = path.join(print_files, "XXXXX_CS.pdf")
    print_CoverPage_email_golden_file = path.join(print_files, "XXXXX_CoverPage_email_golden.pdf")
    print_CoverPage_edit_golden_file = path.join(print_files, "XXXXX_CoverPage_edit_golden.pdf")
    print_CoverPage_erProxy_golden_file = path.join(print_files, "XXXXX_CoverPage_erProxy_golden.pdf")
    print_CoverPage_return_mail_golden_file = path.join(print_files, "XXXXX_CoverPage_return_mail.pdf")
    print_Epson_Reciept_Adjusted_golden_file = path.join(print_files,
                                                         "XXXXX_EpsonRecieptPrinterConfig_Adjusted_copy_golden.txt")
    print_Epson_Reciept_Duplicate_golden_file = path.join(print_files,
                                                          "XXXXX_EpsonRecieptPrinterConfig_Duplicate_copy_golden.txt")
    print_Epson_Reciept_erProxy_golden_file = path.join(print_files,
                                                        "XXXXX_EpsonRecieptPrinterConfig_erProxy_golden.txt")
    print_Epson_Reciept_Original_golden_file = path.join(print_files,
                                                         "XXXXX_EpsonRecieptPrinterConfig_Original_golden.txt")
    print_Reciept_golden_file = path.join(print_files, "XXXXX_Receipt_golden.pdf")

    download_dir = path.join(path.expanduser("~"), "Downloads")

    path_to_PredefinedImagesConfig_xml = path.join(test_data_path, 'scanner', 'PredefinedImages',
                                                   'PredefinedImagesConfig.xml')

    tiff_file_path = path.join(test_data_path, 'scanner', 'PredefinedImages', 'testScanner.tiff')

    filename_for_deskew_test = '444.tiff'

    # print(datetime.now().strftime("%x_%X"))

    zero_price = "$0.00"
    scroll_js = 'arguments[0].scrollIntoView();'
    default_zip = '90001'

    printing_pattern = (
        {
            "data": "GenericReceipt_",
            "name": "GENERIC",
            "method": "download_and_compare_pdf_new"
        },
        {
            "data": "EpsonRecieptPrinterConfig_",
            "name": "EPSONRECIEPT",
            "method": "download_and_compare_txt_new"
        }
    )

    data_mapping = {
        "user_id": "rp_oit_workflow.005_get_customers_by_email",
        "address_id": "rp_oit_workflow.006_get_user_address_by_user_id",
        "order_id": "rp_oit_workflow.013_order_actions",
        "order_item_id": "rp_oit_workflow.013_order_actions",
        "order_number": "rp_oit_workflow.013_order_actions",
        "first_oit_id": "rp_oit_workflow.017_duplicate_order_item",
        "second_oit_id": "rp_oit_workflow.017_duplicate_order_item",
        "price": "rp_oit_workflow.022_check_out_order",
        "final_order_item_id": "rp_oit_workflow.024_show_order_finalization",
        "instrument_number": "rp_oit_workflow.024_show_order_finalization",
        "finalize_order": "rp_oit_workflow.023_post_action",
        "delete_oit": "rp_oit_workflow.018_delete_order_item",
        "scanner_id": "rp_oit_workflow.029_initiate_scan_session",
        "stop_scan": "rp_oit_workflow.030_stop_batch_scan",
        "document_id": "rp_oit_workflow.031_get_last_scanned_files",
        "azure_file_path": "rp_oit_workflow.031_get_last_scanned_files",
        "scan_date": "rp_oit_workflow.031_get_last_scanned_files",
        "document_saved": "rp_oit_workflow.033_save_documentItem_details",
        "indexing_task_id": "rp_oit_workflow.035_show_index_queue",
        "scan_complete": "rp_oit_workflow.034_save_batch_scan",
        "dm_id": "rp_oit_workflow.036_indexing_task_entry",
        "order_item_saved_in_indexing": "rp_oit_workflow.038_order_actions_indexing",
        "order_indexed": "rp_oit_workflow.041_process_indexing_task_and_pickup_the_next_one",
        "verification_task_id": "rp_oit_workflow.042_show_verification_queue",
        "order_item_saved_in_verification": "rp_oit_workflow.045_order_actions_verification",
        "order_in_archive": "rp_oit_workflow.048_process_verification_task_and_pickup_the_next_one",
        "company_account_id": "front_office_workflow.003_get_company_accounts_search_result",
        "company_account_name": "front_office_workflow.003_get_company_accounts_search_result",
        "company_account_code": "front_office_workflow.003_get_company_accounts_search_result",
        "company_account_user_id": "front_office_workflow.006_get_free_users",
        "company_account_user_email": "front_office_workflow.006_get_free_users",
        "company_account_user_removed": "front_office_workflow.005_save_company_account",
        "type_and_head_record_id": "front_office_workflow.008_get_all_party_names",
        "last_row_data": "order_search.003_get_order_search_result_search_by_date_range",
        "location_ids": "order_search.003_get_order_search_result_search_by_date_range",
        "department_ids": "order_search.003_get_order_search_result_search_by_date_range",
        "origin_ids": "order_search.003_get_order_search_result_search_by_date_range",
        "assigned_to": "order_search.003_get_order_search_result_search_by_date_range",
        "order_payment_type_ids": "order_search.003_get_order_search_result_search_by_date_range",
        "row_with_doc_number": "order_search.002_get_order_search_result_search_all",
        "row_with_department": "order_search.002_get_order_search_result_search_all",
        "package_row_data": "order_search.013_get_order_package_search_result_search_all",
        "an_url": "portal.001_index_page",
        "portal_order_number": "portal.003_create_an_order",
        "portal_order_id": "portal.004_find_new_order_in_order_queue",
        "portal_package_id": "portal.004_find_new_order_in_order_queue",
        "portal_order_item_id": "portal.005_get_order_summary",
        "portal_order_item_type_id": "portal.005_get_order_summary",
        "portal_order_price": "portal.007_order_acton",
        "portal_scanner_id": "portal.009_initiate_scan_session",
        "portal_doc_number": "portal.008_checkout_order",
        "portal_document_id": "portal.010_get_last_scanned_files",
        "portal_azure_file_path": "portal.010_get_last_scanned_files",
        "portal_scan_date": "portal.010_get_last_scanned_files",
        "portal_document_saved": "portal.011_save_documentItem_details",
        "portal_scan_complete": "portal.012_save_batch_scan",
        "portal_indexing_task_id": "portal.013_show_index_queue",
        "portal_dm_id": "portal.014_indexing_task_entry",
        "portal_order_item_saved_in_indexing": "portal.015_order_actions_indexing",
        "portal_order_indexed": "portal.016_process_indexing_task_and_pickup_the_next_one",
        "portal_verification_task_id": "portal.017_show_verification_queue",
        "cs_rp_doc_groups": "clerc_search.property_records.001_open_rp_index_page",
        "cs_rp_party_names": "clerc_search.property_records.001_open_rp_index_page",
        "cs_rp_search_fields": "clerc_search.property_records.001_open_rp_index_page",
        "copy_first_rp_order": "clerc_search.property_records.002_search_rp_by_data_range",
        "certified_copy_first_rp_order": "clerc_search.property_records.002_search_rp_by_data_range",
        "re_capture_first_rp_order": "clerc_search.property_records.002_search_rp_by_data_range",
        "re_index_first_rp_order": "clerc_search.property_records.002_search_rp_by_data_range",
        "cs_first_rp_order": "clerc_search.property_records.002_search_rp_by_data_range",
        "cs_inbox_clear": "clerc_search.property_records.003_clear_inbox",
        "cs_order_in_inbox": "clerc_search.property_records.004_add_to_inbox",
        "cs_copy_order_number": "clerc_search.property_records.006_submit_inbox_copy",
        "cs_certified_copy_order_number": "clerc_search.property_records.007_submit_inbox_certified_copy",
        "cs_re_index_order_number": "clerc_search.property_records.009_submit_inbox_re_index",
        "cs_re_capture_order_number": "clerc_search.property_records.008_submit_inbox_re_capture",
        "cs_re_index_indexing_task_id": "clerc_search.property_records.010_show_index_queue_re_index_order",
        "cs_re_index_order_id": "clerc_search.property_records.010_show_index_queue_re_index_order",
        "cs_re_index_indexing_status_id": "clerc_search.property_records.010_show_index_queue_re_index_order",
        "re_index_order_dm_id": "clerc_search.property_records.011_indexing_task_entry_re_index_order",
        "re_index_order_item_id": "clerc_search.property_records.011_indexing_task_entry_re_index_order",
        "re_index_order_item_type_id": "clerc_search.property_records.011_indexing_task_entry_re_index_order",
        "re_index_order_type_id": "clerc_search.property_records.011_indexing_task_entry_re_index_order",
        "re_index_order_doc_type_id": "clerc_search.property_records.011_indexing_task_entry_re_index_order",
        "re_index_order_item_saved_in_indexing": "clerc_search.property_records.012_order_actions_indexing_re_index_order",
        "re_capture_capture_task_id": "clerc_search.property_records.014_show_capture_queue_re_capture",
        "re_capture_status": "clerc_search.property_records.014_show_capture_queue_re_capture",
        "re_capture_doc_number": "clerc_search.property_records.014_show_capture_queue_re_capture",
        "re_capture_order_id": "clerc_search.property_records.015_open_capture_summary_page",
        "re_capture_document_id": "clerc_search.property_records.015_open_capture_summary_page",
        "re_capture_order_item_id": "clerc_search.property_records.015_open_capture_summary_page",
        "re_capture_order_item_type_id": "clerc_search.property_records.015_open_capture_summary_page",
        "re_capture_order_year": "clerc_search.property_records.015_open_capture_summary_page",
        "re_capture_doc_type": "clerc_search.property_records.015_open_capture_summary_page",
        "re_capture_doc_group": "clerc_search.property_records.015_open_capture_summary_page",
        "re_capture_pages": "clerc_search.property_records.015_open_capture_summary_page",
        "re_capture_scanned": "clerc_search.property_records.015_open_capture_summary_page",
        "re_capture_initial_batch_items": "clerc_search.property_records.015_open_capture_summary_page",
        "re_capture_scan_task_id": "clerc_search.property_records.015_open_capture_summary_page",
        "re_capture_recorded_year": "clerc_search.property_records.015_open_capture_summary_page",
        "re_capture_is_scanned": "clerc_search.property_records.016_initiate_scan_session_re_capture",
        "re_capture_azure_file_path": "clerc_search.property_records.017_get_last_scanned_files_re_capture",
        "re_capture_scan_date": "clerc_search.property_records.017_get_last_scanned_files_re_capture",
        "re_capture_document_saved": "clerc_search.property_records.018_save_documentItem_details_re_capture",
        "copy_order_status_id": "clerc_search.property_records.020_show_order_queue_copy",
        "copy_order_id": "clerc_search.property_records.020_show_order_queue_copy",
        "copy_package_id": "clerc_search.property_records.020_show_order_queue_copy",
        "copy_order_item_id": "clerc_search.property_records.021_get_order_summary_copy",
        "copy_order_item_type_id": "clerc_search.property_records.021_get_order_summary_copy",
        "copy_order_price": "clerc_search.property_records.021_get_order_summary_copy",
        "certified_copy_order_id": "clerc_search.property_records.023_show_order_queue_certified_copy",
        "certified_copy_order_status_id": "clerc_search.property_records.023_show_order_queue_certified_copy",
        "certified_copy_package_id": "clerc_search.property_records.023_show_order_queue_certified_copy",
        "certified_copy_order_item_id": "clerc_search.property_records.024_get_order_summary_certified_copy",
        "certified_copy_order_item_type_id": "clerc_search.property_records.024_get_order_summary_certified_copy",
        "certified_copy_order_price": "clerc_search.property_records.024_get_order_summary_certified_copy",
        "cs_an_party_names": "clerc_search.assumed_names.001_open_an_index_page",
        "cs_an_search_fields": "clerc_search.assumed_names.001_open_an_index_page",
        "cs_fl_search_fields": "clerc_search.foreclosures.001_open_fl_index_page",
        "cs_ml_party_names": "clerc_search.marriage_licenses.001_open_ml_index_page",
        "cs_ml_search_fields": "clerc_search.marriage_licenses.001_open_ml_index_page",
        "cs_br_party_names": "clerc_search.birth_records.001_open_br_index_page",
        "cs_br_search_fields": "clerc_search.birth_records.001_open_br_index_page",
        "cs_dr_party_names": "clerc_search.death_records.001_open_dr_index_page",
        "cs_dr_search_fields": "clerc_search.death_records.001_open_dr_index_page",
        "search_by_order_number": "order_search.005_get_order_search_result_search_by_order_number",
    }
