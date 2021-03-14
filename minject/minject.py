from minject.io.fs import read_file, write_file

from collections import namedtuple
from typing import (
    Generator,
    Iterable,
    List,
    Optional,
    Tuple,
)
from os import chdir, walk
from os.path import abspath, curdir
from warnings import warn


__all__ = ["inject_code_into_md"]


def inject_code_into_md(
    directory: Optional[str] = None,
) -> None:
    """
    Recursively descends a directory, injecting code into
    any Markdown files from sibling code files.

    To instruct this function to inject code into a
    Markdown file, you simply create a md codeblock the
    standard way with triple backticks (```), specify the
    desired language per convention (```python), and add
    the corresponding code file name (```python file1.py).

    When parsing a Markdown file with the above hints, this
    function will search for matching sibling files and
    simply insert the contents between the opening and
    closing codeblock backticks. If the file extension does
    not match the given codeblock syntax, a warning is
    thrown and the process will continue to any remaining
    directories/files.
    """
    if not directory:
        directory = abspath(curdir)

    for loc in markdown_finder(directory):
        inject(loc)


# ---------------------------------------------------------
dirstruct = namedtuple(
    "dirstruct",
    ["root", "dirs", "files"],
)


codeblock = namedtuple(
    "codeblock",
    ["range", "language", "refers_to"],
)


# ---------------------------------------------------------
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


# ---------------------------------------------------------
def inject(loc: dirstruct) -> None:
    # TODO: break out into fnc
    chdir(loc.root)

    md_files = _get_md_files(loc.files)
    for md_file in md_files:
        md = read_file(md_file)
        codeblocks = get_codeblocks(md)

        if not codeblocks:
            return

        new_md = inject_codeblocks(
            blocks=codeblocks, markdown=md
        )
        write_file(md_file, new_md)


def _get_md_files(files: List[str]) -> List[str]:
    return [file for file in files if is_md(file)]


# ---------------------------------------------------------
def get_codeblocks(
    markdown_text: Iterable[str],
) -> Generator[codeblock, None, None]:
    range_start = None
    range_end = None
    language = None
    refers_to = None

    for pos, line in enumerate(markdown_text):
        if not line.strip().startswith("```"):
            continue

        if not range_start:
            range_start = pos + 1
            language, refers_to = _describe_codeblock(line)

        else:
            range_end = pos
            block = codeblock(
                (range_start, range_end),
                language,
                refers_to,
            )
            range_start = None
            range_end = None
            language = None
            refers_to = None

            if block.refers_to:
                yield block


def _describe_codeblock(
    opening_line: str,
) -> Tuple[Optional[str], Optional[str]]:
    remove_ticks = opening_line.strip().replace("```", "")
    chunks = remove_ticks.split()

    if len(chunks) == 2:
        # appeasing mypy
        return (chunks[0], chunks[1])

    if len(chunks) == 0:
        return (None, None)

    if "." not in chunks[0]:
        return (chunks[0], None)
    else:
        return (None, chunks[0])


# ---------------------------------------------------------
def inject_codeblocks(
    blocks: Iterable[codeblock], markdown: Iterable[str]
) -> str:
    markdown = list(markdown)
    blocks = sorted(blocks, key=lambda x: x.range[0])

    chunks = _partition_md(
        blocks=blocks, markdown=markdown
    )

    code = [_resolve_refer(c) for c in blocks]
    code = [c for c in code if c]

    if not code:
        return "".join(markdown)

    md_output = _interlock(chunks, code)

    return "".join(md_output)


def _partition_md(
    blocks: Iterable[codeblock], markdown: Iterable[str]
) -> List[str]:
    markdown = list(markdown)
    sorted(blocks, key=lambda x: x.range[0])

    chunks = []
    bgn = None
    end = None

    for block in blocks:
        b, e = block.range
        end = b
        chunk = "".join(markdown[bgn:end])
        bgn = e
        chunks.append(chunk)

    final_chunk = "".join(markdown[bgn:])
    chunks.append(final_chunk)

    return chunks


def _interlock(l1: list, l2: list) -> list:
    length = len(l1) + len(l2)
    array = [None] * length
    array[0::2] = l1
    array[1::2] = l2
    return array


def _resolve_refer(block: codeblock) -> str:
    path = block.refers_to
    if not path:
        return ""

    try:
        code = read_file(path)
        str_code = "".join(code)
        return str_code
    except FileNotFoundError:
        msg = f"File '{path}' not found"
        warn(msg)
        return ""


# ---------------------------------------------------------
def is_md(filename: str) -> bool:
    return filename.endswith(".md")
