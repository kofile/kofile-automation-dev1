"""erProxy multiple orders"""

from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """erProxy multiple orders creation"""

tags = ['48999_location_2']


class test(TestParent):                                                                                 # noqa

    def __init__(self, data, er_proxy_count=10):
        self.er_proxy_count = er_proxy_count
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: No
        Post-conditions: Several erProxy orders are created
        """
        er_proxy_order_numbers = self.atom.ERProxy.general.create_er_proxy(self.er_proxy_count)[0]
        self.actions.step(f'The following erProxy orders are submitted to CRS - {er_proxy_order_numbers}')


if __name__ == '__main__':
    run_test(__file__)
