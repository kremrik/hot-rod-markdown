from hrm.io.fs import read_file
from hrm.plugins._base import HotRodMarkdown

import re
from collections import namedtuple
from typing import (
    Generator,
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

    ```python INJECT_CODE(file.py)
    ```       ^^^^^^^^^^^^^^^^^^^^

    The underlined portion reflects a relative reference to
    the file whose contents you wish to inject, which will
    then appear between the backticks. The language is not
    required to be specified.
    """

    __help__ = "Injects files into annotated codeblocks"

    def transform(
        self,
        md_contents: Generator[str, None, None],
        **kwargs,
    ) -> str:
        md = list(md_contents)
        codeblocks = self.get_codeblocks(md)
        output = self.inject_codeblocks(
            blocks=codeblocks, markdown=md
        )
        return output

    @staticmethod
    def get_codeblocks(
        markdown_text: List[str],
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
        regex = re.compile(r"INJECT_CODE\((.*?)\)")
        path = regex.findall(opening_line)

        if path:
            return (None, path[0])
        else:
            return (None, None)

    @staticmethod
    def inject_codeblocks(
        blocks: Generator[codeblock, None, None],
        markdown: List[str],
    ) -> str:
        existing_blocks = [
            b for b in blocks if Command._file_exists(b)
        ]
        sorted_blocks = sorted(
            existing_blocks, key=lambda x: x.range[0]
        )

        chunks = Command._partition_md(
            blocks=sorted_blocks, markdown=markdown
        )

        code = [
            Command._resolve_refer(c)
            for c in sorted_blocks
        ]

        if not code:
            return ""

        md_output = Command._interlock(chunks, code)

        return "".join(md_output)

    @staticmethod
    def _partition_md(
        blocks: List[codeblock],
        markdown: List[str],
    ) -> List[str]:
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
