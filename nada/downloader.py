#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import urllib

from ui import UI
from .common import *


class Downloader:
    def __init__(self):
        self.path = DOWNLOAD_PATH
        self.ui = UI()
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def download(self, song):
        url = song['source']
        filename = song['name'] + ' - ' + song['artist'] + '.mp3'
        path = os.path.join(self.path, filename)
        self.ui.status(song['name'], 'Downloading')
        try:
            if not os.path.exists(path):
                urllib.urlretrieve(url , path)
                status = 'Finish Download'
                color = 5
            else:
                status = 'Exists  Download'
                color = 4
        except:
            status = 'Error  Download'
            color = 3
        self.ui.status(song['name'], status, color)
