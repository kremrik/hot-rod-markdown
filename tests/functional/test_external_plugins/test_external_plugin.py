from tests.functional.utils import file_contents

import unittest
from os import chdir, environ
from os.path import dirname
from shutil import copyfile
from subprocess import Popen
from time import sleep


class test_change_headings_decrease(unittest.TestCase):
    def setUp(self) -> None:
        chdir(dirname(__file__))
        environ["HRM_PLUGINS"] = "plugins"

        copyfile("README.bak", "README.md")
        copyfile("sub_dir/README.bak", "sub_dir/README.md")

    def tearDown(self) -> None:
        copyfile("README.bak", "README.md")
        copyfile("sub_dir/README.bak", "sub_dir/README.md")

    def test(self):
        cmd = "hrm test-plugin --change 1 -v".split()
        Popen(cmd)

        sleep(0.15)

        md1_output = file_contents("README.md")
        md2_output = file_contents("sub_dir/README.md")

        md1_gold = file_contents("README.gold")
        md2_gold = file_contents("sub_dir/README.gold")

        self.assertEqual(md1_output, md1_gold)
        self.assertEqual(md2_output, md2_gold)
