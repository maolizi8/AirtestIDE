# -*- encoding=utf8 -*-
"""
Created on {{date}}

@author: {{author}}
"""
from airtest.core.api import *
from airtest.cli.parser import cli_setup

if not cli_setup():
    auto_setup(__file__, logdir={{logdir}}, devices=[{% for dev in devices %}
            "{{ dev }}",{% endfor %}
    ]{% if project_root %}, project_root="{{project_root}}"{% endif %})


# your script content
print("start...")


# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath={{logdir}})

if __name__ == '__main__':
    connect_device('Android:///') #android:/// or Android://127.0.0.1:5037/YOUR_UUID
    # YOUR CODES .....