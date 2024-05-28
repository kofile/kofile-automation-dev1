from os import getlogin
from psutil import process_iter, AccessDenied
import time

scanner_process_name = "Kofile.Vanguard.ScanService.exe"


def wait_until(some_predicate, timeout, period=0.25, *args, **kwargs):
    must_end = time.time() + timeout
    while time.time() < must_end:
        if some_predicate(*args, **kwargs):
            return True
        time.sleep(period)
    return False


def kill_scanner(process):
    process.terminate()
    process.wait()


def get_scanner_process():
    for process in process_iter():
        if process.name() == scanner_process_name:
            try:
                username = process.username()
            except AccessDenied:
                continue
            if getlogin() in username:
                return process
