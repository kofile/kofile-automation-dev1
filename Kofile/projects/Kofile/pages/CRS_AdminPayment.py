"""Admin Payment Page"""

from projects.Kofile.Lib.test_parent import PagesParent


class AdminPayment(PagesParent):
    def __init__(self):
        super(AdminPayment, self).__init__()

    # ---------------------------------------------
    # breadcrumb
    # ---------------------------------------------

    lbl_admin_payment_breadcrumb = (
        'xpath',
        '//*[@class="bredcrum"]/ul/li[contains(text(), "Admin Payment")]',   # noqa
        'Admin Payment Screen breadcrumb')

    # ---------------------------------------------
    # payment grid
    # ---------------------------------------------

    lbl_processing_fee = (
        'xpath',
        '// li[contains(text(), "Processing Fee ")]',
        'Processing Fee Label')

    lbl_processing_fee_amount = (
        "id",
        "ProcessingFee",
        "Processing fee amount")
