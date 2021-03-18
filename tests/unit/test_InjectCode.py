from hrm.plugins.inject_code import Command
import unittest
from unittest.mock import patch
from textwrap import dedent


@patch("hrm.plugins.inject_code.Command._resolve_refer")
@patch("hrm.plugins.inject_code.exists")
class test_transform(unittest.TestCase):
    def test_one_refer_block_one_without(
        self, m_exists, m_read_file
    ):
        m_exists.return_value = True
        m_read_file.return_value = "foo=1\nprint(foo)\n"

        markdown = [
            "# header\n",
            "```python INJECT_CODE(example.py)\n",
            "foo=1\n",
            "```\n",
            "## subheader\n",
            "```json\n",
            '{"foo": 1}\n',
            "```\n",
        ]
        markdown = (line for line in markdown)

        gold = dedent(
            """\
        # header
        ```python INJECT_CODE(example.py)
        foo=1
        print(foo)
        ```
        ## subheader
        ```json
        {"foo": 1}
        ```
        """
        )

        ic = Command(path=".", verbose=False)
        output = ic.transform(markdown)
        self.assertEqual(gold, output)

    def test_refer_block_has_wrong_path(
        self, m_exists, m_read_file
    ):
        m_exists.return_value = False

        markdown = [
            "# header\n",
            "```python INJECT_CODE(example.py)\n",
            "foo=1\n",
            "```\n",
            "## subheader\n",
            "```json\n",
            '{"foo": 1}\n',
            "```\n",
        ]

        gold = ""

        ic = Command(path=".", verbose=False)
        with self.assertWarns(UserWarning):
            output = ic.transform(markdown)
            self.assertEqual(gold, output)

        self.assertEqual(gold, output)


# testing "APIs" for main implementation abstractions
# ---------------------------------------------------------
class test_get_codeblocks(unittest.TestCase):
    def test_no_codeblocks(self):
        md = ["# header\n", "##subheader"]
        gold = []
        output = list(Command.get_codeblocks(md))
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
        output = list(Command.get_codeblocks(md))
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
        output = list(Command.get_codeblocks(md))
        self.assertEqual(gold, output)

    def test_one_codeblock(self):
        md = [
            "# header\n",
            "```python INJECT_CODE(example.py)\n",
            "foo=1\n",
            "```\n",
            "## subheader\n",
        ]
        gold = [((2, 3), None, "example.py")]
        output = list(Command.get_codeblocks(md))
        self.assertEqual(gold, output)

    def test_mult_codeblock(self):
        md = [
            "# header\n",
            "```python INJECT_CODE(example.py)\n",
            "foo=1\n",
            "```\n",
            "## subheader\n",
            "```json\n",
            "```",
        ]
        gold = [
            ((2, 3), None, "example.py"),
        ]
        output = list(Command.get_codeblocks(md))
        self.assertEqual(gold, output)

    def test_codeblock_w_only_refer(self):
        md = [
            "# header\n",
            "```INJECT_CODE(example.py)\n",
            "foo=1\n",
            "```\n",
            "## subheader\n",
            "```json\n",
            "```",
        ]
        gold = [
            ((2, 3), None, "example.py"),
        ]
        output = list(Command.get_codeblocks(md))
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
