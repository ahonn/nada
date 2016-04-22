#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from singleton import Singleton
from .common import *


class Database(Singleton):
    def __init__(self):
        if hasattr(self, '_init'):
            return
        self._init = True
        self.data = {
            "collections" : [[]]
        }
        self.path = DATABASE_PATH
        self.file = None

    def load(self):
        try:
            self.file = file(self.path, 'r')
            self.data = json.loads(self.file.read())
            self.file.close()
        except:
            self.__init__()
        self.save()

    def save(self):
        if os.path.isfile(self.path):
            os.remove(self.path)
        self.file = file(self.path, 'w')
        self.file.write(json.dumps(self.data))
        self.file.close
