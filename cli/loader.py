from hrm.io.fs import read_file

import ast
import re
from collections import namedtuple
from typing import List, Optional
from os import listdir
from os.path import dirname, join
import importlib.util


__all__ = ["load_plugins"]


PLUGIN_PATH = "hrm/plugins"
BASE_CLASS_NAME = "HotRodMarkdown"


command = namedtuple("command", ["module_name", "obj"])


def load_plugins(
    external_path: Optional[str],
) -> List[command]:
    builtin_path = PLUGIN_PATH
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
        module_ast = _path_to_ast(plugin_path)
        class_name = _plugin_class_name_from_ast(
            module_ast
        )
        plugin_name = _plugin_name_from_class(class_name)

        module = _load_module(plugin_name, plugin_path)
        cmd = getattr(module, class_name)
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
    mod = importlib.util.module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(mod)  # type: ignore
    return mod


def _path_to_ast(path: str) -> ast.Module:
    mod = "".join(read_file(path))
    return ast.parse(mod)


def _plugin_class_name_from_ast(module: ast.Module) -> str:
    classes = [
        c
        for c in module.body
        if isinstance(c, ast.ClassDef)
    ]

    hrm_classes = [
        h
        for h in classes
        if h.bases[0].id == BASE_CLASS_NAME  # type: ignore
    ]

    plugin_name = hrm_classes[0].name  # use first

    return plugin_name


def _plugin_name_from_class(classname: str) -> str:
    return re.sub(
        r"(?<!^)(?=[A-Z])", "-", classname
    ).lower()
