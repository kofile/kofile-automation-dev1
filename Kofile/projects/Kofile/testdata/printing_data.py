class PrintData:
    class qa_48999_loc_2:
        zebra_label_printer = {
            "content": ["KofileCert.GRF", "clerk_sig.GRF", "certify", "this", "instrument", "was", "Beta",
                        "County, Texas", "PAGES: ", "User1"]
        }

        drawer_summary = {
            "pages": 1,
            "content": {
                0: ['Drawer Balance Summary', 'Expected', 'Actual', 'Difference', 'Cash', '$300.00', '$0.00', '$300.00',
                    'Cashiers Check', '$0.00', '$0.00', '$0.00', 'Check', '$0.00', '$0.00', '$0.00',
                    'IRS Direct Deposit',
                    '$0.00', '$0.00', '$0.00', 'LegalEase', '$0.00', '$0.00', '$0.00', 'Money Order', '$0.00', '$0.00',
                    '$0.00', 'State Direct Deposit', '$0.00', '$0.00', '$0.00', 'Refund', '$0.00', '$0.00', '$0.00',
                    'Vital Check', '$0.00', '$0.00', '$0.00', 'Void/Refund', '$0.00', '$0.00', '$0.00', 'Over/Short',
                    '$300.00', 'Deposit', '$300.00', 'Beginning Balance', '$-300.00', 'Cash Refund', '$0.00',
                    'Actual Balance', '$-300.00', 'Total Cash', '$0.00', '$0', 'Total Non-Cash', '$0.00', '$0',
                    'Total Voids(0)', '$0.00', 'Drawer Name :', 'Agent Drawer', 'Date and Time:', None,
                    'Printed By:', 'user6 user6', 'Clerk', None, 'Administration',
                    None, 'Accounting', None]
            }
        }

        settle_drawer_summary = {
            "pages": 1,
            "content": {
                0: ['Drawer Balance Summary', 'Expected', 'Actual', 'Difference', 'Cash', '$300.00', None,
                    None, 'Cashiers Check', '$0.00', '$0.00', '$0.00', 'Check', '$0.00', '$0.00', '$0.00',
                    'IRS Direct Deposit', '$0.00', '$0.00', '$0.00', 'LegalEase', '$0.00', '$0.00', '$0.00',
                    'Money Order',
                    '$0.00', '$0.00', '$0.00', 'State Direct Deposit', '$0.00', '$0.00', '$0.00', 'Refund', '$0.00',
                    '$0.00', '$0.00', 'Vital Check', '$0.00', '$0.00', '$0.00', 'Void/Refund', '$0.00', '$0.00',
                    '$0.00',
                    'Over/Short', None, 'Deposit', '$300.00', 'Beginning Balance', '$-300.00', 'Cash Refund',
                    '$0.00', 'Actual Balance', None, 'Total Cash', '$0.00', None, 'Total Non-Cash',
                    '$0.00',
                    '$0.0', 'Total Voids(0)', '$0.00', 'Drawer Name :', 'Agent Drawer', 'Date and Time:',
                    None, 'Printed By:', 'user6 user6', 'Clerk',
                    None, 'Administration', None,
                    'Accounting', None]
            }
        }

        cover_page_guest_golden = {
            "pages": 1,
            "content": {
                0: [None, 'Beta County', 'Charlotte Smith', 'Beta County Clerk', 'Instrument Number:',
                    None, 'Real Property Recordings W/Page', 'Recorded On:', None,
                    'Number of Pages:', '2', '" Examined and Charged as Follows: "', 'Total Recording:', '$', '%order_total',
                    '*********** THIS PAGE IS PART OF THE INSTRUMENT ***********',
                    'Any provision herein which restricts the Sale, Rental or use of the described REAL PROPERTY',
                    'because of color or race is invalid and unenforceable under federal law.', 'File Information:',
                    'Record and Return To:', 'Document Number:', None, 'VoloAutomationTest', 'Receipt Number:',
                    '%order_num', 'Recorded Date/Time:', None, 'User:', 'User1 U',
                    None, 'Station:', 'workstation', 'Charlotte Smith', 'Beta County Clerk',
                    'Beta County, TX', 'STATE OF TEXAS', 'Beta County',
                    'I hereby certify that this Instrument was filed in the File Number sequence on the date/time',
                    'printed hereon, and was duly recorded in the Official Records of', 'Beta County', ', Texas']
            }
        }

        generic_receipt_original_golden = {
            "pages": 1,
            "content": {
                0: ['Order Total', '(', '1', ')', '$', '%order_total', 'Seq', 'Item', 'Document', 'Description',
                    'Number',
                    'Number Of', 'Amount', 'Serial Number', 'GF Number', '1', 'Real Property', 'Recordings W/Page', 'M',
                    None, '2', '$', '%order_total', '200-RM', 'Records Management', '$', None, '300-RA',
                    'Records Archive Fee', '$', None, '400-CS', 'Courthouse Security', '$', None, '100-Recording',
                    'Recording Fees', '$', None, 'Total Payments', 'Change Due', '(', '1', ')', '$', '%order_total',
                    '$', '0.00',
                    'Seq', 'Payment Method', 'Transaction Id', 'Comment', 'Total', '1', 'Cash', 'TRID11', 'comment_1_1',
                    '$', None, "For more information about the County Clerk's office and to search property",
                    'records online, please visit www.kofile.com', '1 of 1', 'voloautomationtest', None,
                    None, 'Charlotte Smith', 'Beta County Clerk', '6300 Cedar Springs Rd',
                    'Dallas, TX 75235', 'Main:', '(555)555-5555', 'Fax:', '(555)555-5555', '%order_num', 'Receipt:',
                    '%order_date', 'Date:', 'Time:', '%order_time', 'By:', 'User1 U', 'Station:', 'workstation',
                    'Status:',
                    'ORIGINAL COPY']
            }
        }

        epson_receipt_original_golden = {
            "content": ["BALDWIN COUNTY", "HARRY D'OLIVE", "Cashier ID:", "User1 U", "Status:", "ORIGINAL COPY",
                        "Total Fees:", "Payment Type", "Caash", "Amount", "Total Payment:",
                        "Change:", "Thank You", "Have a nice day"]
        }

        generic_receipt_duplicate_golden = {
            "pages": 1,
            "content": {
                0: ['Order Total', '(', '1', ')', '$', '%order_total', 'Seq', 'Item', 'Document', 'Description',
                    'Number',
                    'Number Of', 'Amount', 'Serial Number', 'GF Number', '1', 'Real Property', 'Recordings W/Page', 'M',
                    None, '2', '$', '%order_total', '200-RM', 'Records Management', '$', None, '300-RA',
                    'Records Archive Fee', '$', None, '400-CS', 'Courthouse Security', '$', None, '100-Recording',
                    'Recording Fees', '$', None, 'Total Payments', 'Change Due', '(', '1', ')', '$', '%order_total',
                    '$', '0.00',
                    'Seq', 'Payment Method', 'Transaction Id', 'Comment', 'Total', '1', 'Cash', 'TRID11', 'comment_1_1',
                    '$', None, "For more information about the County Clerk's office and to search property",
                    'records online, please visit www.kofile.com', '1 of 1', 'voloautomationtest', None,
                    None, 'Charlotte Smith', 'Beta County Clerk', '6300 Cedar Springs Rd',
                    'Dallas, TX 75235', 'Main:', '(555)555-5555', 'Fax:', '(555)555-5555', '%order_num', 'Receipt:',
                    '%order_date', 'Date:', 'Time:', '%order_time', 'By:', 'User1 U', 'Station:', 'workstation',
                    'Status:',
                    'DUPLICATE COPY']
            }
        }

        generic_receipt_adjusted_golden = {
            "pages": 1,
            "content": {
                0: ['Order Total', '(', '1', ')', '$', '%order_total', 'Seq', 'Item', 'Document', 'Description',
                    'Number',
                    'Number Of', 'Amount', 'Serial Number', 'GF Number', '1', 'Real Property', 'Recordings W/Page', 'M',
                    None, '3', '$', '%order_total', '200-RM', 'Records Management', '$', None, '300-RA',
                    'Records Archive Fee', '$', None, '400-CS', 'Courthouse Security', '$', None, '100-Recording',
                    'Recording Fees', '$', None, 'Total Payments', 'Change Due', '(', '2', ')', '$', '%order_total',
                    '$', '0.00',
                    'Seq', 'Payment Method', 'Transaction Id', 'Comment', 'Total', '1', 'Cash', 'TRID11', 'comment_1_1',
                    '$', None, '2', 'Refund', 'some_comment_1', '$', None,
                    "For more information about the County Clerk's office and to search property",
                    'records online, please visit www.kofile.com', '1 of 1', 'voloautomationtest', None,
                    None, 'Charlotte Smith', 'Beta County Clerk', '6300 Cedar Springs Rd',
                    'Dallas, TX 75235', 'Main:', '(555)555-5555', 'Fax:', '(555)555-5555', '%order_num', 'Receipt:',
                    '%order_date', 'Date:', 'Time:', '%order_time', 'By:', 'User1 U', 'Station:', 'workstation',
                    'Status:',
                    'ADJUSTED COPY']
            }
        }

        epson_receipt_adjusted_golden = {
            "content": ["BALDWIN COUNTY", "HARRY D'OLIVE", "Cashier ID:", "User1 U", "Status:", "ADJUSTED COPY",
                        "Total Fees:", "Payment Type", "Cash", "Amount", "Total Payment:",
                        "Change:", "Thank You", "Have a nice day"]
        }

        cover_page_email_golden = {
            "pages": 1,
            "content": {
                0: [None, 'Beta County', 'Charlotte Smith', 'Beta County Clerk', 'Instrument Number:', None,
                    'Real Property Recordings W/Page', 'Recorded On:', None, 'Number of Pages:',
                    '2', '" Examined and Charged as Follows: "', 'Total Recording:', '$', '%order_total',
                    '*********** THIS PAGE IS PART OF THE INSTRUMENT ***********',
                    'Any provision herein which restricts the Sale, Rental or use of the described REAL PROPERTY',
                    'because of color or race is invalid and unenforceable under federal law.', 'File Information:',
                    'Record and Return To:', 'Document Number:', None, 'ReturnByMailCustomerName', 'Receipt Number:',
                    '%order_num', None, 'Recorded Date/Time:', None, 'User:',
                    'User1 U', 'SCHENECTADY NY 12345-6789', 'Station:', 'workstation', 'Charlotte Smith',
                    'Beta County Clerk', 'Beta County, TX', 'STATE OF TEXAS', 'Beta County',
                    'I hereby certify that this Instrument was filed in the File Number sequence on the date/time',
                    'printed hereon, and was duly recorded in the Official Records of', 'Beta County', ', Texas']
            }
        }

        cover_page_return_mail_golden = {
            "pages": 1,
            "content": {
                0: [None, 'Beta County', 'Charlotte Smith', 'Beta County Clerk', 'Instrument Number:',
                    None, 'Real Property Recordings W/Page', 'Recorded On:', None,
                    'Number of Pages:', '2', '" Examined and Charged as Follows: "', 'Total Recording:', '$', '%order_item_price',
                    '*********** THIS PAGE IS PART OF THE INSTRUMENT ***********',
                    'Any provision herein which restricts the Sale, Rental or use of the described REAL PROPERTY',
                    'because of color or race is invalid and unenforceable under federal law.', 'File Information:',
                    'Record and Return To:', 'Document Number:', None, 'Receipt Number:', None,
                    'Recorded Date/Time:', None, 'User:', 'User1 U', 'Station:', 'workstation',
                    'Charlotte Smith', 'Beta County Clerk', 'Beta County, TX', 'STATE OF TEXAS', 'Beta County',
                    'I hereby certify that this Instrument was filed in the File Number sequence on the date/time',
                    'printed hereon, and was duly recorded in the Official Records of', 'Beta County', ', Texas']
            }
        }

        cover_page_edit_golden_file = {
            "pages": 1,
            "content": {
                0: [None, 'Beta County', 'Charlotte Smith', 'Beta County Clerk', 'Instrument Number:', None,
                    'Real Property Recordings W/Page', 'Recorded On:', None, 'Number of Pages:',
                    '3', '" Examined and Charged as Follows: "', 'Total Recording:', '$', '%order_item_price',
                    '*********** THIS PAGE IS PART OF THE INSTRUMENT ***********',
                    'Any provision herein which restricts the Sale, Rental or use of the described REAL PROPERTY',
                    'because of color or race is invalid and unenforceable under federal law.', 'File Information:',
                    'Record and Return To:', 'Document Number:', None, 'Receipt Number:', None,
                    'TestAddress1', 'Recorded Date/Time:', None, 'User:', 'User1 U',
                    'BLUE RIDGE TX 75424-2542', 'Station:', 'workstation', 'Charlotte Smith', 'Beta County Clerk',
                    'Beta County, TX', 'STATE OF TEXAS', 'Beta County',
                    'I hereby certify that this Instrument was filed in the File Number sequence on the date/time',
                    'printed hereon, and was duly recorded in the Official Records of', 'Beta County', ', Texas']
            }
        }

        print_rejection_golden = {
            "pages": 1,
            "content": {
                0: ['Recording Department: 555-555-5555', 'Vital Statistics:\xa0 555-555-5555',
                    'Website:\xa0 www.kofile.com', 'John Doe', 'County Clerk', 'Product Management County Courts',
                    'Building', '6300 Cedar Springs Rd, Dallas, TX', '75235',
                    'Our office has received the above mentioned order.\xa0 We are unable to complete your request for processing due',
                    'to the reason(s) listed below.\xa0 Should you have any questions, please call us at your earliest convenience.',
                    'The attached order is being returned and has NOT been recorded with the County Clerk due to:',
                    'Date:', None, 'To:', 'SIMPLIFILE', 'Lemmon Ave', 'Dallas', ',', 'AK', '75001',
                    'Re: Order #', None, '; Tracking ID', None, 'Test', 'Test', 'ORDER TICKET',
                    '(', 'for clerk reference only)', 'PLEASE DO NOT REMOVE', 'User1 U', ',', 'Deputy Clerk',
                    'Should you have any questions, please contact the undersigned clerk at your earliest convenience.',
                    'User1 U', ', Deputy Clerk', 'Date:', None, 'To:', 'SIMPLIFILE', 'Lemmon Ave', 'Dallas',
                    ',', 'AK', '75001', 'Re: Order #', None, '; Tracking ID', None]
            }
        }

        epson_reciept_erProxy_golden = {
            "content": ["BALDWIN COUNTY", "HARRY D'OLIVE", "Cashier ID:", "User1 U", "Status:", "DUPLICATE COPY",
                        "Total Fees:", "Payment Type", "Cash", "Amount", "Company Account", "Total Payment:",
                        "Change:", "Thank You", "Have a nice day"]
        }

        generic_reciept_erProxy_golden = {
            "pages": 1,
            "content": {
                0: ['Order Total', '(', '1', ')', '$', '%order_total', 'Seq', 'Item', 'Document', 'Description',
                    'Number',
                    'Number Of', 'Amount', 'Serial Number', 'GF Number', '1', 'eRecording - Real', 'Property TX', 'AF',
                    None, None, '$', '%order_total', 'Total Payments', 'Change Due', '(', '1', ')', '$', '%order_total',
                    '$',
                    '0.00', 'Seq', 'Payment Method', 'Transaction Id', 'Comment', 'Total', '1', 'Company Account', '$', '%order_total',
                    "For more information about the County Clerk's office and to search property",
                    'records online, please visit www.kofile.com', '1 of 1', 'VoloAutoTest', None,
                    'Charlotte Smith', 'Beta County Clerk', '6300 Cedar Springs Rd',
                    'Dallas, TX 75235', 'Main:', '(555)555-5555', 'Fax:', '(555)555-5555', '%order_num', 'Receipt:',
                    '%order_date', 'Date:', 'Time:', '%order_time', 'By:', 'User1 U', 'Station:', 'workstation',
                    'Status:',
                    'DUPLICATE COPY', 'Balance After Finalization:', None]
            }
        }

        epson_receipt_duplicate_golden = {
            "content": ["BALDWIN COUNTY", "HARRY D'OLIVE", "Cashier ID:", "User1 U", "Status:", "DUPLICATE COPY",
                        "Total Fees:", "Payment Type", "Cash", "Amount", "Company Account", "Total Payment:",
                        "Change:", "Thank You", "Have a nice day"]
        }

    class uat_48999_loc_2:
        zebra_label_printer = {
            "content": ["KofileCert.GRF", "clerk_sig.GRF", "certify", "this", "instrument", "was", "Beta",
                        "County, Texas", "PAGES: ", "User1"]
        }

        drawer_summary = {
            "pages": 1,
            "content": {
                0: ['Drawer Balance Summary', 'Expected', 'Actual', 'Difference', 'Cash', '$300.00', '$0.00', '$300.00',
                    'Cashiers Check', '$0.00', '$0.00', '$0.00', 'Check', '$0.00', '$0.00', '$0.00',
                    'IRS Direct Deposit',
                    '$0.00', '$0.00', '$0.00', 'LegalEase', '$0.00', '$0.00', '$0.00', 'Money Order', '$0.00', '$0.00',
                    '$0.00', 'State Direct Deposit', '$0.00', '$0.00', '$0.00', 'Refund', '$0.00', '$0.00', '$0.00',
                    'Vital Check', '$0.00', '$0.00', '$0.00', 'Void/Refund', '$0.00', '$0.00', '$0.00', 'Over/Short',
                    '$300.00', 'Deposit', '$300.00', 'Beginning Balance', '$-300.00', 'Cash Refund', '$0.00',
                    'Actual Balance', '$-300.00', 'Total Cash', '$0.00', '$0', 'Total Non-Cash', '$0.00', '$0',
                    'Total Voids(0)', '$0.00', 'Drawer Name :', 'Agent Drawer', 'Date and Time:', None,
                    'Printed By:', 'user6 user6', 'Clerk', None, 'Administration',
                    None, 'Accounting', None]
            }
        }

        settle_drawer_summary = {
            "pages": 1,
            "content": {
                0: ['Drawer Balance Summary', 'Expected', 'Actual', 'Difference', 'Cash', '$300.00', '$15912.00',
                    '$-15612.00', 'Cashiers Check', '$0.00', '$0.00', '$0.00', 'Check', '$0.00', '$0.00', '$0.00',
                    'IRS Direct Deposit', '$0.00', '$0.00', '$0.00', 'LegalEase', '$0.00', '$0.00', '$0.00',
                    'Money Order',
                    '$0.00', '$0.00', '$0.00', 'State Direct Deposit', '$0.00', '$0.00', '$0.00', 'Refund', '$0.00',
                    '$0.00', '$0.00', 'Vital Check', '$0.00', '$0.00', '$0.00', 'Void/Refund', '$0.00', '$0.00',
                    '$0.00',
                    'Over/Short', '$-15612.00', 'Deposit', '$300.00', 'Beginning Balance', '$-300.00', 'Cash Refund',
                    '$0.00', 'Actual Balance', '$15612.00', 'Total Cash', '$0.00', '$15912.00', 'Total Non-Cash',
                    '$0.00',
                    '$0.0', 'Total Voids(0)', '$0.00', 'Drawer Name :', 'Agent Drawer', 'Date and Time:',
                    None, 'Printed By:', 'user6 user6', 'Clerk',
                    None, 'Administration', None,
                    'Accounting', None]
            }
        }

        cover_page_guest_golden = {
            "pages": 1,
            "content": {
                0: [None, 'Beta County', 'Charlotte Smith', 'Beta County Clerk', 'Instrument Number:',
                    None, 'Real Property Recordings W/Page', 'Recorded On:', None,
                    'Number of Pages:', '2', '" Examined and Charged as Follows: "', 'Total Recording:', '$', '%order_total',
                    '*********** THIS PAGE IS PART OF THE INSTRUMENT ***********',
                    'Any provision herein which restricts the Sale, Rental or use of the described REAL PROPERTY',
                    'because of color or race is invalid and unenforceable under federal law.', 'File Information:',
                    'Record and Return To:', 'Document Number:', None, 'voloautomationtest', 'Receipt Number:',
                    '%order_num', None, 'Recorded Date/Time:', None, 'User:', 'User1 U',
                    None, 'Station:', 'workstation', 'Charlotte Smith', 'Beta County Clerk',
                    'Beta County, TX', 'STATE OF TEXAS', 'Beta County',
                    'I hereby certify that this Instrument was filed in the File Number sequence on the date/time',
                    'printed hereon, and was duly recorded in the Official Records of', 'Beta County', ', Texas']
            }
        }

        generic_receipt_original_golden = {
            "pages": 1,
            "content": {
                0: ['Order Total', '(', '1', ')', '$', '%order_total', 'Seq', 'Item', 'Document', 'Description',
                    'Number',
                    'Number Of', 'Amount', 'Serial Number', 'GF Number', '1', 'Real Property', 'Recordings W/Page', 'M',
                    None, '2', '$', '%order_total', '200-RM', 'Records Management', '$', None, '300-RA',
                    'Records Archive Fee', '$', None, '400-CS', 'Courthouse Security', '$', None, '100-Recording',
                    'Recording Fees', '$', None, 'Total Payments', 'Change Due', '(', '1', ')', '$', '%order_total',
                    '$',
                    '0.00', 'Seq', 'Payment Method', 'Transaction Id', 'Comment', 'Total', '1', 'Cash', 'TRID11',
                    'comment_1_1', '$', '%order_total',
                    "For more information about the County Clerk's office and to search property",
                    'records online, please visit www.kofile.com', '1 of 1', 'voloautomationtest', None, None,
                    'Beta County Clerk', '6300 Cedar Springs Rd',
                    'Dallas, TX 75235', 'Main:', '(555)555-5555', 'Fax:', '(555)555-5555', '%order_num', 'Receipt:',
                    '%order_date', 'Date:', 'Time:', '%order_time', 'By:', 'User1 U', 'Station:', 'workstation',
                    'Status:',
                    'ORIGINAL COPY']
            }
        }

        epson_receipt_original_golden = {
            "content": ["BALDWIN COUNTY", "HARRY D'OLIVE", "Cashier ID:", "User1 U", "Status:", "ORIGINAL COPY",
                        "Total Fees:", "Payment Type", "Cash", "Amount", "Total Payment:",
                        "Change:", "Thank You", "Have a nice day"]
        }

        generic_receipt_duplicate_golden = {
            "pages": 1,
            "content": {
                0: ['Order Total', '(', '1', ')', '$', '%order_total', 'Seq', 'Item', 'Document', 'Description',
                    'Number',
                    'Number Of', 'Amount', 'Serial Number', 'GF Number', '1', 'Real Property', 'Recordings W/Page', 'M',
                    None, '2', '$', '%order_total', '200-RM', 'Records Management', '$', None, '300-RA',
                    'Records Archive Fee', '$', None, '400-CS', 'Courthouse Security', '$', None, '100-Recording',
                    'Recording Fees', '$', None, 'Total Payments', 'Change Due', '(', '1', ')', '$', '%order_total',
                    '$',
                    '0.00', 'Seq', 'Payment Method', 'Transaction Id', 'Comment', 'Total', '1', 'Cash', 'TRID11',
                    'comment_1_1', '$', '%order_total',
                    "For more information about the County Clerk's office and to search property",
                    'records online, please visit www.kofile.com', '1 of 1', 'voloautomationtest', None, None,
                    'Beta County Clerk', '6300 Cedar Springs Rd',
                    'Dallas, TX 75235', 'Main:', '(555)555-5555', 'Fax:', '(555)555-5555', '%order_num', 'Receipt:',
                    '%order_date', 'Date:', 'Time:', '%order_time', 'By:', 'User1 U', 'Station:', 'workstation',
                    'Status:',
                    'DUPLICATE COPY']
            }
        }

        generic_receipt_adjusted_golden = {
            "pages": 1,
            "content": {
                0: ['Order Total', '(', '1', ')', '$', '%order_total', 'Seq', 'Item', 'Document', 'Description',
                    'Number',
                    'Number Of', 'Amount', 'Serial Number', 'GF Number', '1', 'Real Property', 'Recordings W/Page', 'M',
                    None, '3', '$', '%order_total', '200-RM', 'Records Management', '$', None, '300-RA',
                    'Records Archive Fee', '$', None, '400-CS', 'Courthouse Security', '$', None, '100-Recording',
                    'Recording Fees', '$', None, 'Total Payments', 'Change Due', '(', '2', ')', '$', '%order_total',
                    '$', '0.00',
                    'Seq', 'Payment Method', 'Transaction Id', 'Comment', 'Total', '1', 'Cash', 'TRID11', 'comment_1_1',
                    '$', None, '2', 'Refund', 'some_comment_1', '$', '%order_total',
                    "For more information about the County Clerk's office and to search property",
                    'records online, please visit www.kofile.com', '1 of 1', 'voloautomationtest', None, None,
                    'Beta County Clerk', '6300 Cedar Springs Rd',
                    'Dallas, TX 75235', 'Main:', '(555)555-5555', 'Fax:', '(555)555-5555', '%order_num', 'Receipt:',
                    '%order_date', 'Date:', 'Time:', '%order_time', 'By:', 'User1 U', 'Station:', 'workstation',
                    'Status:',
                    'ADJUSTED COPY']
            }
        }

        epson_receipt_adjusted_golden = {
            "content": ["BALDWIN COUNTY", "HARRY D'OLIVE", "Cashier ID:", "User1 U", "Status:", "ADJUSTED COPY",
                        "Total Fees:", "Payment Type", "Cash", "Amount", "Total Payment:",
                        "Change:", "Thank You", "Have a nice day"]
        }

        cover_page_email_golden = {
            "pages": 1,
            "content": {
                0: [None, 'Beta County', 'Charlotte Smith', 'Beta County Clerk', 'Instrument Number:', None,
                    'Real Property Recordings W/Page', 'Recorded On:', None, 'Number of Pages:',
                    '2', '" Examined and Charged as Follows: "', 'Total Recording:', '$', '%order_total',
                    '*********** THIS PAGE IS PART OF THE INSTRUMENT ***********',
                    'Any provision herein which restricts the Sale, Rental or use of the described REAL PROPERTY',
                    'because of color or race is invalid and unenforceable under federal law.', 'File Information:',
                    'Record and Return To:', 'Document Number:', None, 'ReturnByMailCustomerName', 'Receipt Number:',
                    '%order_num', None, 'Recorded Date/Time:', None, 'User:',
                    'User1 U', 'SCHENECTADY NY 12345-6789', 'Station:', 'workstation', 'Charlotte Smith',
                    'Beta County Clerk', 'Beta County, TX', 'STATE OF TEXAS', 'Beta County',
                    'I hereby certify that this Instrument was filed in the File Number sequence on the date/time',
                    'printed hereon, and was duly recorded in the Official Records of', 'Beta County', ', Texas']
            }
        }

        cover_page_return_mail_golden = {
            "pages": 1,
            "content": {
                0: [None, 'Beta County', 'Charlotte Smith', 'Beta County Clerk', 'Instrument Number:',
                    None, 'Real Property Recordings W/Page', 'Recorded On:', None,
                    'Number of Pages:', '2', '" Examined and Charged as Follows: "', 'Total Recording:', '$', '%order_item_price',
                    '*********** THIS PAGE IS PART OF THE INSTRUMENT ***********',
                    'Any provision herein which restricts the Sale, Rental or use of the described REAL PROPERTY',
                    'because of color or race is invalid and unenforceable under federal law.', 'File Information:',
                    'Record and Return To:', 'Document Number:', None, 'Receipt Number:', None,
                    'Recorded Date/Time:', None, 'User:', 'User1 U', 'Station:', 'workstation',
                    'Charlotte Smith', 'Beta County Clerk', 'Beta County, TX', 'STATE OF TEXAS', 'Beta County',
                    'I hereby certify that this Instrument was filed in the File Number sequence on the date/time',
                    'printed hereon, and was duly recorded in the Official Records of', 'Beta County', ', Texas']
            }
        }

        cover_page_edit_golden_file = {
            "pages": 1,
            "content": {
                0: [None, 'Beta County', 'Charlotte Smith', 'Beta County Clerk', 'Instrument Number:', None,
                    'Real Property Recordings W/Page', 'Recorded On:', None, 'Number of Pages:',
                    '3', '" Examined and Charged as Follows: "', 'Total Recording:', '$', '%order_item_price',
                    '*********** THIS PAGE IS PART OF THE INSTRUMENT ***********',
                    'Any provision herein which restricts the Sale, Rental or use of the described REAL PROPERTY',
                    'because of color or race is invalid and unenforceable under federal law.', 'File Information:',
                    'Record and Return To:', 'Document Number:', None, 'Receipt Number:', None,
                    'TestAddress1', 'Recorded Date/Time:', None, 'User:', 'User1 U',
                    'BLUE RIDGE TX 75424-2542', 'Station:', 'workstation', 'Charlotte Smith', 'Beta County Clerk',
                    'Beta County, TX', 'STATE OF TEXAS', 'Beta County',
                    'I hereby certify that this Instrument was filed in the File Number sequence on the date/time',
                    'printed hereon, and was duly recorded in the Official Records of', 'Beta County', ', Texas']
            }
        }

        print_rejection_golden = {
            "pages": 1,
            "content": {
                0: ['Recording Department: 555-555-5555', 'Vital Statistics:\xa0 555-555-5555',
                    'Website:\xa0 www.kofile.com', 'John Doe', 'County Clerk', 'Product Management County Courts',
                    'Building', '6300 Cedar Springs Rd, Dallas, TX', '75235',
                    'Our office has received the above mentioned order.\xa0 We are unable to complete your request for processing due',
                    'to the reason(s) listed below.\xa0 Should you have any questions, please call us at your earliest convenience.',
                    'The attached order is being returned and has NOT been recorded with the County Clerk due to:',
                    'Date:', None, 'To:', 'SIMPLIFILE', '123 Main Street', 'kyiv', ',', 'TX', '04159',
                    'Re: Order #', None, '; Tracking ID', None, 'Test', 'Test', 'ORDER TICKET',
                    '(', 'for clerk reference only)', 'PLEASE DO NOT REMOVE', 'User1 U', ',', 'Deputy Clerk',
                    'Should you have any questions, please contact the undersigned clerk at your earliest convenience.',
                    'User1 U', ', Deputy Clerk', 'Date:', None, 'To:', 'SIMPLIFILE', '123 Main Street',
                    'kyiv', ',', 'TX', '04159', 'Re: Order #', None, '; Tracking ID', None]
            }
        }

        epson_reciept_erProxy_golden = {
            "content": ["BALDWIN COUNTY", "HARRY D'OLIVE", "Cashier ID:", "User1 U", "Status:", "DUPLICATE COPY",
                        "Total Fees:", "Payment Type", "Cash", "Amount", "Company Account", "Total Payment:",
                        "Change:", "Thank You", "Have a nice day"]
        }

        generic_reciept_erProxy_golden = {
            "pages": 1,
            "content": {
                0: ['Order Total', '(', '1', ')', '$', '%order_total', 'Seq', 'Item', 'Document', 'Description',
                    'Number',
                    'Number Of', 'Amount', 'Serial Number', 'GF Number', '1', 'eRecording - Real', 'Property TX', 'AF',
                    None, None, '$', '%order_total', 'Total Payments', 'Change Due', '(', '1', ')', '$', '%order_total',
                    '$',
                    '0.00', 'Seq', 'Payment Method', 'Transaction Id', 'Comment', 'Total', '1', 'Company Account', '$', '%order_total',
                    "For more information about the County Clerk's office and to search property",
                    'records online, please visit www.kofile.com', '1 of 1', 'VoloAutoTest', None,
                    None, 'Charlotte Smith', 'Beta County Clerk', '6300 Cedar Springs Rd',
                    'Dallas, TX 75235', 'Main:', '(555)555-5555', 'Fax:', '(555)555-5555', '%order_num', 'Receipt:',
                    '%order_date', 'Date:', 'Time:', '%order_time', 'By:', 'User1 U', 'Station:', 'workstation',
                    'Status:',
                    'DUPLICATE COPY']
            }
        }

        epson_receipt_duplicate_golden = {
            "content": ["BALDWIN COUNTY", "HARRY D'OLIVE", "Cashier ID:", "User1 U", "Status:", "DUPLICATE COPY",
                        "Total Fees:", "Payment Type", "Cash", "Amount", "Company Account", "Total Payment:",
                        "Change:", "Thank You", "Have a nice day"]
        }

    class uat_ref:
        zebra_label_printer = {
            "content": ["Filed for Record", "in the Official Records Of:", "Reference County", "the PLAT Records",
                        "Doc Number:", "Number of Pages:", "Amount:", "Name_"]
        }

        drawer_summary = {
            "pages": 1,
            "content": {
                0: ['Drawer Balance Summary', 'Expected', 'Actual', 'Difference', 'Cash', None, '$0.00', None,
                    'Cashiers Check', '$0.00', '$0.00', '$0.00', 'Check', '$0.00', '$0.00', '$0.00', 'Credit Card',
                    '$0.00', '$0.00', '$0.00', 'IRS Direct Deposit', '$0.00', '$0.00', '$0.00', 'LegalEase', '$0.00',
                    '$0.00', '$0.00', 'Money Order', '$0.00', '$0.00', '$0.00', 'State Direct Deposit', '$0.00',
                    '$0.00', '$0.00', 'Refund', '$0.00', '$0.00', '$0.00', 'Vital Check', '$0.00', '$0.00', '$0.00',
                    'Void/Refund', '$0.00', '$0.00', '$0.00', 'Over/Short', None, 'Deposit', None,
                    'Beginning Balance', None, 'Actual Balance', None, 'Total Cash', '$0.00', '$0',
                    'Total Non-Cash', '$0.00', '$0', 'Total Voids(0)', '$0.00', 'Drawer Name :', 'Drawer',
                    'Date and Time:', None, 'Printed By:', 'user6 user6', 'Clerk',
                    '______________________________________', 'Administration',
                    '______________________________________', 'Accounting', '______________________________________']
            }
        }

        settle_drawer_summary = {
            "pages": 1,
            "content": {
                0: ['Drawer Balance Summary', 'Expected', 'Actual', 'Difference', 'Cash', '$300.00', '$15912.00',
                    '$-15612.00', 'Cashiers Check', '$0.00', '$0.00', '$0.00', 'Check', '$0.00', '$0.00', '$0.00',
                    'Credit Card', '$0.00', '$0.00', '$0.00', 'IRS Direct Deposit', '$0.00', '$0.00', '$0.00',
                    'LegalEase', '$0.00', '$0.00', '$0.00', 'Money Order', '$0.00', '$0.00', '$0.00',
                    'State Direct Deposit', '$0.00', '$0.00', '$0.00', 'Refund', '$0.00', '$0.00', '$0.00',
                    'Vital Check', '$0.00', '$0.00', '$0.00', 'Void/Refund', '$0.00', '$0.00', '$0.00', 'Over/Short',
                    '$-15612.00', 'Deposit', '$300.00', 'Beginning Balance', '$-300.00', 'Actual Balance', '$15612.00',
                    'Total Cash', '$0.00', '$15912.00', 'Total Non-Cash', '$0.00', '$0.0', 'Total Voids(0)', '$0.00',
                    'Drawer Name :', 'Drawer', 'Date and Time:', None, 'Printed By:', 'user6 user6',
                    'Clerk', '______________________________________', 'Administration',
                    '______________________________________', 'Accounting', '______________________________________']
            }
        }

        cover_page_guest_golden = {
            "pages": 1,
            "content": {
                0: [None, 'Reference County', 'John Doe', 'Reference County Clerk',
                    'Instrument Number:', None, 'Real Property Recordings', 'Recorded On:', None,
                    'Number of Pages:', '2', '" Examined and Charged as Follows: "', 'Total Recording:', '$', '%order_total',
                    '*********** THIS PAGE IS PART OF THE INSTRUMENT ***********',
                    'Any provision herein which restricts the Sale, Rental or use of the described REAL PROPERTY',
                    'because of color or race is invalid and unenforceable under federal law.', 'File Information:',
                    'Record and Return To:', 'Document Number:', None, 'autotest', 'Receipt Number:',
                    '%order_num', None, 'Recorded Date/Time:', None, 'User:',
                    'User1 U', 'SCHENECTADY NY 12345-6789', 'Station:', 'workstation', 'John Doe',
                    'Reference County Clerk', 'Reference County, TX', 'STATE OF TEXAS', 'Reference County',
                    'I hereby certify that this Instrument was filed in the File Number sequence on the date/time',
                    'printed hereon, and was duly recorded in the Official Records of', 'Reference County', ', Texas']
            }
        }

        generic_receipt_original_golden = {
            "pages": 1,
            "content": {
                0: ['Order Total', '(', '1', ')', '$', '%order_total', 'Seq', 'Item', 'Document', 'Description',
                    'Number',
                    'Number Of', 'Amount', 'Serial Number', 'GF Number', '1', 'Real Property', 'Recordings', 'M',
                    None, '2', '$', None, 'Total Payments', 'Change Due', '(', '1', ')', '$', '%order_total', '$',
                    '0.00', 'Seq', 'Payment Method', 'Transaction Id', 'Comment', 'Total', '1', 'Cash', 'TRID11',
                    'comment_1_1', '$', '%order_total',
                    "For more information about the County Clerk's office and to search property",
                    'records online, please visit www.dentoncounty.com/ccl', '1 of 1', 'autotest',
                    'auto tester address', 'SCHENECTADY, NY 12345-6789', 'John Doe', '1450 E McKinney St',
                    'Denton, TX 76209', 'Main:', '(555)555-5555', 'Fax:', '(555)555-5555', '%order_num', 'Receipt:',
                    '%order_date', 'Date:', 'Time:', '%order_time', 'By:', 'User1 U', 'Station:', 'workstation',
                    'Status:',
                    'ORIGINAL COPY', 'Reference County Clerk']
            }
        }

        epson_receipt_original_golden = {
            "content": ["BALDWIN COUNTY", "HARRY D'OLIVE", "Cashier ID:", "User1 U", "Status:", "ORIGINAL COPY",
                        "Total Fees:", "Payment Type", "Cash", "Amount", "Total Payment:",
                        "Change:", "Thank You", "Have a nice day"]
        }

        generic_receipt_duplicate_golden = {
            "pages": 1,
            "content": {
                0: ['Order Total', '(', '1', ')', '$', '%order_total', 'Seq', 'Item', 'Document', 'Description',
                    'Number',
                    'Number Of', 'Amount', 'Serial Number', 'GF Number', '1', 'Real Property', 'Recordings', 'M',
                    None, '2', '$', None, 'Total Payments', 'Change Due', '(', '1', ')', '$', '%order_total', '$',
                    '0.00', 'Seq', 'Payment Method', 'Transaction Id', 'Comment', 'Total', '1', 'Cash', 'TRID11',
                    'comment_1_1', '$', '%order_total',
                    "For more information about the County Clerk's office and to search property",
                    'records online, please visit www.dentoncounty.com/ccl', '1 of 1', 'autotest',
                    'auto tester address', 'SCHENECTADY, NY 12345-6789', 'John Doe', '1450 E McKinney St',
                    'Denton, TX 76209', 'Main:', '(555)555-5555', 'Fax:', '(555)555-5555', '%order_num', 'Receipt:',
                    '%order_date', 'Date:', 'Time:', '%order_time', 'By:', 'User1 U', 'Station:', 'workstation',
                    'Status:',
                    'DUPLICATE COPY', 'Reference County Clerk']
            }
        }

        generic_receipt_adjusted_golden = {
            "pages": 1,
            "content": {
                0: ['Order Total', '(', '1', ')', '$', '%order_total', 'Seq', 'Item', 'Document', 'Description',
                    'Number',
                    'Number Of', 'Amount', 'Serial Number', 'GF Number', '1', 'Real Property', 'Recordings', 'M',
                    None, '3', '$', None, 'Total Payments', 'Change Due', '(', '2', ')', '$', '%order_total', '$',
                    '0.00', 'Seq', 'Payment Method', 'Transaction Id', 'Comment', 'Total', '1', 'Cash', 'TRID11',
                    'comment_1_1', '$', None, '2', 'Refund', 'some_comment_1', '$', '%order_total',
                    "For more information about the County Clerk's office and to search property",
                    'records online, please visit www.dentoncounty.com/ccl', '1 of 1', 'autotest',
                    'auto tester address', 'SCHENECTADY, NY 12345-6789', 'John Doe', '1450 E McKinney St',
                    'Denton, TX 76209', 'Main:', '(555)555-5555', 'Fax:', '(555)555-5555', '%order_num', 'Receipt:',
                    '%order_date', 'Date:', 'Time:', '%order_time', 'By:', 'User1 U', 'Station:', 'workstation',
                    'Status:',
                    'ADJUSTED COPY', 'Reference County Clerk']
            }
        }

        epson_receipt_adjusted_golden = {
            "content": ["BALDWIN COUNTY", "HARRY D'OLIVE", "Cashier ID:", "User1 U", "Status:", "ADJUSTED COPY",
                        "Total Fees:", "Payment Type", "Cash", "Amount", "Company Account", "Total Payment:",
                        "Change:", "Thank You", "Have a nice day"]
        }

        cover_page_email_golden = {
            "pages": 1,
            "content": {
                0: [None, 'Reference County', 'John Doe', 'Reference County Clerk',
                    'Instrument Number:', None, 'Real Property Recordings', 'Recorded On:', None,
                    'Number of Pages:', '2', '" Examined and Charged as Follows: "', 'Total Recording:', '$', '%order_total',
                    '*********** THIS PAGE IS PART OF THE INSTRUMENT ***********',
                    'Any provision herein which restricts the Sale, Rental or use of the described REAL PROPERTY',
                    'because of color or race is invalid and unenforceable under federal law.', 'File Information:',
                    'Record and Return To:', 'Document Number:', None, 'ReturnByMailCustomerName', 'Receipt Number:',
                    '%order_num', None, 'Recorded Date/Time:', None, 'User:',
                    'User1 U', 'SCHENECTADY NY 12345-6789', 'Station:', 'workstation', 'John Doe',
                    'Reference County Clerk', 'Reference County, TX', 'STATE OF TEXAS', 'Reference County',
                    'I hereby certify that this Instrument was filed in the File Number sequence on the date/time',
                    'printed hereon, and was duly recorded in the Official Records of', 'Reference County', ', Texas']
            }
        }

        cover_page_return_mail_golden = {
            "pages": 1,
            "content": {
                0: [None, 'Reference County', 'John Doe', 'Reference County Clerk',
                    'Instrument Number:', None, 'Real Property Recordings', 'Recorded On:', None,
                    'Number of Pages:', '2', '" Examined and Charged as Follows: "', 'Total Recording:', '$', '%order_total',
                    '*********** THIS PAGE IS PART OF THE INSTRUMENT ***********',
                    'Any provision herein which restricts the Sale, Rental or use of the described REAL PROPERTY',
                    'because of color or race is invalid and unenforceable under federal law.', 'File Information:',
                    'Record and Return To:', 'Document Number:', None, 'Receipt Number:', None,
                    'Recorded Date/Time:', None, 'User:', 'User1 U', 'Station:', 'workstation',
                    'John Doe', 'Reference County Clerk', 'Reference County, TX', 'STATE OF TEXAS', 'Reference County',
                    'I hereby certify that this Instrument was filed in the File Number sequence on the date/time',
                    'printed hereon, and was duly recorded in the Official Records of', 'Reference County', ', Texas']
            }
        }

        cover_page_edit_golden_file = {
            "pages": 1,
            "content": {
                0: [None, 'Reference County', 'John Doe', 'Reference County Clerk',
                    'Instrument Number:', None, 'Real Property Recordings', 'Recorded On:', None,
                    'Number of Pages:', '3', '" Examined and Charged as Follows: "', 'Total Recording:', '$', '%order_total',
                    '*********** THIS PAGE IS PART OF THE INSTRUMENT ***********',
                    'Any provision herein which restricts the Sale, Rental or use of the described REAL PROPERTY',
                    'because of color or race is invalid and unenforceable under federal law.', 'File Information:',
                    'Record and Return To:', 'Document Number:', None, 'Receipt Number:', None,
                    'Recorded Date/Time:', None, 'User:', 'User1 U', 'Station:', 'workstation',
                    'John Doe', 'Reference County Clerk', 'Reference County, TX', 'STATE OF TEXAS', 'Reference County',
                    'I hereby certify that this Instrument was filed in the File Number sequence on the date/time',
                    'printed hereon, and was duly recorded in the Official Records of', 'Reference County', ', Texas']
            }
        }

        print_rejection_golden = {
            "pages": 1,
            "content": {
                0: ['Recording Department: 555-555-5555', 'Vital Statistics:\xa0 555-555-5555',
                    'Website:\xa0 www.kofile.com', 'John Doe', 'County Clerk', 'Reference County Courts Building',
                    '6300 Cedar Springs Rd, Dallas, TX', '75235',
                    'Our office has received the above mentioned order.\xa0 We are unable to complete your request for processing due',
                    'to the reason(s) listed below.\xa0 Should you have any questions, please call us at your earliest convenience.',
                    'The attached order is being returned and has NOT been recorded with the County Clerk due to:',
                    'Date:', None, 'To:', 'VoloAutoTest', 'DFDF', 'Yerevan', ',', 'KS', '11111-1111',
                    'Re: Order #', None, '; Tracking ID', None, 'Test', 'Test', 'ORDER TICKET',
                    '(', 'for clerk reference only)', 'PLEASE DO NOT REMOVE', 'User1 U', ',', 'Deputy Clerk',
                    'Should you have any questions, please contact the undersigned clerk at your earliest convenience.',
                    'User1 U', ', Deputy Clerk', 'Date:', None, 'To:', 'VoloAutoTest', 'DFDF', 'Yerevan',
                    ',', 'KS', '11111-1111', 'Re: Order #', None, '; Tracking ID', None]
            }
        }

        generic_reciept_erProxy_golden = {
            "pages": 1,
            "content": {
                0: ['Order Total', '(', '1', ')', '$', '%order_total', 'Seq', 'Item', 'Document', 'Description',
                    'Number',
                    'Number Of', 'Amount', 'Serial Number', 'GF Number', '1', 'Real Property', 'Recordings W/Page', 'M',
                    None, None, '$', '%order_total', '200-RM', 'Records Management', '$', None, '300-RA',
                    'Records Archive Fee', '$', None, '400-CS', 'Courthouse Security', '$', None, '100-Recording',
                    'Recording Fees', '$', None, 'Total Payments', 'Change Due', '(', '1', ')', '$', '%order_total',
                    '$',
                    '0.00', 'Seq', 'Payment Method', 'Transaction Id', 'Comment', 'Total', '1', 'Cash', 'TRID11',
                    'comment_1_1', '$', '%order_total',
                    "For more information about the County Clerk's office and to search property",
                    'records online, please visit www.kofile.com', '1 of 1', 'voloautomationtest', 'TestAddress1',
                    'New York, NY 75424-2542', 'Charlotte Smith', 'Beta County Clerk', '6300 Cedar Springs Rd',
                    'Dallas, TX 75235', 'Main:', '(555)555-5555', 'Fax:', '(555)555-5555', '%order_num', 'Receipt:',
                    '%order_date', 'Date:', 'Time:', '%order_time', 'By:', 'User1 U', 'Station:', 'workstation',
                    'Status:',
                    'DUPLICATE COPY']
            }
        }

        epson_reciept_erProxy_golden = {
            "content": ["BALDWIN COUNTY", "HARRY D'OLIVE", "Cashier ID:", "User1 U", "Status:", "DUPLICATE COPY",
                        "Total Fees:", "Payment Type", "Cash", "Amount", "Total Payment:",
                        "Change:", "Thank You", "Have a nice day"]
        }

        epson_receipt_duplicate_golden = {
            "content": ["BALDWIN COUNTY", "HARRY D'OLIVE", "Cashier ID:", "User1 U", "Status:", "DUPLICATE COPY",
                        "Total Fees:", "Payment Type", "Cash", "Amount", "Total Payment:",
                        "Change:", "Thank You", "Have a nice day"]
        }

    class cuyahoga_county:
        epson_reciept_erProxy_golden = {
            "content": ["Cuyahoga County", "Michael Chambers", "Cashier ID:", "User1 U", "Status:", "DUPLICATE COPY",
                        "Total Fees:", "Payment Type", "Cash", "Amount", "Company Account", "Total Payment:",
                        "Change:", "Thank You", "Have a nice day"]
        }

    class qa_ref:
        zebra_label_printer = {
            "content": ["Filed for Record", "in the Official Records Of:", "Reference County", "the PLAT Records",
                        "Doc Number:", "Number of Pages:", "Amount:", "Name_"]
        }
