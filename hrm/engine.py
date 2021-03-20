import logging
from os import walk
from os.path import abspath, join, isfile
from typing import Generator, List, Optional


__all__ = ["main"]


def main(cmd, path: str, verbose: bool, **kwargs) -> None:
    level = logging.ERROR
    if verbose:
        level = logging.INFO
    logging.getLogger().setLevel(level)

    # this could easily be parallelized
    path = abspath(path)

    if isfile(path):
        job = cmd(path=path)
        job.run(**kwargs)

    else:
        for md_file in markdown_finder(path):
            job = cmd(path=md_file)
            job.run(**kwargs)


# ---------------------------------------------------------
def markdown_finder(
    directory: str,
    ignore: Optional[List[str]] = None,
) -> Generator:
    if not ignore:
        ignore = []

    for d in _walk_dir(directory=directory, ignore=ignore):
        yield d


def _walk_dir(
    directory: str, ignore: list
) -> Generator[str, None, None]:
    for root, dirs, files in walk(directory, topdown=True):
        for ign in ignore:
            if ign in dirs:
                dirs.remove(ign)

        for dir in dirs:
            if dir.startswith("."):
                dirs.remove(dir)

        for file in files:
            if is_md(file):
                yield join(root, file)


def is_md(filename: str) -> bool:
    return filename.endswith(".md")
