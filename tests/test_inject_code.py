from minject.inject_code import (
    markdown_finder,
    get_codeblocks,
    codeblock,
    dirstruct,
    inject_codeblocks
)
import unittest
from unittest.mock import patch
from textwrap import dedent


@patch("minject.inject_code.read_file")
class test_inject_codeblock(unittest.TestCase):
    def test(self, m_read_file):
        m_read_file.return_value = [
            "foo=1\n", 
            "print(foo)\n"
        ]

        blocks = [
            codeblock(
                range=(2, 3),
                language="python",
                refers_to="example.py",
            ),
            codeblock(
                range=(6, 6),
                language="json",
                refers_to=None,
            ),
        ]

        markdown = [
            "# header\n",
            "```python example.py\n",
            "foo=1\n",
            "```\n",
            "## subheader\n",
            "```json\n",
            "```\n",
        ]

        gold = dedent(
        """\
        # header
        ```python example.py
        foo=1
        print(foo)
        ```
        ## subheader
        ```json
        ```
        """)

        output = inject_codeblocks(
            blocks=blocks, markdown=markdown
        )

        self.assertEqual(gold, output)


def mock_walk():
    paths = [
        dirstruct(
            "/path",
            ["subpath1", "subpath2"],
            [".gitignore"],
        ),
        dirstruct("/path/subpath1", [], ["README.md"]),
        dirstruct("/path/subpath2", [], ["test.py"]),
    ]
    for path in paths:
        yield path


class test_markdown_finder(unittest.TestCase):
    @patch("minject.inject_code._walk_dir")
    def test_null(self, m_walk_dir):
        m_walk_dir.return_value = []
        gold = []
        output = [m for m in markdown_finder()]
        self.assertEqual(gold, output)

    @patch("minject.inject_code._walk_dir")
    def test_one_dir_with_md(self, m_walk_dir):
        m_walk_dir.return_value = mock_walk()
        gold = [
            ("/path/subpath1", [], ["README.md"]),
        ]
        output = [m for m in markdown_finder()]
        self.assertEqual(gold, output)


class test_get_codeblocks(unittest.TestCase):
    def test_no_codeblocks(self):
        md = [
            "# header\n",
            "##subheader"
        ]
        gold = []
        output = list(get_codeblocks(md))
        self.assertEqual(gold, output)

    def test_one_codeblock_no_language_no_refer(self):
        md = [
            "# header\n",
            "```\n",
            "foo=1\n",
            "```\n",
            "## subheader\n",
        ]
        gold = [((2, 3), None, None)]
        output = list(get_codeblocks(md))
        self.assertEqual(gold, output)

    def test_one_codeblock_no_refer(self):
        md = [
            "# header\n",
            "```python\n",
            "foo=1\n",
            "```\n",
            "## subheader\n",
        ]
        gold = [((2, 3), "python", None)]
        output = list(get_codeblocks(md))
        self.assertEqual(gold, output)

    def test_one_codeblock(self):
        md = [
            "# header\n",
            "```python example.py\n",
            "foo=1\n",
            "```\n",
            "## subheader\n",
        ]
        gold = [((2, 3), "python", "example.py")]
        output = list(get_codeblocks(md))
        self.assertEqual(gold, output)

    def test_mult_codeblock(self):
        md = [
            "# header\n",
            "```python example.py\n",
            "foo=1\n",
            "```\n",
            "## subheader\n",
            "```json\n",
            "```"
        ]
        gold = [
            ((2, 3), "python", "example.py"),
            ((6, 6), "json", None),
        ]
        output = list(get_codeblocks(md))
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
