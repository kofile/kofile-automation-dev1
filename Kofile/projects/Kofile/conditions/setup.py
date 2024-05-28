import requests
import re

from shutil import rmtree, copyfile
from webdriver_manager.chrome import ChromeDriverManager
from golem.core import session
from os.path import join, sep
from golem import execution
from projects.Kofile.Lib.DB import DB


def update_drivers():
    drivers_dir = f"{session.testdir}_drivers"
    rmtree(drivers_dir, ignore_errors=True)
    paths = ChromeDriverManager(path=drivers_dir).install()
    copyfile(paths, join(session.testdir, "drivers", paths.split(sep)[-1]))
    rmtree(drivers_dir)


def set_location():
    ip = requests.get("http://10.11.36.111:6329/").text
    assert re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip)
    data_set = getattr(execution, "data_set")
    _, temp = list(), dict(ip=ip)
    for data in data_set:
        if not data.get("env", {}).get("project_db"):
            continue
        if data["env"]["name"] not in _:
            execution.data = data
            try:
                with DB(data) as db:
                    ws = db.get_workstation_by_ip(ip)
                    new_location = data.get("env", {}).get("location", {}).get("id")
                    if ws and new_location:
                        location = db.get_location_by_workstation(ws)
                        if location != new_location:
                            db.update_location(ws, new_location)
                            temp[data["env"]["name"]] = {
                                "ws_id": ws, "data": data, "location": {
                                    "old": location,
                                    "new": new_location}
                            }
                _.append(data["env"]["name"])
            except Exception as e:
                print(type(e).__name__)
    setattr(execution, "temp", temp)
