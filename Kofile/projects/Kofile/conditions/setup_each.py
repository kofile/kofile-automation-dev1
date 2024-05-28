from golem import execution
from projects.Kofile.conditions import utils
import xml.etree.ElementTree as et
from os.path import join
from subprocess import Popen


def run_scanner():
    need_reload, tree, second_tree, file_tree, changed = False, None, None, None, False
    scanner_path = join(execution.project_path, "testdata", "scanner")
    new_scanner_id = execution.data["env"].get("scanned_id")
    if new_scanner_id:
        tree = et.parse(join(scanner_path, "ScannerConfig.xml"))
        root = tree.getroot()
        for child in root.iter("ScannerId"):
            if child.text != str(new_scanner_id):
                child.text = str(new_scanner_id)
                changed = True
        if changed:
            changed = False
            need_reload = True
        else:
            tree = None

    domain = execution.data["env"].get("domain")
    code = execution.data["env"].get("code")
    if domain and code:
        second_tree = et.parse(join(scanner_path, "ScannerServiceConfig.xml"))
        second_root = second_tree.getroot()
        for child in second_root.iter("BaseAddress"):
            new_text = f"http://{domain}/{code}/capturemodule/api"
            if child.text != new_text:
                child.text = new_text
                changed = True
        if changed:
            changed = False
            need_reload = True
        else:
            second_tree = None

    new_scanner_file = execution.data.get("scanner_file", "testScanner.tiff")
    if new_scanner_file:
        file_tree = et.parse(join(scanner_path, "PredefinedImages", "PredefinedImagesConfig.xml"))
        file_root = file_tree.getroot()
        for child in file_root.iter("string"):
            if child.text != str(new_scanner_file):
                child.text = str(new_scanner_file)
                changed = True
        if changed:
            need_reload = True
        else:
            file_tree = None

    scanner_process = utils.get_scanner_process()

    if need_reload:
        if tree:
            tree.write(join(scanner_path, "ScannerConfig.xml"))
        if second_tree:
            second_tree.write(join(scanner_path, "ScannerServiceConfig.xml"))
        if file_tree:
            file_tree.write(join(scanner_path, "PredefinedImages", "PredefinedImagesConfig.xml"))
        if scanner_process:
            utils.kill_scanner(scanner_process)
            scanner_process = not utils.wait_until(lambda: utils.get_scanner_process() is None, 10, period=1)

    if not scanner_process:
        Popen(utils.scanner_process_name, cwd=scanner_path, shell=True)
        utils.wait_until(utils.get_scanner_process, 20, 1)
