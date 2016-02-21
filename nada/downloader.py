#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import urllib
import threading

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
        try:
            self.ui.status(filename, 'Downloading')
            if not os.path.exists(path):
                def download_thread(url, path):
                    urllib.urlretrieve(url , path)
                    self.ui.status(filename, 'Finish Download', 5)
                thread = threading.Thread(target=download_thread, args=(url, path))
                thread.start()
            else:
                self.ui.status(filename, 'Exists Download', 4)
        except:
            self.ui.status(filename, 'Error Download', 3)
        
        
