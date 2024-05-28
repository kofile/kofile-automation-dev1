from projects.Kofile.Lib.general_helpers import GeneralHelpers
from projects.Kofile.Lib.testdata_helpers import ClerkSearchTestDataHelpers
from projects.Kofile.Lib.work_with_files import Files
from projects.Kofile.Lib.CRS.AddPayment_functions import AddPayment, order_finalization
from projects.Kofile.Lib.CRS.AdminPayment_functions import AdminPayment
from projects.Kofile.Lib.CRS.BalanceDrawer_functions import BalanceDrawer
from projects.Kofile.Lib.CRS.FrontOffice_functions import FrontOffice
from projects.Kofile.Lib.CRS.ImageViewer_functions import ImageViewer
from projects.Kofile.Lib.CRS.IndexingEntry_functions import capture, OrderEntry_functions
from projects.Kofile.Lib.CRS.IndexingQueue_functions import IndexingQueue, CRS_functions
from projects.Kofile.Lib.CRS.IndexingSummary_functions import IndexingSummary
from projects.Kofile.Lib.CRS.OIT_functions import OIT, IndexingEntry_functions
from projects.Kofile.Lib.CRS.OrderPackage_functionsy import OrderPackage
from projects.Kofile.Lib.CRS.OrderQueue_functions import OrderQueue
from projects.Kofile.Lib.CRS.OrderSearch_functions import OrderSearch
from projects.Kofile.Lib.CRS.OrderEntry_functions import crs_required_fields
from projects.Kofile.Lib.CRS.OrderSummary_functions import OrderSummary
from projects.Kofile.Lib.CRS.PackageSearch_functions import PackageSearch
from projects.Kofile.Lib.CRS.VerificationEntry_functions import VerificationEntry
from projects.Kofile.Lib.CRS.VerificationQueue_functions import VerificationQueue
from projects.Kofile.Lib.CRS.VerificationSummary_functions import VerificationSummary
from projects.Kofile.Lib.CRS.VoidOrderPayment_functions import VoidOrderPayment, OrderHeader_functions
from projects.Kofile.Lib.CRS.VoidOrderSummary_functions import VoidOrderSummary
from projects.Kofile.Lib.KS.KS_functions import KS
from projects.Kofile.Lib.PS_CS.CS_functions import CS
from projects.Kofile.Lib.PS_CS.PS_functions import PS
from projects.Kofile.Lib.PS_CS.PS_mainpage import PSMainPage, ps_inbox
from projects.Kofile.Lib.PS_CS.PS_preview import PSPreview
from projects.Kofile.Lib.PS_CS.PS_summarytab import PSSummaryTab
from projects.Kofile.Lib.Azure import AzureBlobStorage
from projects.Kofile.Lib.DB import DB, DataBaseWithVPN
from projects.Kofile.Lib.Image_Recognition import ImageRecognition


class Lib:
    def __init__(self, data):
        self.azure = AzureBlobStorage(data)
        self.db = DB(data)
        self.db_with_vpn = self.db_vpn = DataBaseWithVPN(data)
        self.data_helper = ClerkSearchTestDataHelpers()
        self.general_helper = GeneralHelpers()
        self.required_fields = crs_required_fields
        self.files = Files()
        self.image_recognition = ImageRecognition()
        self.CRS = self.__CRS()
        self.KS = self.__KS()
        self.CS = self.__CS()
        self.PS = self.__PS()

    class __CRS:
        def __init__(self):
            self.add_payment = AddPayment()
            self.admin_payments = AdminPayment()
            self.balance_drawer = BalanceDrawer()
            self.capture = capture
            self.crs = CRS_functions
            self.front_office = FrontOffice()
            self.image_viewer = ImageViewer()
            self.indexing_entry = IndexingEntry_functions
            self.indexing_queue = IndexingQueue()
            self.indexing_summary = IndexingSummary()
            self.order_item_type = OIT()
            self.order_entry = OrderEntry_functions
            self.order_finalization = order_finalization
            self.order_header = OrderHeader_functions
            self.order_package = OrderPackage()
            self.order_queue = OrderQueue()
            self.order_search = OrderSearch()
            self.order_summary = OrderSummary()
            self.package_search = PackageSearch()
            self.verification_entry = VerificationEntry()
            self.verification_queue = VerificationQueue()
            self.verification_summary = VerificationSummary()
            self.void_order_payment = VoidOrderPayment()
            self.void_order_summary = VoidOrderSummary()

    class __KS:
        def __init__(self):
            self.general = KS()

    class __CS:
        def __init__(self):
            self.general = CS()

    class __PS:
        def __init__(self):
            self.general = PS()
            self.ps_inbox = ps_inbox
            self.ps_main_page = PSMainPage()
            self.ps_preview = PSPreview()
            self.ps_summary_tab = PSSummaryTab()
