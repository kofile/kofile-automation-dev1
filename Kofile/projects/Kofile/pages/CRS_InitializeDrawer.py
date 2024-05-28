# ---------------------------------------------
# DrawerInitializationTable
# ---------------------------------------------
from projects.Kofile.Lib.test_parent import PagesParent


class CRSInitializeDrawer(PagesParent):
    def __init__(self):
        super(CRSInitializeDrawer, self).__init__()

    txt_itit_amount = (
        "xpath",
        "(.//*[@id='cashDrawerInitializationTable']//following-sibling::input)[1]",
        "Drawer Ininialization amount field")
    btn_submit = (
        "id",
        "submitInitializeDrawer",
        "Drawer Initialization Submit button")
    btn_cancel = (
        "id",
        "cancelinitializeDrawer",
        "Drawer Initialization Cancel button")
    lbl_workstation_name = (
        "xpath",
        ".//*[@id='cashDrawerInitializationTable']/div/div[3]/div[1]",
        "Drawer Initialization workstation name")
    btn_submit_inactive_id = (
        "xpath",
        "//input[@id='submitInitializeDrawer1' or @id='submitInitializeDrawer']",
        "Submit button for inactive id when initialize drawer in the second time")
    btn_admin_key = (
        "xpath",
        ".//*[@id='successmessage']/following::a",
        "Admin Key icon")
    _lbl_workstation_name_by_row_number = (
        "xpath",
        ".//*[@id='drawerlist']/div[%s]/div[1]/label",
        "Workstation name in Drawer Initialization")
    _cbx_workstation_checkbox_by_row_number = (
        "xpath",
        "(.//*[@id='drawerlist']//input[@type='checkbox'])[%s]",
        "Checkbox next to workstation name")
    # ---------------------------------------------
    # postedDatesBlock
    # ---------------------------------------------

    txt_postdate_field = (
        "xpath",
        ".//*[@id='PostDate']",
        "Drawer Initialization Date field ")

    btn_search = (
        "xpath",
        "//*[@id='PostDate']/following::input",
        "Drawer Initialization Search button")
    cbx_drawer_checkbox = (
        "xpath",
        ".//*[@id='sessionlist']//input[@type='checkbox']",
        "Drawer Initialization drawer checkbox")
    btn_submit_PostedDate = (
        "xpath",
        ".//*[@id='submitPostedDate']",
        "Submit Posted Date")
    lbl_search_result_message = (
        "xpath",
        ".//*[@id='successPostMessage']",
        "Search result message text")

    # ---------------------------------------------
    # postedDatesBlock
    # ---------------------------------------------
    btn_ok_on_warning_popup = (
        "id",
        "infobox_Ok",
        "Ok Button on warning popup")
