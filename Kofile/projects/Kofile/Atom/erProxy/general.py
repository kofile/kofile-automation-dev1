import os
import re
import shutil
import uuid
import xml.etree.ElementTree as Et
from time import time

from projects.Kofile.Atom.CRS.add_payment import AddPayment
from projects.Kofile.Atom.CRS.order_queue import OrderQueue
from projects.Kofile.Atom.CRS.order_summary import OrderSummary
from projects.Kofile.Atom.CRS.general import General as CRSGeneral

from projects.Kofile.Lib.VPN import vpn_connect, vpn_disconnect
from projects.Kofile.Lib.general_helpers import ErProxyHelpers
from projects.Kofile.Lib.test_parent import AtomParent


class General(AtomParent):
    def __init__(self):
        super(General, self).__init__()

    def __del__(self):
        self._lib.general_helper.kill_proc_by_name('erProxyTester.exe')

    def create_er_proxy(self, er_proxy_count=1, account_name=None, account_password=None, oit_count=1,
                        exit_from_er_proxy=True, ds=False):
        """
        er_proxy_count = number of erProxy orders to submit (number of xml-s)
        oit_count = number of order items in 1 order (number of docs in xml)
        ds = False creates regular erProxy, True - direct submission erProxy (DS)
        """
        print(er_proxy_count)
        env_code = self._lib.general_helper.get_env_code()
        env_name = 'QA' if 'qa' in self._lib.general_helper.get_env_name().lower() else 'UAT'
        current_dir = os.getcwd().replace('\\', '/')
        er_proxy_package = self._names.erProxy_file_path
        payload_folder_name = "Payloads"
        payload_folder_path = os.path.join(er_proxy_package, payload_folder_name)
        er_proxy_folder_name = "erProxy"
        config_file_name = "erProxyTester.exe.config"
        config_file = os.path.join(er_proxy_package, f'{env_code}_{env_name}',
                                   er_proxy_folder_name, config_file_name)
        self._lib.data_helper.__init__()
        data = self._lib.general_helper.get_data()
        account = data.config.order_header_fill('er_proxy_account_name_password')

        if account_name and account_password:
            account_name_password_folder_dir = f"{payload_folder_path}/{account_name}-{account_password}"
        else:
            account_name_password_folder_dir = f"{payload_folder_path}/{account['name']}-{account['pass']}"

        self._actions.step("--- ATOMIC TEST --- {} ---".format(__name__))

        # change the url in erProxyTester.exe.config file based on running tenant
        tree = Et.parse(config_file)
        root = tree.getroot()
        tags = root.findall('appSettings/add')
        for tag in tags:
            key_value = tag.attrib['key']
            if key_value == 'ProxyURL':
                tag.attrib['value'] = ErProxyHelpers.get_url()
            elif key_value == 'PayloadFolder':
                tag.attrib['value'] = payload_folder_path
        tree.write(config_file)

        # remove Payload folder content and create accountname-accountpassword folder           # noqa
        if os.path.exists(payload_folder_path) and os.listdir(payload_folder_path):
            shutil.rmtree(payload_folder_path, ignore_errors=True)
        if not os.path.exists(payload_folder_path):
            os.mkdir(os.path.relpath(payload_folder_path))
        os.mkdir(os.path.relpath(account_name_password_folder_dir))

        # copy the erProxy.xml file to accountname-accountpassword folder and give it a unique name    # noqa
        er_proxy_xml_list = []
        for _ in range(er_proxy_count):
            xml_file_name = f"erProxy_ds_{oit_count}.xml" if ds else f"erProxy_{oit_count}.xml"
            shutil.copy(f"{er_proxy_package}/{xml_file_name}", account_name_password_folder_dir)
            unique_name = str(uuid.uuid4()).replace("-", '')
            self._actions.wait(0.01)
            os.rename(f"{account_name_password_folder_dir}/{xml_file_name}",
                      f"{account_name_password_folder_dir}/{unique_name}.xml")
            er_proxy_xml_list.append(unique_name)
        try:
            os.chdir(f"{er_proxy_package}/{env_code}_{env_name}/erProxy")
            os.startfile("erProxyTester.exe")
            self._actions.wait(5)
        finally:
            # change the dir to current dir to pass a correct dir to next running tests
            os.chdir(current_dir)

        """ Check in database 
            1. PACKAGE_ID = xml name
            2. ORDER_NUM !=  Null
        """
        try:
            vpn_connect()
            self._lib.db.connect_to_db()

            # check that all erProxy orders are submitted in database within the specified time
            max_time = time() + er_proxy_count * 30
            er_proxy_order_numbers = []
            er_proxy_package_ids = []
            # is_searching_by_package_id == True searches for package without submitter name
            # False - with submitter name
            is_searching_by_package_id = bool(
                self._lib.db.get_info_via_given_table_and_columnname(
                    table_name='PACKAGE_NAME',
                    select_column_name='count(PACKAGE_SEARCH_ID)')[0][0])
            while time() < max_time:
                for xml_name in er_proxy_xml_list:
                    order_num = self._lib.db.get_info_via_given_table_and_columnname(
                        table_name='ER_PACKAGE',
                        select_column_name='ORDER_NUM',
                        where_column_name='PACKAGE_ID',
                        where_value=xml_name)
                    if order_num and order_num[0][0]:
                        order_num = order_num[0][0]
                        self._actions.step(f'erProxy with name - {xml_name} is submitted successfully. '
                                           f'Order number is - {order_num}')
                        er_proxy_order_numbers.append(order_num)
                        if is_searching_by_package_id:
                            er_proxy_package_ids.append(xml_name)
                        else:
                            er_proxy_package_ids.append(
                                re.sub(r"^.*/|-.*$", "", account_name_password_folder_dir) + '_' + xml_name)
                        er_proxy_xml_list.remove(xml_name)
                    else:
                        # wait to not spam the DB with requests
                        self._actions.wait(2)
                if not er_proxy_xml_list:
                    break

            # check if all erProxy orders are submitted
            if len(er_proxy_xml_list) == 0:
                self._actions.step(f'{er_proxy_count} erProxy are submitted successfully!')
            else:
                self._actions.fail(f'The following erProxy are not submitted! - {er_proxy_xml_list}')

        finally:
            if exit_from_er_proxy:
                self._lib.general_helper.kill_proc_by_name('erProxyTester.exe')
            self._lib.db.disconnect_from_db()
            vpn_disconnect()

        self._actions.step("--- ATOMIC TEST END --- {} ---".format(__name__))
        # return the submitted erProxy order number, package ID = xml name
        return er_proxy_order_numbers, er_proxy_package_ids

    def create_and_finalize_er_proxy(self, data):
        """
            Pre-conditions: No
            Post-conditions: erProxy order is created and finalized
            """

        self._actions.step(f"--- ATOMIC TEST --- {__name__} ---")

        # get test data from tenant config file
        self._lib.data_helper.__init__()

        # submit erProxy and get the order number
        data["order_number"] = self.create_er_proxy()[0][0]

        # assign the order
        CRSGeneral().go_to_crs()
        self._lib.CRS.crs.go_to_order_queue()
        OrderQueue().assign_order()
        self._lib.general_helper.wait_for_spinner()

        # review the order
        data["current_oit"] = data.OIT
        self._lib.CRS.crs.click_running_man()
        self._actions.wait_for_element_displayed(self._pages.CRS.order_summary.lbl_order_number)
        OrderSummary().edit_oit()

        # finalize the order
        AddPayment().finalize_order()

        self._actions.step(f"--- ATOMIC TEST END --- {__name__} ---")
