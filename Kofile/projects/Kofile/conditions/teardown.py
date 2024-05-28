from projects.Kofile.conditions import utils
from golem import execution
from projects.Kofile.Lib.DB import DB


def kill_scanner():
    scanner_process = utils.get_scanner_process()
    if scanner_process:
        utils.kill_scanner(scanner_process)
        utils.wait_until(lambda: utils.get_scanner_process() is None, 10, period=1)


def set_old_location():
    if hasattr(execution, "temp"):
        temp = getattr(execution, "temp")
        ip = temp.get("ip")
        del temp["ip"]
        for name, config in temp.items():
            ws = config.get("ws_id")
            data = config.get("data")
            old_location = config.get("location", {}).get("old")
            new_location = config.get("location", {}).get("new")
            if ws and data and old_location and new_location:
                with DB(data) as db:
                    db.update_location(ws, old_location)
