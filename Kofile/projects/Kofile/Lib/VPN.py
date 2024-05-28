import logging
import os
import time
import re
from projects.Kofile.Lib.general_helpers import GeneralHelpers

QA_VPN_NAME = "VPN AT"
UAT_VPN_NAME = "VPN_Connection_2"


class RoutesGetter:
    route, old_routes_text = "16", ""
    old_routes, new_routes = list(), list()
    is_default = True

    @staticmethod
    def get_print():
        try:
            result = os.popen("route print").read()
            if "Interface List" in result:
                return result
        except Exception as e:
            logging.info(type(e).__name__)
        return ""

    @staticmethod
    def parse_route(routes_text, connection_name="VPN Connection"):
        try:
            regex = r"(\d{1,3}?)\.+%s" % connection_name
            routes = re.findall(regex, routes_text)
            return routes
        except Exception as e:
            logging.info(type(e).__name__)

    def get_dif_route(self, new_routes):
        for r in new_routes:
            if r not in self.old_routes:
                self.is_default = False
                return r
        return self.route

    def __init__(self, vpn_name):
        self.vpn_name = vpn_name

    def __enter__(self):
        self.old_routes = self.parse_route(self.get_print())
        return self

    def get_route(self):
        new_routes = self.parse_route(self.get_print())
        self.route = self.get_dif_route(new_routes)
        logging.info(f"Current route {self.route}, is default: {str(self.is_default)}")
        return self.route

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def vpn_connect():
    """
    connect to VPN
    """
    try:
        logging.info("-----VPN connection-----")
        if 'uat' in GeneralHelpers.get_env_name().lower():
            vpn = os.popen(f"rasdial \"{UAT_VPN_NAME}\"").read()
            logging.info(vpn)
        else:
            # with RoutesGetter(QA_VPN_NAME) as route:
            vpn2 = os.popen(f"rasdial \"{QA_VPN_NAME}\"").read()
            logging.info(vpn2)
            time.sleep(1)
                # os.popen(f"route add 10.0.0.7 MASK 255.255.255.255 0.0.0.0 IF {route.get_route()}").read()
    except Exception as e:
        raise ValueError(f"-----VPN connection has been failed!-----:\n {e}")


def vpn_disconnect():
    """
    disconnect from VPN
    """
    try:
        if 'uat' in GeneralHelpers.get_env_name().lower():
            os.system(f"rasdial \"{UAT_VPN_NAME}\" /disconnect")
        os.system(F"rasdial \"{QA_VPN_NAME}\" /disconnect")
        logging.info("-----VPN disconnected-----")
    except Exception as e:
        logging.warning(e)
        logging.error("-----VPN disconnection has been failed!-----")
