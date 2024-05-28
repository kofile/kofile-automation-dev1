"""
development tenant (48999) location 2 test data
"""

DRAWER = {
    # possible values for type:
    # 'auto' - automatically initialized when clicking on New Order + button,
    # 'manual'- popup after clicking on New Order + button,
    # 'init'- through Initialize Drawer tab
    "type": "manual"
}

ORDER_HEADER = {
    "account": {
        "type": "account",
        "value": "SIMPLIFILE - kofiletestautomation@gmail.com",
    },
    "email": {
        "type": "email",
        "value": "test@gmail.com",
    },
    "guest": {
        "type": "guest",
        "value": "VoloAutomationTest",
    },

    "er_proxy_account_name_password": {
        "name": "VoloAutoTest",
        "pass": "VoloAutoTest"
    },
    "address": {
        "address": "PO BOX 1001",
        "zip": "75021",
        "city": "DENISON",
        "state": "TX"
    }
}

OITs = {
    "Default": {
        "order_type": "Real Property Recordings W/Page",
        "order_doc_type": "MISCELLANEOUS",
        "doc_type": True,
        "doc_group": "REAL PROPERTY",
        "default_doc_type": "",
        "order_item_description": {
            "value": "$26.00, $4.00/page after 1st, $0.25/name after 5th, Optional Penalty"
        },
        "order_summary": {
            "year_on_order_summary": False,
            "doc_number_on_order_summary": False,
            "serial_number": False,
            "save_prop_address": False,
            "use_row_checkbox": False
        },
        "discount": {
            "show": False,
            "value": ["100%", "RA"]
        },
        "finalization": {
            "with_payment": True,
            "void_with_payment": True,
            "void_report_radiobutton": True,
            "payment_method": "Cash",
            "payment_method_account": "Company Account",
            "transaction_id": "TRID",
            "comment_on_payment": "comment",
            "finalization_status": "Finalized",
            "year_on_order_finalization": True,
            "doc_number_on_order_finalization": True

        },
        "fund_distribution": [
            {
                "fund_label": "Records Management",
                "value": "$ 10.00",
                "RA": False

            },
            {
                "fund_label": "Records Archive Fee",
                "value": "$ 10.00",
                "RA": True
            },
            {
                "fund_label": "Courthouse Security",
                "value": "$ 1.00",
                "RA": False
            },
            {
                "fund_label": "Recording Fees",
                "value": "100%",
                "RA": False
            },
        ],
        "payment_methods": {
            "value": ["Company Account", "Cash", "Check", "VitalChek",
                      "Money Order", "Cashiers Check", "LegalEase", "Over/Short"],

            "processing_fee": {
                "by_range": False,
                "ranges": {"1-50": 1.75, "50.01-75": 2},
                "fix_amount": True,
                "amount": 5,
                "by_percentage": False,
                "percent": 2,
                "no_fee": True

            }
        },
        "capture": {
            "step": False,
            "expanded_indexing": False,
            "capture_review": False,
            "upload_image": {
                "value": False,
                "folder": "Auto_Plats"
            },
            "start_from_capture": {
                "value": False
            }
        },
        "indexing": {
            "step": False,
            "indexing_type": "self",
            "first_page_to_last_page": False
        },
        "verification": {
            "step": False,
            "rekey": False,
            "reenter_property": False
        },
        "image_viewer": {
            "restore_secured_document": False
        },
    },

    "Real_Property_Recordings_W_Page": {
        "per_page_fee": "4.00",
        "non_fee_pages": "1",
        "per_name_fee": "0.25",
        "non_fee_names": "5",
        "missing_grantee_addresses_fee": "25.0",
        "payment_methods": {
            "value": ["Company Account", "Cash", "Check", "Credit Card",
                      "Money Order", "Direct Deposit"]
        },
        "capture": {
            "step": True
        },
        "indexing": {
            "step": True,
            "first_page_to_last_page": True,
            "doc_fields": ["DOCUMENT", "Instrument Date"],
            "party_name": ["Name"],
            "property": {
                "newdesc": ['Legal Description / Remarks'],
                "subdivision": ["Subdivision", "Lot", "Block", "Unit", "Volume", "Page"],
                "survey": ["Abstract", "Block", "Survey", "Township", "Section", "Tract", "Acres"],

            },
            "default_ptop_type": "newdesc",
            "prop_values": {
                "LegalDescriptionRemarks": "new_desc",
                "Township": "Kofile Township 002N 317W",
                "Subdivision": "SINGLE LOT",
                "Lot": "Lot1",
                "Block": "Block1",
                "Volume": "Volume1",
                "Page": "P123",
                "Remarks": "Some remark",
                "Abstract": "Abstr1",
                "Survey": "Survey1",
                "Section": "12",
                "Tract": "Tract1",
                "Acres": "10",
                "Condominium": "CONDOMINIUM NAME",
                "Unit": "Unit1",
                "Building": "Building1",
                "Half": "E",
                "Quarter": "SN",
                "GovtLot": "01",
                "Corner": "M-13"
            }
        },
        "verification": {
            "step": True,
            "rekey": True,
            "reentry": {
                "reenter_document": True,
                "reenter_grantor": True,
                "reenter_grantee": True,
                "reenter_property": True,
            },
            "first_page_to_last_page": True
        },
        "image_viewer": {
            "restore_secured_document": False
        },
    },

    "Real_Property_Recordings_W_Label": {
        "doc_group": "REAL PROPERTY OHIO",
        "default_doc_type": "MORTGAGE",
        "order_item_description": {
            "value": "$30.00"
        },
        "discount": {
            "show": True,
            "value": ["100%"]
        },
        "payment_methods": {
            "value": ["Company Account", "Cash", "Cashiers Check", "Check", "Credit Card",
                      "Money Order"]
        },
        "capture": {
            "step": True
        },
        "indexing": {
            "step": True,
            "first_page_to_last_page": False,
            "party_name": ["GRANTOR", "GRANTEE"],
            "property": {
                "newdesc": ['Legal Description / Remarks'],
                "subdivision": ["Subdivision", "Lot", "Block", "Unit", "Volume", "Page"],
                "survey": ["Abstract", "Block", "Survey", "Township", "Section", "Tract", "Acres"],

            },
            "default_ptop_type": "newdesc",
            "prop_values": {
                "LegalDescriptionRemarks": "new_desc",
                "Township": "Kofile Township 002N 317W",
                "Subdivision": "EDDEN CROSSING",
                "Lot": "Lot1",
                "Block": "Block1",
                "Remarks": "Some remark",
                "Abstract": "Abstr1",
                "Survey": "Survey1",
                "Section": "12",
                "Tract": "Tract1",
                "Acres": "10",
                "Condominium": "CONDOMINIUM NAME",
                "Unit": "Unit1",
                "Building": "Building1",
                "Half": "E",
                "Quarter": "SN",
                "GovtLot": "01",
                "Corner": "M-13"
            }
        },
        "verification": {
            "step": True,
        },
    },

    "Real_Property_With_Transfer_Tax_SC": {
        "doc_group": "REAL PROPERTY",
        "default_doc_type": "ABANDONMENT",
        "order_item_description": {
            "value": "$30.00 Transfer Tax to be calculated"
        },
        "discount": {
            "show": True,
            "value": ["100%"]
        },
        "payment_methods": {
            "value": ["Company Account", "Cash", "Check", "Credit Card", "Direct Deposit",
                      "Money Order"]
        },
        "capture": {
            "step": True
        },
        "indexing": {
            "step": True,
            "first_page_to_last_page": False,
            "party_name": ["GRANTOR", "GRANTEE"],
            "property": {
                "newdesc": ['Legal Description / Remarks'],
                "subdivision": ["Subdivision", "Lot", "Block", "Unit", "Volume", "Page"],
                "survey": ["Abstract", "Block", "Survey", "Township", "Section", "Tract", "Acres"],

            },
            "default_ptop_type": "newdesc",
            "prop_values": {
                "LegalDescriptionRemarks": "new_desc",
                "Township": "Kofile Township 002N 317W",
                "Subdivision": "EDDEN CROSSING",
                "Lot": "Lot1",
                "Block": "Block1",
                "Remarks": "Some remark",
                "Abstract": "Abstr1",
                "Survey": "Survey1",
                "Section": "12",
                "Tract": "Tract1",
                "Acres": "10",
                "Condominium": "CONDOMINIUM NAME",
                "Unit": "Unit1",
                "Building": "Building1",
                "Half": "E",
                "Quarter": "SN",
                "GovtLot": "01",
                "Corner": "M-13"
            }
        },
        "verification": {
            "step": True,
        },
    },

    "Birth_Certificate_County": {
        "order_type": "Birth Certificate County",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "BIRTH RECORDS",
        "default_doc_type": "BIRTH RECORD",

        "order_item_description": {
            "value": "$23.00, $21.00 BC Verification, $23.00/additional copy, $5.00/contribution"
        },
        "payment_methods": {
            "value": ["Cash", "Check", "Money Order", "Cashiers Check", "Credit Card"]
        },
        "order_summary": {
            "serial_number": True
        },
        "discount": {
            "show": True,
            "value": ["100%"]
        },
        "finalization": {
            "year_on_order_finalization": False,
            "doc_number_on_order_finalization": False
        },
        "capture": {
            "start_from_capture": {
                "value": False
            }
        }
    },

    "Birth_Certificate_State": {
        "order_type": "Birth Certificate State",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "",

        "order_item_description": {
            "value": "$23.00/BC or $3.00/BC Election, $23.00/additional copy, $5.00/contribution"
        },
        "order_summary": {
            "serial_number": True,
        },
        "discount": {
            "show": True,
            "value": ["100%"]
        },
        "finalization": {
            "year_on_order_finalization": False,
            "doc_number_on_order_finalization": False
        },
    },

    "Bonds_Oaths_Deputations": {
        "order_type": "Bonds, Oaths, Deputations",
        "order_doc_type": "",
        "doc_type": True,
        "doc_group": "BONDS AND DEPUTATIONS",
        "default_doc_type": "BOND , (GOV)",

        "order_item_description": {
            "value": "No Fee"
        },
        "finalization": {
            "with_payment": False,
        },
        "capture": {
            "step": True
        },
        "indexing": {
            "step": True
        },
    },

    "Child_Support_Lien": {
        "order_type": "Child Support Lien",
        "order_doc_type": "CHILD SUPPORT LIEN",
        "doc_type": True,
        "doc_group": "CHILD SUPPORT LIENS",
        "default_doc_type": "CHILD SUPPORT LIEN",

        "order_item_description": {
            "value": "No Fee"
        },
        "finalization": {
            "with_payment": False,
            "void_with_payment": False
        },
        "capture": {
            "step": True
        },
        "indexing": {
            "step": True,
            "indexing_type": "self",
            "first_page_to_last_page": False
        },
        "verification": {
            "step": True,
            "rekey": False,
            "reenter_property": False
        },
        "image_viewer": {
            "restore_secured_document": False
        },
    },

    "Civil_New": {
        "order_type": "Civil New",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "",
        "additional_fee_labels":
            {
                "additional_fee_1_label": "Bond Approval",
                "additional_fee_2_label": "Certified Mail",
                "additional_fee_3_label": "Citation",
                "additional_fee_4_label": "Notice",
                "additional_fee_5_label": "Posting",
                "additional_fee_6_label": "Subpoena"
            },
        "additional_fee_values":
            {
                "additional_fee_1_per_no_fee": "3.0",
                "additional_fee_2_amount": "20.0",
                "additional_fee_3_per_no_fee": "4.0",
                "additional_fee_4_per_no_fee": "5.0",
                "additional_fee_5_amount": "25.0",
                "additional_fee_6_per_no_fee": "4.0"
            },
        "order_item_description":
            {
                "value": "$252.00"
            },
        "finalization":
            {
                "year_on_order_finalization": False,
                "doc_number_on_order_finalization": False
            },
        "fund_distribution": [
            {
                "fund_label": "Records Management",
                "value": "$ 5.00"
            },
            {
                "fund_label": "Records Archive Fee",
                "value": "$ 10.00"
            },
            {
                "fund_label": "Courthouse Security",
                "value": "$ 1.00"
            },
            {
                "fund_label": "Judicial Support",
                "value": "$ 42.00"
            },
            {
                "fund_label": "Mediation Fund",
                "value": "$ 15.00"
            },
            {
                "fund_label": "Law Library",
                "value": "$ 20.00"
            },
            {
                "fund_label": "Court Reporter",
                "value": "$ 15.00"
            },
            {
                "fund_label": "Judicial Salary",
                "value": "$ 40.00"
            },
            {
                "fund_label": "Judicial and Court Personnel Training",
                "value": "$ 5.00"
            },
            {
                "fund_label": "Indigent Fee",
                "value": "$ 10.00"
            },
            {
                "fund_label": "Appellate Fund",
                "value": "$ 5.00"
            },
            {
                "fund_label": "Facilities Fund",
                "value": "$ 15.00"
            },
            {
                "fund_label": "Electronic Filing Fee",
                "value": "$ 30.00"
            },
            {
                "fund_label": "Bailiff Fund",
                "value": "$ 20.00"
            },
            {
                "fund_label": "Recording Fees/County Clerk",
                "value": "100%"
            },
        ],
    },

    "Real_Property_OH": {
        "order_type": "Real Property OH",
        "order_doc_type": "",
        "doc_type": True,
        "doc_group": "",
        "min_consideration": 1000,
        "increment": 1000,
        "tax_rate": 4,
        "additional_fee_labels":
            {
                "additional_fee_1_label": "Conveyance Fee OH",
                "additional_fee_2_label": "Transfer Fee OH"
            },
        "additional_fee_values":
            {
                "additional_fee_1_per_amount": "4.0",
                "additional_fee_2_per_no_fee": "0.5"
            },
        "order_item_description":
            {
                "value": "$34.00, $8.00/page after 2nd, Transfer Tax to be calculated"
            },
        "finalization":
            {
                "year_on_order_finalization": False,
                "doc_number_on_order_finalization": False
            },
        "fund_distribution": [
            {
                "fund_label": "Recording Fees",
                "value": "100%"
            }]
    },

    "Civil_Filing": {
        "order_type": "Civil Filing",
        "order_doc_type": "CIVIL COURT",
        "doc_type": True,
        "doc_group": "CIVIL COURT",

        "order_item_description": {
            "value": "Enter Amount"
        },
        "finalization": {
            "with_payment": False,
            "year_on_order_finalization": False,
            "doc_number_on_order_finalization": False
        },
    },

    "Criminal_New": {
        "order_type": "Criminal New",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "",

        "order_item_description": {
            "value": "$285.00"
        },
        "fund_distribution": [
            {
                "fund_label": "Records Management",
                "value": "$ 5.00"
            },
            {
                "fund_label": "Records Archive Fee",
                "value": "$ 10.00"
            },
            {
                "fund_label": "Courthouse Security",
                "value": "$ 5.00"
            },
            {
                "fund_label": "Judicial Salary",
                "value": "$ 40.00"
            },
            {
                "fund_label": "State Jury",
                "value": "$ 15.00"
            },
            {
                "fund_label": "TX Commission Law Enforcement",
                "value": "$ 25.00"
            },
            {
                "fund_label": "Drug And Intoxication Fee",
                "value": "$ 60.00"
            },
            {
                "fund_label": "District Attorney",
                "value": "$ 25.00"
            },
            {
                "fund_label": "Sheriff Fee",
                "value": "$ 15.00"
            },
            {
                "fund_label": "Recording Fees/County Clerk",
                "value": "$ 85.00"
            },
        ],

    },

    "Criminal_Filing": {
        "order_type": "Criminal Filing",
        "order_doc_type": "",
        "doc_type": "CRIMINAL COURT",
        "doc_group": "CRIMINAL COURT",

        "order_item_description": {
            "value": "Enter Amount"
        },
        "finalization": {
            "with_payment": True
        },
    },

    "Commissioners_Court": {
        "order_type": "",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "COMMISSIONERS COURTS MINUTES",
        "default_doc_type": "COMMISSIONERS COURT",

        "capture": {
            "start_from_capture": {
                "value": True
            }
        },
    },

    "Export_One_Time": {
        "order_type": "Export One Time",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "",

        "order_item_description": {
            "value": "No Fee"
        },
        "finalization": {
            "with_payment": False
        },
    },

    "Print_Export": {
        "order_type": "Print Export",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "",

        "order_item_description": {
            "value": "No Fee"
        },
        "finalization": {
            "with_payment": False,
            "year_on_order_finalization": False,
            "doc_number_on_order_finalization": False
        },
    },

    "Probate_and_Civil_Capture": {
        "order_type": "Probate and Civil Capture",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "PROBATE",
        "default_doc_type": "PROBATE",
        "dept": "Probates",

        "capture": {
            "step": True,
            "expanded_indexing": True
        },
        "indexing": {
            "step": True
        },
        "verification": {
            "step": False,
            "rekey": False
        },
    },

    "Real_Estate_Transfer_MI": {
        "order_type": "Real Estate Transfer MI",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "RP OWNERSHIP TRANSFER",
        "default_doc_type": "",
        "order_item_description": {
            "value": "$30.00 Fee"
        },
        "dept": "Land Records",
        "discount": {
            "show": True,
            "value": ["100%"]
        },
        "finalization": {
            "with_payment": True
        },
        "capture": {
            "step": False
        },
        "indexing": {
            "step": True
        },
        "verification": {
            "step": False,
            "rekey": False
        },
    },

    "Historical_RP": {
        "order_type": "Historical RP",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "REAL PROPERTY",
        "default_doc_type": "ABANDONMENT",

        "capture": {
            "step": True,
            "expanded_indexing": True
        },
        "expended_form": {
            "Applicant1": "Applicant1",
            "Applicant2": "Applicant2",
            "ReturnAddress": ["AddressLine1", "City", "Zip Code"]
        },
        "indexing": {
            "step": True
        },
        "verification": {
            "step": True,
            "rekey": True
        },
    },

    "Historical_ML": {
        "order_type": "Historical ML",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "MARRIAGE LICENSES",
        "default_doc_type": "MARRIAGE",

        "capture": {
            "step": True,
            "expanded_indexing": True
        },
        "expended_form": {
            "Applicant1": "Applicant1",
            "Applicant2": "Applicant2",
            "ReturnAddress": ["AddressLine1", "City", "Zip Code"]
        },
        "indexing": {
            "step": False
        },
        "verification": {
            "step": False,
        },
    },

    "Marriage_License": {
        "order_type": "Marriage License",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "MARRIAGE LICENSES",
        "doc_group_id": 6,
        "default_doc_type": "MARRIAGE",
        "default_doc_type_id": 318,

        "order_item_description": {
            "value": "$82.00 w/o premarital cert, $22.00 w/premarital cert, $182.00/out of state, $5.00/contribution"
        },
        "discount": {
            "show": True,
            "value": ["100%"]
        },
        "capture": {
            "step": True,
            "expanded_indexing": True
        },
        "expended_form": {
            "Applicant1": "Applicant1",
            "Applicant2": "Applicant2",
            "ReturnAddress": ["AddressLine1", "City", "Zip Code"]
        },
        "verification": {
            "step": True,
        },
    },

    "Plats": {
        "order_type": "Plat",
        "order_doc_type": "PLAT",
        "doc_type": True,
        "doc_group": "PLATS",
        "default_doc_type": "PLAT",
        "order_item_description": {
            "value": "$50.00/page"
        },
        "order_summary": {
            "year_on_order_summary": True,
            "doc_number_on_order_summary": True,
        },
        "discount": {
            "show": True,
        },
        "capture": {
            "step": True,
            "upload_image": {
                "value": True,
                "folder": "Auto_Plats"
            },
        },
        "indexing": {
            "birth_upload_image_folder": "BirthUpload",
            "death_upload_image_folder": "DeathUpload",
            "party_name": ["Name"]
        },
        "verification":{
            "step": True
        }
    },

    "Plat_Copy": {
        "order_type": "Plat Copy",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "",
        "default_doc_type": "",
        "order_item_description": {
            "value": "$1.00/page Plat Small Copy, $10.00/page Plat Large Copy, $5.00/certification"
        },
        "per_certification_fee": "5.00",
        "non_fee_certifications": "0",
        "per_page_fee": "1.00",
        "non_fee_pages": "0"
    },

    "Assumed_Name": {
        "order_type": "Assumed Name",
        "order_doc_type": "",
        "doc_type": True,
        "doc_group": "ASSUMED NAME",

        "order_item_description": {
            "value": "$26.00/Acknowledgment or $25.00/Notary"
        },
        "discount": {
            "show": True,
            "value": ["100%"]
        },
        "capture": {
            "step": True
        },
        "indexing": {
            "step": True,
            "party_name": ["Name"],
        },
        "verification": {
            "step": True
        }
    },

    "Marks_and_Brands": {
        "order_type": "Marks and Brands",
        "dept": "Marks and Brands",
        "dept_id": "11",
        "doc_type_in_cs": "NEW BRAND",
        "oit_type_id": 17,
        "order_item_description": {"value": "$26.00, $5.00/brand location after 1st"},
        "capture": {
            "step": True
        },
        "indexing": {
            "step": True,
            "party_name": ["Name"],
        },
        "verification":{
            "step": False
        }
    },

    "Judgements_KDI": {
        "order_type": "KDI",
        "dept": "Land Records",
        "dept_id": "1",
        "doc_type_in_cs": "AJ-ABSTRACT OF JUDGMENT",
        "oit_type_id": 114,
        "order_item_description": {"value": "$24.00"}
    },

    "Account_Payment": {
        "order_type": "Account Payment",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "",

        "order_header": {
            "type": "account",
            "value": "TestAcc - automation_test_account@mailinator.com",
        },
        "order_item_description": {
            "value": "Enter an Amount"
        },
        "finalization": {
            "payment_method_account": "Cash",
            "year_on_order_finalization": False,
            "doc_number_on_order_finalization": False
        },
    },

    "Death_Certificate": {
        "order_type": "Death Certificate",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "DEATH CERTIFICATE",
        "default_doc_type": "DEATH RECORD",

        "order_item_description": {
            "value": "$21.00, $18.00 Death Verification, $4.00/additional copy, $5.00/contribution"
        },
        "order_summary": {
            "serial_number": True
        },
        "discount": {
            "show": True,
            "value": ["100%"]
        },
        "finalization": {
            "year_on_order_finalization": False,
            "doc_number_on_order_finalization": False
        },
        "capture": {
            "start_from_capture": {
                "value": True
            },
        }
    },

    "Duplicate_Marriage_License": {
        "order_type": "Duplicate Marriage License",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "",
        "default_doc_type": "MARRIAGE",

        "order_item_description": {
            "value": "$34.00"
        },
        "discount": {
            "show": True,
            "value": ["100%"]
        },
        "finalization": {
            "year_on_order_finalization": False,
            "doc_number_on_order_finalization": False
        },
    },

    "Financing_Statement_UCC": {
        "order_type": "Financing Statement (UCC)",
        "order_doc_type": "FINANCING STATEMENT",
        "doc_group": "FINANCING STATEMENTS",
        "doc_type": False,
        "default_doc_type": "FINANCING STATEMENT",
        "additional_fee_labels":
            {
                "additional_fee_1_label": "Billable Pages"
            },
        "additional_fee_values":
            {
                "additional_fee_1_per_no_fee": "4.0"
            },
        "order_item_description":
            {
                "value": "$36.00 Standard,$51.00 Non-Standard,$5.00/debtor after 1st,Billable pages fee"
            },
        "discount":
            {
                "show": True,
                "value": ["100%"]
            },

        "capture":
            {
                "step": True,
            },
        "indexing":
            {
                "step": True,
            },
        "verification":
            {
                "step": True,
            },
    },

    "Governmentals": {
        "order_type": "Governmentals",
        "order_doc_type": "BOND FOR PAYMENT",
        "doc_type": True,
        "doc_group": "GOVERNMENTALS",
        "default_doc_type": "BOND FOR PAYMENT",

        "order_item_description": {
            "value": "Enter an Amount"
        },
        "discount": {
            "show": True,
            "value": ["100%"]
        },

        "finalization": {
            "with_payment": True,
            "void_with_payment": True
        },
        "fee_distribution": [
            {
                "fee_fund_label": "",
                "value": ""
            },
        ],

        "capture": {
            "step": True
        },
        "indexing": {
            "step": True
        },
    },

    "Military_Discharge": {
        "order_type": "Military Discharge",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "MILITARY DISCHARGES",
        "default_doc_type": "EXPUNGED",
        "order_item_description": {
            "value": "No Fee"
        },
        "finalization": {
            "with_payment": False,
            "void_with_payment": False
        },
        "capture": {
            "step": True,
            "expanded_indexing": True,
            "capture_review": False,
            "upload_image": {
                "value": False,
                "folder": "Auto_Plats"
            },
        },
        "verification": {
            "step": False
        },
    },

    "Plats_Label": {
        "order_type": "Plat Label",
        "order_doc_type": "PLATS",
        "doc_type": False,
        "doc_group": "PLATS",
        "default_doc_type": "PLATS",

        "order_item_description": {
            "value": "$0.25/label"
        },
        "discount": {
            "show": True,
            "value": ["100%"]
        },
        "finalization": {
            "year_on_order_finalization": False,
            "doc_number_on_order_finalization": False
        },
    },

    "Map_AL": {
        "order_type": "Map AL",
        "order_doc_type": "MAP AL",
        "doc_group": "MAPS ALABAMA",
        "default_doc_type": "MAP AL",  # capture mapping doctype
        "order_item_description": {
            "value": "$15.00/page after 1st"
        },
        "payment_methods": {
            "value": ["Company Account", "Cash", "Check", "Credit Card", "Money Order"],
        },
        "capture": {
            "step": True,
        },
        "indexing": {
            "step": True,
        },
        "verification": {
            "step": True,
        },
    },

    # Eform OITs
    "Eform_Abandonment": {
        "order_type": "Abandonment of Assumed Name",
        "order_doc_type": "",
        "doc_group": "ASSUMED NAME",
        "default_doc_type": "WITHDRAWAL OF ASSUMED NAME",
        "order_item_description": {
            "value": "$25.00/Acknowledgment or $24.00/Notary, $0.50/name after 2nd"
        },
        "capture": {
            "step": True,
        },
        "indexing": {
            "step": True,
        },
    },

    "Eform_Assumed_names": {
        "order_type": "Assumed Names",
        "order_doc_type": "",
        "doc_group": "ASSUMED NAME",
        "default_doc_type": "ASSUMED NAME",

        "start_process_order_from_edit_oi": True,

        "order_item_description": {
            "value": "$25.00/Acknowledgment or $24.00/Notary, $0.50/name after 2nd"
        },
        "capture": {
            "step": True,
        },
        "indexing": {
            "step": True,
        },

    },

    "Eform_Marriage_License": {
        "order_type": "Marriage License",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "MARRIAGE LICENSES",
        "default_doc_type": "MARRIAGE",

        "start_process_order_from_edit_oi": True,

        "order_item_description": {
            "value": "$82.00 w/o premarital cert, $22.00 w/premarital cert, $182.00/out of state, $5.00/contribution"
        },
        "discount": {
            "show": True,
            "value": ["100%"]
        },
        "capture": {
            "step": True,
            "expanded_indexing": True,
        },
    },

    "Eform_Informal_Marriage_License": {
        "order_type": "Informal Marriage License",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "INFORMAL MARRIAGE",
        "default_doc_type": "INFORMAL MARRIAGE",

        "start_process_order_from_edit_oi": True,

        "order_item_description": {
            "value": "$47.00, $5.00/contribution"
        },
        "discount": {
            "show": True,
            "value": ["100%"]
        },
        "capture": {
            "step": True,
            "expanded_indexing": True,
        },
    },

    "Eform_Military_Discharge_Request": {
        "order_type": "Military Discharge Request",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "",
        "default_doc_type": "MID",

        "order_item_description": {
            "value": "No Fee"
        },
        "finalization": {
            "with_payment": False,
            "void_with_payment": False
        },
        "payment_methods": {
            "value": [""]
        },
    },

    "Eform_Cattle_Brands": {
        "order_type": "Marks and Brands",
        "order_doc_type": "",
        "doc_group": "MARKS AND BRANDS",
        "default_doc_type": "NEW BRAND",

        "order_item_description": {
            "value": "$26, $5/additional brand location"
        },
        "discount": {
            "show": True,
            "value": ["100%"]
        },
        "capture": {
            "step": True,
        },
        "indexing": {
            "step": True,
        },
    },

    "Eform_Birth_Certified_Copy": {
        "order_type": "Birth/Death Certificate Request",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "",
        "default_doc_type": "BIRTH",

        "order_item_description": {
            "value": "No Fee"
        },
        "finalization": {
            "with_payment": False,
            "void_with_payment": False,
            "year_on_order_finalization": False,
            "doc_number_on_order_finalization": False
        },
        "payment_methods": {
            "value": [""]
        },
    },

    "Eform_Death_Certified_Copy": {
        "order_type": "Birth/Death Certificate Request",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "",
        "default_doc_type": "DEATH DC",

        "order_item_description": {
            "value": "No Fee"
        },
        "finalization": {
            "with_payment": False,
            "void_with_payment": False,
            "year_on_order_finalization": False,
            "doc_number_on_order_finalization": False
        },
        "payment_methods": {
            "value": [""]
        },
    },

    "erProxy": {

        "order_type": "erProxy",
        "order_doc_type": "",
        "doc_type": False,
        "doc_group": "Real Property",
        "doc_type_in_cs": "AFFIDAVIT",
        "doc_group_id": "1",
        "default_doc_type": "RP",
        "dept_id": "1",
        "order_item_description": {
            "value": "ERecordings-Assumed Name -OR- WITHDRAWAL OF ASSUMED NAME"
        },
        "discount": {
            "value": [""]
        },
        "finalization": {
            "with_payment": False,
            "void_with_payment": True,
            "year_on_order_finalization": False,
            "doc_number_on_order_finalization": False
        },
        "payment_methods": {
            "value": [""]
        },
        "order": {
            "first_page_to_last_page": True
        },
        "ReCapture": {
            "first_page_to_last_page": True
        },
        "indexing": {
            "step": True,
            "indexing_type": "self",
            "first_page_to_last_page": True
        },
        "verification": {
            "step": True,
            "rekey": True,
            "reentry": {
                "reenter_document": True,
                "reenter_grantor": True,
                "reenter_grantee": True,
                "reenter_property": True,
            },
        },
        "cover_page": False,
        "cover_page_text": "ERecordings-RP",
    },
}

