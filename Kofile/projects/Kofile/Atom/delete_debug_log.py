import os
import glob
from golem import actions

description = """
In report folder search and delete debug log files 
"""


def test(data):
    current_dir = os.getcwd().replace('\\', '/')
    log_dir = current_dir + '/projects/Kofile/reports/test'
    debug_file = glob.glob(log_dir + "/**/*execution_debug.log", recursive=True)
    try:
        for file in debug_file:
            os.remove(file)

    except OSError:
        message = "Access-error on file"
        actions.step(message)
