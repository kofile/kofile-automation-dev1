"""
Edit Order Item Page Object Model
"""
from projects.Kofile.Lib.test_parent import PagesParent


class CRSEditOrderItem(PagesParent):
    def __init__(self):
        super(CRSEditOrderItem, self).__init__()

    lnk_start_capture_to_scan_attachments = ("id", "scanAttachmentsButton", "Scan Attachment link")
    lbl_attached_filename = ("xpath", "//li[@class='attahchmentRow']/div", "Additional Image filename")
