"""
development tenant (48999) location 6 test data
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
                "amount": 2,
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
            "indexing_type": "kdi",
            "first_page_to_last_page": True
        },
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
