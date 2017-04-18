#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Nada
"""
import locale
# import sys

locale.setlocale(locale.LC_ALL, "")
code = locale.getpreferredencoding()
# reload(sys)
# sys.setdefaultencoding('UTF-8')

from menu import Menu


def start():
    Menu().start()
