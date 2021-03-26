from cli.parser import make_parser
from hrm.plugins.inject_code import InjectCode

import unittest
from argparse import ArgumentParser, _SubParsersAction
from textwrap import dedent
from typing import List, Optional


class test_make_parser(unittest.TestCase):
    def test(self):
        output = make_parser(
            prog="test",
            plugins=[("inject_code", InjectCode)],
        )
        self.assertEqual(output.prog, "test")

        subparsers = get_subparsers(output)
        self.assertEqual(len(subparsers), 1)

        subparser = subparsers[0]
        desc = subparser_description(subparser)
        help = subparser_help(subparser)
        self.assertEqual(desc, dedent(InjectCode.__doc__))
        self.assertEqual(help, InjectCode.__help__)


def get_subparsers(
    parser: ArgumentParser,
) -> List[_SubParsersAction]:
    return [
        p
        for p in parser._subparsers._actions
        if isinstance(p, _SubParsersAction)
    ]


def subparser_description(
    subparser: _SubParsersAction,
) -> Optional[str]:
    sp_name = list(subparser.choices.keys())[0]
    desc = subparser.choices[sp_name].description
    return desc


def subparser_help(
    subparser: _SubParsersAction,
) -> Optional[str]:
    help = subparser.__dict__["_choices_actions"][0].help
    return help


if __name__ == "__main__":
    unittest.main()
