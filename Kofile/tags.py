from os import walk
from os.path import join, dirname
import time
import importlib.util as util
import json

DEBUG = False


class PathManager:
    base_dir = join(dirname(__file__), "projects", "Kofile")
    tests_dir = join(base_dir, "tests")
    tags_file_dir = join(base_dir, ".tags")
    files_black_list = ("__init__.py",)

    def fix_path(self, path):
        return path.replace(self.tests_dir, "").replace("/", ".").replace("\\", ".").replace(".py", "").lstrip(".")

    def get_next_file_path(self):
        for path, folders, files in walk(self.tests_dir):
            for file_name in files:
                if file_name not in self.files_black_list and file_name.endswith(".py"):
                    yield join(path, file_name)


class TagManager(PathManager):
    new_tags = dict()

    def __init__(self):
        super(TagManager, self).__init__()
        for path in self.get_next_file_path():
            tags = self.get_tags(path)
            if tags is not None:
                self.add_tag(tags, path)

    def get_tags(self, path):
        spec = util.spec_from_file_location("tags", path)
        foo = util.module_from_spec(spec)
        try:
            spec.loader.exec_module(foo)
        except TypeError:
            if DEBUG:
                print(path)
            return
        try:
            return foo.tags
        except AttributeError:
            if DEBUG:
                print(path)
            return

    def add_tag(self, tags, path: str):
        tag_name = self.fix_path(path)
        if tag_name not in self.new_tags:
            self.new_tags[tag_name] = {"tags": tags, "timestamp": time.time()}
        else:
            if DEBUG:
                print(path)

    def write_new_tags(self):
        with open(self.tags_file_dir, "w") as f:
            f.write(json.dumps(self.new_tags, indent=4, sort_keys=True))


if __name__ == '__main__':
    main = TagManager()
    main.write_new_tags()
