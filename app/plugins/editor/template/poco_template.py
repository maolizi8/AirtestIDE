#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Poco init code."""

POCO_TEMPLATE = {
    "cocos-lua": {
        "keyword": "StdPoco",
        "content": """\rfrom poco.drivers.std import StdPoco\rpoco = StdPoco()\r""",
    },
    "cocos-js": {
        "keyword": "CocosJsPoco",
        "content": """\rfrom poco.drivers.cocosjs import CocosJsPoco\rpoco = CocosJsPoco()\r""",
    },
    "std-broker": {
        "keyword": "StdPoco",
        "content": """\rfrom poco.drivers.std import StdPoco\rfrom poco.utils.device import VirtualDevice\rpoco = StdPoco(15004, VirtualDevice('localhost'))\r""",
    },
    "unity": {
        "keyword": "UnityPoco",
        "content": """\rfrom poco.drivers.unity3d import UnityPoco\rpoco = UnityPoco()\r""",
    },
    "android": {
        "keyword": "AndroidUiautomationPoco",
        "content": """\rfrom poco.drivers.android.uiautomation import AndroidUiautomationPoco\rpoco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)\r""",
    },
    "netease": {
        "keyword": "NeteasePoco",
        "content": """\rfrom poco.drivers.netease.internal import NeteasePoco\rpoco = NeteasePoco()\r""",
    },
    "ios": {
        "keyword": "iosPoco",
        "content": """\rfrom poco.drivers.ios import iosPoco\rpoco = iosPoco()\r"""
    }
}
