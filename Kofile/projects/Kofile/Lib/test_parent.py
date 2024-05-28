import logging
import random
import time
from datetime import datetime, timedelta

import requests
from golem import actions
from jsonschema import validate
from selenium.webdriver.common.keys import Keys

from projects.Kofile.Lib.general_helpers import GeneralHelpers, get_url, ClerkSearchGeneralHelpers
from projects.Kofile.api.api_child import API
from projects.Kofile.api.api_services import ApiService
from projects.Kofile.pages.api_urls import ApiUrls
from projects.Kofile.testdata.api_tests_data import ApiTestData
from projects.Kofile.testdata.names import Names

ALLOWED_ORIGINS = ("sameorigin", "deny")
PACKAGE = "projects.Kofile.tests.API"


class LibParent:
    def __init__(self, data=None):
        from projects.Kofile.Lib.pages_child import Pages
        self._general_helper = GeneralHelpers()
        self._data = data if data else actions.get_data()
        self._names = Names(self._data)
        self._pages = Pages(self._data)
        self._keys = Keys
        self._api = API()
        self._actions, self._logging = actions, logging
        self._keys, self._random = Keys, random
        mode_name = f"__{self._data['env']['code']}__"
        if hasattr(self, mode_name):
            getattr(self, mode_name).__call__()
        location_id = self._data["env"].get("location", {}).get("id")
        mode_name = f"__location_{location_id}__"
        if hasattr(self, mode_name):
            getattr(self, mode_name).__call__()
        oit = self._data.get("OIT")
        if oit:
            mode_name = f"__{oit}__"
            if hasattr(self, mode_name):
                getattr(self, mode_name).__call__()


class PagesParent:
    def __init__(self, data=None):
        self._data = data if data else actions.get_data()
        self._names = Names(self._data)
        self._api, self._random = API(), random
        mode_name = f"__{self._data['env']['code']}__"
        if hasattr(self, mode_name):
            getattr(self, mode_name).__call__()
        location_id = self._data["env"].get("location", {}).get("id")
        mode_name = f"__location_{location_id}__"
        if hasattr(self, mode_name):
            getattr(self, mode_name).__call__()
        oit = self._data.get("OIT")
        if oit:
            mode_name = f"__{oit}__"
            if hasattr(self, mode_name):
                getattr(self, mode_name).__call__()


class AtomParent:
    def __init__(self, data=None):
        from projects.Kofile.Lib.pages_child import Pages
        from projects.Kofile.Lib.lib_child import Lib
        self._data = data if data else actions.get_data()
        self._lib = Lib(self._data)
        self._api = API()
        self._names = Names(self._data)
        self._pages = Pages(self._data)
        self._actions, self._logging = actions, logging
        self._keys, self._random = Keys, random
        mode_name = f"__{self._data['env']['code']}__"
        self._lib.data_helper.reload()
        if hasattr(self, mode_name):
            getattr(self, mode_name).__call__()
        location_id = self._data["env"].get("location", {}).get("id")
        mode_name = f"__location_{location_id}__"
        if hasattr(self, mode_name):
            getattr(self, mode_name).__call__()
        oit = self._data.get("OIT")
        if oit:
            mode_name = f"__{oit}__"
            if hasattr(self, mode_name):
                getattr(self, mode_name).__call__()


class TestParent:
    def __init__(self, data, name, precondition=None):
        from projects.Kofile.Lib.lib_child import Lib
        from projects.Kofile.Lib.pages_child import Pages
        from projects.Kofile.Atom.atom_child import Atom
        self.lib, self.pages = Lib(data), Pages(data)
        self.names, self.atom = Names(data), Atom(data)
        self.data, self.actions = data, actions
        self.logging, self.datetime, self.timedelta = logging, datetime, timedelta
        self.api, self.keys, self.random = API(), Keys, random
        actions.step(f"--- TEST START --- {name} ---")
        self.lib.data_helper.reload()
        mode_name = f"__{data['env']['code']}__"
        if hasattr(self, mode_name):
            getattr(self, mode_name).__call__()
        if hasattr(precondition, "__call__"):
            precondition.__call__()
        location_id = data["env"].get("location", {}).get("id")
        mode_name = f"__location_{location_id}__"
        if hasattr(self, mode_name):
            getattr(self, mode_name).__call__()
        oit = data.get("OIT")
        if oit:
            mode_name = f"__{oit}__"
            if hasattr(self, mode_name):
                getattr(self, mode_name).__call__()
        start_time = time.time()
        self.__test__()
        duration = time.time() - start_time
        if hasattr(self, "timeout"):
            timeout = getattr(self, "timeout")
            if duration > timeout:
                self.logging.warning(f"TEST TIMEOUT: {duration=}, {timeout=}")
            else:
                self.logging.info(f"TEST TIMEOUT: {duration=}, {timeout=}")
        else:
            self.logging.info(f"TEST TIMEOUT: {duration=}")
        actions.step(f"--- TEST END --- {name} ---")

    def __test__(self):
        pass


