from hrm import plugins
from hrm.engine import main

from argparse import ArgumentParser, Namespace
from os import getcwd
from typing import List


def cli(arguments: List[str]) -> Namespace:
    parser = ArgumentParser(prog='PROG')
    add_subparsers(parser)
    return parser.parse_args(arguments)


def get_plugin_locs() -> List[str]:
    return [
        p 
        for p in dir(plugins) 
        if not p.startswith("_")
    ]


def add_subparsers(parser: ArgumentParser) -> None:
    plugin_names = get_plugin_locs()
    subparsers = parser.add_subparsers(
        help="sub-command help",
    )

    for plugin_name in plugin_names:
        cli_name = plugin_name.replace("_", "-")
        cmd = getattr(plugins, plugin_name).Command
        attrs = dict(cmd.__dict__)
        args = attrs.get("__annotations__", {})
        help = attrs.get("__help__")
        
        sp = subparsers.add_parser(cli_name, help=help)
        sp.set_defaults(callback=cmd)

        sp.add_argument(
            "path", 
            nargs="?", 
            default=getcwd(),
            help="Path to directory at which to begin"
        )  # default arg all commands take

        for arg, typ in args.items():
            a_name = f"--{arg}"
            a_type = arg_type(typ)
            req = arg_required(typ)
            sp.add_argument(a_name, type=a_type, required=req)


def arg_type(arg_type) -> type:
    if isinstance(arg_type, type):
        return arg_type
    
    arg = arg_type.__dict__.get("__args__")
    return arg[0]


def arg_required(arg_type) -> bool:
    if isinstance(arg_type, type):
        return True
    
    arg = arg_type.__dict__.get("__args__")
    if type(None) in arg:
        return False
    
    return True


if __name__ == "__main__":
    parser = ArgumentParser(prog='PROG')
    add_subparsers(parser)
    # print(parser.parse_args(["-h"]))
    print(parser.parse_args(["inject-code"]))