CS_OITS = {
    "Certified Copy - GOV": {
        "department_in_cs": {
            "value": "Governmentals"
        },
        "recorded_date_range": {
            "exists": True
        },
        "instrument_date_range": {
            "exists": False
        },
        "order_type_in_inbox": {
            "value": "Certified Copy"
        },
        "comment_in_inbox": {
            "value": "testcomment"
        },
        "customer_name_in_inbox": {
            "value": "testname"
        },
        "order_summary_type": {
            "value": "Copies"
        },
        "finalization_status": {
            "value": "Finalized",
        },
        "order_summary_status": {
            "value": "Pending"
        }
    }
}

MAIN_MENU_ITEMS = {
    "MainMenu": {
        "Orders": {
            "value": "orders"
        },
        "Capture": {
            "value": "capture"
        },
        "Indexing": {
            "value": "indexing"
        },
        "Verification": {
            "value": "verification"
        },
        "Search": {
            "value": "searching"
        },
        "Reports": {
            "value": "report"
        }
    },
    "SubMenu": {
        "Order_Queue": {
            "value": "orderQueue"
        },
        "Initialize_Drawer": {
            "value": "initializeDrawer"
        },
        "Balance_Drawer": {
            "value": "balanceDrawer"
        },
        "Capture_Queue": {
            "value": "captureQueue"
        },
        "Indexinq_Queue": {
            "value": "indexQueue"
        },
        "Verification_Queue": {
            "value": "verificationQueue"
        },
        "Search_Orders": {
            "value": "orderSearch"
        },
        "Search_Packages": {
            "value": "packageSearch"
        }
    }
}

