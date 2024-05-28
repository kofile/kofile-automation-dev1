"""
Image Viewer Page Object Model
"""
# ---------------------------------------------
# ICONS
# ---------------------------------------------
from projects.Kofile.Lib.test_parent import PagesParent


class CRSImageViewer(PagesParent):
    def __init__(self):
        super(CRSImageViewer, self).__init__()

    icn_redaction = (
        "id",
        "enableRedacted",
        "Redaction icon of image viewer"
    )
    icn_restore_redaction = (
        "id",
        "restoreRedacted",
        "Restore Redaction icon of image viewer"
    )
    print_image_container = (
        "id",
        "printImageContainer",
        "Print Image Container of image viewer"
    )
    icn_crop = (
        "id",
        "crop",
        "Crop icon in image viewer"
    )
    icn_restore_crop = (
        "id",
        "restoreCrop",
        "Restore Crop icon in image viewer"
    )
    btn_print_icon = (
        "xpath",
        "//a[@id='printImages' and @class='printImages previewbt']",
        "Print Icon in image viewer"
    )
    icn_C1 = (
        "id",
        "clerk1stamp",
        "C1 stamp icon"
    )
    icn_C2 = (
        "id",
        "clerk2stamp",
        "C2 stamp icon"
    )
    icn_C3 = (
        "id",
        "clerk3stamp",
        "C3 stamp icon"
    )
    icn_page_edit = (
        "id",
        "pageedit",
        "Page Edit icon in image viewer"
    )
    icn_rotate_right = (
        "xpath",
        "//a[@id='rotateRight' and @class='rotateRight previewbt']",
        "Rotate Right icon"
    )
    icn_rotate_left = (
        "xpath",
        "//a[@id='rotateLeft' and @class='rotateLeft previewbt']",
        "Rotate Left icon"
    )
    # ---------------------------------------------
    image_viewer_spinner = (
        "xpath",
        "//div[@class='ajax-overlay-under-popups']",
        "Image viewer spinner"
    )
    btn_print_style = (
        "xpath",
        "//a[@id='printImages' and @class='printImages previewbt']/..",
        "Print Icon display/not display style "
    )
    lnk_print = (
        "id",
        "widget-kofileinfobubble-printui-id1",
        "print link"
    )
    pup_print_dialog = (
        "xpath",
        "//div[@id='dialog-content-holder']//div[@class='dialog-title-left']",
        "print_popup_title"
    )
    pup_print_dialog_content = (
        "xpath",
        "//div[@class='docImageInfoboxContent']",
        "Print popup content"
    )
    btn_close_pup_print = (
        "id",
        "infobox_Close",
        "close button on printing popup"
    )
    image_container = (
        "xpath",
        "//div[@id='eStampCropImageContainer']//img[@class='under']",
        "Image in image viewer "
    )
    redaction_box = (
        "xpath",
        "//span[@class='vtip']",
        "Redaction box"
    )
    image_src = (
        "xpath",
        "//div[@id='singleImageContainer']/img",
        "Image source"
    )
    custom_stamp_box = (
        "xpath",
        "//div[@id='eStampCropImageContainer']//following-sibling::div",
        "C1 stamp box"
    )
    image = (
        "xpath",
        "//div[contains(@class, 'cropper-container')]/img",
        "Image in Image Container"
    )
    cropper = (
        "xpath",
        "//div[@class='cropper-cropbox']//following::span[@class='cropper-point point-n']",
        "Cropper"
    )
    cropped_box = (
        "xpath",
        "//div[@class='cropper-cropbox']",
        "Crop box"
    )
    btn_move_to_last_page = (
        "id",
        "moveLast",
        "Button Move to last page"
    )

    icn_dock_viewer = (
        "id",
        "dockViewerButton",
        "Dock Viewer Button"
    )

    lbl_total_images = (
        "id",
        "totalImages",
        "Image Viewer Total Images"
    )

    page_number_input = (
        "id",
        "imagePaging",
        "Page number input"
    )

    txt_docked_img_text = (
        "id",
        "dockedText",
        "Docked Image Text"
    )

    single_image_viewer_container = ("id", "singleImageContainer", "Image single viewer")
    estamp_image_viewer_container = ("id", "eStampImageContainer", "Image single viewer")
    eStamp_button = ("id", "eStamp", "Edit stamps button")
    eStampCancel_button = ("id", "eStampCancel", "Cancel stamps button")
    remove_stamp_button = ("id", "removeStamp", "Remove stamps button")
    image_viewer_container = ("id", "imageContainer", "Image viewer")
    zoom_in_button = ("id", "zoomIn", "Zoom in button")
    zoom_out_button = ("id", "zoomOut", "Zoom out button")
    fit_width_button = ("id", "fitWidth", "Fit width button")
    fit_height_button = ("id", "fitHeight", "Fit height button")
    print_rotated_image = ("id", "printRotatedImage", "Print rotated image button")
    preview_viewer_block = ("id", "previewviewerBlock", "Image viewer")
    fit_best_button = ("id", "fit", "Fit best button")
    multidoc_button = ("id", "multidoc", "Multi doc button")
    multi_selectdoc_button = ("id", "multiselectdoc", "Multi select doc button")
    multi_selectdoc_delete_button = ("id", "deleteSelectedPages", "Multi select doc delete button")
    multi_selectdoc_split_button = ("id", "splitDocument", "Multi select doc split button")
    multi_selectdoc_rollback_button = ("id", "rollbackMultiselect", "Multi select doc rollback button")
    thumbnail_image_container_button = ("id", "thumbnailImageContainer", "Thumbnail Image Container button")
    image_maintenance_tool_button = ("id", "ImageMaintenanceTool", "Image Maintenance Tool button")
    deskew_checkbox = ("id", "deskew", "Deskew checkbox")
    print_document_success = ("id", "print-document-success", "Print dialog content wrapper")
    image_information_button = ("id", "imageInformation", "Image Information button")
    un_do_page_edit_button = ("id", "undopageedit", "Un do page edit button")
    print_option_bubble_imageCont = ("id", "printOptionBubbleImageCont", "Print image preview container")
    apply_error_button = ("id", "YesButtonId", "Apply error button")
    infobox_yes_button = ("id", "infobox_Yes", "Infobox Yes button")
    set_secured_document_content_button = ("id", "setSecuredDocumentContent", "Secure document button")
    restore_secured_document_content_button = ("id", "secureddoc", "Restore secure document button")
    thumbnail_pages = ("xpath", "//img[@alt='Thumbnail']", "Thumbnail pages")
    middle_left_pages = ("xpath", "//div[@class='middleLeft']/a", "Scan before")
    middle_right_pages = ("xpath", "//div[@class='middleRight']/a", "Scan after")
    btn_insert_after = ("xpath", "//a[@class='btnInsertAfter']", "Insert after button")
    btn_insert_before = ("xpath", "//a[@class='btnInsertBefore']", "Insert before button")
    btn_thumb_delete_page = ("xpath", "//a[@class='btnThumbDeletePage']", "Delete page button")
    btn_switch_to_image_details = ("xpath", "//a[@class='btnThumbSwitchToImageDetails']", "Image details button")
    multi_selectdoc_checkbox = ("xpath", "//div[@class='thumbnailSelection']/a", "Multi doc checkbox")
    select_all_button = ("xpath", "//li[text()='Select All']", "Select all button")
    de_select_all_button = ("xpath", "//li[text()='DeSelect All']", "Deselect all button")
    close_modal = ("xpath", "//a[@title='Close']", "Close modal window button")
    any_img = ("xpath", "//img", "Any img")
    print_image = ("id", "printOptionBubbleImage", "print image")
    print_width = ("xpath", "//div[contains(@class, 'widthBorderText')]/span", "Print preview width")
    print_height = ("xpath", "//div[contains(@class, 'heightBorderText')]/span", "Print preview height")
    first_oit_on_show_order_finalization = (
    "xpath", '//table[@id="orderSummary"]/tbody/tr', "First OIT on Show Order Fina lization")
    margin_top = ("xpath", "//input[@name='actionOptions1' and @value='%s']", "Margin top radiobutton")
    margin_left = ("xpath", "//input[@name='actionOptions2' and @value='%s']", "Margin left radiobutton")
    margin_right = ("xpath", "//input[@name='actionOptions4' and @value='%s']", "Margin right radiobutton")
    margin_bottom = ("xpath", "//input[@name='actionOptions3' and @value='%s']", "Margin bottom radiobutton")
