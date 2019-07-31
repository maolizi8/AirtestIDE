#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is a sample launcher file."""

from airtest.cli.runner import run_script
from airtest.cli.parser import runner_parser
from airtest.core.settings import Settings as ST

if not globals().get("AirtestCase"):
    from airtest.cli.runner import AirtestCase


class CustomCase(AirtestCase):
    """Custom launcher."""

    def __init__(self):
        super(CustomCase, self).__init__()

    def setUp(self):
        """Custom setup logic here."""
        print("custom setup")
        # # add var/function/class/.. to globals:
        # self.scope["add"] = lambda x: x+1

        # # exec setup test script:
        # self.exec_other_script("setup.air")

        # # set custom parameter in Settings:
        # ST.THRESHOLD = 0.75

        super(CustomCase, self).setUp()

    def tearDown(self):
        """Custom tear down logic here."""
        print("custom tearDown")
        # # exec teardown script:
        # self.exec_other_script("teardown.air")

        super(CustomCase, self).tearDown()


if __name__ == '__main__':
    ap = runner_parser()
    args = ap.parse_args()
    run_script(args, CustomCase)
