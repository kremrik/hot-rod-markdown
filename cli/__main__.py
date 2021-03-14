from minject import inject_code_into_md
from cli.parser import cli

from sys import argv


if __name__ == "__main__":
    command_line_args = argv[1:]
    args = cli(command_line_args)
    inject_code_into_md(args.directory)
