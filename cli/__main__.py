from hrm import inject_code_into_md
from cli.parser import cli

from sys import argv


def main():
    command_line_args = argv[1:]
    args = cli(command_line_args)
    inject_code_into_md(args.directory)


if __name__ == "__main__":
    main()
