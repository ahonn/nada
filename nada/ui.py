#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses
from luoo import Luoo
from echo import Echo

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

	def playinfo(self, name, artist=None, pause=False):
		self.screen.move(1, 1)
		self.screen.clrtoeol()
		self.screen.move(2, 1)
		self.screen.clrtoeol()
		if pause:
			self.screen.addstr(1, 19, '_ _ z Z Z', curses.color_pair(3))
		else:
			self.screen.addstr(1, 19, '♫  ♪ ♫  ♪', curses.color_pair(3))
		if artist is None:
			self.screen.addstr(1, 32, name , curses.color_pair(4))
		else:
			self.screen.addstr(1, 32, name + '  -  ' + artist, curses.color_pair(4))
		self.screen.refresh()

	def loading(self):
		self.screen.addstr(6, 19, '♫  ♪ Nada ♫  ♪ Loading...', curses.color_pair(1))
		self.screen.refresh()

	def menu(self, datatype, title, datalist, offset, index, step, number, playing):
		self.screen.move(4, 1)
		self.screen.clrtobot()
		self.screen.addstr(4, 19, title, curses.color_pair(1))

		if len(datalist) == 0:
			self.screen.addstr(8, 19, 'Nothing ...')
		else:
			if datatype == 'menu':
				for i in xrange(offset, min(len(datalist), offset+step)):
					if i == index:
						self.screen.addstr(i - offset + 8, 16, '-> ' + str(i) + '. ' + datalist[i], curses.color_pair(2))
					else:
						self.screen.addstr(i - offset + 8, 19, str(i) + '. ' + datalist[i])

			elif datatype == 'luooType':
				for i in xrange(offset, min(len(datalist), offset+step)):
					if i == index:
						self.screen.addstr(i - offset + 8, 16, '-> ' + str(i) + '. ' + datalist[i]["name"], curses.color_pair(2))
					else:
						self.screen.addstr(i - offset + 8, 19, str(i) + '. ' + datalist[i]["name"])

			elif datatype == 'echoType':
				for i in xrange(offset, min(len(datalist), offset+step)):
					if i == index:
						self.screen.addstr(i - offset + 8, 16, '-> ' + str(i) + '. ' + datalist[i], curses.color_pair(2))
					else:
						self.screen.addstr(i - offset + 8, 19, str(i) + '. ' + datalist[i])
						
			elif datatype == 'songs':
				song = datalist['song']
				for i in xrange(offset, min(len(song), offset+step)):
					if i == index and i == playing and number == datalist['number']:
						self.screen.addstr(i - offset + 8, 16, ('>> ' + str(i) + '. ' + song[i]['name'] + '  -  ' + song[i]['artist'])[:51], curses.color_pair(2))
					elif i == playing and number == datalist['number']:
						self.screen.addstr(i - offset + 8, 17, ('> ' + str(i) + '. ' + song[i]['name'] + '  -  ' + song[i]['artist'])[:50], curses.color_pair(5))
					elif i == index:
						self.screen.addstr(i - offset + 8, 16, ('-> ' + str(i) + '. ' + song[i]['name'] + '  -  ' + song[i]['artist'])[:51], curses.color_pair(2))
					else:
						self.screen.addstr(i - offset + 8, 19, (str(i) + '. ' + song[i]['name'] + '  -  ' + song[i]['artist'])[:48])

			elif datatype == 'echos':
				song = datalist['song']
				for i in xrange(offset, min(len(song), offset+step)):
					if i == index and i == playing and number == datalist['number']:
						self.screen.addstr(i - offset + 8, 16, ('>> ' + str(i) + '. ' + song[i]['name'])[:31], curses.color_pair(2))
					elif i == playing and number == datalist['number']:
						self.screen.addstr(i - offset + 8, 17, ('> ' + str(i) + '. ' + song[i]['name'])[:30], curses.color_pair(5))
					elif i == index:
						self.screen.addstr(i - offset + 8, 16, ('-> ' + str(i) + '. ' + song[i]['name'])[:31], curses.color_pair(2))
					else:
						self.screen.addstr(i - offset + 8, 19, (str(i) + '. ' + song[i]['name'])[:28])

			elif datatype == 'luooVols' or datatype == 'echoVols':
				for i in xrange(offset, min(len(datalist), offset+step)):
					if i == index:
						self.screen.addstr(i - offset + 8, 16, '-> ' + datalist[i]['name'], curses.color_pair(2))
					else:
						self.screen.addstr(i - offset + 8, 19, datalist[i]['name'])

			elif datatype == 'about':
				self.screen.addstr(8, 15, 'The mind is like a serpent, ')
				self.screen.addstr(9, 15, 'forgetting all its unsteadiness by hearing the nada,')
				self.screen.addstr(10, 15, 'it does not run away anywhere.')
				self.screen.addstr(12, 60, 'By Ahonn ')

			else:
				for i in xrange(offset, min(len(datalist), offset+step)):
					if i == index:
						self.screen.addstr(i - offset + 8, 16, '-> ' + str(i) + '. ' + datalist[i], curses.color_pair(2))
					else:
						self.screen.addstr(i - offset + 8, 19, str(i) + '. ' + datalist[i])

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
		curses.echo()
		info = self.screen.getstr(10, 19, 60)
		curses.noecho()
		if info.strip() is '':
		    return self.get_param(prompt_string)
		else:
		    return info