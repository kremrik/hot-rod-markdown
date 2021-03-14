from hrm.plugins.inject_code import InjectCode, codeblock
import unittest
from unittest.mock import patch
from textwrap import dedent


@patch("hrm.plugins.inject_code.read_file")
class test_inject_codeblocks(unittest.TestCase):
    def test_one_refer_block_one_without(self, m_read_file):
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
        ]

        markdown = [
            "# header\n",
            "```python example.py\n",
            "foo=1\n",
            "```\n",
            "## subheader\n",
            "```json\n",
            '{"foo": 1}\n',
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
        {"foo": 1}
        ```
        """)

        output = InjectCode.inject_codeblocks(
            blocks=blocks, markdown=markdown
        )

        self.assertEqual(gold, output)

    @patch("hrm.plugins.inject_code.exists", return_value=False)
    def test_refer_block_has_wrong_path(self, m_read_file, m_exists):
        blocks = [
            codeblock(
                range=(2, 3),
                language="python",
                refers_to="example.py",
            ),
        ]

        markdown = [
            "# header\n",
            "```python example.py\n",
            "foo=1\n",
            "```\n",
            "## subheader\n",
            "```json\n",
            '{"foo": 1}\n',
            "```\n",
        ]

        gold = dedent(
        """\
        # header
        ```python example.py
        foo=1
        ```
        ## subheader
        ```json
        {"foo": 1}
        ```
        """)

        with self.assertWarns(UserWarning):
            output = InjectCode.inject_codeblocks(
                blocks=blocks, markdown=markdown
            )

        self.assertEqual(gold, output)


class test_get_codeblocks(unittest.TestCase):
    def test_no_codeblocks(self):
        md = [
            "# header\n",
            "##subheader"
        ]
        gold = []
        output = list(InjectCode.get_codeblocks(md))
        self.assertEqual(gold, output)

    def test_one_codeblock_no_language_no_refer(self):
        md = [
            "# header\n",
            "```\n",
            "foo=1\n",
            "```\n",
            "## subheader\n",
        ]
        gold = []
        output = list(InjectCode.get_codeblocks(md))
        self.assertEqual(gold, output)

    def test_one_codeblock_no_refer(self):
        md = [
            "# header\n",
            "```python\n",
            "foo=1\n",
            "```\n",
            "## subheader\n",
        ]
        gold = []
        output = list(InjectCode.get_codeblocks(md))
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
        output = list(InjectCode.get_codeblocks(md))
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
        ]
        output = list(InjectCode.get_codeblocks(md))
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