class ApiTestParent:
    response = None

    def __init__(self, data, name, with_browser=False, use_same_token=True):
        self.data = data
        place = getattr(self, "place") if hasattr(self, "place") else "crs"
        if hasattr(actions.execution, f"{place}_token") and use_same_token:
            self.cookies = getattr(actions.execution, f"{place}_token")
        else:
            if data.env.get("api_params", {}).get("api_auth_type") != "browser" and place != "cs":
                self.cookies = {'ASP.NET_SessionId': ApiService(self.data, use_db=False).cookie.split("=")[-1]}
            else:
                if not with_browser:
                    actions.execution.browser_definition = {'name': 'chrome', 'full_name': None, 'remote': False,
                                                            'capabilities': {}}
                actions.get(ClerkSearchGeneralHelpers.get_url() if place == "cs" else get_url())
                self.cookies = {i["name"]: i["value"] for i in actions.get_cookies() if
                                i.get("name") and i.get("value")}
                actions.close_browser()
                if not with_browser:
                    actions.execution.browser_definition = {'name': 'none', 'full_name': None, 'remote': False,
                                                            'capabilities': {}}
            self.set(f"{place}_token", self.cookies)

        self.api_test_data = ApiTestData()
        self.api_urls = ApiUrls()
        self.validate = validate
        self.requests = requests
        self.names = Names(data)
        self.data_mapping = self.names.data_mapping
        self.actions = actions
        self.logging = logging
        self.api_lib = API()
        self.datetime = datetime
        self.random = random
        self.session = requests.session()
        self.session.hooks['response'].append(self.log_response)
        self.session.cookies.update(self.cookies)
        self.set_headers()
        actions.step(f"--- TEST START --- {name} ---")
        mode_name = f"test{data['env']['code']}"
        if hasattr(self, mode_name):
            if func := getattr(self, mode_name):
                func.__call__()
        if hasattr(self, "__before__"):
            if func := getattr(self, "__before__"):
                func.__call__()
        self.__test__()
        if hasattr(self, "__after__"):
            if func := getattr(self, "__after__"):
                func.__call__()
        if place == "crs":
            self.check_header()
        actions.step(f"--- TEST END --- {name} ---")

    def __test__(self):
        pass

    def check_header(self):
        if self.response:
            header = self.response.headers
            logging.info(f"Current x-frame-options: {header.get('x-frame-options')}")
            assert header.get("x-frame-options", "").lower() in ALLOWED_ORIGINS, header.get(
                "x-frame-options", "").lower()

    def get_url(self, url_path, domain_key="domain"):
        return f"https://{self.data.env[domain_key]}/{self.data.env.code}{url_path}"

    @staticmethod
    def get(key, timeout=1, should_exist=True):
        for _ in range(timeout):
            if hasattr(actions.execution, key):
                return getattr(actions.execution, key)
            time.sleep(1)
        if should_exist:
            raise ValueError(f"Cant find {key} variable")

    @staticmethod
    def set(key, value):
        setattr(actions.execution, key, value)

    @staticmethod
    def delete(key):
        delattr(actions.execution, key)

    def set_content_type(self, content_type: str = "application/x-www-form-urlencoded"):
        self.session.headers['Content-Type'] = content_type

    def set_headers(self, header: dict = None):
        self.session.headers = self.api_test_data.default_headers if header is None else header

    def call_module(self, name, *args, **kwargs):
        __import__(f"{PACKAGE}.{name}", fromlist=(PACKAGE,)).test.__call__(self.data, *args, **kwargs)

    def run_dependencies(self, dependencies: tuple):
        for dep in dependencies:
            if not self.get(dep, should_exist=False):
                self.call_module(self.data_mapping.get(dep))

    def log_response(self, response, **kwargs):  # noqa
        self.actions.log(f'-> API -> {response.status_code} ---> {response.request.method} ---> {response.request.url}')
