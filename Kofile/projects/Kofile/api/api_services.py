import requests
from requests_ntlm import HttpNtlmAuth
from urllib.parse import urlencode
from projects.Kofile.Lib.DB import InternalDB
from re import search
import logging
import time
from golem import actions, execution


class ApiService:

    def __init__(self, data, crs=True, user_index=0, use_db=True):
        self.crs = crs
        self.user_index = user_index
        self.env_data = data
        self.env_code = data.env.code
        self.test_config = self.env_data.get("test_config", {})
        if not hasattr(execution, "open_site_try"):
            execution.open_site_try = 0
        error = None
        for retry in range(5):
            self.session = requests.session()
            self.cookie = ""
            self.domain = ""
            self.return_url = ""
            try:
                self.get_cookie(use_db=use_db)
                error = None
                break
            except AssertionError as e:
                error = e
                if execution.open_site_try > 30:
                    raise e
                execution.open_site_try += 1
                logging.warning(f"Server error, wait 1 min, retry: {retry + 1}, error count: {execution.open_site_try}")
                time.sleep(60)
        if error:
            raise error

    def request_(self, request_type, url, data=None, json_=None, expected_code=200, form_data=None, try_count=5):
        params = {"url": url, "verify": False}
        # TODO need refactor this
        params.update({"data": form_data if form_data else data, "json": json_})
        content_type = "application/x-www-form-urlencoded" if form_data else "application/json"
        params.update({"headers": {"Content-Type": content_type, "cookie": self.cookie}})
        request_type = str(request_type).upper()
        log_data = f" with data:\n\t{json_}{data}{form_data}" if (json_ or data or form_data) else ""
        logging.info(f"\n*{request_type}*  --->  *{url}*{log_data}")
        return self._send_request(expected_code, try_count, request_type, **params)

    def _send_request(self, expected_code, try_count, request_type, **params):
        try:
            r = requests.request(request_type, **params)
            self.assert_response(r, expected_code)
            return r
        except AssertionError as e:
            if not try_count:
                raise e
            actions.wait(3)
            return self._send_request(expected_code, try_count=try_count - 1, request_type=request_type, **params)

    def get_cookie(self, use_db=True):
        actions.step(f"API -> Auth to {'CRS' if self.crs else 'ClerkSearch'} '{self.env_data.env.name}' "
                     f"with '{self.env_data.env.user[self.user_index]}'")
        auth_url = self.env_data.env.url if self.crs else self.env_data.env.search_url.format(mode="clerksearch",
                                                                                              is_clerk=True)
        url = auth_url.replace('%s:%s@', '').replace('%s', f'{self.env_code}').replace('&amp;Referrer=', '')
        cookie, r_url = "", ""
        loaded = False
        if use_db:
            with InternalDB(self.env_data) as internal_db:
                cookie, r_url = internal_db.get_cookies_for_user(user_index=self.user_index, crs=self.crs)
        if not cookie:
            logging.info(f"API -> Get new token from '{url}'")
            self.session.auth = HttpNtlmAuth(self.env_data.env.user[self.user_index],
                                             self.env_data.env.password[self.user_index])
            r = self.session.get(url, allow_redirects=False, timeout=30)
            self.assert_response(r, 200)
            content = r.text
            token = search(r"(?<='saml' value=').*?(</Assertion>)", content).group(0)
            agent = search(r"(?<='agentname' value=').*?(?='><input)", content).group(0)
            payload = {"saml": token, "agentname": agent, "targetUrl": ""}
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            logging.info(f"API -> Get cookies for '{agent}'")
            r2 = self.session.post(url.split('ReturnUrl=')[1].split("&")[0], data=urlencode(payload), headers=headers,
                                   verify=False)
            self.assert_response(r2, 200)
            cookie = r2.request.headers['Cookie']
            r_url = r2.url
        else:
            loaded = True
        self.cookie = cookie
        self.return_url = r_url
        self.domain = f"{self.return_url.split(str(self.env_code))[0]}{self.env_code}/api"

        if use_db and not loaded:
            with InternalDB(self.env_data) as internal_db:
                internal_db.save_cookies_for_user(cookies=cookie, url=r_url, user_index=self.user_index, crs=self.crs)
        return self.cookie

    @staticmethod
    def assert_response(response, expected_code=200):
        """
        response: response from request in json format
        expected_code: expected status_code in response
        return: return errors in response
        """
        if not expected_code:
            return
        logging.info("--- Check status code ---")
        code = response.status_code
        assert code == expected_code, f"Actual status_code: '{code}' not equal to expected: '{expected_code}'\n " \
                                      f"Response: {response}\n{response.text}"
        logging.info(f"--- {code} OK ---")
