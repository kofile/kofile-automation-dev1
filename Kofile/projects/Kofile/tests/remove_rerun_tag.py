"""initialize drawer test"""
import logging
import os

from golem.test_runner import execution_logger

from runner import run_test

description = """Rerun failed tests"""


def fix_path(path, char="\\"):
    return path.replace(char, '/')


def test(data):
    #  find test path
    log_path = execution_logger.file_handler_info.__dict__['baseFilename']
    test_folder = os.path.join(log_path.split('report')[0], "tests")
    # in tests fro, rerun.txt file replace rerun tag to regression
    result_path = os.path.join(test_folder, "rerun.txt")
    with open(result_path, "r") as f:
        files = [i.strip() for i in f.readlines() if i.strip()]
    for test_file in files:
        with open(test_file, 'r') as f:
            old_test_data = f.read()
            test_cont = old_test_data.replace("tags = ['rerun']", "tags = ['regression']")

        if test_cont:
            with open(test_file.rstrip('\n'), 'wt') as f:
                try:
                    f.write(test_cont)
                except Exception as e:
                    logging.error(f"{description}\n{e}")
                    f.write(old_test_data)
    os.remove(result_path)


if __name__ == '__main__':
    run_test(__file__)
