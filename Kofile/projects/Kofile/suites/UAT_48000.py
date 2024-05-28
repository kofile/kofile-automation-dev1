

browsers = [
    'chrome'
]

environments = [
    'uat_ref'
]

tags = [
    'regression'
]

processes = 1

tests = [
    '64289_75294_Balance_Drawer.*',
    '64290_Ordering.*',
    '64297_Fee_Calculation.*',
    '64298_Fund_Distribution.*',
    '64299_Void.*',
    '64302_Capture.64303_Capture.*',
    '64302_Capture.64305_Historical_Capture.*',
    '64302_Capture.64306_Prep_ML_Capture.*',
    '64302_Capture.64308_Capture_Review.*',
    '64310_Indexing.*',
    '64315_Verification.*',
    '64319_Front_Office.*',
    '64320_erProxy.*',
    '64321_eForms.*',
    '64322_Image_Viewer.*',
    '64323_CRS_Search.*',
    '64326_Clerk_Search.*',
    '64327_Public_Search.*',
    '64328_Kiosk_Search.*',
    '74984_Printing.*',
    'release_3_10.US_62889.capture_and_map',
    'release_3_10.US_62889.capture_review',
    'release_3_10.US_62889.capture_with_cover_page',
    'release_3_10.US_62889.finalize_order',
    'release_3_10.US_62889.load_capture_cover',
    'release_3_10.US_62889.load_failed_cover',
    'release_3_10.US_62889.load_finalize',
    'release_3_10.US_62889.load_finalize_manual_capture',
    'release_3_10.US_62889.order_summary',
    'release_3_10.US_62889.process_order_with_capture',
    'release_3_10.US_62889.scan_utils',
    'release_3_10.US_62889.test_data',
    'release_3_10.US_62889.timing',
    'self_test.*',
    'add_rerun_tag',
    'remove_rerun_tag'
]
