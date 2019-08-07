# -*- encoding=utf8 -*-
"""
Created on {{date}}

@author: {{author}}
"""
from airtest.core.api import *
# import your elements, eg.
# from set_element.home import *

# your functions ...
def func():
    """
    descriptions
    """
    pass




if __name__ == '__main__':
    auto_setup(__file__, devices=[{% for dev in devices %}
            "{{ dev }}",{% endfor %}
    ], logdir={{logdir}}{% if project_root %}, project_root="{{project_root}}"{% endif %})
    
    # debug codes ...
    # func()
    
    # generate html report, put this in the bottom
    # from airtest.report.report import simple_report
    # simple_report(__file__, logpath={{logdir}})