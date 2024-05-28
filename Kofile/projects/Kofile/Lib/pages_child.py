from projects.Kofile.pages.CRS_AddPayment import AddPayment
from projects.Kofile.pages.CRS_AdminPayment import AdminPayment
from projects.Kofile.pages.CRS_BalanceDrawer import CRSBalanceDrawer
from projects.Kofile.pages.CRS_CaptureQueue import CRSCaptureQueue
from projects.Kofile.pages.CRS_CaptureSummary import CRSCaptureSummary
from projects.Kofile.pages.CRS_EditOrderItem import CRSEditOrderItem
from projects.Kofile.pages.CRS_Fields import CRSFields
from projects.Kofile.pages.CRS_FrontOffice import CRSFrontOffice
from projects.Kofile.pages.CRS_FrontOfficeNSFNames import CRSFrontOfficeNSFNames
from projects.Kofile.pages.CRS_General import General
from projects.Kofile.pages.CRS_Image_viewer import CRSImageViewer
from projects.Kofile.pages.CRS_IndexingEntry import CRSIndexingEntry
from projects.Kofile.pages.CRS_IndexingQueue import CRSIndexingQueue
from projects.Kofile.pages.CRS_IndexingSummary import CRSIndexingSummary
from projects.Kofile.pages.CRS_Initialization import CRSInitialization
from projects.Kofile.pages.CRS_InitializeDrawer import CRSInitializeDrawer
from projects.Kofile.pages.CRS_Login import Login
from projects.Kofile.pages.CRS_OrderData import CRSOrderData
from projects.Kofile.pages.CRS_OrderEntry import CRSOrderEntry
from projects.Kofile.pages.CRS_OrderFinalization import CRSOrderFinalization
from projects.Kofile.pages.CRS_OrderHeader import CRSOrderHeader
from projects.Kofile.pages.CRS_OrderQueue import CRSOrderQueue
from projects.Kofile.pages.CRS_OrderSearch import CRSOrderSearch
from projects.Kofile.pages.CRS_OrderSummary import CRSOrderSummary
from projects.Kofile.pages.CRS_PackageSearch import CRSPackageSearch
from projects.Kofile.pages.CRS_RejectedOrderSummary import CRSRejectedOrderSummary
from projects.Kofile.pages.CRS_UploadPopup import CRSUploadPopup
from projects.Kofile.pages.CRS_VerificationEntry import CRSVerificationEntry
from projects.Kofile.pages.CRS_VerificationQueue import CRSVerificationQueue
from projects.Kofile.pages.CRS_VerificationSummary import CRSVerificationSummary
from projects.Kofile.pages.CRS_VoidOrderPayment import CRSVoidOrderPayment
from projects.Kofile.pages.CRS_VoidOrderSummary import CRSVoidOrderSummary
from projects.Kofile.pages.CS_MainPage import CSMainPage
from projects.Kofile.pages.Eform import EForm
from projects.Kofile.pages.KS_Homepage import KSHomepage
from projects.Kofile.pages.PS_portal import PSPortal
from projects.Kofile.pages.PS_psattachmentstab import PSAttachmentsTab
from projects.Kofile.pages.PS_psimagetab import PSImageTab
from projects.Kofile.pages.PS_psinbox import PSInbox
from projects.Kofile.pages.PS_psmainpage import PSMainPage
from projects.Kofile.pages.PS_psppcart import PSPpCart
from projects.Kofile.pages.PS_psppinit import PSPrint
from projects.Kofile.pages.PS_pspppayment import PSPayment
from projects.Kofile.pages.PS_pspreview import PSPreview
from projects.Kofile.pages.PS_pssummarytab import PSSummaryTab
from projects.Kofile.pages.yopmail import YOPMail


class Pages:
    def __init__(self, data):
        self.__data = data
        self.eform = EForm()
        self.mail = YOPMail()
        self.CRS = self.__CRS()
        self.KS = self.__KS()
        self.CS = self.__CS()
        self.PS = self.__PS()

    class __CRS:
        def __init__(self):
            self.add_payment = AddPayment()
            self.admin_payment = AdminPayment()
            self.balance_drawer = CRSBalanceDrawer()
            self.capture_queue = CRSCaptureQueue()
            self.capture_summary = CRSCaptureSummary()
            self.edit_order_item = CRSEditOrderItem()
            self.fields = CRSFields()
            self.front_office = CRSFrontOffice()
            self.fo_nsf_names = CRSFrontOfficeNSFNames()
            self.general = General()
            self.image_viewer = CRSImageViewer()
            self.indexing_entry = CRSIndexingEntry()
            self.indexing_queue = CRSIndexingQueue()
            self.indexing_summary = CRSIndexingSummary()
            self.initialization = CRSInitialization()
            self.initialize_drawer = CRSInitializeDrawer()
            self.login = Login()
            self.order_data = CRSOrderData()
            self.order_entry = CRSOrderEntry()
            self.order_finalization = CRSOrderFinalization()
            self.order_header = CRSOrderHeader()
            self.order_queue = CRSOrderQueue()
            self.order_search = CRSOrderSearch()
            self.order_summary = CRSOrderSummary()
            self.package_search = CRSPackageSearch()
            self.rejected_order_summary = CRSRejectedOrderSummary()
            self.verification_entry = CRSVerificationEntry()
            self.verification_queue = CRSVerificationQueue()
            self.verification_summary = CRSVerificationSummary()
            self.void_order_payment = CRSVoidOrderPayment()
            self.up = self.upload_popup = CRSUploadPopup()
            self.void_order_summary = CRSVoidOrderSummary()

    class __CS:
        def __init__(self):
            self.main_page = CSMainPage()

    class __KS:
        def __init__(self):
            self.home_page = KSHomepage()

    class __PS:
        def __init__(self):
            self.portal = PSPortal()
            self.attachments_tab = PSAttachmentsTab()
            self.image_tab = PSImageTab()
            self.inbox = PSInbox()
            self.main_page = PSMainPage()
            self.cart = PSPpCart()
            self.pprint = PSPrint()
            self.payment = PSPayment()
            self.preview = PSPreview()
            self.summary_tab = PSSummaryTab()
