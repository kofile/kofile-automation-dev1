import sys
import os
from golem import main


def run():
    path = sys.argv[-1]
    file = path.split("projects\\Kofile\\tests\\")[1]     # path to your project tests
    del sys.argv[-1]
    sys.argv.append("run")
    proj = "Kofile"  # if proj == "" else proj              # Kofile is project name
    sys.argv.append(proj)
    sys.argv.append(file)
    sys.argv.append("-e")
    env = 'qa_dev'                                        # environment name
    for i in env.split(" "):
        sys.argv.append(i)
    os.chdir("..\\..\\")
    main.execute_from_command_line(".")


if __name__ == '__main__':
    run()

        