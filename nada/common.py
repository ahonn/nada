#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

BASEDIR = '.nada'
DATABASE = 'database.json'
BASE_PATH = os.path.join(os.path.expanduser('~'), BASEDIR)
DATABASE_PATH = os.path.join(BASE_PATH, DATABASE)

carousel = lambda left, right, x: left if (x > right) else (right if x < left else x)