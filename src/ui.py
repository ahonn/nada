#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ahonn
# @Date:   2016-01-23 13:52:19
# @Last Modified by:   ahonn
# @Last Modified time: 2016-01-25 16:42:01


import curses
from api import Luoo

class UI:
	def __init__(self):
		self.screen = curses.initscr()
		curses.cbreak()
		curses.noecho()
		self.screen.keypad(1)
		self.luoo = Luoo()
		
		curses.start_color()
		curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
		curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
		curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
		curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)

	def playinfo(self, name, artist, pause=False):
		self.screen.move(1, 1)
		self.screen.clrtoeol()
		self.screen.move(2, 1)
		self.screen.clrtoeol()
		if pause:
			self.screen.addstr(1, 19, '_ _ z Z Z', curses.color_pair(3))
		else:
			self.screen.addstr(1, 19, '♫  ♪ ♫  ♪', curses.color_pair(3))
		self.screen.addstr(1, 32, name + '  -  ' + artist, curses.color_pair(4))
		self.screen.refresh()

	def loading(self):
		self.screen.addstr(6, 19, '我们，记录独立音乐， Loading...', curses.color_pair(1))
		self.screen.refresh()

	def menu(self, datatype, title, datalist, offset, index, step, playing):
		self.screen.move(4, 1)
		self.screen.clrtobot()
		self.screen.addstr(4, 19, title, curses.color_pair(1))

		if len(datalist) == 0:
			self.screen.addstr(8, 19, 'Nothing ...')
		else:
			if datatype == 'menu':
				for i in xrange(offset, len(datalist)):
					if i == index:
						self.screen.addstr(i - offset + 8, 16, '-> ' + str(i) + '. ' + datalist[i], curses.color_pair(2))
					else:
						self.screen.addstr(i - offset + 8, 19, str(i) + '. ' + datalist[i])

			elif datatype == 'vtype':
				for i in xrange(offset, min(len(datalist), offset+step)):
					if i == index:
						self.screen.addstr(i - offset + 8, 16, '-> ' + str(i) + '. ' + datalist[i]["name"], curses.color_pair(2))
					else:
						self.screen.addstr(i - offset + 8, 19, str(i) + '. ' + datalist[i]["name"])
						
			elif datatype == 'songs':
				for i in xrange(offset, len(datalist)):
					if i == index and i == playing:
						self.screen.addstr(i - offset + 8, 16, ('>> ' + str(i) + '. ' + datalist[i]['name'] + '  -  ' + datalist[i]['artist'])[:51], curses.color_pair(2))
					elif i == index:
						self.screen.addstr(i - offset + 8, 16, ('-> ' + str(i) + '. ' + datalist[i]['name'] + '  -  ' + datalist[i]['artist'])[:51], curses.color_pair(2))
					elif i == playing:
						self.screen.addstr(i - offset + 8, 17, ('> ' + str(i) + '. ' + datalist[i]['name'] + '  -  ' + datalist[i]['artist'])[:50], curses.color_pair(5))
					else:
						self.screen.addstr(i - offset + 8, 19, (str(i) + '. ' + datalist[i]['name'] + '  -  ' + datalist[i]['artist'])[:48])

			elif datatype == 'vols':
				for i in xrange(offset, min(len(datalist), offset+step)):
					if i == index:
						self.screen.addstr(i - offset + 8, 16, '-> ' + datalist[i]['name'], curses.color_pair(2))
					else:
						self.screen.addstr(i - offset + 8, 19, datalist[i]['name'])

			elif datatype == 'about':
				self.screen.addstr(8, 15, 'LuooMusic 基于 Python，所有音乐来自落网（www.luoo.net）')
				self.screen.addstr(10, 60, 'By Ahonn ')

		self.screen.refresh()

	def search(self):
		luoo = self.luoo
		vol_number = self.get_param('搜索期刊：')
		try:
			data = luoo.vol(vol_number)
			return data
		except Exception, e:
			return []

	def get_param(self, prompt_string):
		self.screen.move(4,1)
		self.screen.clrtobot()
		self.screen.addstr(5, 19, prompt_string, curses.color_pair(1))
		self.screen.refresh()
		info = self.screen.getstr(10, 19, 60)
		if info.strip() is '':
		    return self.get_param(prompt_string)
		else:
		    return info