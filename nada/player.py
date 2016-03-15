#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import subprocess
import threading
import time

from ui import UI
from .common import *


class Player:
    def __init__(self):
        self.ui = UI()

        self.popen_handler = None
        self.play = False
        self.pause = False
        self.songs = []
        self.play_vol = -1
        self.play_id = -1
        self.view = 'songs'

    def popen_recall(self, onExit, popenArgs):
        def runInThread(onExit, popenArgs):
            self.popen_handler = subprocess.Popen(['mpg123', popenArgs], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                                  stderr=subprocess.PIPE)
            self.popen_handler.wait()
            if self.play:
                self.play_id = carousel(0, len(self.songs) - 1, self.play_id + 1)
                onExit()
            return

        thread = threading.Thread(target=runInThread, args=(onExit, popenArgs))
        thread.start()
        return thread

    def recall(self):
        self.play = True
        song = self.songs[self.play_id]
        self.ui.playinfo(song)
        self.popen_recall(self.recall, song['source'])

    def play_song(self, view, model, idx):
        self.view = view

        if view == 'songs':
            songs = model['songs']
            id = model['id']

            if idx == self.play_id and songs == self.songs:
                if self.pause:
                    self.resume()
                else:
                    self.pause_song()
            else:
                self.songs = songs
                self.play_id = idx
                self.play_vol = id

                if self.play:
                    self.switch()
                else:
                    self.recall()

        else:
            if self.play:
                if self.pause:
                    self.resume()
                else:
                    self.pause_song()

    def pause_song(self):
        self.pause = True
        os.kill(self.popen_handler.pid, signal.SIGSTOP)
        self.ui.playinfo(self.songs[self.play_id], pause=True)

    def resume(self):
        self.pause = False
        os.kill(self.popen_handler.pid, signal.SIGCONT)
        self.ui.playinfo(self.songs[self.play_id])

    def switch(self):
        self.stop()
        time.sleep(0.1)
        self.recall()

    def stop(self):
        if self.play and self.popen_handler:
            self.popen_handler.kill()
            self.play = False

    def next_song(self):
        self.stop()
        time.sleep(0.1)
        self.play_id = carousel(0, len(self.songs) - 1, self.play_id + 1)
        self.recall()

    def prev_song(self):
        self.stop()
        time.sleep(0.1)
        self.play_id = carousel(0, len(self.songs) - 1, self.play_id - 1)
        self.recall()
