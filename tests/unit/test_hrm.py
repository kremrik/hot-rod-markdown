from hrm.engine import markdown_finder

import unittest
from unittest.mock import patch


def mock_walk():
    paths = [
        ("/hrm", ["io", "plugins"], ["README.md"]),
        ("/hrm/io", [], ["fs.py", "README.md"]),
        ("/hrm/plugins", [], ["__init__.py"]),
    ]
    return (path for path in paths)


@patch("hrm.engine.walk")
class test_markdown_finder(unittest.TestCase):
    def test_without_ignore(self, m_walk):
        m_walk.return_value = mock_walk()
        directory = "doesn't matter"

        gold = ["/hrm/README.md", "/hrm/io/README.md"]

        output = list(markdown_finder(directory))

        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
