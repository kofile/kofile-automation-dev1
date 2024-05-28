from projects.Kofile.api.api_BalanceDrawer import BalanceDrawer
from projects.Kofile.api.api_Capture import CaptureAPI
from projects.Kofile.api.api_FrontOffice import FrontOfficeAPI
from projects.Kofile.api.api_clerk_search import ClerkSearch
from projects.Kofile.api.api_crs import CRS


class API:
    def __init__(self):
        self.balance_drawer = BalanceDrawer
        self.capture = CaptureAPI
        self.clerc_search = ClerkSearch
        self.front_office = FrontOfficeAPI
        self.crs = CRS()
