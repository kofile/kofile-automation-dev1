from os.path import abspath, dirname, join
from os import chdir, getcwd
from sys import argv
from golem import main


def run_test(test_file=None, env="qa_48999_loc_2", browser="chrome"):
    test_file = getcwd() if not test_file else test_file
    # old
    # dir_, test = abspath(test_file).split('projects\\Kofile\\tests\\')
    dir_, test = abspath(test_file).split(join('projects', 'Kofile', 'tests', ""))
    chdir(dirname(abspath(__file__)))
    args = ["run", "Kofile", test, "-e", env, "-b", browser]
    for i in args:
        argv.append(i)
    main.execute_from_command_line(dir_)
