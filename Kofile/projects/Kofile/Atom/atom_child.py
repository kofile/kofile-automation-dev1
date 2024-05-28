from projects.Kofile.Atom.CRS.add_payment import AddPayment
from projects.Kofile.Atom.CRS.capture import Capture
from projects.Kofile.Atom.CRS.image_viewer import ImageViewer
from projects.Kofile.Atom.CRS.indexing import Indexing, general
from projects.Kofile.Atom.CRS.initialize_drawer import InitializeDrawer
from projects.Kofile.Atom.CRS.order_finalization import OrderFinalization
from projects.Kofile.Atom.CRS.order_queue import OrderQueue, OrderEntry
from projects.Kofile.Atom.CRS.order_search import OrderSearch
from projects.Kofile.Atom.CRS.order_summary import OrderSummary
from projects.Kofile.Atom.CRS.package_search import PackageSearch
from projects.Kofile.Atom.CRS.verification import Verification
from projects.Kofile.Atom.CS.general import General as CSGeneral
from projects.Kofile.Atom.Eform.general import General as EFormGeneral
from projects.Kofile.Atom.erProxy.general import General as ERProxyGeneral
from projects.Kofile.Atom.KS.general import General as KSGeneral
from projects.Kofile.Atom.CS.api_helper import ApiHelper as CSApiHelper


class Atom:
    def __init__(self, data=None):
        self._data = data
        self.CRS = self.__CRS()
        self.CS = self.__CS()
        self.EForm = self.__EForm()
        self.ERProxy = self.__ERProxy()
        self.KS = self.__KS()

    class __CRS:
        def __init__(self):
            self.add_payment = AddPayment()
            self.capture = Capture()
            self.general = general
            self.image_viewer = ImageViewer()
            self.indexing = Indexing()
            self.initialize_drawer = InitializeDrawer()
            self.order_entry = OrderEntry()
            self.order_finalization = OrderFinalization()
            self.order_queue = OrderQueue()
            self.order_search = OrderSearch()
            self.order_summary = OrderSummary()
            self.package_search = PackageSearch()
            self.verification = Verification()

    class __CS:
        def __init__(self):
            self.general = CSGeneral()
            self.api_helper = CSApiHelper()

    class __EForm:
        def __init__(self):
            self.general = EFormGeneral()

    class __ERProxy:
        def __init__(self):
            self.general = ERProxyGeneral()

    class __KS:
        def __init__(self):
            self.general = KSGeneral()
