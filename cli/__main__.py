from hrm.engine import main
from cli.parser import cli

from sys import argv


def execute():
    command_line_args = argv[1:]
    args = cli(command_line_args)

    callback = args.callback
    kwargs = {
        k: v
        for k, v in args.__dict__.items()
        if k != "callback"
    }

    main(callback, **kwargs)


if __name__ == "__main__":
    execute()
