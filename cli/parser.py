from hrm import plugins

from argparse import ArgumentParser, Namespace
from typing import List


def cli(arguments: List[str]) ->Namespace:
    parser = ArgumentParser()

    parser.add_argument(
        "--directory",
        "-d",
        type=str,
        required=False,
        help="Path to directory to begin traversal",
    )

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
        cmd = getattr(plugins, plugin_name).Command
        attrs = dict(cmd.__dict__)
        args = attrs.get("__annotations__", {})
        help = attrs.get("__help__")
        
        sp = subparsers.add_parser(plugin_name, help=help)

        sp.add_argument(
            "path", 
            nargs="?", 
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
    # subparsers = parser.add_subparsers(help="help")
    # sp = subparsers.add_parser("inject_code")
    # sp.add_argument("--foo", type=str)
    # sp.add_argument(
    #     "path",
    #     nargs="?",
    #     help="Path to directory to begin traversal",
    # )
    # print(parser.parse_args(["inject_code", "--foo", "1"]))
    add_subparsers(parser)
    # print(parser.parse_args(["-h"]))
    print(parser.parse_args(["inject_code", "/path"]))
