#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate template script code."""

import sys
import io
import six
import traceback
from jinja2 import Template
import time

from app.plugins.editor.template.poco_template import POCO_TEMPLATE
from app.utils import custom_decode
from app.params import SCRIPTTPL, PYCLITPL


def get_author():
    print('    get_author>>>>>')
    try:
        import getpass
        author = getpass.getuser()
        if six.PY2:
            author = author.decode(sys.getfilesystemencoding())
    except:
        traceback.print_exc()
        author = ""
    return author


def getTemplateCode(tplconf={}, author=""):
    """渲染项目模板代码."""
    print('    getTemplateCode>>>>>')
    with io.open(SCRIPTTPL, "r", encoding="utf-8") as f:
        template_code = f.read()
    tpl = Template(template_code)
    # 获取用户名作为默认的author
    if not author:
        author = get_author()
    today = time.strftime('%Y-%m-%d')
    template_script = tpl.render(cfg=tplconf, author=author, date=today)
    return template_script


def getPycliTemplateCode(author="", devices=[], logdir=True, project_root=None):
    print('    getPycliTemplateCode>>>>>')
    with io.open(PYCLITPL, "r", encoding="utf-8") as f:
        template_code = f.read()
    tpl = Template(template_code)
    # 获取用户名作为默认的author
    if not author:
        author = get_author()
    today = time.strftime('%Y-%m-%d')
    template_script = tpl.render(author=author, devices=devices, logdir=logdir, project_root=project_root, date=today)
    return template_script


def getModeTemplate(mode_name="cocos"):
    """
    根据poco的类型获取对应的初始化代码内容，填入编辑器.
    Args:
        poco_mode:

    Returns:

    """
    print('    getModeTemplate>>>>>')
    mode_name = mode_name.lower()
    template = POCO_TEMPLATE.get(mode_name, {})
    return template


























