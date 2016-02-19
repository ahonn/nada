#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os



BASEDIR = '.nada'
DOWNLOADDIR = 'Music/nada'
DATABASE = 'database.json'

HOME = os.path.expanduser('~')

BASE_PATH = os.path.join(HOME, BASEDIR)
DOWNLOAD_PATH = os.path.join(HOME, DOWNLOADDIR)
DATABASE_PATH = os.path.join(BASE_PATH, DATABASE)

carousel = lambda left, right, x: left if (x > right) else (right if x < left else x)