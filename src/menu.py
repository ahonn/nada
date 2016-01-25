#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Ahonn
# @Date:   2016-01-14 23:41:58
# @Last Modified by:   ahonn
# @Last Modified time: 2016-01-25 16:43:37

'''
落网 Menu
'''

import curses
import locale
import sys
import os
import json
import time
import webbrowser

from api import Luoo
from player import Player
from ui import UI

locale.setlocale(locale.LC_ALL, "")
code = locale.getpreferredencoding()

carousel = lambda left, right, x: left if (x>right) else (right if x<left else x)

class Menu:
	def __init__(self):
		reload(sys)
		sys.setdefaultencoding('UTF-8')
		self.datatype = 'menu'
		self.title = '落网'
		self.datalist = ['最新期刊', '分类期刊','搜索期刊', '关于']
		self.offset = 0
		self.index = 0
		self.playing = -1
		self.presentsong = []
		self.player = Player()
		self.ui = UI()
		self.luoo = Luoo()
		self.screen = curses.initscr()
		self.screen.keypad(1)
		self.step = 10
		self.stack = []
		
	def start(self):
		self.ui.menu(self.datatype, self.title, self.datalist, self.offset, self.index, self.step, self.playing)
		self.stack.append([self.datatype, self.title, self.datalist, self.offset, self.index])

		while True:
			datatype = self.datatype
			title = self.title
			datalist = self.datalist
			offset = self.offset
			idx = index = self.index
			step = self.step
			stack = self.stack
			key = self.screen.getch()
			self.ui.screen.refresh()

			if key == ord('q'):
				break
			
			elif key == ord('k'):
				if idx == offset:
					if offset == 0:
					    continue
					self.offset -= step
					self.index = offset - 1
				else:
					self.index = carousel(offset, min( len(datalist), offset + step) - 1, idx - 1)

			elif key == ord('j'):
				if idx == min( len(datalist), offset + step) - 1:
					if offset + step >= len( datalist ):
						continue
					self.offset += step
					self.index = offset + step
				else:
					self.index = carousel(offset, min( len(datalist), offset + step) - 1, idx + 1)

			elif key == ord('l'):
				if self.datatype == 'songs' or self.datatype == 'about':
					continue
				self.ui.loading()
				self.dispatch(idx)
				self.index = 0
				self.offset = 0

			elif key == ord('h'):
				if len(self.stack) == 1:
					continue
				up = stack.pop()
				self.datatype = up[0]
				self.title = up[1]
				self.datalist = up[2]
				self.offset = up[3]
				self.index = up[4]

			elif key == ord('f'):
				self.search()

			elif key == ord(' '):
				self.presentsongs = ['songs', title, datalist, offset, index]
				self.player.play(datatype, datalist, idx)

			elif key == ord(']'):
				self.player.next()
				self.index = self.player.idx
				time.sleep(0.1)

			elif key == ord('['):
				self.player.prev()
				self.index = self.player.idx
				time.sleep(0.1)

			elif key == ord('p'):
				if len(self.presentsongs) == 0:
					continue
				self.stack.append([datatype, title, datalist, offset, index])
				self.datatype = self.presentsongs[0]
				self.title = self.presentsongs[1]
				self.datalist = self.presentsongs[2]
				self.offset = self.presentsongs[3]
				self.index = self.presentsongs[4]

			elif key == ord('m'):
				if datatype != 'mian':
					self.stack.append([datatype, title, datalist, offset, index])
					self.datatype = self.stack[0][0]
					self.title = self.stack[0][1]
					self.datalist = self.stack[0][2]
					self.offset = 0
					self.index = 0

			self.playing = self.player.idx
			self.ui.menu(self.datatype, self.title, self.datalist, self.offset, self.index, self.step, self.playing)
			self.ui.screen.refresh()

		self.player.stop()
		curses.endwin()

	def dispatch(self, idx):
		luoo = self.luoo
		datatype = self.datatype
		title = self.title
		datalist = self.datalist
		offset = self.offset
		index = self.index
		self.stack.append([datatype, title, datalist, offset, index])

		if datatype == 'menu':
			self.choice(idx)
		
		elif datatype == 'vtype':
			type_id = datalist[idx]["id"]
			type_name = datalist[idx]["name"]
			self.datatype = 'vols'
			self.datalist = luoo.music(type_id)
			self.title += ' > ' + type_name

		elif datatype == 'vols':
			vol_number = datalist[idx]['number']
			self.datatype = 'songs'
			vol = luoo.vol(vol_number)
			self.datalist = vol['song']
			self.title += ' > ' + datalist[idx]['name']

	def choice(self, idx):
		luoo = self.luoo
		if idx == 0:
			self.datalist = luoo.music()
			self.datatype = 'vols'
			self.title += ' > 最新期刊'

		elif idx == 1:
			self.datalist = luoo.typelist()
			self.datatype = 'vtype'
			self.title += ' > 分类期刊'

		elif idx == 2:
			self.search()

		elif idx == 3:
			self.datatype = 'about'
			self.title += ' > 关于'

		self.offset = 0
		self.index = 0 

	def search(self):
		luoo = self.luoo
		ui = self.ui
		self.stack.append([self.datatype, self.title, self.datalist, self.offset, self.index])
		self.index = 0
		self.offset = 0

		self.datatype = 'songs'
		vol = ui.search()
		self.datalist = vol['song']
		self.title = 'vol. ' + vol['number'] + ' ' + vol['title']



