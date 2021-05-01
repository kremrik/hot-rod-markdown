from cli.loader import load_plugins, command

from argparse import (
    ArgumentParser,
    Namespace,
    RawDescriptionHelpFormatter,
    _SubParsersAction,
)
from textwrap import dedent
from typing import List, Optional
from os import getcwd, getenv
from os.path import abspath


__all__ = ["cli"]


PARSER_NAME = "hrm"
PLUGIN_ENV = "HRM_PLUGINS"


def cli(arguments: List[str]) -> Namespace:
    plugins = load_plugins(_get_external_path())
    parser = make_parser(prog=PARSER_NAME, plugins=plugins)
    return parser.parse_args(arguments)


def make_parser(
    prog: str, plugins: List[command]
) -> ArgumentParser:
    parser = ArgumentParser(prog=prog)

    subparsers = parser.add_subparsers()

    for name, cmd in plugins:
        add_subparser(
            subparsers=subparsers,
            plugin_name=name,
            plugin=cmd,
        )

    return parser


def add_subparser(
    subparsers: _SubParsersAction, plugin_name: str, plugin
) -> None:
    args = _plugin_args(plugin)
    help = _plugin_help(plugin)
    docs = _plugin_desc(plugin)
    cli_name = _friendly_plugin_name(plugin_name)

    sp = subparsers.add_parser(
        cli_name,
        help=help,
        formatter_class=RawDescriptionHelpFormatter,
        description=docs,
    )

    sp.set_defaults(callback=plugin)

    sp.add_argument(
        "path",
        nargs="?",
        default=getcwd(),
        help="Path to directory at which to begin",
    )

    sp.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
    )

    for arg, typ in args.items():
        a_name = _arg_name(arg)
        a_type = _arg_type(typ)
        req = _arg_required(typ)
        sp.add_argument(a_name, type=a_type, required=req)


def _friendly_plugin_name(module_name: str) -> str:
    return module_name.replace("_", "-")


def _plugin_args(obj) -> dict:
    attrs = dict(obj.__dict__)
    return attrs.get("__annotations__", {})


def _plugin_help(obj) -> str:
    attrs = dict(obj.__dict__)
    return attrs.get("__help__", "")


def _plugin_desc(obj) -> str:
    attrs = dict(obj.__dict__)
    docs = attrs.get("__doc__", "")

    if docs:
        return dedent(docs)
    else:
        return ""


def _arg_name(arg: str) -> str:
    return f"--{arg}"


def _arg_type(arg_type) -> type:
    if isinstance(arg_type, type):
        return arg_type

    arg = arg_type.__dict__.get("__args__")
    return arg[0]


def _arg_required(arg_type) -> bool:
    if isinstance(arg_type, type):
        return True

    arg = arg_type.__dict__.get("__args__")
    if type(None) in arg:
        return False

    return True


def _get_external_path() -> Optional[str]:
    external_path = getenv(PLUGIN_ENV)
    if not external_path:
        return None

    return abspath(external_path)
