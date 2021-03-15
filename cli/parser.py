from argparse import ArgumentParser, Namespace
from os import getcwd, listdir
from typing import List
from os.path import basename, dirname, join, splitext
import importlib.util


__all__ = ["cli"]


def cli(arguments: List[str]) -> Namespace:
    parser = ArgumentParser(prog='PROG')
    add_plugin_parsers(parser)
    return parser.parse_args(arguments)


def add_plugin_parsers(parser: ArgumentParser) -> None:
    plugin_locs = _plugin_locs()
    subparsers = parser.add_subparsers(
        help="sub-command help",
    )

    for plugin_path in plugin_locs:
        plugin_name = _mod_name_from_path(plugin_path)
        cli_name = _friendly_plugin_name(plugin_name)
        cmd = _load_module(plugin_name, plugin_path).Command

        args = _plugin_args(cmd)
        help = _plugin_help(cmd)
        
        sp = subparsers.add_parser(cli_name, help=help)
        sp.set_defaults(callback=cmd)

        # default arg all _base commands take
        sp.add_argument(
            "path", 
            nargs="?", 
            default=getcwd(),
            help="Path to directory at which to begin"
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


def _plugin_locs() -> List[str]:
    plugins_dir = join(dirname(dirname(__file__)), "hrm/plugins")
    plugins = [
        join(plugins_dir, p)
        for p in listdir(plugins_dir)
        if not p.startswith("_") and p.endswith(".py")
    ]
    return plugins


def _load_module(module_name: str, module_path: str):
    spec = importlib.util.spec_from_file_location(
        module_name, module_path
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    return mod


def _mod_name_from_path(module_path: str) -> str:
    return splitext(basename(module_path))[0]


def _friendly_plugin_name(module_name: str) -> str:
    return module_name.replace("_", "-")


def _plugin_args(obj) -> dict:
    attrs = dict(obj.__dict__)
    return attrs.get("__annotations__", {})


def _plugin_help(obj) -> str:
    attrs = dict(obj.__dict__)
    return attrs.get("__help__", "")


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
