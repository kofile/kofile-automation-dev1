"""initialize drawer test"""
import json
import os
import re
from golem.test_runner import execution_logger
import logging
from runner import run_test

description = """Add rerun tag to failed tests"""


def fix_path(path, char="\\"):
    return path.replace(char, '/')


def test(data):
    #  find test path
    log_path = execution_logger.file_handler_info.__dict__['baseFilename']
    # find report folder path
    report_dir = os.path.join(fix_path(log_path.split('single_tests')[0]), 'test')
    # get nightly report folder-sort folders by date and select second-to-last one
    report_folder = (sorted(os.listdir(report_dir)))[-1]
    # get json file from report folder
    json_file = os.path.join(report_dir, report_folder, 'report.json')
    # get failed tests names
    failed_tests = []
    with open(json_file) as f:
        data = json.load(f)
    json_data = data.get("tests")
    for i in json_data:
        status = i.get("result")
        if status != 'success':
            test_name = i.get("full_name")
            failed_tests.append(test_name)

    # create rerun.txt file and add failed test paths to this file
    test_folder = os.path.join(log_path.split('report')[0], "tests")
    rerun_txt_file_path = os.path.join(test_folder, "rerun.txt")
    if os.path.exists(rerun_txt_file_path):
        os.remove(rerun_txt_file_path)
    for test_name in failed_tests:
        test_file = f"{test_folder}/{fix_path(test_name, '.')}.py"
        with open(rerun_txt_file_path, "a+") as f:
            f.write(test_file + '\n')

        # replace regression tag  to rerun tag
        with open(test_file, 'rt') as f:
            old_test_data = f.read()
            test_cont = re.sub(r"tags[ ]?=[ ]?\[(.*?)]", r"tags = ['rerun']", old_test_data)

        if test_cont:
            with open(test_file, 'wt') as f:
                try:
                    f.write(test_cont)
                except Exception as e:
                    logging.error(f"{description}\n{e}")
                    f.write(old_test_data)


if __name__ == '__main__':
    run_test(__file__)
