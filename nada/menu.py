#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses
import locale
import sys
import time

from api import Luoo, Echo
# from player import Player
from ui import UI

locale.setlocale(locale.LC_ALL, "")
code = locale.getpreferredencoding()

carousel = lambda left, right, x: left if (x > right) else (right if x < left else x)


class Menu:
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('UTF-8')

        self.title = 'Nada'
        self.model = ['luoo 落网', 'echo 回声', '关于']
        self.view = 'menu'
        self.ctrl = 'menu'

        self.offset = 0
        self.index = 0
        self.step = 10
        self.play_id = -1
        self.play_vol = -1

        self.present = []
        self.stack = []

        self.player = None
        self.ui = UI()
        self.luoo = Luoo()
        self.echo = Echo()

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

            if key == ord('q'):
                break

            elif key == ord('k'):
                if view == 'songs':
                    length = len(model['songs'])
                else:
                    length = len(model)
                if idx == offset:
                    if offset == 0:
                        continue
                    self.offset -= step
                    self.index = offset - 1
                else:
                    self.index = carousel(offset, min(length, offset + step) - 1, idx - 1)

            elif key == ord('j'):
                if view == 'songs':
                    length = len(model['songs'])
                else:
                    length = len(model)
                if idx == min(length, offset + step) - 1:
                    if offset + step >= length:
                        continue
                    self.offset += step
                    self.index = offset + step
                else:
                    self.index = carousel(offset, min(length, offset + step) - 1, idx + 1)


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
                    self.present = [title, model, view, ctrl, offset, index, self.play_vol, self.play_id]
                self.player.play(view, model, idx)

            elif key == ord(']'):
                self.player.next()
                if view == 'songs':
                    self.index = self.player.idx
                time.sleep(0.1)

            elif key == ord('['):
                self.player.prev()
                if view == 'songs':
                    self.index = self.player.idx
                time.sleep(0.1)

            elif key == ord('p'):
                if len(self.present) == 0:
                    continue
                self.stack.append([self.title, self.model, self.view, self.ctrl, self.offset, self.index])

                self.title = self.present[0]
                self.model = self.present[1]
                self.view = self.present[2]
                self.ctrl = self.present[3]
                self.offset = self.present[4]
                self.index = self.present[5]

            elif key == ord('m'):
                if view != 'menu':
                    self.stack.append([self.title, self.model, self.view, self.ctrl, self.offset, self.index])

                    self.title = self.stack[0][0]
                    self.model = self.stack[0][1]
                    self.view = self.stack[0][2]
                    self.ctrl = self.stack[0][3]
                    self.offset = self.stack[0][4]
                    self.index = self.stack[0][5]

            # self.play_vol = self.player.vol
            # self.play_id = self.player.idx
            self.ui.build(self.title, self.model, self.view, self.offset, self.index, self.step, self.play_vol,
                          self.play_id)
            self.ui.screen.refresh()

        self.player.stop()
        curses.endwin()

    def control(self, idx):
        self.stack.append([self.title, self.model, self.view, self.ctrl, self.offset, self.index])

        ctrl = self.ctrl
        if ctrl == 'menu':
            self.menu(idx)

        elif ctrl == 'luoo':
            self.luooMenu(idx)

        elif ctrl == 'luoo_vols':
            self.luoo_vols(idx)

        elif ctrl == 'luoo_vtype':
            self.luoo_vtype(idx)

        elif ctrl == 'echo':
            self.echoMenu(idx)

        elif ctrl == 'echo_hot':
            self.echo_hot(idx)

        elif ctrl == 'echo_tag':
            self.echo_tag(idx)

        elif ctrl == 'echo_vol':
            self.echo_vol(idx)

        self.offset = 0
        self.index = 0

    def menu(self, idx):
        if idx == 0:
            self.title += ' > luoo 落网'
            self.model = ['最新期刊', '分类期刊', '搜索期刊']
            self.view = 'list'
            self.ctrl = 'luoo'

        elif idx == 1:
            self.title += ' > echo 落网'
            self.model = ['每日推荐', '热门推荐', '频道分类']
            self.view = 'list'
            self.ctrl = 'echo'

        elif idx == 2:
            self.title += ' > 关于 Nada'
            self.view = 'about'
            self.ctrl = 'about'

    def luooMenu(self, idx):
        if idx == 0:
            self.title += ' > 最新期刊'
            self.model = self.luoo.new()
            self.view = 'vols'
            self.ctrl = 'luoo_vols'

        elif idx == 1:
            self.title += ' > 分类期刊'
            self.model = self.luoo.vtype()
            self.view = 'vols'
            self.ctrl = 'luoo_vtype'

        elif idx == 2:
            vol_number = self.ui.search('搜索期刊: ')
            try:
                self.model = self.luoo.vol(vol_number)
                self.title += ' > 搜索期刊 > Vol.' + self.model['number'] + ' ' + self.model['title']
                self.view = 'songs'
                self.ctrl = 'songs'
            except Exception, e:
                self.model = []

    def luoo_vols(self, idx):
        self.title += ' > ' + self.model[idx]['name']
        vol_number = self.model[idx]['number']
        self.model = self.luoo.vol(vol_number)
        self.view = 'songs'
        self.ctrl = 'songs'

    def luoo_vtype(self, idx):
        self.title += ' > ' + self.model[idx]['name']
        type_number = self.model[idx]['number']
        self.model = self.luoo.vols(type_number)
        self.view = 'vols'
        self.ctrl = 'luoo_vols'

    def echoMenu(self, idx):
        if idx == 0:
            self.title += ' > 每日推荐'
            self.model = self.echo.new()
            self.view = 'songs'
            self.ctrl = 'songs'

        elif idx == 1:
            self.title += ' > 热门推荐'
            self.model = ['本日热门', '本周热门', '本月热门']
            self.view = 'list'
            self.ctrl = 'echo_hot'

        elif idx == 2:
            self.title += ' > 频道分类'
            self.model = self.echo.all_tag()
            self.view = 'vols'
            self.ctrl = 'echo_tag'

    def echo_hot(self, idx):
        if idx == 0:
            self.title += ' > 本日热门'
            self.model = self.echo.daily_hot()

        elif idx == 1:
            self.title += ' > 本周热门'
            self.model = self.echo.weekly_hot()

        elif idx == 2:
            self.title += ' > 本月热门'
            self.model = self.echo.monthly_hot()

        self.view = 'songs'
        self.ctrl = 'songs'

    def echo_tag(self, idx):
        self.title += ' > ' + self.model[idx]['name']
        if idx == 0:
            self.model = self.echo.new_vols()
        elif idx == 1:
            self.model = self.echo.hot_vols()
        else:
            tag_number = self.model[idx]['number']
            self.model = self.echo.tag_vols(tag_number)

        self.view = 'vols'
        self.ctrl = 'echo_vol'

    def echo_vol(self, idx):
        self.title += ' > ' + self.model[idx]['name']
        vol_number = self.model[idx]['number']
        self.model = self.echo.vol(vol_number)
        self.view = 'songs'
        self.ctrl = 'songs'
