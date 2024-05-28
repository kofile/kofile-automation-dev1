"""
Front Office -> Financial -> NSF Names Page Object Model
"""
from projects.Kofile.Lib.test_parent import PagesParent


class CRSFrontOfficeNSFNames(PagesParent):
    def __init__(self):
        super(CRSFrontOfficeNSFNames, self).__init__()

    nsf_names_breadcrumb = (
        "xpath",
        "//div[@class='bredcrum']//li[text()='NSF Names']",                # noqa
        "NSF Names breadcrumb")
    # --------------------------------
    # NSF Name - Search grid
    # --------------------------------
    lookup_nsf_name = (
        "id",
        "NSFName",
        "NSF Name lookup field")
    lnk_nsf_new_row = (
        "id",
        "newRow",
        "New Row action link - NSF Names")
    btn_search = (
        "id",
        "searchNSFName",
        "NSF Name Search button")
    # --------------------------------
    # New NSF Name Entry form
    # --------------------------------
    txt_nsf_name = (
        "id",
        "nsf-name-field",
        "NSF Name input field")
    txt_check_number = (
        "id",
        "nsf-checknum-field",                                             # noqa
        "Check Number input field - NSF Names")
    txt_check_amount = (
        "id",
        "nsf-checkamount-field",                                          # noqa
        "Check Amount input field - NSF Names")
    txt_check_date = (
        "id",
        "nsf-checkdate-field",                                            # noqa
        "Check Date input field - NSF Names")
    txt_order_number = (
        "id",
        "nsf-ordernum-field",                                             # noqa
        "Order_Number input field - NSF Names")
    chx_active = (
        "id",
        "nsf-active-field",
        "Active checkbox - NSF Names")
    btn_save = (
        "xpath",
        "//input[@type='submit' and @value='Save']",
        "Save button - NSF Names")
    # --------------------------------
    # NSF Name - Search results table
    # --------------------------------
    td_nsf_names = (
        "xpath",
        "//td[@class='nsfNameField']/input",
        "NSF Name column value in search results table")
