"""
DB connection and project wide DB query methods
"""
import requests
from golem import actions
import pymssql
import logging
from datetime import datetime, timedelta
from projects.Kofile.Lib.general_helpers import GeneralHelpers
from projects.Kofile.Lib.VPN import vpn_connect, vpn_disconnect


class DB:
    """
    DB connection and project wide DB query methods.
    if VPN is required, VPN connection should be established
    before any of these methods
     data - environment settings
    """
    connection = None
    cursor = None

    def __init__(self, data):
        self._config = data["env"].get("project_db")
        if self._config:
            self.database = self._config["database"]
            self.tenant_schema = f"VG{data['env']['code']}"
            self.data = data

    def __enter__(self):
        try:
            vpn_connect()
            self.connect_to_db()
            return self
        except Exception as e:
            vpn_disconnect()
            raise ValueError(f"DB connection fail!: {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect_from_db()
        vpn_disconnect()

    def __del__(self):
        try:
            self.disconnect_from_db()
            vpn_disconnect()
        except AssertionError:
            pass

    def connection_test(self):
        self.cursor.execute("SELECT @@VERSION")
        if version := self.cursor.fetchone():
            logging.info(f"CONNECTION IS OK, VERSION: {version}")

    def connect_to_db(self, connection_timeout=10, retry=5, use_vpn=False):
        """
        establishes DB connection, returns active DB connection, or None if error.
        active DB connection is stored in 'self.connection' variable
         connection_timeout - timeout to connect to db
        """
        try:
            if use_vpn:
                vpn_connect()
            conn, error = None, None
            for _ in range(retry):
                try:
                    conn = pymssql.connect(self._config["server"], self._config["user"], self._config["password"],
                                           self.database, login_timeout=connection_timeout)
                    break
                except Exception as e1:
                    error = e1
                    actions.wait(3)
            if conn is None:
                raise error
            self.connection = conn
            self.cursor = conn.cursor()
            logging.info("[DB connected successfully]")
            return conn
        except Exception as e:
            assert not e, f"Unable to connect to DB:\n\t{e}"

    def disconnect_from_db(self, use_vpn=False):
        """
        disconnects existing DB connection
        """
        try:
            if use_vpn:
                vpn_disconnect()
            self.connection.close()
            logging.info("[DB disconnected successfully]")
        except Exception as e:
            assert not e, f"Unable to disconnect from DB:\n\t{e}"

    def get_workstation_by_ip(self, ip):
        query = f"""select top 1 WORK_STATION_ID from {self.database}.{self.tenant_schema}.WORK_STATION 
        where WORK_STATION_ADDRESS = '{ip}';"""
        self.cursor.execute(query)
        data = self.cursor.fetchone()
        return data[0] if data else None

    def get_location_by_workstation(self, workstation_id):
        query = f"""select top 1 location_id from {self.database}.{self.tenant_schema}.location_work_station 
                where work_station_id = '{workstation_id}';"""
        self.cursor.execute(query)
        data = self.cursor.fetchone()
        return data[0] if data else None

    def update_location(self, workstation_id, location_id):
        query = f"""update {self.database}.{self.tenant_schema}.location_work_station set location_id={location_id}
         where work_station_id={workstation_id}"""
        self.cursor.execute(query)
        self.connection.commit()

    def get_status_auto_redaction_job(self, order_number):
        query = f"""SELECT status_id FROM {self.database}.{self.tenant_schema}.AUTO_REDACTION_TASK 
        WHERE ORDER_ID in (SELECT ORDER_ID FROM {self.database}.{self.tenant_schema}.[ORDER] 
        WHERE ORDER_NUM = {order_number})"""
        self.cursor.execute(query)
        data = self.cursor.fetchone()
        return data[0] if data else 0

    def scheduler_job_update_for_export(self, scheduler_job_code="ExportOneTime"):
        """
        updates schedule job, based on schedule job code
         scheduler_job_code - string, 'ExportOneTime', 'ExportDaily', 'ExportWeekly', 'ExportMonthly', 'ExportYearly'
        """
        actions.step("[DB] -> Scheduler job update for export")
        sql_update_scheduler_job = """
            UPDATE {0}.VANGUARD.SCHEDULE_JOB
            SET NEXT_EXECUTE_DATE = DATEADD(SECOND, 1, GETDATE()), IS_CANCELED = 0
            WHERE TENANT_ID = (
                SELECT TENANT_ID
                FROM {0}.VANGUARD.TENANT
                WHERE TENANT_SCHEMA = '{1}')
            AND SCHEDULE_JOB_CODE = '{2}'
        """.format(self.database, self.tenant_schema, scheduler_job_code)

        sql_update_is_canceled_value = """
            UPDATE {0}.VANGUARD.SCHEDULE_JOB
            SET IS_CANCELED = 1
            WHERE TENANT_ID = (
                SELECT TENANT_ID
                FROM {0}.VANGUARD.TENANT
                WHERE TENANT_SCHEMA = '{1}')
            AND SCHEDULE_JOB_CODE = '{2}'
        """.format(self.database, self.tenant_schema, scheduler_job_code)

        # select existing data
        result_before = self.get_schedule_job_next_execute_date(scheduler_job_code)
        is_canceled_before = result_before[0]
        next_execute_date_before = result_before[1]
        logging.info(f"[DB] -> IS_CANCELED before update {is_canceled_before}\n"
                     f"NEXT_EXECUTE_DATE before update {next_execute_date_before}")
        # update schedule job
        self.cursor.execute(sql_update_scheduler_job)
        self.connection.commit()
        # select updated data
        result_after = self.get_schedule_job_next_execute_date(scheduler_job_code)
        is_canceled_after = result_after[0]
        next_execute_date_after = result_after[1]
        logging.info(f"[DB] -> IS_CANCELED after update {is_canceled_after}\n"
                     f"NEXT_EXECUTE_DATE after update {next_execute_date_after}")
        if bool(is_canceled_before):
            self.cursor.execute(sql_update_is_canceled_value)
            self.connection.commit()
        return True

    def get_department_id(self, dept_name="plats"):
        query = """
            SELECT DEPT_ID
            FROM VANGUARD.DEPT
            WHERE DEPT_DESC = '{}'
        """.format(dept_name)
        self.cursor.execute(query)
        return self.cursor.fetchall[0][0]

    def get_states(self):
        query = """select ST_CODE from VANGUARD.STATE"""
        self.cursor.execute(query)
        return [i[0] for i in self.cursor.fetchall()]

    def get_schedule_job_next_execute_date(self, department):
        """return (IS_CANCELED, NEXT_EXECUTE_DATE) values for department"""
        department = f"EsExportDep{department}" if str(department).isdigit() else department
        sql_get_values = """
            SELECT IS_CANCELED, NEXT_EXECUTE_DATE
            FROM {0}.VANGUARD.SCHEDULE_JOB
            WHERE TENANT_ID = (
                SELECT TENANT_ID
                FROM {0}.VANGUARD.TENANT
                WHERE TENANT_SCHEMA = '{1}')
            AND SCHEDULE_JOB_CODE = '{2}'
        """.format(self.database, self.tenant_schema, department)
        self.cursor.execute(sql_get_values)
        return self.cursor.fetchone()

    def get_package_status(self, order_number):
        sql = f"select ER_PACKAGE_STATUS_ID from {self.database}.{self.tenant_schema}.ER_PACKAGE where ORDER_NUM = {order_number}"
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        assert data, f"Cant find recorder in {self.database}.{self.tenant_schema}.ER_PACKAGE with order number {order_number}"
        return data[0]

    def scheduler_job_update_for_set_export_document(self, dept_name="plats", dept_id=None):
        """
        updates department schedule job, based on department name
         dept_name - department name
        """
        actions.step("[DB] -> Scheduler job update for set export document")
        department_id = dept_id if dept_id else self.get_department_id(dept_name)

        sql_update_scheduler_job = """
            UPDATE {0}.VANGUARD.SCHEDULE_JOB
            SET NEXT_EXECUTE_DATE = DATEADD(SECOND, 1, GETDATE())
            WHERE TENANT_ID = (
                SELECT TENANT_ID
                FROM {0}.VANGUARD.TENANT
                WHERE TENANT_SCHEMA = '{1}')
            AND SCHEDULE_JOB_CODE = 'EsExportDep{2}'
        """.format(self.database, self.tenant_schema, department_id)
        # update schedule job
        self.cursor.execute(sql_update_scheduler_job)
        self.connection.commit()
        # select updated data
        next_execute_date_after = self.get_schedule_job_next_execute_date(department_id)[1]
        logging.info("NEXT_EXECUTE_DATE after update {}".format(next_execute_date_after))
        return True

    def get_info_via_given_table_and_columnname(self, table_name, select_column_name, where_column_name="",
                                                where_value=""):
        """
        returns specified value
        """
        actions.step(f"[DB] -> Get info from '{table_name}' table and '{select_column_name}' column")
        if where_column_name and where_value:
            query = """
                SELECT {}
                FROM {}.{}.[{}]
                WHERE {} = '{}'
            """.format(select_column_name, self.database, self.tenant_schema, table_name, where_column_name,
                       where_value)
        else:
            query = """
                SELECT {}
                FROM {}.{}.[{}]
            """.format(select_column_name, self.database, self.tenant_schema, table_name)
        logging.info(f"[DB] -> {query}")
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # KDI EXPORT - - - - - - - - - - - - - - - - - - - - - - - - -
    def kdi_export(self, order_number):
        actions.step("[DB] -> KDI export")
        # asynchronous DM_CONTENT export
        self.update_scheduler_next_execution_date("OrderItemContentExport")
        # get indexing status
        indexing_task_id = self.get_indexing_task_id(order_number)
        status = self.get_kdi_index_status(indexing_task_id)
        retry_1 = 10
        while status != 3 and retry_1:
            reference_id = self.get_reference_id(indexing_task_id)
            retry_2 = 4
            while (not reference_id) and retry_2:
                # export to KDI
                self.update_scheduler_next_execution_date("IndexedDocExport")
                reference_id = self.get_reference_id(indexing_task_id)
                retry_2 -= 1
            # import from KDI
            self.update_scheduler_next_execution_date("IndexedDocImport")
            status = self.get_kdi_index_status(indexing_task_id)
            retry_1 -= 1

    def update_scheduler_next_execution_date(self, schedule_job_code):
        query = """
                    UPDATE {0}.VANGUARD.SCHEDULE_JOB
                    SET NEXT_EXECUTE_DATE = DATEADD(SECOND, 1, GETDATE())
                    WHERE TENANT_ID = (
                        SELECT TENANT_ID
                        FROM {0}.VANGUARD.TENANT
                        WHERE TENANT_SCHEMA = '{1}')
                    AND SCHEDULE_JOB_CODE = '{2}'
                """.format(self.database, self.tenant_schema, schedule_job_code)

        self.cursor.execute(query)
        self.connection.commit()
        actions.wait(3)

    def insert_file(self, user_index=0):
        data = GeneralHelpers.get_data()
        sql = f"select top 1 PATH from {self.database}.{self.tenant_schema}.SCANNED_FILE " \
              "where PATH is not NULL and SCANNER_TASK_ID is not NULL;"
        self.cursor.execute(sql)
        path = self.cursor.fetchone()[0]
        sql = f"insert into {self.database}.{self.tenant_schema}.SCANNER_TASK select top 1 WORKSTATION_ID, " \
              f"SCANNER_CONFIGURATION, 4, SCANNER_ID, SCANNER_TASK_CONFIGURATION, " \
              f"CLERK_DETAILS from {self.database}.{self.tenant_schema}.SCANNER_TASK where status = 4 " \
              f"order by SCANNER_TASK_ID desc;"
        self.cursor.execute(sql)
        self.connection.commit()
        self.cursor.execute("SELECT @@IDENTITY AS ID;")
        scanner_id = self.cursor.fetchone()[0]

        sql = f"select ADUSER_ID from {self.database}.{self.tenant_schema}.AD_USER where ADUSER_FIRSTNAME=" \
              f"'{data['env']['user_first'][user_index]}' and ADUSER_LASTNAME='{data['env']['user_last'][user_index]}';"
        self.cursor.execute(sql)
        user_id = self.cursor.fetchone()[0]

        sql = f"insert into {self.database}.{self.tenant_schema}.SCANNER_BATCH VALUES ({user_id}, {scanner_id}, 4)"
        self.cursor.execute(sql)
        self.connection.commit()

        sql = f"insert into {self.database}.{self.tenant_schema}.SCANNED_FILE VALUES(NULL, NULL, YEAR(GETDATE()), 1, " \
              f"NULL , '{path}', {self.database}.{self.tenant_schema}.GetTenantDate(), " \
              f"NULL, {scanner_id}, 2, 1, 1, NULL, 1, 0);"

        self.cursor.execute(sql)
        self.connection.commit()
        self.cursor.execute("SELECT @@IDENTITY AS ID;")
        l_id = self.cursor.fetchone()[0]
        return int(l_id), int(scanner_id), path

    def get_indexing_task_id(self, order_number):
        query = """
                    SELECT INDEXING_TASK_ID 
                    FROM {0}.{1}.INDEXING_TASK_ORDER_ITEM 
                    WHERE ORDER_ITEM_ID IN
                    (SELECT ORDER_ITEM_ID FROM {0}.{1}.ORDER_ITEM WHERE ORDER_ID in 
                    (SELECT ORDER_ID FROM {0}.{1}.[ORDER] WHERE ORDER_NUM = {2}))
        """.format(self.database, self.tenant_schema, order_number)

        self.cursor.execute(query)
        result = self.cursor.fetchone()
        indexing_task_id = result[0] if result else None
        return indexing_task_id

    def get_reference_id(self, indexing_task_id):
        query = """
                    SELECT REFERENCE_ID
                    FROM {0}.{1}.KOFILE_INDEX
                    WHERE INDEXING_TASK_ID = {2}
        """.format(self.database, self.tenant_schema, indexing_task_id)

        self.cursor.execute(query)
        result = self.cursor.fetchone()
        reference_id = result[0] if result else None
        if reference_id:
            actions.step("KDI export finished successfully")
        return reference_id

    def get_kdi_index_status(self, indexing_task_id):
        query = """
                    SELECT INDEX_STATUS_ID
                    FROM {0}.{1}.KOFILE_INDEX
                    WHERE INDEXING_TASK_ID = {2}
        """.format(self.database, self.tenant_schema, indexing_task_id)

        self.cursor.execute(query)
        result = self.cursor.fetchone()
        index_status_id = result[0] if result else None
        if index_status_id == 3:
            actions.step("KDI import finished successfully")
        return index_status_id

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # BALANCE DRAWER - - - - - - - - - - - - - - - - - - - - - - -
    def get_available_payments(self, order_num):
        """
        returns all available payments
        """

        query = """
        select PAYMENT_METHOD_NAME from {0}.{1}.ORDER_ITEM_TYPE_PAYMENT_METHOD oitpm
        join {0}.{1}.PAYMENT_METHOD pm on pm.PAYMENT_METHOD_ID=oitpm.PAYMENT_METHOD_ID
        where  (IS_MANUAL_DEPOSIT=1 or PAYMENT_METHOD_NAME='Credit Card')
        and ORDER_ITEM_TYPE_ID in
        (select ORDER_ITEM_TYPE_ID from {0}.{1}.ORDER_ITEM where ORDER_ID in 
        (select order_id from {0}.{1}.[Order] where ORDER_NUM={2}))
        """.format(self.database, self.tenant_schema, order_num)

        logging.info(f"[DB] -> {query}")
        payments = []
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        for payment in result:
            payments.append(str(payment[0]))
        return payments

    def get_ad_user_id_by_user_name(self, user_name):
        """Return ADUSED_ID for specified user_name"""
        logging.info(f"[DB] -> Get ADUSED_ID for user '{user_name}'")
        query = """SELECT [ADUSER_ID]
                   FROM {}.{}.[AD_USER]
                   WHERE ADUSER_DOMAIN LIKE '%{}'
                   """.format(self.database, self.tenant_schema, user_name)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        assert result, f"ADUSER_ID for user'{user_name}' not found!"
        logging.info(f"-> '{result[0][0]}'")
        return result[0][0]

    def get_active_balance_session(self, user_name=None, drawer_id=None):
        """Return active balance session_id for specified user_name"""
        if not user_name and not drawer_id:
            return ""
        aduser_id = self.get_ad_user_id_by_user_name(user_name) if user_name else ""
        logging.info(f"[DB] -> Get active balance session for "
                     f"'{user_name if user_name else ''}[{aduser_id if aduser_id else drawer_id}]'")
        date = datetime.now().strftime("%m/%d/%Y")
        column = "ADUSER_ID" if aduser_id else "DEVICE_ID"
        value = aduser_id if aduser_id else drawer_id

        query = """SELECT BALANCESESSION_ID 
                   FROM {}.{}.[BM_BALANCESESSION] 
                   WHERE {} = '{}'
                   AND CONVERT(DATE, initialize_date, 101) = '{}'
                """.format(self.database, self.tenant_schema, column, value, date)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        logging.info(f"-> '{result}'")
        if result:
            result = ",".join(str(i[0]) for i in result)  # if sessions more than 1
            return result
        else:
            return False

    def delete_active_balance_session(self, user_name=None, balance_session_id=None, drawer_id=None):
        """
        DELETE active session for specified user_name
            or delete specified balance_session_id
        """
        tables = ['BM_BALANCE', 'BM_BALANCEPOST', 'BM_BALANCEPOST_HISTORY', 'BM_BALANCE_CHEQUE', 'BM_BALANCESESSION']
        if not any(i for i in [user_name, drawer_id, balance_session_id]):
            return False
        balance_session_id = balance_session_id if balance_session_id else \
            self.get_active_balance_session(user_name=user_name, drawer_id=drawer_id)
        if not balance_session_id:
            logging.info(f"[DB] -> Balance session for '{user_name if user_name else drawer_id}' not found")
            return
        actions.step(f"[DB] -> DELETE balance session '{balance_session_id}' for "
                     f"'{user_name if user_name else drawer_id}'")
        for table in tables:
            query = """DELETE FROM {}.{}.{} WHERE BALANCESESSION_ID IN ({})""" \
                .format(self.database, self.tenant_schema, table, balance_session_id)
            logging.info(query)
            self.cursor.execute(query)
        self.connection.commit()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def update_device_job_for_ocr(self, ip):
        """
        updates device job for a given workstation IP address
         ip - workstation IP address
        """
        actions.step("[DB] -> Update device job for OCR")
        query = """
            UPDATE {0}.{1}.DEVICE_JOB
            SET DEVICE_JOB_STATUS = 1, NEXT_EXECUTION_DATE = DATEADD(SECOND, 1, GETDATE())
            WHERE CAST(DEVICE_JOB_CONFIG AS NVARCHAR(MAX)) LIKE '%FileCopyJobConfig%'
                AND DEVICE_ID IN (
                    SELECT DEVICE_ID
                    FROM {0}.{1}.DEVICE
                    WHERE DEVICE_HOST_ADDR = '{2}'
                        AND DEVICE_TYPE_ID = 10)
        """.format(self.database, self.tenant_schema, ip)
        logging.info(f"[DB] -> {query}")
        self.cursor.execute(query)
        self.connection.commit()

    def get_last_ocr_number_by_host_ip(self, retries=15):
        """
        returns last OCR order number
        """
        actions.step("[DB] -> Get last OCR number")
        query = f"""SELECT top 1 o.ORDER_NUM FROM {self.database}.{self.tenant_schema}.ORDER_ITEM oi
                JOIN {self.database}.{self.tenant_schema}.[ORDER] o ON o.ORDER_ID = oi.ORDER_ID
                WHERE ORDER_ITEM_ID in
                    (SELECT top 5 [ORDER_ITEM _ID] FROM {self.database}.{self.tenant_schema}.OCR_SUBMIT_HISTORY 
                    WHERE ACTION_INFO = 'SubmittedOcr'
                    AND DATE_TIME >= DATEADD(MINUTE, -5, {self.database}.{self.tenant_schema}.GetTenantDate())
                    ORDER BY DATE_TIME DESC) 
                and oi.ORDER_ITEM_TYPE_ID = {self.data.OIT_ID} and o.WORKFLOW_STEP_ID = 3 order by o.ORDER_NUM desc"""
        logging.info(f"[DB] -> {query}")
        while retries:
            retries -= 1
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            if len(results) > 0:
                return results[0][0]
            else:
                actions.wait(10)
        raise Exception("Last ocr number by host ip not found in database")

    def update_all_scanner_statuses(self):
        actions.step("[DB] -> Update all scanner statuses")
        query = """
            UPDATE {}.{}.SCANNER
            SET SCANNER_STATUS = 1
            WHERE SCANNER_STATUS = 3
        """.format(self.database, self.tenant_schema)
        logging.info(f"[DB] -> {query}")
        self.cursor.execute(query)
        self.connection.commit()

    def get_is_refundable_and_refund_days_from_payment_method(self, method="Cash"):
        query = """SELECT Is_Refundable, refund_days 
        FROM {}.{}.PAYMENT_METHOD 
        where PAYMENT_METHOD_NAME='{}';
                """.format(self.database, self.tenant_schema, method)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def update_refundable_and_refund_days_from_payment_method(self, is_refundable=1, refund_days=1, method="Cash"):
        __is_refundable, __refund_days = self.get_is_refundable_and_refund_days_from_payment_method()
        if is_refundable != __is_refundable or refund_days != __refund_days:
            query = """UPDATE {}.{}.PAYMENT_METHOD SET Is_Refundable={}, refund_days={}
                    where PAYMENT_METHOD_NAME='{}';
                            """.format(self.database, self.tenant_schema, is_refundable, refund_days, method)
            self.cursor.execute(query)
            self.connection.commit()

    def confirm_user_by_email(self, email, hash_pwd, hash_salt, status=3):
        query = f"""UPDATE {self.database}.VANGUARD.[USER] SET PASSWORD='{hash_pwd}', PASSWORD_SALT='{hash_salt}', 
                    USER_STATUS_ID={status}, ISAPPROVED=1, ISLOCKED=0 where EMAIL_ID='{email}';"""
        self.cursor.execute(query)
        self.connection.commit()

    def set_account_password(self, account):
        query = f"""UPDATE {self.database}.{self.tenant_schema}.[ACCOUNT] SET erSUBMITTER_PASSWORD='{account}' 
                    where ACCT_CODE='{account}';"""
        self.cursor.execute(query)
        self.connection.commit()

    def set_er_schema(self, account_code, config_id, schema_name):
        query = f"""SELECT ACCT_ID from {self.database}.{self.tenant_schema}.[ACCOUNT] 
                where ACCT_CODE='{account_code}';"""
        self.cursor.execute(query)
        account_id = self.cursor.fetchone()
        assert account_id, f"account {account_code} not found"
        query = f"""insert into {self.database}.{self.tenant_schema}.[ER_SCHEMA] (ER_SCHEMA_NAME, CONFIG_ID, ACCOUNT_ID)
                    VALUES ('{schema_name}', {config_id}, {account_id[0]});"""
        self.cursor.execute(query)
        self.connection.commit()

    def get_file_name_by_started_pattern_from_xml(self, pattern, device_job_id=None):
        xml_data = self.get_last_device_jobs(10, device_job_id=device_job_id)
        for i in xml_data:
            file_name = i[5].split("FilePath")[1]
            if pattern in file_name:
                return file_name.translate({ord(i): None for i in '></'})

    def update_pending_status_to_reviewed_order_summary(self, orderid):
        query = """CREATE TABLE #OITS
            (
                Seq INT IDENTITY(1,1),
                ID INT NOT NULL
            )

            INSERT INTO #OITS
            SELECT ORDER_ITEM_ID AS ID FROM {0}.{1}.ORDER_ITEM WHERE ORDER_ID = {2}

            SELECT ID FROM #OITS


            DECLARE @cnt INT, @i  INT = 1 

            SELECT @cnt = COUNT(*) FROM #OITS

            WHILE (@i<=@cnt)
            BEGIN
            DECLARE @OIID INT
            SELECT @OIID = ID FROM #OITS WHERE Seq = @i

            IF (SELECT count(*) FROM {0}.{1}.ORDER_ITEM_STATUS WHERE ORDER_ITEM_ID = @OIID) <> 1
            BEGIN 
            INSERT INTO {0}.{1}.ORDER_ITEM_STATUS VALUES (@OIID,1,NULL)
            END 

            SET @i=@i+1

            END

            DROP TABLE #OITS""".format(self.database, self.tenant_schema, orderid)
        self.cursor.execute(query)
        self.connection.commit()

    def get_device_jobs_id(self, device_id, device_job_id):
        query = f"""select top 1 DEVICE_JOB_ID 
                       from {self.database}.{self.tenant_schema}.DEVICE_JOB 
                       where DEVICE_JOB_ID > {device_job_id} AND DEVICE_ID = {device_id} 
                       order by DEVICE_JOB_ID desc"""
        self.cursor.execute(query)
        data = self.cursor.fetchone()
        return data[0] if data else 0

    def get_last_device_jobs(self, count=1, device_id=None, device_job_id=None):
        """return last DEVICE_JOB"""
        if device_job_id:
            sql_get_values = f"""SELECT * FROM {self.tenant_schema}.DEVICE_JOB WHERE DEVICE_JOB_ID = {device_job_id}"""
        else:
            if device_id:
                sql_get_values = f"""SELECT  TOP {count} * FROM {self.tenant_schema}.DEVICE_JOB WHERE 
                DEVICE_ID = {device_id} ORDER BY CREATED_DATE DESC"""
            else:
                if self.data.get('order_number'):
                    if self.data.get('device_id'):
                        sql_get_values = """
                            SELECT  TOP {1} * FROM {0}.DEVICE_JOB
                            WHERE ORDER_ID = (SELECT ORDER_ID FROM {0}.[ORDER] WHERE ORDER_NUM = '{2}') 
                            AND DEVICE_ID = {3}
                            ORDER BY 
                            CREATED_DATE DESC
                        """.format(self.tenant_schema, count, self.data.order_number, self.data.device_id)
                    else:
                        sql_get_values = """
                            SELECT  TOP {1} * FROM {0}.DEVICE_JOB
                            WHERE ORDER_ID = (SELECT ORDER_ID FROM {0}.[ORDER] WHERE ORDER_NUM = '{2}') ORDER BY 
                            CREATED_DATE DESC
                        """.format(self.tenant_schema, count, self.data.order_number)
                else:
                    sql_get_values = """
                        SELECT  TOP {1} * FROM {0}.DEVICE_JOB
                            ORDER BY CREATED_DATE DESC
        """.format(self.tenant_schema, count)
        logging.info(f"[DB] -> {sql_get_values}")
        self.cursor.execute(sql_get_values)
        return self.cursor.fetchall()

    def get_doc_type_id_by_doc_type_code(self, doc_type_code):
        """Return DOC_TYPE_ID for specified doc_type_code"""
        logging.info(f"[DB] -> Get DOC_TYPE_ID for doc type '{doc_type_code}'")
        query = """SELECT [DOC_TYPE_ID] 
                FROM {}.{}.[DOC_TYPE] 
                WHERE DOC_TYPE_CODE='{}'
                   """.format(self.database, self.tenant_schema, doc_type_code)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        assert result, f"DOC_TYPE_ID for doc type '{doc_type_code}' not found!"
        logging.info(f"-> '{result[0][0]}'")
        return result[0][0]

    def get_exist_doc_number_and_year_by_department(self):
        query = f"""select top 1 
                  DM_YEAR,
                  CF_VCINSTNUM
                from {self.database}.{self.tenant_schema}.DOC_MASTER  
                where DEPT_ID = {self.data.departments.RP} 
                and CF_VCINSTNUM is not NULL and DM_YEAR is not null
                and DM_BK IS NOT NULL AND DM_PAGE IS NOT null"""
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_exist_doc_number_and_year_by_department_with_parties(self, doc_type):
        query = f"""select top 1 
                  DM_YEAR,
                  CF_VCINSTNUM
                from {self.database}.{self.tenant_schema}.DOC_MASTER  dm
                JOIN {self.database}.{self.tenant_schema}.DM_PARTIES dmp
                ON dmp.DM_ID=dm.DM_ID
                where DEPT_ID = {self.data.departments.RP} and CF_VCINSTNUM is not NULL and DM_YEAR is not null
                and dmp.PARTY_NAME1 IS NOT NULL AND dmp.PARTY_NAME2 IS NOT null
                AND dm.DOC_TYPE_ID IN (
                SELECT DOC_TYPE_ID FROM {self.database}.{self.tenant_schema}.
                       DOC_TYPE WHERE DOC_TYPE_CODE='{doc_type}')
"""
        self.cursor.execute(query)
        res = self.cursor.fetchone()
        assert res, f'No data found using SQL: \n {query}'
        return res

    def get_exist_doc_vol_and_page_by_department(self):
        query = f"""select top 1 
                  DM_BK, DM_PAGE
                from {self.database}.{self.tenant_schema}.DOC_MASTER dm
                JOIN {self.database}.{self.tenant_schema}.DM_PARTIES dm_p ON dm.DM_ID = dm_p.DM_ID
                where dm.DM_PAGE is not null 
                and dm.DM_BK is not null 
                and NULLIF(dm.DM_PAGE, '') IS NOT NULL
                and NULLIF(dm.DM_BK, '') IS NOT NULL
                and dm.DEPT_ID={self.data.departments.RP};"""
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_historical_capture_doc_groups(self):
        query = """SELECT WF.DOC_GROUP_ID, DG.DOC_GROUP_DESC, OIT.ORDER_ITEM_TYPE_DISPLAY_NAME
                    FROM {0}.{1}.WORKFLOW AS WF
                        INNER JOIN {0}.{1}.DOC_GROUP AS DG ON DG.DOC_GROUP_ID = WF.DOC_GROUP_ID
                        INNER JOIN {0}.{1}.ORDER_ITEM_TYPE AS OIT ON OIT.ORDER_ITEM_TYPE_ID = WF.ORDER_ITEM_TYPE_ID
                    WHERE WF.TENANT_SERVICE_TYPE_ID IN (
                        SELECT TENANT_SERVICE_TYPE_ID FROM {0}.{1}.TENANT_SERVICE_TYPE WHERE SERVICE_TYPE_ID IN (
                            SELECT SERVICE_TYPE_ID FROM VANGUARD.SERVICE_TYPE 
                            WHERE SERVICE_TYPE_DESC = 'Historical Capture'))
                """.format(self.database, self.tenant_schema)
        logging.info(f"[DB] -> {query}")
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        logging.info(f"[DB] <-- {result}")
        return result

    def update_printer_job(self, device_id, job_id=None):
        if job_id:
            query = """update {0}.{1}.DEVICE_JOB 
                                    set DEVICE_JOB_STATUS = 3
                                    where DEVICE_JOB_ID = {2}""".format(self.database, self.tenant_schema, job_id)
        else:
            query = """update {0}.{1}.DEVICE_JOB 
                        set DEVICE_JOB_STATUS = 3
                        where DEVICE_ID = {2}""".format(self.database, self.tenant_schema, device_id)
        logging.info(f"[DB] -> {query}")
        self.cursor.execute(query)
        self.connection.commit()

    def get_order_item_content_export_by_order_number(self, order_num):
        """check that OIT is taken from order item export table"""
        query = """           
            SELECT * FROM {0}.ORDER_ITEM_CONTENT_EXPORT WHERE ORDER_ITEM_ID IN 
            (SELECT ORDER_ITEM_ID FROM {0}.ORDER_ITEM WHERE ORDER_ID IN 
            (SELECT ORDER_ID FROM {0}.[ORDER] WHERE ORDER_NUM='{1}'))
                """.format(self.tenant_schema, order_num)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_account_balance_by_account_code(self, account_code):
        """return last ACCT_BALANCE for mentioned ACCT_CODE"""
        sql_get_values = """
                SELECT TOP 1 ACCT_BALANCE FROM {0}.ACCOUNT_ACTIVITY 
                WHERE ACCT_ID=(SELECT ACCT_ID from {0}.ACCOUNT WHERE 
                ACCT_CODE='{1}') ORDER BY ACCT_ACTIVITY_ID DESC
                """.format(self.tenant_schema, account_code)
        self.cursor.execute(sql_get_values)
        return self.cursor.fetchall()

    def update_files_in_upload_folder(self, folder_name, file_number):
        """"update Upload_Files table, set is_uploaded flag to 0
        for given folder"""
        query = """           
            UPDATE {0}.UPLOAD_FILES
            SET IS_UPLOADED=0
            WHERE UPLOAD_FILE_ID IN 
            (SELECT TOP {1} UPLOAD_FILE_ID FROM {0}.UPLOAD_FILES WHERE IS_UPLOADED=1 
            AND  FILE_NAME LIKE '{2}%'
            ORDER BY UPLOAD_FILE_ID desc)
                """.format(self.tenant_schema, file_number, folder_name)
        logging.info(f"[DB] -> {query}")
        self.cursor.execute(query)
        self.connection.commit()

    def get_active_files_in_upload_folder(self, folder_name):
        """return active files count (IS_UPLOADED = 0) from the Upload_Files table using specified folder name"""
        query = """
                SELECT count(UPLOAD_FILE_ID) from {0}.UPLOAD_FILES
                where FILE_NAME like '{1}%' and IS_UPLOADED = 0
                """.format(self.tenant_schema, folder_name)
        logging.info(f"[DB] -> {query}")
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_processing_fee_fund(self, order_num):
        """return processing fee fund value and fund name """
        sql_get_values = """
                SELECT total, feefund_desc FROM {0}.ORDER_FEE_FUND offn 
                JOIN {0}.FEE_FUND ff  ON ff.feefund_id=offn.feefund_id
                WHERE order_id in (Select order_id from {0}.[Order] where order_num={1})
                """.format(self.tenant_schema, order_num)
        self.cursor.execute(sql_get_values)
        return self.cursor.fetchone()[0]

    def get_oi_workflow_step_and_dmc_path(self, doc_num):
        """return order item's workflow step_id and dmc_path from dm_content table"""
        query = """
            SELECT oi.WORKFLOW_STEP_ID, dmc.DMC_PATH from {0}.DOC_MASTER dm
            join {0}.ORDER_ITEM oi on dm.DM_ID = oi.DM_ID
            left join {0}.DM_CONTENT dmc on dm.DM_ID = dmc.DM_ID
            where dm.CF_VCINSTNUM = '{1}' and dm.DM_RECORDED >= DATEADD(hour, -1, GETDATE())
            """.format(self.tenant_schema, doc_num)
        logging.info(f"[DB] -> {query}")
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_order_workflow_step(self, order_num):
        """return order's workflow step_id"""
        query = """
            SELECT WORKFLOW_STEP_ID FROM {0}.[ORDER] WHERE ORDER_NUM = '{1}'
            """.format(self.tenant_schema, order_num)
        logging.info(f"[DB] -> {query}")
        self.cursor.execute(query)
        data = self.cursor.fetchone()
        return data[0] if data else 0

    def get_tenant_date(self):
        query = "SELECT {0}.GetTenantDate()".format(self.tenant_schema)
        logging.info(f"[DB] -> {query}")
        self.cursor.execute(query)
        return self.cursor.fetchone()[0].strftime('%m/%d/%Y')

    def get_order_total_datetime_num_oit_price(self):
        query = f"""
        SELECT CONVERT(VARCHAR, ORDER_TOTAL), CONVERT(VARCHAR, ORDER_DATE, 101),FORMAT(ORDER_DATE, 'hh:mm tt'), ORDER_NUM, CONVERT(VARCHAR,PRICE)
        FROM {self.tenant_schema}.[ORDER]
        JOIN {self.tenant_schema}.ORDER_ITEM ON ORDER_ITEM.ORDER_ID = [ORDER].ORDER_ID
        WHERE ORDER_NUM = {self.data.get('order_number')}
        ORDER BY ORDER_ITEM_ID
        """
        logging.info(f"[DB] -> {query}")
        self.cursor.execute(query)
        return self.cursor.fetchall()


class DataBaseWithVPN:

    def __init__(self, data=None):
        self.data = data if data else actions.get_data()
        self.db = DB(self.data)

    def get_info_via_given_table_and_column_name(self, table_name, select_column_name, where_column_name, where_value):
        try:
            vpn_connect()
            self.db.connect_to_db()
            return self.db.get_info_via_given_table_and_columnname(
                table_name=table_name, select_column_name=select_column_name,
                where_column_name=where_column_name, where_value=where_value)
        except Exception as e:
            raise ValueError(f"Get info via given table('{table_name}') "
                             f"and column name('{select_column_name}') FAILED!: {e}")
        finally:
            self.db.disconnect_from_db()
            vpn_disconnect()

    def delete_drawer_session(self, user_name=None, drawer_id=None):
        try:
            vpn_connect()
            self.db.connect_to_db()
            self.db.delete_active_balance_session(user_name=user_name, drawer_id=drawer_id)
        except Exception as e:
            raise ValueError(e)
        finally:
            self.db.disconnect_from_db()
            vpn_disconnect()

    def update_device_job_for_ocr(self):
        vpn_disconnect()
        try:
            ip = requests.get("http://10.11.36.111:6329/").text
            vpn_connect()
            self.db.connect_to_db()
            return self.db.update_device_job_for_ocr(ip)
        except Exception as e:
            raise ValueError(f"Update device job for OCR FAILED!: {e}")
        finally:
            self.db.disconnect_from_db()
            vpn_disconnect()

    def get_last_ocr_number_by_host_ip(self):
        try:
            vpn_connect()
            self.db.connect_to_db()
            return self.db.get_last_ocr_number_by_host_ip()
        except Exception as e:
            raise ValueError(f"Get last OCR number FAILED!: {e}")
        finally:
            self.db.disconnect_from_db()
            vpn_disconnect()

    def scheduler_job_update_for_set_export_document(self, dept_id):
        try:
            vpn_connect()
            self.db.connect_to_db()
            res = self.db.scheduler_job_update_for_set_export_document(dept_id=dept_id)
            actions.wait(20)
            return res
        except Exception as e:
            raise ValueError(f"Scheduler export job update FAILED!: {e}")
        finally:
            self.db.disconnect_from_db()
            vpn_disconnect()

    def scheduler_job_update_for_export(self, scheduler_job_code):
        try:
            vpn_connect()
            self.db.connect_to_db()
            return self.db.scheduler_job_update_for_export(scheduler_job_code=scheduler_job_code)
        except Exception as e:
            raise ValueError(f"Scheduler job update for export FAILED!: {e}")
        finally:
            self.db.disconnect_from_db()
            vpn_disconnect()

    def update_all_scanner_statuses(self):
        try:
            vpn_connect()
            self.db.connect_to_db()
            return self.db.update_all_scanner_statuses()
        except Exception as e:
            raise ValueError(f"Scheduler job update for export FAILED!: {e}")
        finally:
            self.db.disconnect_from_db()
            vpn_disconnect()

    def get_payment_methods(self, order_num):
        try:
            vpn_connect()
            self.db.connect_to_db()
            return self.db.get_available_payments(order_num)
        except Exception as e:
            raise ValueError(e)
        finally:
            self.db.disconnect_from_db()
            vpn_disconnect()

    def update_oit_status_in_order_summary(self, order_id):
        try:
            vpn_connect()
            self.db.connect_to_db()
            return self.db.update_pending_status_to_reviewed_order_summary(order_id)
        except Exception as e:
            raise ValueError(f"Update for export FAILED!: {e}")
        finally:
            self.db.disconnect_from_db()
            vpn_disconnect()

    def check_async_export_executed(self, order_num, retries=5):
        try:
            vpn_connect()
            self.db.connect_to_db()
            while retries > 0:
                if self.db.get_order_item_content_export_by_order_number(order_num) is None:
                    break
                actions.wait(3)
                retries -= 1
        except Exception:
            raise ValueError(f"Order Item does not exported")
        finally:
            self.db.disconnect_from_db()
            vpn_disconnect()

    def select_last_device_jobs(self, count=1, device_job_id=None):
        try:
            vpn_connect()
            self.db.connect_to_db()
            return self.db.get_last_device_jobs(count, device_job_id=device_job_id)
        except Exception as e:
            raise ValueError(f"Device jobs select FAILED!: {e}")
        finally:
            self.db.disconnect_from_db()
            vpn_disconnect()

    def get_file_name_from_xml(self, row=0, device_job_id=None):
        xml_data = self.select_last_device_jobs(5, device_job_id=device_job_id)[row][5]
        return xml_data.split("FilePath")[1].translate({ord(i): None for i in '></'})

    def get_file_name_by_started_pattern_from_xml(self, pattern, device_job_id=None):
        xml_data = self.select_last_device_jobs(10, device_job_id=device_job_id)
        for i in xml_data:
            file_name = i[5].split("FilePath")[1]
            if isinstance(pattern, tuple):
                for x in pattern:
                    if x.get("data") in file_name:
                        return file_name.translate({ord(i): None for i in '></'}), x
            else:
                if pattern in file_name:
                    return file_name.translate({ord(i): None for i in '></'})

    def get_doc_type_id_by_doc_type_code(self, doc_type_code):
        try:
            vpn_connect()
            self.db.connect_to_db()
            return self.db.get_doc_type_id_by_doc_type_code(doc_type_code)
        except Exception as e:
            raise ValueError(f"Scheduler job update for export FAILED!: {e}")
        finally:
            self.db.disconnect_from_db()
            vpn_disconnect()

    def select_account_balance_by_account_code(self, account_code):
        try:
            vpn_connect()
            self.db.connect_to_db()
            return self.db.get_account_balance_by_account_code(account_code)
        except Exception as e:
            raise ValueError(f"Account balance select FAILED!: {e}")
        finally:
            self.db.disconnect_from_db()
            vpn_disconnect()

    def add_files_in_upload_folder(self, folder_name='BirthUpload', file_number=50):
        try:
            vpn_connect()
            self.db.connect_to_db()
            return self.db.update_files_in_upload_folder(folder_name, file_number)
        except Exception as e:
            raise ValueError(f"File upload FAILED!: {e}")
        finally:
            self.db.disconnect_from_db()
            vpn_disconnect()

    def get_processing_fee_fund_distribution(self, order_num):
        try:
            vpn_connect()
            self.db.connect_to_db()
            return self.db.get_processing_fee_fund(order_num)
        except Exception as e:
            raise ValueError(f"File upload FAILED!: {e}")
        finally:
            self.db.disconnect_from_db()
            vpn_disconnect()

    def get_active_balance_session(self, drawer_id):
        try:
            vpn_connect()
            self.db.connect_to_db()
            return self.db.get_active_balance_session(drawer_id=drawer_id)
        finally:
            self.db.disconnect_from_db()
            vpn_disconnect()

    def get_order_total_datetime_num_oit_price(self):
        try:
            vpn_connect()
            self.db.connect_to_db()
            return self.db.get_order_total_datetime_num_oit_price()
        finally:
            self.db.disconnect_from_db()
            vpn_disconnect()


class InternalDB:
    conn = None
    cur = None

    def __init__(self, data):
        self.data = data

    def __enter__(self):
        self.connect_to_sqlite()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect_from_sqlite()

    def __del__(self):
        self.disconnect_from_sqlite()

    def connect_to_sqlite(self, retries=20, wait_time=0.3):
        import sqlite3
        from projects.Kofile.testdata.names import Names
        while not self.conn or retries:
            retries -= 1
            try:
                self.conn = sqlite3.connect(Names(self.data).internal_db)
                self.cur = self.conn.cursor()
                self._create_cookies_table()
                return
            except Exception as e:
                if retries:
                    logging.warning(e)
                    actions.wait(wait_time)
                else:
                    self.disconnect_from_sqlite()
                    raise ValueError(e)

    def disconnect_from_sqlite(self):
        try:
            self.conn.close()
        except Exception as e:
            logging.warning(e)

    def _create_cookies_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS cookies
            (env_user TEXT PRIMARY KEY, created INTEGER, cookies TEXT, url TEXT);""")
        self.conn.commit()

    def get_cookies_for_user(self, user_index=0, crs=True):
        env_user = f"{'CRS' if crs else 'CS'}_{self.data.env.name}_{self.data.env.user[user_index]}"
        stamp = (datetime.now() - timedelta(minutes=30 if crs else 10)).timestamp().__int__()
        logging.info(f"Internal DB -> Load cookies for {env_user}")
        self.cur.execute("""SELECT cookies, url FROM cookies 
                            WHERE env_user == '{}' AND created > {};""".format(env_user, stamp))
        result = self.cur.fetchone()
        return result if result else (None, None)

    def save_cookies_for_user(self, cookies, url, user_index=0, crs=True):
        env_user = f"{'CRS' if crs else 'CS'}_{self.data.env.name}_{self.data.env.user[user_index]}"
        stamp = datetime.now().timestamp().__int__()
        logging.info(f"Internal DB -> Save cookies for {env_user}")
        self.cur.execute("""INSERT OR REPLACE INTO cookies(env_user, created, cookies, url) 
           VALUES('{}', '{}', '{}', '{}');""".format(env_user, stamp, cookies, url))
        self.conn.commit()
