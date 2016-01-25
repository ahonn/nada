#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ahonn
# @Date:   2016-01-22 19:35:36
# @Last Modified by:   ahonn
# @Last Modified time: 2016-01-24 15:36:10

import subprocess
import threading
import time
import os
import signal
from ui import UI

carousel = lambda left, right, x: left if (x>right) else (right if x<left else x)

class Player:

	def __init__(self):
		self.ui = UI()
		self.datatype = 'songs'
		self.popen_handler = None
		self.playing_flag = False
		self.pause_flag = False
		self.songs = []
		self.idx = 0

	def popen_recall(self, onExit, popenArgs):

		def runInThread(onExit, popenArgs):
			self.popen_handler = subprocess.Popen(['mpg123', popenArgs], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			self.popen_handler.wait()
			if self.playing_flag:
				self.idx = carousel(0, len(self.songs)-1, self.idx+1)
				onExit()
			return
		thread = threading.Thread(target=runInThread, args=(onExit, popenArgs))
		thread.start()
		return thread

	def recall(self):
		self.playing_flag = True
		item = self.songs[self.idx]
		self.ui.playinfo(item['name'], item['artist'])
		self.popen_recall(self.recall, item['url'])

	def play(self, datatype, songs, idx):
		self.datatype = datatype

		if datatype == 'songs':
			if idx == self.idx and songs == self.songs:
				if self.pause_flag:
					self.resume()
				else: 
					self.pause()

			else:
				self.songs = songs
				self.idx = idx

				if self.playing_flag:
					self.switch()
				else:
					self.recall()

		else:
			if self.playing_flag:
				if self.pause_flag:
					self.resume()
				else:
					self.pause()
			else:
				pass

	def switch(self):
		self.stop()
		time.sleep(0.01)
		self.recall()

	def stop(self):
		if self.playing_flag and self.popen_handler:
			self.playing_flag = False
			self.popen_handler.kill()

	def pause(self):
		self.pause_flag = True
		os.kill(self.popen_handler.pid, signal.SIGSTOP)
		item = self.songs[self.idx]
		self.ui.playinfo(item['name'], item['artist'], pause=True)

	def resume(self):
		self.pause_flag = False
		os.kill(self.popen_handler.pid, signal.SIGCONT)
		item = self.songs[self.idx]
		self.ui.playinfo(item['name'], item['artist'])

	def next(self):
		self.stop()
		time.sleep(0.01)
		self.idx = carousel(0, len(self.songs)-1, self.idx+1)
		self.recall()
		return self.idx

	def prev(self):
		self.stop()
		time.sleep(0.01)
		self.idx = carousel(0, len(self.songs)-1, self.idx-1)
		self.recall()
		return self.idx