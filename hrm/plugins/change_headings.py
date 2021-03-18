from hrm.plugins._base import HotRodMarkdown

from typing import Generator, Union


class Command(HotRodMarkdown):
    """
    Takes `change` as a required input, which represents
    the change in the number of heading '#' you wish to
    apply to each heading. For example:

    hrm change-headings --change 1

    would add one '#' to each heading
    """

    __help__ = "Adds/removes heading level(s)"

    change: int

    def transform(
        self,
        md_contents: Generator[str, None, None],
        **kwargs,
    ) -> Union[str, Generator[str, None, None]]:
        change = kwargs["change"]

        for line in md_contents:
            if not line.startswith("#"):
                yield line

            else:
                current_level = line.count("#")
                new_level = current_level + change
                level = "#" * new_level
                stripped_line = line.replace("#", "")
                new_line = f"{level}{stripped_line}"

                yield new_line
