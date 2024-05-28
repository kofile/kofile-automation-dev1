"""
classes and functions for test data operations
"""
import importlib
from typing import Any
import jmespath
from golem import actions


class CRSTestDataHelpers:
    """
    CRS test data helpers
    """

    def __init__(self, *args):
        data = actions.execution.data
        actions.store("current_oit", data.get("OIT"))
        if not data.get("user_type"):
            actions.store("user_type", "guest")  # Set default user_type to 'guest'
        if not data.get("orderheader"):
            actions.store("orderheader", "guest")  # Set default orderheader to 'guest'
        if data.env.get('config_import_path') and data.env.get('config_name'):
            self.config_file = importlib.import_module(f"{data.env.get('config_import_path')}."
                                                       f"{data.env.get('config_name')}")
        actions.store("config", self)

    def reload(self):
        self.__init__()

    def test_data(self, path_to_data: str) -> Any:
        """
        returns a value from an OITs dict for a given key (path_to_data) for current environment,
        if exception returns None
        """
        res = jmespath.search(path_to_data, self.config_file.OITs)
        actions.step(res)
        if res is not None:
            return res
        else:
            split_path = path_to_data.split('.')
            default_path = path_to_data.replace(split_path[0], 'Default')
            default_res = jmespath.search(default_path, self.config_file.OITs)
            return default_res

    def get_order_types(self) -> Any:
        """
        returns OIT_names from OITs dict for a given key (path_to_data) for current environment,
        if exception returns None
        """
        res = (self.config_file.OITs.keys())
        return res

    def order_header_fill(self, path_to_data: str) -> Any:
        """
        returns names according to user type, from HEAD of test data config.
        use jmespath notation to define the path_to_data
        if exception returns None
        """

        res = jmespath.search(path_to_data, self.config_file.ORDER_HEADER)
        return res

    def get_status(self, path_to_data: str) -> Any:
        """
        returns Status name, from STATUSES of test data config.
        use jmespath notation to define the path_to_data
        if exception returns None
        """

        res = jmespath.search(path_to_data, self.config_file.STATUSES)
        return res

    def get_tab_name(self, path_to_data: str) -> Any:
        """
        returns Tab name name, from TAB_NAME  of test data config.
        use jmespath notation to define the path_to_data
        if exception returns None
        """
        res = jmespath.search(path_to_data, self.config_file.TAB_NAME)
        return res

    def get_front_office(self):
        """
        Add 'front_office' dictionary to 'data'
        """
        env_name = "UAT" if "uat" in actions.execution.data.env.name else "QA"
        res = self.config_file.front_office
        res = res.get(env_name, res)
        actions.store("front_office", res)
        return res

    def get_ps_password(self):
        res = self.config_file.ps_password
        actions.store("ps_password", res)
        return res

    def get_er_schema(self):
        res = self.config_file.er_schema
        actions.store("er_schema", res)
        return res

    def get_dept_id(self):
        res = self.config_file.departments
        actions.store("departments", res)

    def get_stamp_text(self, path_to_data: str):
        res = jmespath.search(path_to_data, self.config_file.CUSTOM_STAMPS)
        return res

    def get_kiosk_search(self, path_to_data: str):
        return jmespath.search(path_to_data, self.config_file.kiosk_search)


class ClerkSearchTestDataHelpers(CRSTestDataHelpers):
    """
    Clerk Search test data helpers
    """

    def test_config(self, oit=None):
        """
        returns a value from a dict for a given key (data.OIT) for current environment,
        """
        data = actions.execution.data
        test_config = {}
        order_type = data.get("order_type")
        oit = oit if oit else data.get("OIT")
        conf_dict = self.config_file.CS_OITs_configs
        test_config.update(conf_dict.get("default"))  # 'default' CS OIT configuration
        if oit:
            assert conf_dict.get(oit) is not None, f"'{oit}' OIT not found in configuration for current tenant!"
            test_config.update({"order_type": order_type})
            test_config.update(conf_dict.get(oit))  # update 'default' configuration with OIT configuration
            order_type_config = test_config.get(order_type)  # specific configs in case of Certified/Re-Index/Re-Capture
            assert order_type_config is not False, f"'{order_type}' is not available for '{oit}' OIT on current tenant"
            test_config.update(order_type_config) if order_type_config else None  # update config for current order type
        actions.store("test_config", test_config)
        return test_config
