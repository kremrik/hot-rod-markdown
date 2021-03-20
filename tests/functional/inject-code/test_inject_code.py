import unittest
from os import chdir
from os.path import dirname
from shutil import copyfile
from subprocess import Popen
from time import sleep


chdir(dirname(__file__))


class test_inject_code(unittest.TestCase):
    def setUp(self) -> None:
        copyfile("README.bak", "README.md")
        copyfile("subdir/README.bak", "subdir/README.md")

    def tearDown(self) -> None:
        copyfile("README.bak", "README.md")
        copyfile("subdir/README.bak", "subdir/README.md")

    def test(self):
        cmd = "hrm inject-code -v".split()
        Popen(cmd)

        sleep(0.05)

        md1_output = file_contents("README.md")
        md2_output = file_contents("subdir/README.md")

        md1_gold = file_contents("README.gold")
        md2_gold = file_contents("subdir/README.md")

        self.assertEqual(md1_output, md1_gold)
        self.assertEqual(md2_output, md2_gold)


def file_contents(path: str) -> str:
    with open(path, "r") as f:
        data = f.read()
    return data
