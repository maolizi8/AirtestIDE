# -*- encoding=utf8 -*-
__author__ = "{{author}}"

from airtest.core.api import *
from airtest.cli.parser import cli_setup

if not cli_setup():
    auto_setup(__file__, logdir={{logdir}}, devices=[{% for dev in devices %}
            "{{ dev }}",{% endfor %}
    ]{% if project_root %}, project_root="{{project_root}}"{% endif %})


# script content
print("start...")


# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath={{logdir}})