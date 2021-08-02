from hrm.engine import main
from cli.parser import cli

from sys import argv


def execute():
    """
    the `callback` argument of `args` is an uninstantiated
    concrete class of HotRodMarkdown. An object needs to be
    instantiated once per Markdown file, and since there
    may be many of these the job of instantiating said
    object is delayed until the last minute. This enables a
    much more contained "job", seeing as each instance of
    HRM is completely self-sufficient and is content to run
    as a daemon thread or separate process.
    """
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
