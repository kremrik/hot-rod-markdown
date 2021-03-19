from hrm.plugins.change_headings import Command
import unittest


class test_transform(unittest.TestCase):
    def test_zero(self):
        _md = [
            "# level 1\n",
            "text 1\n",
            "## level 2\n",
            "text 2",
        ]
        md = (line for line in _md)

        gold = [
            "# level 1\n",
            "text 1\n",
            "## level 2\n",
            "text 2",
        ]

        cmd = Command(".", False)
        output = list(cmd.transform(md, change=0))
        self.assertEqual(gold, output)

    def test_positive(self):
        _md = [
            "# level 1\n",
            "text 1\n",
            "## level 2\n",
            "text 2",
        ]
        md = (line for line in _md)

        gold = [
            "## level 1\n",
            "text 1\n",
            "### level 2\n",
            "text 2",
        ]

        cmd = Command(".", False)
        output = list(cmd.transform(md, change=1))
        self.assertEqual(gold, output)

    def test_negative(self):
        _md = [
            "# level 1\n",
            "text 1\n",
            "## level 2\n",
            "text 2",
        ]
        md = (line for line in _md)

        gold = [
            " level 1\n",
            "text 1\n",
            "# level 2\n",
            "text 2",
        ]

        cmd = Command(".", False)
        output = list(cmd.transform(md, change=-1))
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
