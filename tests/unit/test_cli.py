from cli.parser import cli
from hrm.plugins.inject_code import Command

from argparse import ArgumentParser, _SubParsersAction
from typing import List
import unittest
from unittest.mock import patch


@patch("cli.parser.getcwd", return_value="./")
class test_cli(unittest.TestCase):
    def test_default_path(self, m_getcwd):
        arguments = ["inject-code"]

        gold_rest = {
            "path": "./",
            "verbose": False,
        }
        gold_callback = Command

        output = cli(arguments).__dict__
        callback = output["callback"]
        rest = {
            k: v
            for k, v in output.items()
            if k != "callback"
        }

        self.assertEqual(
            gold_callback.__name__, callback.__name__
        )
        self.assertEqual(gold_rest, rest)


def get_subparsers(
    parser: ArgumentParser,
) -> List[_SubParsersAction]:
    # sp.choices['inject-code'].description
    return [
        p
        for p in parser._subparsers._actions
        if isinstance(p, _SubParsersAction)
    ]


if __name__ == "__main__":
    unittest.main()