STATUSES = {
    "Order": {
        "Cancel_status": {
            "value": "Cancelled"
        },
        "Reject_status": {
            "value": "Rejected"
        },
        "Send_to_Admin_status": {
            "value": "Admin Hold"
        },
        "Save_status": {
            "value": "Suspended"
        },
        "Void_status": {
            "value": "Voided"
        },
        "Finalized_status": {
            "value": "Finalized"
        },
        "Scheduled_status": {
            "value": "Scheduled"
        },
        "Admin_Adjustment_status": {
            "value": "Admin Adjustment"
        },
        "In_Process": {
            "value": "In Process"
        },
        "Re_Entry": {
            "value": "Re-Entry"
        },
        "Pending": {
            "value": "Pending"
        },
        "Reprocess_status": {
            "value": "Reprocess"
        },
        "Historical": {
            "value": "Historical Documents"
        }
    },
    "Capture": {
        "Reprocess_status": {
            "value": "Reprocess"
        },
        "Pending_status": {
            "value": "Pending"
        },
    },
    "Indexing": {
        "Review_status": {
            "value": "Review"
        },
    },
    "Verification": {
        "Send_to_Admin_status": {
            "value": "AdminSuspend"
        },
        "Save_status": {
            "value": "Suspended"
        },
        "Review_status": {
            "value": "Review"
        },
        "In_Process_status": {
            "value": "In Process"
        },
    },
    "Order_Search": {
        "Cancel_status": {
            "value": "Cancelled"
        },
        "Reject_status": {
            "value": "Rejected"
        },
        "Send_to_Admin_status": {
            "value": "Order"
        },
        "Save_status": {
            "value": "Order"
        },
        "Void_status": {
            "value": "VOIDED"
        },

        "order_status": {
            "value": "Order"
        },
        "capture_status": {
            "value": "Capture"
        },
        "indexing_status": {
            "value": "Indexing"
        },
        "verification_status": {
            "value": "Verification"
        },
        "archive_status": {
            "value": "Archive"
        },
        "Admin_Adjustment_status": {
            "value": "Admin Adjustment"
        },
    },
}

