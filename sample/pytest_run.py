#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is a sample launcher file."""

from airtest.cli.runner import run_script
from airtest.cli.parser import runner_parser
from airtest.core.settings import Settings as ST

if __name__ == '__main__':
    ap = runner_parser()
    args = ap.parse_args()
    print('custom args: ',args)
    args.devices=[
            "Android:///",
    ]
    args=[__file__,'-m run_case','-s']
    #pytest.main(args)
