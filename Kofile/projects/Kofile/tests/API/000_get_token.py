from projects.Kofile.Lib.test_parent import ApiTestParent
from runner import run_test

description = """
check and update token before all tests
"""

tags = ['API', "SYSTEM"]


class test(ApiTestParent):                                                                                # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        pass


if __name__ == '__main__':
    run_test(__file__, browser="none")
