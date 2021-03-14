from collections import namedtuple
from os import walk
from typing import Generator, List, Optional


dirstruct = namedtuple(
    "dirstruct",
    ["root", "dirs", "files"],
)


def markdown_finder(
    directory: str,
    ignore: List[str] = None,
) -> Generator:
    for d in _walk_dir(directory=directory, ignore=ignore):
        if _is_md_dir(d):
            yield d


def _walk_dir(
    directory: str, ignore: Optional[List[str]]
) -> Generator[dirstruct, None, None]:
    if not ignore:
        ignore = []

    for root, dirs, files in walk(directory, topdown=True):
        for ign in ignore:
            if ign in dirs:
                dirs.remove(ign)

        for dir in dirs:
            if dir.startswith("."):
                dirs.remove(dir)

        yield dirstruct(root, dirs, files)


def _is_md_dir(loc: dirstruct) -> bool:
    for file in loc.files:
        if is_md(file):
            return True
    return False


def is_md(filename: str) -> bool:
    return filename.endswith(".md")
