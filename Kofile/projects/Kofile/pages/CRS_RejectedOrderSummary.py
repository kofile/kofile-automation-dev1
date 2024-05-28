"""Order Search -> Reject Order Summary Page"""

from projects.Kofile.Lib.test_parent import PagesParent


class CRSRejectedOrderSummary(PagesParent):
    doc_number = "documentNumber"

    def __init__(self):
        super(CRSRejectedOrderSummary, self).__init__()

# ---------------------------------------------
# breadcrumb
# ---------------------------------------------


    lbl_rej_order_summary_breadcrumb = (
        'xpath',
        '// li[contains(text(), "Rejected Order Summary")]',
        'order Search-> Rejected Order Summary breadcrumb')
