import random

from projects.Kofile.Lib.test_parent import AtomParent, ApiTestParent
from projects.Kofile.api.api_BalanceDrawer import BalanceDrawer
import json
from urllib.parse import urlparse, parse_qs
import re
from datetime import datetime


class ApiHelper(AtomParent):
    order_id, doc_type_id, doc_type_desc, doc_group_id, doc_group_code, order_amount = None, None, None, None, None, None
    order_item_id, order_item_type_id, address_id, doc_group_name, dm_id = None, None, None, None, None

    def __init__(self):
        super().__init__()
        self._api, self.get_url, self.urls = None, None, None
        self.oit_config = self._data['config'].test_data(f"{self._data.OIT}")

    @property
    def api(self):
        if self._api is None:
            self._api = ApiTestParent(self._data, __name__, with_browser=True, use_same_token=False)
            self.api.set_content_type()
            self.get_url = self.api.get_url
            self.urls = self.api.api_urls
        return self._api

    def _get_oit(self):
        return self._data.get('OIT') if self._data.get('OIT') else 'Default'

    def initialize_drawer(self):
        BalanceDrawer(self._data).initialize_drawer()

    def create_order(self, payment_type_id: str = '1', origin_id: str = '4'):
        """
        The function creates and finalizes order by given parameters and OIT from the execution data

        :param payment_type_id: 1 = Cash, 2 = Check, 3 = Company Account etc.
        :param origin_id: 4 = CRS
        :return:
        """
        # Get the user data by email_user_id
        self._actions.step(
            f"-> API -> Get user address id by username {self._data.config.config_file.ORDER_HEADER.get('guest')['value']}")
        self.api.response = self.api.session.get(
            self.get_url(self.urls.GetCustomerNames),
            params=(('customerName', self._data.config.config_file.ORDER_HEADER.get('guest')['value']),)
        )
        self._verify_response('Address')
        user_address = json.loads(self.api.response.text)[0].get('Address')
        user_id = json.loads(self.api.response.text)[0].get('Id')

        # Create order with the given OI
        post_data = self._prepare_user_header_data(
            self.api.api_test_data.get_data_by_oit('order_actions', self._get_oit()).copy(), user_address, user_id)
        if self._get_oit() == 'Assumed_Name':
            post_data.append(('Order.OrderItems[0].Document.DocumentExtras.Business.UnIncorporatedBusinessName',
                              self._actions.random_str()))

        self._actions.step(f"-> API -> Post a new order with {self._get_oit()} OIT")
        self.api.response = self.api.session.post(
            self.get_url(self.urls.OrderActions), data=post_data)

        self._verify_response('"OrderNumber":', '"DocumentTypeId":', '"DocumentTypeDesc":', '"DocumentGroupId":',
                              '"Code":')
        self.order_id = parse_qs(urlparse(self.api.response.url).query).get("orderId")[0]
        self.doc_type_id = re.findall('"DocumentTypeId":(.*?),', self.api.response.text)[0]
        self.doc_type_desc = re.findall('"DocumentTypeDesc":"(.*?)",', self.api.response.text)[0]
        self.doc_group_id = re.findall('"DocumentGroupId":(.*?),', self.api.response.text)[0]
        self.doc_group_code = re.findall('"Code":"(.*?)",', self.api.response.text)[0]
        self._data['order_number'] = re.findall('"OrderNumber":"(.*?)","', self.api.response.text)[0]

        # Check out order and get the price, orderItemId, orderItemTypeId
        post_data = self._prepare_user_header_data(self.api.api_test_data.check_out_order_data.copy(), user_address,
                                                   user_id)
        post_data.append(('Order.OrderId', self.order_id))
        post_data.append(('Order.OrderHeader.OrderNumber', self._data['order_number']))

        self._actions.step(f"-> API -> Check out the order# {self._data['order_number']} with {self._get_oit()} OIT")
        self.api.response = self.api.session.post(
            self.get_url(self.urls.CheckOutOrder), data=post_data)

        self._verify_response('id="orderTotalAmt"', 'orderItemId', 'orderItemTypeId')
        self.order_amount = re.findall('<span id="orderTotalAmt" class="hidden">(.*?)</span>', self.api.response.text)[0]
        self.order_item_id = re.findall('orderItemId&quot;:(.*?),&quot;', self.api.response.text)[0]
        self.order_item_type_id = re.findall('orderItemTypeId&quot;:(.*?),&quot', self.api.response.text)[0]

        # Finalise order
        post_data = self._prepare_user_header_data(
            self.api.api_test_data.get_data_by_oit('post_action', self._get_oit()).copy(), user_address, user_id)
        post_data.append(('Order.OrderHeader.OrderNumber', self._data['order_number']))
        post_data.append(('Order.OrderId', self.order_id))
        post_data.append(('orderId', self.order_id))
        post_data.append(('Order.OrderHeader.OriginId', origin_id))
        post_data.append(('OrderPayment[0].PaymentMethod.PaymentTypeId', payment_type_id))
        inner_data = [
            '{"orderItemId":%s,"orderItemTypeId":%s,"orderItemTypeDesc":"%s","orderItemSequence":%s}' % (
                self.order_item_id, self.order_item_type_id, self._get_oit(), 1)]
        post_data.append(('receivedByMailList',
                          '{"orderId":%s,"orderItems":[%s]}' % (self.order_id, ",".join(inner_data))))
        post_data.append(('OrderPayment[0].Amount', self.order_amount))

        self._actions.step(f"-> API -> Finalise the order# {self._data['order_number']} with {self._get_oit()} OIT")

        self.api.response = self.api.session.post(
            self.get_url(self.urls.PostAction), data=post_data
        )

        self._verify_response('Document_DocAndAppNum', 'Document_RecordedYear', 'InstrumentNumber')
        self._data["doc_num"] = re.findall('Document_DocAndAppNum":"(.*?)",', self.api.response.text)[0].split('/')[-1]
        self._data["doc_year"] = re.findall('"Document_RecordedYear":"(.*?)",', self.api.response.text)[0]
        self._data["doc_year-doc_num"] = f'{self._data["doc_year"]}-{self._data["doc_num"]}'
        self._data["instrument_number"] = re.findall(',"InstrumentNumber":"(.*?)",', self.api.response.text)[0]
        a_id = re.findall("\"Document\":{.*Address\":{\"AddressId\":(.*?),", self.api.response.text)
        self.address_id = a_id[0] if len(a_id) else None

    def capture_document(self, scan_count=1):
        """
        The function makes capturing for OIT, doc# from the execution data

        :param scan_count: how many times the start scan button should be pressed
        :return:
        """
        if not self.oit_config.get('capture', {}).get('step'): return

        oit_data = self._data.config.config_file.OITs.get(self._get_oit())

        scanner_session = 0
        document_id = 0
        page_count = 0
        is_insert_action = False
        current_docs_count = 0

        for _ in range(scan_count):
            # Start scanner session
            scanner_session = self._start_scanner_session(scanner_session, document_id, page_count + 1,
                                                          is_insert_action)
            # Get scanned files
            scanned_files = self._get_scanned_files(scanner_session, current_docs_count, document_id)
            scan_date = scanned_files[0].get('ScanDate')
            file_name = scanned_files[0].get('Path')
            page_count = scanned_files[0].get('Scanned')
            document_id = scanned_files[0].get('DocumentId')
            is_insert_action = True
            current_docs_count = 1

        # Get the document group name
        post_data = (('term', self.doc_group_code[0]),)
        self._actions.step(
            f"-> API -> Get document group name for id: {self.doc_group_id} and code: {self.doc_group_code}")
        self.api.response = self.api.session.get(self.get_url(self.api.api_urls.GetDocumentGroupNumber),
                                                 params=post_data)
        self._verify_response()
        for el in self.api.response.json():
            if el.get('Id') == int(self.doc_group_id):
                self.doc_group_name = el.get('Name')
                break

        time = datetime.now()
        # SaveDocumentItemDetails
        post_data = self.api.api_test_data.save_document_item_details_data.copy()
        params = {
            'isReprocessing': 'false',
            'isReCapture': 'false',
            'isAdminSuspend': 'false',
            'isCaptureReview': 'false',
            'isUpload': 'false',
        }
        post_data["documentItem"]["DocumentId"] = document_id
        post_data["documentItem"]["Year"] = time.strftime("%Y")
        post_data["documentItem"]["Scanned"] = page_count
        post_data["documentItem"]["ScanDate"] = scan_date                                                   # noqa
        post_data["documentItem"]["Path"] = file_name                                                       # noqa
        post_data["documentItem"]["ScanTaskId"] = scanner_session
        post_data["documentItem"]["RecordedYear"] = time.strftime("%Y-01-01T00:00:00")
        post_data["DocumentId"] = document_id
        post_data["DocumentGroup"]["Id"] = self.doc_group_id
        post_data["DocumentGroup"]["Name"] = self.doc_group_name
        post_data["DocumentType"]["Key"] = self.doc_type_id
        post_data["DocumentType"]["Value"] = self.doc_type_desc
        post_data["OrderNumber"] = self._data['order_number']
        post_data["Number"] = self._data["instrument_number"]
        post_data["Year"] = time.strftime("%Y")
        post_data["Pages"] = page_count
        post_data["Scanned"] = page_count
        post_data["Path"] = file_name
        post_data["ScanDate"] = scan_date
        post_data["ScanTaskId"] = scanner_session

        self._actions.step(f"-> API -> Save Document Details for doc# {self._data['doc_num']}")
        self.api.set_content_type('application/json')
        self.api.response = self.api.session.post(self.get_url(self.api.api_urls.SaveDocumentItemDetails),
                                                  json=post_data,
                                                  params=params)
        self._verify_response()

        # Save scanned document
        item_data = self.api.api_test_data.save_batch_scan_item_data.copy()
        outer_data = self.api.api_test_data.save_batch_scan_data.copy()
        item_data["DocumentId"] = document_id
        item_data["OrderId"] = self.order_id
        item_data["OrderNumber"] = self._data['order_number']
        item_data["Number"] = self._data["instrument_number"]
        item_data["Path"] = file_name
        item_data["OrderItemId"] = self.order_item_id
        item_data["ScanDate"] = scan_date
        item_data["ScanTaskId"] = scanner_session
        item_data["Year"] = time.strftime("%Y")
        item_data["Pages"] = page_count
        item_data["Scanned"] = page_count
        item_data["OrderItemTypeId"] = self.order_item_type_id
        item_data["IsHistoricalDocMapped"] = True
        item_data["IsPrepMlDocMapped"] = True
        document_group = {
            "Id": self.doc_group_id,
            "Name": self.doc_group_name,
            "IsAutoGenerated": True
        }
        item_data.update({'DocumentGroup': document_group})
        document_type = {
            'Key': self.doc_type_id,
            'Value': self.doc_type_desc
        }
        item_data.update({'DocumentType': document_type})

        if oit_data.get('capture').get('expanded_indexing'):
            item_data.update({"CaptureAndIndexAvailable": True})
            document = {
                "DocumentItem": {
                    "RecordedYear": f"01/01/{time.strftime('%Y')}"
                },
                "RecordedDate": time.strftime("%m/%d/%Y"),
                "InstrumentNumber": self._data["instrument_number"],
                "VitalIndexExtras": {
                    "EventDate": time.strftime("%m/%d/%Y")
                },
                "MarriedBy": "BOB DYLAN",
                "CountyOfMarriage": "Test with dev",
                "CityOfMarriage": "",
                "Parties": [
                    {
                        "FirstName": "SMITH JOHN",
                        "TypeCode": "G",
                        "TypeId": "7"
                    },
                    {
                        "FirstName": "SMITH LUCCY",
                        "TypeCode": "B",
                        "TypeId": "8"
                    }
                ],
                "": "on",
                "undefined": "True",
                "Order": {
                    "OrderItems": [
                        {
                            "ReturnByEmail": "True"
                        }
                    ]
                },
                "Address": {
                    "AddressName": "JOHN SMITH",
                    "AddressId": self.address_id,
                    "AddressLine1": "ADDRESS1",
                    "AddressLine2": "",
                    "ZipCode": "90001",
                    "City": "LOS ANGELES",
                    "StateCode": "6",
                    "StateName": "CA",
                    "CountryCode": "US"
                }
            }
            item_data.update({"Document": document})

        outer_data.update({"Documents": [item_data]})

        self._actions.step(f"-> API -> Save scanned and mapped image to OI")
        self.api.set_content_type('application/json')
        self.api.response = self.api.session.post(self.get_url(self.api.api_urls.SaveBatchScan), json=outer_data)
        self._verify_response('"overAllSuccess":true')

    def index_document(self, prop_type=False, add_remark=False, set_ref=()):
        """
        The function process order through the indexing, adds property, remark, reference document depending on given
        parameters

        :param prop_type: set it True for adding preconfigured property
        :param add_remark: set it True for adding remark to the document
        :param set_ref: set it as set(vol, page) to adding a reference document to the document in process
        :return:
        """

        if not self.oit_config.get('indexing', {}).get('step'): return

        # Get the indexing task ID
        indexing_task_id = self._show_queue('indexing')

        # Open order to the indexing process
        self.dm_id = self._open_order_to_process('indexing', indexing_task_id)

        # Save the OI in the indexing process
        self._save_oi('indexing', indexing_task_id, prop_type, add_remark, set_ref)

        # Process order to the next workflow step
        self._process_order_to_next_workflow('indexing', indexing_task_id)

    def verify_document(self, prop_type=False, add_remark=False, set_ref=()):
        """
        The function process order through the verification, adds property, remark, reference document depending on given
        parameters

        :param prop_type: set it True for adding preconfigured property
        :param add_remark: set it True for adding remark to the document
        :param set_ref: set it as set(vol, page) to adding a reference document to the document in process
        :return:
        """

        if not self.oit_config.get('verification', {}).get('step'): return

        # Get the verification task ID
        verification_task_id = self._show_queue('verification')

        # Open order to the verification process
        self.dm_id = self._open_order_to_process('verification', verification_task_id)

        # Save the OI in the verification process
        self._save_oi('verification', verification_task_id, prop_type, add_remark, set_ref)

        # Process order to the next workflow step
        self._process_order_to_next_workflow('verification', verification_task_id)

    def unpost_drawer_session(self):
        BalanceDrawer(self._data).unpost_drawer_session()

    def _verify_response(self, *args: str, expected_rsp_code: int = 200, body_required=True):
        """
        Verify response status code, body and keywords in body (if given)

        :param args: expected body keywords ('id', 'doc_num' etc.)
        :param expected_rsp_code: expected status code (200, 404, 403 etc.)
        :param body_required: if response shouldn't contain body, set it False
        :return:
        """
        assert self.api.response.status_code == expected_rsp_code, \
            f"Actual response code: {self.api.response.status_code} sin't equal expected {expected_rsp_code}"
        if body_required: assert self.api.response.text, "The response body is empty"
        for _ in args:
            assert _ in self.api.response.text, \
                f"The expected data key: {_} is missing in the response body: \n{self.api.response.text[:500] + '..'}"

    def _show_queue(self, queue_name: str) -> str:
        """
        The function gets all orders in the given queue and returns the Task ID for order_id from the self-attribute

        :param queue_name: it should be 'indexing' or 'verification'
        :return: task it by order_id from the self-attribute
        """
        link = self.get_url(self.api.api_urls.ShowIndexQueue) if queue_name == 'indexing' else self.get_url(
            self.api.api_urls.ShowVerificationQueue)
        self._actions.step(f"-> API -> Getting the {queue_name} task ID for order_id: {self.order_id}")
        task_id, counter = None, 10
        while (not task_id) and counter:
            self._actions.wait(3)
            try:
                self.api.response = self.api.session.get(link, timeout=120)
                task_id = \
                    re.findall(f'"Order_OrderId":{self.order_id},"{queue_name.capitalize()}TaskId":(.*?),',
                               self.api.response.text)[0]
            except Exception as e:
                self._actions.log(e)
            counter -= 1
        assert task_id, f"Can't found {queue_name} task id in {queue_name} queue for order id {self.order_id}"
        return task_id

    def _open_order_to_process(self, queue_name: str, task_id: str) -> str:
        """
        The function opens order by given task_id to process from the given queue and returns the dm_id data

        :param queue_name: it should be 'indexing' or 'verification'
        :param task_id: indexing or verification task_id
        :return: dm_id data
        """
        link = self.get_url(self.api.api_urls.GetIndexingTask) if queue_name == 'indexing' else self.get_url(
            self.api.api_urls.GetVerificationTask)
        post_data = ((f'{queue_name.capitalize()}TaskId', task_id),)
        self.api.set_headers(self.api.api_test_data.indexing_headers)
        self._actions.step(f"-> API -> Open order# {self._data['order_number']} to the {queue_name} process")
        self.api.response = self.api.session.get(link, params=post_data)
        self._verify_response('id="dmId"')
        return re.findall('id="dmId".*value="(.*?)"', self.api.response.text)[0]

    def _save_oi(self, queue_name: str, task_id: str, prop_type: bool, add_remark: bool, set_ref: tuple):
        """
        The function collects the data for saving order item during indexing or verification depending on given parameter and saves OI

        :param queue_name: it should be 'indexing' or 'verification'
        :param task_id: indexing or verification task_id
        :param prop_type: set it True for adding preconfigured property
        :param add_remark: set it True for adding remark to the document
        :param set_ref: set it as set(vol, page) to adding a reference document to the document in process
        :return:
        """
        link = self.get_url(self.api.api_urls.IndexingOrderActions) if queue_name == 'indexing' else self.get_url(
            self.api.api_urls.VerificationOrderActions)
        post_data = self.api.api_test_data.order_actions_indexing_data.copy() if queue_name == 'indexing' else self.api.api_test_data.order_actions_verification_data.copy()

        post_data["Order.OrderId"] = self.order_id
        post_data["Order.OrderItems[0].OrderItemId"] = self.order_item_id
        post_data["orderItemId"] = self.order_item_id
        post_data[f'{queue_name.capitalize()}TaskId'] = task_id
        post_data["orderNum"] = self._data['order_number']
        post_data["dmId"] = self.dm_id
        post_data['Order.OrderItems[0].Document.InstrumentNumber'] = self._data["instrument_number"]
        post_data['Order.OrderItems[0].Document.VitalIndexExtras.EventDate'] = datetime.now().strftime("%m/%d/%Y")
        configured_party_name = self.oit_config.get('indexing').get('party_name')
        p_f_names = ['JOHN', 'LUCY', 'MICHAEL', 'MARY']
        p_l_names = ['SMITH', 'BROWN', 'WILLIAMS', 'GARCIA']
        if len(configured_party_name) == 1 and configured_party_name[0] == 'Name':
            post_data[
                'Order.OrderItems[0].Document.Parties[0].FirstName'] = f'{random.choice(p_f_names)} {random.choice(p_l_names)}'
            post_data[
                'Order.OrderItems[0].Document.Parties[1].FirstName'] = f'{random.choice(p_f_names)} {random.choice(p_l_names)}'
            post_data['Order.OrderItems[0].Document.Parties[0].LastName'] = ''
            post_data['Order.OrderItems[0].Document.Parties[1].LastName'] = ''
        else:
            post_data['Order.OrderItems[0].Document.Parties[0].FirstName'] = random.choice(p_f_names)
            post_data['Order.OrderItems[0].Document.Parties[1].FirstName'] = random.choice(p_f_names)
            post_data['Order.OrderItems[0].Document.Parties[0].LastName'] = random.choice(p_l_names)
            post_data['Order.OrderItems[0].Document.Parties[1].LastName'] = random.choice(p_l_names)

        if prop_type:
            prop_types = self._data['config'].test_data(f"{self._get_oit()}.indexing.property")
            property_index = 0
            for prop in prop_types.keys():
                prop_name = 'Description' if prop == 'newdesc' else prop.capitalize()
                post_data[
                    f'Order.OrderItems[0].Document.Properties[{property_index}].LegalDescription.PropertyType'] = prop_name
                post_data[
                    f'Order.OrderItems[0].Document.Properties[{property_index}].LegalDescription.SequenceNumber'] = property_index + 1
                field_names = prop_types.get(prop)
                for field_name in field_names:
                    field_name = 'LegalDescriptionRemarks' if field_name == 'Legal Description / Remarks' else field_name
                    field_name = 'GovtLot' if field_name == 'Govt Lot' else field_name
                    field_content = self._data['config'].test_data(
                        f"{self._get_oit()}.indexing.prop_values.{field_name}")
                    field_name_api = 'UnparsedProperty' if field_name == 'LegalDescriptionRemarks' else field_name
                    post_data[
                        f'Order.OrderItems[0].Document.Properties[{property_index}].LegalDescription.{field_name_api}'] = field_content
                property_index += 1

        if add_remark:
            post_data['Order.OrderItems[0].Document.DocumentRemarks[0].DDDesc'] = 'test remark'
            post_data['Order.OrderItems[0].Document.DocumentRemarks[0].DDSeq'] = 1
        if set_ref:
            inner_post_data = [
                ('orderItemTypeId', self.order_item_type_id),
                ('page', set_ref[1]),
                ('book', set_ref[0]),
                ('docGroupId', self.doc_group_id)
            ]

            self._actions.step(f"-> API -> get doc type desc by vol: {set_ref[0]}, page: {set_ref[1]} parameters")
            self.api.response = self.api.session.get(self.get_url(self.api.api_urls.GetDocTypeDescription),
                                                     params=inner_post_data)
            self._verify_response()
            doc_ref_data = self.api.response.json().get('data')[0]
            doc_ref_doc_id = doc_ref_data.get('DocumentId')
            doc_ref_doc_year = doc_ref_data.get('RecordedYear')
            doc_ref_doc_type_desc = doc_ref_data.get('DocumentTypeDesc')

            post_data['Order.OrderItems[0].Document.DocumentRefs[0].Volume'] = set_ref[0]
            post_data['Order.OrderItems[0].Document.DocumentRefs[0].Page'] = set_ref[1]
            post_data['Order.OrderItems[0].Document.DocumentRefs[0].DocumentId'] = doc_ref_doc_id
            post_data['Order.OrderItems[0].Document.DocumentRefs[0].Year'] = doc_ref_doc_year
            post_data['Order.OrderItems[0].Document.DocumentRefs[0].DocumentTypeDesc'] = doc_ref_doc_type_desc

        self.api.set_headers(self.api.api_test_data.indexing_headers)
        self._actions.step(f"-> API -> Save document# {self._data['doc_num']} in the {queue_name} process")
        self.api.response = self.api.session.post(link, data=post_data)
        self._verify_response(body_required=False)

    def _process_order_to_next_workflow(self, queue_name: str, task_id: str):
        """
        The function process order with already saved OIs to the next workflow step by given queue name and task_id

        :param queue_name: it should be 'indexing' or 'verification'
        :param task_id: indexing or verification task_id
        :return:
        """
        link = self.get_url(
            self.api.api_urls.ProcessIndexingTaskAndPickupTheNextOne) if queue_name == 'indexing' else self.get_url(
            self.api.api_urls.ProcessVerificationTaskAndPickupTheNextOne)
        post_data = ((f'{queue_name.capitalize()}TaskId', task_id),)
        self.api.set_headers(self.api.api_test_data.indexing_headers)
        self._actions.step(f"-> API -> Process order# {self._data['order_number']} to the next workflow step")
        self.api.response = self.api.session.get(link, params=post_data)
        self._verify_response(body_required=False)

    def _start_scanner_session(self, scanner_session: int, document_id: int, insert_index: int,
                               is_insert_action: bool) -> int:
        post_data = self.api.api_test_data.initiate_scan_session_data.copy()
        post_data['ScannerTaskId'] = scanner_session
        post_data['ScannerTaskConfiguration']['DocumentId'] = document_id
        post_data['ScannerTaskConfiguration']['InsertIndex'] = insert_index
        post_data['ScannerTaskConfiguration']['IsInsertAction'] = is_insert_action

        self.api.set_content_type('application/json')
        self._actions.step(f"-> API -> Initiate Scan Session")
        self.api.response = self.api.session.post(self.get_url(self.api.api_urls.InitiateScanSession), json=post_data)

        self._verify_response()
        return self.api.response.json()

    def _get_scanned_files(self, scanner_session: int, current_docs_count: int, selected_file_id: int) -> list:
        post_data = {
            'scannerTaskId': scanner_session,
            'currentDocsCount': current_docs_count,
            'selectedFileId': selected_file_id,
        }
        self._actions.step(f"-> API -> Getting the scanned files")
        scanned_files, attempt_count = None, 10
        while not scanned_files and attempt_count:
            try:
                self.api.response = self.api.session.get(self.get_url(self.api.api_urls.GetLastScannedFiles),
                                                         params=post_data)
                self._verify_response(body_required=False)
                scanned_files = self.api.response.json().get('scannedFiles')
                attempt_count -= 1
                self._actions.wait(3)
            except Exception as e:
                self.api.set_content_type('application/json')
                self.api.response = self.api.session.post(self.get_url(self.api.api_urls.StopBatchScan),
                                                          json=scanner_session)
                raise e
        return scanned_files

    def _prepare_user_header_data(self, post_data: list, user_address: dict, user_id: int) -> list:
        """
        The function modifies given post_data with adding the user address data

        :param post_data: The data that will be used in pos request
        :param user_address: The user address data
        :param user_id: The user id
        :return:
        """
        if ('Order.OrderHeader.OrderUser.UserType', 'Personal') in post_data:
            post_data.remove(('Order.OrderHeader.OrderUser.UserType', 'Personal'))
        post_data.append(('Order.OrderHeader.OrderUser.UserType', 'Guest'))
        post_data.append(('Order.OrderHeader.OrderUser.User.Email', ''))
        post_data.append(('Order.OrderHeader.OrderUser.PersonalUserId', user_id))
        post_data.append(('Order.OrderHeader.OrderUser.User.Address.Email', user_address.get('Email')))
        post_data.append(('Order.OrderHeader.OrderUser.User.Address.AddressId', user_address.get('AddressId')))  # noqa
        post_data.append(('Order.OrderHeader.OrderUser.User.Address.AddressName', user_address.get('AddressName')))
        post_data.append(('Order.OrderHeader.OrderUser.User.Address.PhoneNumber', user_address.get('PhoneNumber')))
        post_data.append(('Order.OrderHeader.OrderUser.User.Address.AddressLine1', user_address.get('AddressLine1')))
        post_data.append(('Order.OrderHeader.OrderUser.User.Address.ZipCode', user_address.get('ZipCode')))
        post_data.append(('Order.OrderHeader.OrderUser.User.Address.City', user_address.get('City')))
        post_data.append(('Order.OrderHeader.OrderUser.User.Address.StateCode', user_address.get('StateCode')))
        post_data.append(('Order.OrderHeader.OrderUser.User.UnparsedName',
                          self._data.config.config_file.ORDER_HEADER.get('guest')['value']))
        return post_data
