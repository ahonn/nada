#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses
import time


class UI:
    def __init__(self):
        self.screen = curses.initscr()
        curses.cbreak()
        curses.noecho()
        self.screen.keypad(1)

        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)

    def playinfo(self, song, pause=False):
        self.screen.move(1, 1)
        self.screen.clrtoeol()
        self.screen.move(2, 1)
        self.screen.clrtoeol()
        if pause:
            self.screen.addstr(2, 5, '_ - z Z Z', curses.color_pair(3))
        else:
            self.screen.addstr(2, 5, '♩  ♪  ♫  ♬', curses.color_pair(3))
        self.screen.addstr(2, 19, song['name'] + ' - ' + song['artist'], curses.color_pair(4))
        self.screen.refresh()

    def status(self, info, opt, color=1):
        string = opt + ' <' + info + '>'
        self.screen.move(20, 1)
        self.screen.clrtoeol()
        self.screen.addstr(20, 5, string, curses.color_pair(color))
        self.screen.refresh()
        time.sleep(0.5)
        self.screen.move(20, 1)
        self.screen.clrtoeol()

    def loading(self):
        self.screen.addstr(6, 5, '♫  ♪ Nada ♫  ♪ Loading...', curses.color_pair(1))
        self.screen.refresh()

    def build(self, title, model, view, offset, index, step, play_vol, play_id):
        self.screen.move(4, 1)
        self.screen.clrtobot()
        self.screen.addstr(5, 5, title, curses.color_pair(1))

        if view == 'songs':
            model_len = len(model['songs'])
        else:
            model_len = len(model)

        if model_len == 0:
            self.screen.addstr(8, 5, 'Nothing ...')
        else:
            if view == 'menu':
                for i in xrange(offset, min(len(model), offset + step)):
                    if i == index:
                        self.screen.addstr(i - offset + 8, 2, '-> ' + model[i], curses.color_pair(2))
                    else:
                        self.screen.addstr(i - offset + 8, 5, model[i])

            elif view == 'list':
                for i in xrange(offset, min(len(model), offset + step)):
                    if i == index:
                        self.screen.addstr(i - offset + 8, 2, '-> ' + model[i], curses.color_pair(2))
                    else:
                        self.screen.addstr(i - offset + 8, 5, model[i])

            elif view == 'vols':
                for i in xrange(offset, min(len(model), offset + step)):
                    if i == index:
                        self.screen.addstr(i - offset + 8, 2, '-> ' + model[i]["name"], curses.color_pair(2))
                    else:
                        self.screen.addstr(i - offset + 8, 5, model[i]["name"])

            elif view == 'songs':
                vol_id = model['id']
                songs = model['songs']
                for i in xrange(offset, min(len(songs), offset + step)):
                    if i == index and i == play_id and play_vol == vol_id:
                        self.screen.addstr(i - offset + 8, 2, '>> ' + str(i) + '. ' + songs[i]['name'] + ' - ' + songs[i]['artist'],
                                           curses.color_pair(2))
                    elif i == play_id and play_vol == vol_id:
                        self.screen.addstr(i - offset + 8, 3, '> ' + str(i) + '. ' + songs[i]['name'] + ' - ' + songs[i]['artist'],
                                           curses.color_pair(5))
                    elif i == index:
                        self.screen.addstr(i - offset + 8, 2, '-> ' + str(i) + '. ' + songs[i]['name'] + ' - ' + songs[i]['artist'],
                                           curses.color_pair(2))
                    else:
                        self.screen.addstr(i - offset + 8, 5, str(i) + '. ' + songs[i]['name'] + ' - ' + songs[i]['artist'])

            elif view == 'about':
                self.screen.addstr(8, 12, 'The mind is like a serpent, ')
                self.screen.addstr(9, 12, 'forgetting all its unsteadiness by hearing the nada,')
                self.screen.addstr(10, 12, 'it does not run away anywhere.')
                self.screen.addstr(12, 45, 'By Ahonn@Nada-1.0.0')

    def search(self, string):
        self.screen.move(4, 1)
        self.screen.clrtobot()
        self.screen.addstr(5, 19, string, curses.color_pair(1))
        self.screen.refresh()
        curses.echo()
        info = self.screen.getstr(10, 10, 60)
        curses.noecho()
        if info.strip() is '':
            return self.search(string)
        else:
            return info