TAB_NAME = {
    "Tabs": {
        "Order_Item": {
            "value": "Order Item"
        },
        "Document": {
            "value": "Document"
        },
        "Parties": {
            "value": "Parties"
        },
        "Properties": {
            "value": "Properties"
        },
        "Attachments": {
            "value": "Attachments"
        },
        "Notes": {
            "value": "Notes"
        },
        "Business": {
            "value": "Business"
        },
        "Owners/Agents": {
            "value": "Owners/Agents"
        },
        "Applicant1": {
            "value": "Applicant1"
        },
        "Applicant2": {
            "value": "Applicant2"
        },
        "Applicant": {
            "value": "Applicant"
        },
        "Owners": {
            "value": "Owners"
        },
    },
}

CS_OITs_configs = {

    "default": {
        "fee_calc": "num_p_cs * 1",
        "fee_description": "$1/page",
        "dept": "Property Records",
        "dept_id": "1",
        "doc_group": None,
        "doc_group_id": None,
        "oit_type_before": "Clerk Search Copies",
        "oit_type_after": "Clerk Search Copies",
        "order_status_before": "Pending",
        "order_status_after": "Finalized",
        "is_package": False,
        "fill_required_fields": False,
        "number_certifications_popup": False,
        "is_serial_number": False,
        "doc_type_in_cs": "",
        "oit_type_id": 1
    },

    "Real_Property_Recordings_W_Page": {

    },

    "RP_Recordings": {
        "Certified Copy": {

            "fee_calc": "num_p_cs * 1 + no_of_cert * 5",
            "fee_description": "$1.00/page, $5.00/certification",
        },
        "doc_type_in_cs": "MISCELLANEOUS",
        "doc_group": "REAL PROPERTY",
        "doc_group_id": 1
    },

    "Commissioners_Court": {
        "dept": "Commissioners Court",
        "dept_id": "8",
        "oit_type_id": 197,
        "or": 203,
        "doc_type_column": 0
    },

    "Informal_Marriage_License":
        {
            "Re-Index": False,
            "Certified Copy": {
                "fee_calc": "6",
                "fee_description": "$47.00, $5.00/contribution",
                "oit_type_before": "Clerk Search Informal Marriage License Certified Copy",
                "oit_type_after": "Clerk Search Informal Marriage License Certified Copy",
                "fill_required_fields": True
            },

            "fee_calc": "num_p_cs * 1",
            "fee_description": "$1/page",
            "dept": "Marriage Licenses",
            "dept_id": "6",
            "oit_type_before": "Clerk Search Marriage Copies",
            "oit_type_after": "Clerk Search Marriage Copies",
            "fill_required_fields": True,
            "doc_type_in_cs": "INFORMAL MARRIA-INFORMAL MARRIAGE",
            "oit_type_id": 15
        },

    "Marriage_License": {
        "Re-Index": False,
        "Certified Copy": {
            "fee_calc": "no_of_cert*20",
            "fee_description": "$20.00/copy",
            "oit_type_before": "Clerk Search Marriage License Certified Copy",
            "oit_type_after": "Clerk Search Marriage License Certified Copy",
            "fill_required_fields": False
        },
        "fee_calc": "num_p_cs* 1",
        "fee_description": "$1/page",
        "dept": "Marriage Licenses",
        "dept_id": "6",
        "oit_type_before": "Clerk Search Marriage Copies",
        "oit_type_after": "Clerk Search Marriage Copies",
        "fill_required_fields": True,
        "doc_type_in_cs": "MARRIAGE-MARRIAGE",
        "oit_type_id": 11
    },

    "Plats": {
        "Certified Copy": {
            "fee_calc": "num_p_cs * 1 + no_of_cert * 5",
            "fee_description": "$1.00/page, $5.00/certification"
        },
        "fee_calc": "num_p_cs * 1",
        "fee_description": "$1.00/page, $5.00/certification",
        "dept": "Plats",
        "dept_id": "2",
        "doc_group": "PLATS",
        "doc_group_id": 2,
        "oit_type_before": "Clerk Search Plat Copies",
        "oit_type_after": "Clerk Search Plat Copies",
        "oit_type_id": 3,
        "doc_type_in_cs": "PL-PLAT"
    },

    "Birth_Record": {
        "Copy": False,
        "Certified Copy": {
            "fee_calc": "23 + no_of_addtl_copies * 23 + no_of_contr * 5",
            "fee_description": "$23.00, $23.00/additional copy, $5.00/contribution",
            "oit_type_before": "Clerk Search Birth Certificate",
            "oit_type_after": "Clerk Search Birth Certificate",
            "is_package": True,
            "fill_required_fields": True,
            "number_certifications_popup": True,
            "is_serial_number": True
        },
        "fee_description": "$1/page",
        "dept": "Birth Records",
        "dept_id": "5",
        "oit_type_id": 215
    },

    "Death_Record": {
        "Copy": False,
        "Certified Copy": {
            "fee_calc": "21 + no_of_addtl_copies * 4+no_of_contr * 5",
            "fee_description": "$21.00, $4.00/additional copy, $5.00/contribution",
            "oit_type_before": "Clerk Search Death Certificate",
            "oit_type_after": "Clerk Search Death Certificate",
            "is_package": True,
            "fill_required_fields": True,
            "number_certifications_popup": True,
            "is_serial_number": True
        },
        "fee_description": "$1/page",
        "dept": "Death Records",
        "dept_id": "9",
        "oit_type_id": 216
    },

    "Assumed_Name": {
        "dept": "Assumed Names",
        "dept_id": "4",
        "doc_type_in_cs": "AN-ASSUMED NAME",
        "oit_type_id": 26
    },

    "Marks_and_Brands": {
        "dept": "Marks and Brands",
        "dept_id": "11",
        "doc_type_in_cs": "NEW BRAND",
        "oit_type_id": 17
    },

    "erProxy":
        {
            "doc_type_in_cs": "AFFIDAVIT",
            "doc_group": "REAL PROPERTY",
            "doc_group_id": 1
        }

}

front_office = {
    "account_code": "20230616142550",
    "company_name": "Auto20230616142550",
    "type_ahead_department": "RealPropertyRecords",
    "workflow_dates_department": "Property Records"
}

CUSTOM_STAMPS = {
    "Stamp_text": {
        "C1_stamp": {
            "value": "RECEIVED IN BAD CONDITION"
        },
        "C2_stamp": {
            "value": "PAGE INTENTIONALLY LEFT BLANK"
        },
        "C3_stamp": {
            "value": "DECEASED"
        }
    }
}

ps_password = {
    "password": "Password_01",
    "password_hash": "sMEap4DW0qcU/+w1bQTqqqUJQzGpjFUCNLWjFJl1Wdo=",
    "password_hash_salt": "ez4b7/gow9co7MTh9GO5rFDNfTK/x5V3fPhpJFmZwVs="
}

er_schema = {
    "ER_SCHEMA_NAME": "Default",
    "CONFIG_ID": 3066
}

departments = {
    "RP": 1
}

kiosk_search = {
    "convenience_fee": 2.0
}
