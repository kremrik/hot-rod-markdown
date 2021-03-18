from collections import namedtuple
from typing import List, Optional
from os import listdir
from os.path import basename, dirname, join, splitext
import importlib.util


__all__ = ["load_plugins"]


command = namedtuple("command", ["module_name", "obj"])


def load_plugins(
    external_path: Optional[str],
) -> List[command]:
    builtin_path = "hrm/plugins"
    paths = [builtin_path]
    if external_path:
        paths.append(external_path)

    plugins = []
    for path in paths:
        _plugins = _load_plugins(path)
        plugins.extend(_plugins)

    return plugins


def _load_plugins(path: str) -> List[command]:
    plugin_locs = _plugin_locs(path)

    plugins = []
    for plugin_path in plugin_locs:
        plugin_name = _mod_name_from_path(plugin_path)
        cmd = _load_module(
            plugin_name, plugin_path
        ).Command
        plugins.append(command(plugin_name, cmd))

    return plugins


def _plugin_locs(path: str) -> List[str]:
    plugins_dir = join(dirname(dirname(__file__)), path)
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
