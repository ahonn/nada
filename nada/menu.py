#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
落网 Menu
"""

import curses
import locale
import sys
import os
import json
import time
import webbrowser

from luoo import Luoo
from echo import Echo
from player import Player
from ui import UI

locale.setlocale(locale.LC_ALL, "")
code = locale.getpreferredencoding()

carousel = lambda left, right, x: left if (x > right) else (right if x < left else x)


class Menu:
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('UTF-8')
        self.datatype = 'menu'
        self.title = 'Nada'
        self.datalist = ['luoo落网', 'echo回声', '关于']

        self.offset = 0
        self.index = 0
        self.playing = -1
        self.number = -1
        self.presentsong = []
        self.step = 10
        self.stack = []
        
        self.player = Player()
        self.ui = UI()
        self.luoo = Luoo()
        self.echo = Echo()
        self.screen = curses.initscr()
        self.screen.keypad(1)


    def start(self):
        self.ui.menu(self.datatype, self.title, self.datalist, self.offset, self.index, self.step, self.number,
                     self.playing)
        self.stack.append([self.datatype, self.title, self.datalist, self.offset, self.index, self.playing])

        while True:
            datatype = self.datatype
            title = self.title
            datalist = self.datalist
            offset = self.offset
            idx = index = self.index
            playing = self.playing
            step = self.step
            stack = self.stack
            key = self.screen.getch()
            self.ui.screen.refresh()

            if key == ord('q'):
                break

            elif key == ord('k'):
                if datatype == 'songs' or datatype == 'echos':
                    length = len(datalist['song'])
                else:
                    length = len(datalist)

                if idx == offset:
                    if offset == 0:
                        continue
                    self.offset -= step
                    self.index = offset - 1
                else:
                    self.index = carousel(offset, min(length, offset + step) - 1, idx - 1)

            elif key == ord('j'):
                if datatype == 'songs' or datatype == 'echos':
                    length = len(datalist['song'])
                else:
                    length = len(datalist)

                if idx == min(length, offset + step) - 1:
                    if offset + step >= length:
                        continue
                    self.offset += step
                    self.index = offset + step
                else:
                    self.index = carousel(offset, min(length, offset + step) - 1, idx + 1)

            elif key == ord('l'):
                if self.datatype == 'songs' or self.datatype == 'about' or self.datatype == 'echos':
                    continue
                self.ui.loading()
                self.dispatch(idx)
                self.index = 0
                self.offset = 0
                self.playing = -1

            elif key == ord('h'):
                if len(self.stack) == 1:
                    continue
                up = stack.pop()
                self.datatype = up[0]
                self.title = up[1]
                self.datalist = up[2]
                self.offset = up[3]
                self.index = up[4]
                self.playing = up[5]

            elif key == ord('f'):
                self.search()

            elif key == ord(' '):
                self.presentsongs = ['songs', title, datalist, offset, index, playing]
                self.player.play(datatype, datalist, idx)

            elif key == ord(']'):
                self.player.next()
                if datatype == 'songs':
                    self.index = self.player.idx
                time.sleep(0.1)

            elif key == ord('['):
                self.player.prev()
                if datatype == 'songs':
                    self.index = self.player.idx
                time.sleep(0.1)

            elif key == ord('p'):
                if len(self.presentsongs) == 0:
                    continue
                self.stack.append([datatype, title, datalist, offset, index, playing])
                self.datatype = self.presentsongs[0]
                self.title = self.presentsongs[1]
                self.datalist = self.presentsongs[2]
                self.offset = self.presentsongs[3]
                self.index = self.presentsongs[4]
                self.playing = self.presentsongs[5]

            elif key == ord('m'):
                if datatype != 'menu':
                    self.stack.append([datatype, title, datalist, offset, index, playing])
                    self.datatype = self.stack[0][0]
                    self.title = self.stack[0][1]
                    self.datalist = self.stack[0][2]
                    self.offset = 0
                    self.index = 0

            self.playing = self.player.idx
            self.number = self.player.number
            self.ui.menu(self.datatype, self.title, self.datalist, self.offset, self.index, self.step, self.number,
                         self.playing)

        self.player.stop()
        curses.endwin()

    def dispatch(self, idx):
        datatype = self.datatype
        title = self.title
        datalist = self.datalist

        luoo = self.luoo
        echo = self.echo

        offset = self.offset
        index = self.index
        playing = self.playing
        self.stack.append([datatype, title, datalist, offset, index, playing])

        if datatype == 'menu':
            self.choice(idx)

        elif datatype == 'luoo':
            self.luooChoice(idx)

        elif datatype == 'echo':
            self.echoChoice(idx)

        elif datatype == 'echoHot':
            self.echoHot(idx)

        elif datatype == 'luooType':
            self.luooType(idx)

        elif datatype == 'echoType':
            self.echoType(idx)

        elif datatype == 'luooVols':
            self.luooVols(idx)

        elif datatype == 'echoVols':
            self.echoVols(idx)

        self.offset = 0
        self.index = 0

    def choice(self, idx):
        if idx == 0:
            self.datalist = ['最新期刊', '分类期刊', '搜索期刊']
            self.datatype = 'luoo'
            self.title += ' > luoo落网'

        elif idx == 1:
            self.datalist = ['每日推荐', '热门推荐', '频道分类']
            self.datatype = 'echo'
            self.title += ' > echo回声'

        elif idx == 2:
            self.datatype = 'about'
            self.title += ' > 关于'

    def luooChoice(self, idx):
        if idx == 0:
            self.datalist = self.luoo.music()
            self.datatype = 'luooVols'
            self.title += ' > 最新期刊'

        elif idx == 1:
            self.datalist = self.luoo.typelist()
            self.datatype = 'luooType'
            self.title += ' > 分类期刊'

        elif idx == 2:
            self.search()

        self.offset = 0
        self.index = 0

    def luooType(self, idx):
        self.datatype = 'vols'
        type_number = datalist[idx]["number"]
        self.title += ' > ' + datalist[idx]["name"]
        self.datalist = self.luoo.music(type_number)

    def luooVols(self, idx):
        vol_number = datalist[idx]['number']
        self.datatype = 'songs'
        self.datalist = self.luoo.vol(vol_number)
        self.title += ' > ' + datalist[idx]['name']

    def echoChoice(self, idx):
        if idx == 0:
            self.datalist = {'number' : 0 , 'song' : self.echo.recommend()}
            self.datatype = 'echos'
            self.title += ' > 每日推荐'

        elif idx == 1:
            self.datalist = ['本日热门', '本周热门', '本月热门']
            self.datatype = 'echoHot'
            self.title += ' > 热门推荐'

        elif idx == 2:
            self.datalist = ['全部频道', '最热频道', '最新频道']
            self.datatype = 'echoType'
            self.title += ' > 频道分类'

    def echoHot(self, idx):
        if idx == 0:
            self.datalist = {'number' : 1 , 'song' : self.echo.daily()}
            self.datatype = 'echos'
            self.title += ' > 本日热门'

        elif idx == 2:
            self.datalist = {'number' : 2 , 'song' : self.echo.weekly()}
            self.datatype = 'echos'
            self.title += ' > 本周热门'

        elif idx == 3:
            self.datalist = {'number' : 3 , 'song' : self.echo.monthly()}
            self.datatype = 'echos'
            self.title += ' > 本月热门'

    def echoType(self, idx):
        if idx == 0:
            pass

        elif idx == 1:
            self.datatype = 'echoVols'
            self.title += ' > 最热频道'
            self.datalist = self.echo.hot_type()

        elif idx == 2:
            self.datatype = 'echoVols'
            self.title += ' > 最新频道'
            self.datalist = self.echo.new_type()

    def echoVols(self, idx):
        self.datatype = 'echos'
        self.title += ' > ' + self.datalist[idx]['name']
        vid =  self.datalist[idx]['id']
        self.datalist = {'number' : vid, 'song' : self.echo.vol(vid)}
        
    def search(self):
        luoo = self.luoo
        ui = self.ui
        self.stack.append([self.datatype, self.title, self.datalist, self.offset, self.index, self.playing])
        self.index = 0
        self.offset = 0

        self.datatype = 'songs'
        vol = ui.search()
        self.datalist = vol
        self.title += ' > 落网 > vol. ' + vol['number'] + ' ' + vol['title']





