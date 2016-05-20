#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Nada Player Menu
"""

import curses
import locale
import sys
import time

from ui import UI
from player import Player
from api import Luoo
from database import Database
from downloader import Downloader
from .common import *

locale.setlocale(locale.LC_ALL, "")
code = locale.getpreferredencoding()

if os.path.isdir(BASE_PATH) is False:
    os.mkdir(BASE_PATH)


class Menu:
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('UTF-8')

        self.title = 'Nada'
        self.model = ['最新期刊', '分类期刊', '搜索期刊', '收藏夹', '关于']
        self.view = 'menu'
        self.ctrl = 'menu'

        self.offset = 0
        self.index = 0
        self.step = 10
        self.play_id = -1
        self.play_vol = -1

        self.present = []
        self.stack = []

        self.player = Player()
        self.ui = UI()
        self.luoo = Luoo()
        self.downloader = Downloader()

        self.database = Database()
        self.database.load()
        self.collections = self.database.data['collections'][0]

        self.screen = curses.initscr()
        self.screen.keypad(1)

    def start(self):
        self.ui.build(self.title, self.model, self.view, self.offset, self.index, self.step, self.play_vol,
                      self.play_id)
        self.stack.append([self.title, self.model, self.view, self.ctrl, self.offset, self.index])

        while True:
            title = self.title
            model = self.model
            view = self.view
            ctrl = self.ctrl

            offset = self.offset
            index = idx = self.index
            step = self.step

            key = self.screen.getch()
            self.ui.screen.refresh()

            if view == 'songs':
                length = len(model['songs'])
            else:
                length = len(model)

            if key == ord('q'):
                break

            elif key == ord('k'):
                if idx == offset:
                    if offset == 0:
                        continue
                    self.offset -= step
                    self.index = offset - 1
                else:
                    self.index = carousel(offset, min(length, offset + step) - 1, idx - 1)

            elif key == ord('j'):
                if idx == min(length, offset + step) - 1:
                    if offset + step >= length:
                        continue
                    self.offset += step
                    self.index = offset + step
                else:
                    self.index = carousel(offset, min(length, offset + step) - 1, idx + 1)

            elif key == ord('u'):
                if offset == 0:
                    continue
                self.offset -= step
                self.index = (index - step) // step * step

            elif key == ord('i'):
                if offset + step >= length:
                    continue
                self.offset += step
                self.index = (index + step) // step * step

            elif key == ord('l'):
                if self.view == 'songs':
                    continue
                self.ui.loading()
                self.control(idx)
                self.index = 0
                self.offset = 0

            elif key == ord('h'):
                if len(self.stack) == 1:
                    continue
                up = self.stack.pop()
                self.title = up[0]
                self.model = up[1]
                self.view = up[2]
                self.ctrl = up[3]
                self.offset = up[4]
                self.index = up[5]

            elif key == ord(' '):
                if view == 'songs':
                    self.present = [title, model, view, ctrl, offset]
                self.player.play_song(view, model, idx)

            elif key == ord(']'):
                self.player.next_song()
                if view == 'songs':
                    self.index = self.player.play_id % length
                    if idx == min(length, offset + step) - 1:
                        if offset + step >= length:
                            continue
                        self.offset += step
                time.sleep(0.1)

            elif key == ord('['):
                self.player.prev_song()
                if view == 'songs':
                    self.index = self.player.play_id % length
                    if idx == offset:
                        if offset == 0:
                            continue
                        self.offset -= step
                time.sleep(0.1)

            elif key == ord('p'):
                if len(self.present) == 0:
                    continue
                self.stack.append([self.title, self.model, self.view, self.ctrl, self.offset, self.index])

                self.title = self.present[0]
                self.model = self.present[1]
                self.view = self.present[2]
                self.ctrl = self.present[3]
                self.index = idx = self.player.play_id
                self.offset = idx // step * step

            elif key == ord('m'):
                if view != 'menu':
                    self.stack.append([self.title, self.model, self.view, self.ctrl, self.offset, self.index])

                    self.title = self.stack[0][0]
                    self.model = self.stack[0][1]
                    self.view = self.stack[0][2]
                    self.ctrl = self.stack[0][3]
                    self.offset = self.stack[0][4]
                    self.index = self.stack[0][5]

            elif key == ord('a'):
                if view == 'songs' and ctrl is not 'collections':
                    self.ui.status(model['songs'][idx]['name'], 'Add', 5)
                    self.collections.append(model['songs'][idx])

            elif key == ord('r'):
                if ctrl == 'collections':
                    if length != 0:
                        self.ui.status(model['songs'][idx]['name'], 'Remove', 3)
                        self.model['songs'].pop(idx)
                        self.index = carousel(offset, min(length, offset + step) - 1, idx)

            elif key == ord('c'):
                self.stack.append([self.title, self.model, self.view, self.ctrl, self.offset, self.index])
                self.title = 'Nada > nada 收藏'
                self.collection()

            elif key == ord('d'):
                if view == 'songs':
                    self.downloader.download(model['songs'][idx])

            self.play_vol = self.player.play_vol
            self.play_id = self.player.play_id
            self.ui.build(self.title, self.model, self.view, self.offset, self.index, self.step, self.play_vol,
                          self.play_id)
            self.ui.screen.refresh()

        self.player.stop()
        self.database.save()
        curses.endwin()

    def control(self, idx):
        self.stack.append([self.title, self.model, self.view, self.ctrl, self.offset, self.index])

        ctrl = self.ctrl
        if ctrl == 'menu':
            self.menu(idx)

        elif ctrl == 'vols':
            self.vols(idx)

        elif ctrl == 'vtype':
            self.vtype(idx)

        self.offset = 0
        self.index = 0

    def menu(self, idx):
        if idx == 0:
            self.title += ' > 最新期刊'
            self.model = self.luoo.new()
            self.view = 'vols'
            self.ctrl = 'vols'

        elif idx == 1:
            self.title += ' > 分类期刊'
            self.model = self.luoo.vtype()
            self.view = 'vols'
            self.ctrl = 'vtype'

        elif idx == 2:
            vol_id = self.ui.search('搜索期刊: ')
            try:
                self.model = self.luoo.vol(vol_id)
                self.title += ' > 搜索期刊 > Vol.' + self.model['id'] + ' ' + self.model['title']
                self.view = 'songs'
                self.ctrl = 'songs'
            except Exception, e:
                self.model = []

        elif idx == 3:
            self.title += ' > 收藏夹'
            self.collection()

        elif idx == 4:
            self.title += ' > 关于'
            self.view = 'about'
            self.ctrl = 'about'

    def collection(self):
        self.model = {'id': 'collections', 'songs': self.collections}
        self.view = 'songs'
        self.ctrl = 'collections'
        self.offset = 0
        self.index = 0

    def vols(self, idx):
        self.title += ' > ' + self.model[idx]['name']
        vol_id = self.model[idx]['id']
        self.model = self.luoo.vol(vol_id)
        self.view = 'songs'
        self.ctrl = 'songs'

    def vtype(self, idx):
        self.title += ' > ' + self.model[idx]['name']
        type_id = self.model[idx]['id']
        self.model = self.luoo.vols(type_id)
        self.view = 'vols'
        self.ctrl = 'vols'
