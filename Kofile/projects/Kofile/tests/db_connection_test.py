from golem import actions

from projects.Kofile.Lib.DB import DB
from runner import run_test

description = """"""

tags = []


def test(data):
    with DB(data) as db:
        assert db is not None, "Connection to db failed"
        actions.step("Success connect to db")


if __name__ == '__main__':
    run_test(__file__)
