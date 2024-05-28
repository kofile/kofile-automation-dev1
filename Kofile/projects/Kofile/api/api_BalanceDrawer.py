import json
import logging
from re import search, DOTALL

from golem import actions
from projects.Kofile.api.api_services import ApiService
from datetime import datetime


class BalanceDrawer(ApiService):

    def __init__(self, data, user_index=0):
        ApiService.__init__(self, data, user_index=user_index)

    def initialize_drawer(self, init_amount=300):
        drawer_name, drawer_id = self.get_drawer_id(True)
        url = f"{self.domain}/Balance/InitializeDrawer"
        data = [{"DrawerName": drawer_name, "DrawerId": drawer_id, "InitAmount": str(init_amount),
                 "RecordedDate": str(datetime.now().strftime("%m/%d/%Y")), "IsIndividual": False}]
        actions.step(f"-> API -> Initialize Drawer for user *{drawer_name}*")
        r = self.request_("POST", url, json_=data).json()
        return r

    def unpost_drawer_session(self, user_index_in_env_file=0):
        user = self.env_data.get("env").get("user")
        user = user[user_index_in_env_file] if isinstance(user, list) else user
        all_sessions = self.get_closed_drawer_sessions()
        sessions = [i for i in all_sessions if user.lower() in str(i["DrawerName"]).lower()] if all_sessions else []
        if not sessions:
            logging.info(f"Sessions for user '{user}' not found: {all_sessions}")
            return False
        url = f"{self.domain}/Balance/UnpostSessions"
        actions.step(f"-> API -> UNPOST drawer session for user *{user}*")
        r = self.request_("POST", url, json_=sessions)
        logging.info(r.text)
        return True

    def get_closed_drawer_sessions(self, date="today"):
        date = datetime.now().strftime('%m/%d/%Y') if date == "today" else date
        url = f"{self.domain}/Balance/GetPostedDates?postedDate={date}"
        actions.step(f"-> API -> Get closed drawer sessions for current user")
        r = self.request_("GET", url).json()
        return r

    def get_drawer_summary(self):
        url = f"{self.domain.replace('/api', '')}/Balance/ShowDrawerSessionSummary"
        r = self.request_("GET", url).text
        pattern = r"(?<='DrawerBalance':).*?(?=,*'CurrentAgentInfo')"
        current = search(pattern, r, DOTALL)
        if not current:
            r = self.request_("GET", url.replace('Session', '')).text
        current = search(pattern, r, DOTALL)
        current = current.group(0)
        current_session = str(current).replace('\\', '\\\\').rstrip()[:-1]
        res = json.loads(current_session)
        return res

    def get_drawer_id(self, return_name_and_id=False):
        drawer = self.get_drawer_summary().get("Session")[0]
        drawer_name = drawer.get("DrawerName").replace("\\\\", '\\')
        drawer_id = drawer.get("DrawerId")
        return (drawer_name, drawer_id) if return_name_and_id else drawer_id
