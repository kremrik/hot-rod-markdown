from hrm.io.fs import read_file
from hrm.plugins._base import HotRodMarkdown

from collections import namedtuple
from typing import (
    Generator,
    Iterable,
    List,
    Optional,
    Tuple,
)
from warnings import warn
from os.path import exists


__all__ = ["Command"]


codeblock = namedtuple(
    "codeblock",
    ["range", "language", "refers_to"],
)


class Command(HotRodMarkdown):
    """
    Code from files can be inserted into md codeblocks by
    annotating them like the below example:

    ```python file.py
    ```       ^^^^^^^

    The underlined portion reflects a relative reference to
    the file whose contents you wish to inject, which will
    then appear between the backticks. The language is not
    required to be specified.
    """

    __help__ = (
        "Injects code from files into annotated codeblocks"
    )

    def transform(
        self, md_contents: Iterable[str]
    ) -> Optional[str]:
        codeblocks = self.get_codeblocks(md_contents)
        output = self.inject_codeblocks(
            blocks=codeblocks, markdown=md_contents
        )
        return output

    @staticmethod
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
                (
                    language,
                    refers_to,
                ) = Command._describe_codeblock(line)

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

    @staticmethod
    def _describe_codeblock(
        opening_line: str,
    ) -> Tuple[Optional[str], Optional[str]]:
        remove_ticks = opening_line.strip().replace(
            "```", ""
        )
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

    @staticmethod
    def inject_codeblocks(
        blocks: Iterable[codeblock],
        markdown: Iterable[str],
    ) -> str:
        markdown = list(markdown)
        blocks = [
            b for b in blocks if Command._file_exists(b)
        ]
        blocks = sorted(blocks, key=lambda x: x.range[0])

        chunks = Command._partition_md(
            blocks=blocks, markdown=markdown
        )

        code = [Command._resolve_refer(c) for c in blocks]

        # TODO: this should just return "" to avoid writing
        if not code:
            return "".join(markdown)

        md_output = Command._interlock(chunks, code)

        return "".join(md_output)

    @staticmethod
    def _partition_md(
        blocks: Iterable[codeblock],
        markdown: Iterable[str],
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

    @staticmethod
    def _interlock(l1: list, l2: list) -> list:
        length = len(l1) + len(l2)
        array = [None] * length
        array[0::2] = l1
        array[1::2] = l2
        return array

    @staticmethod
    def _file_exists(block: codeblock) -> bool:
        path = block.refers_to
        if exists(path):
            return True
        else:
            msg = f"File '{path}' not found"
            warn(msg)
            return False

    @staticmethod
    def _resolve_refer(block: codeblock) -> str:
        path = block.refers_to
        if not path:
            return ""

        code = read_file(path)
        str_code = "".join(code)
        return str_code
