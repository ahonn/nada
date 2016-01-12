#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Ahonn
# @Date:   2016-01-11 23:34:49
# @Last Modified by:   Ahonn
# @Last Modified time: 2016-01-12 17:16:33

import os
import sys
import requests
import urllib
import re

reload(sys)
sys.setdefaultencoding('utf-8')

class Luoo:
	"""Get Luoo Vol"""
	url = None
	number = None
	name = None
	tag = None
	cover = None
	desc = None
	music = None
	html = None

	def set_number(self, number):
		self.name = None
		self.tag = None
		self.cover = None
		self.desc = None
		self.music = None
		self.number = number
		self.url = 'http://www.luoo.net/music/' + str(number)
		self.html = requests.get(self.url).content

	def set_path(self, path):
		if path == None:
			self.path = './vol.' + str(self.number) + ' ' + self.get_name() + ' '.join(self.get_tag())
		else:
			self.path = path
		if not os.path.exists(self.path):
			os.mkdir(self.path)

	def get_name(self):
		if self.name == None:
			self.name = re.findall('<span class="vol-title">(.*?)</span>', self.html)[0].decode('utf-8')
		return self.name

	def get_tag(self):
		if self.tag == None:
			self.tag = re.findall('<a href=".*?" target="_blank" class="vol-tag-item">(.*?)</a>', self.html)
		return self.tag

	def get_cover(self):
		if self.cover == None:
			self.cover = re.findall('<img src="(.*?)" alt=".*?" class="vol-cover">', self.html)[0]
		return self.cover

	def get_desc(self):
		if self.desc == None:
			desc = re.findall('<div class="vol-desc">(.*?)</div>', self.html, re.DOTALL)[0]
			self.desc = desc.strip().replace('<br>', ' ')
		return self.desc

	def get_music(self):
		if self.music == None:
			self.music = []
			name = re.findall('<a href="javascript:;" rel="nofollow" class="trackname btn-play">(.*?)</a>', self.html)
			author = re.findall('<span class="artist btn-play">(.*?)</span>', self.html)
			for x in xrange(0, len(name)):
				self.music.append(name[x] + '-' + author[x])
		return self.music

	def download_desc(self, path = None):
		filename = self.path + '/' + self.get_name().decode('utf-8') + '.txt'
		if not os.path.exists(filename):
			f = file(filename, 'wb')
			f.write(self.get_desc())
			f.close()
			return True
		else:
			return False


	def download_cover(self, path = None):
		filename = self.path + '/' + self.get_name() + '.jpg'
		if not os.path.exists(filename):
			f = file(filename, 'wb')
			f.write(self.get_cover())
			f.close()
			return True
		else:
			return False

	def download_music(self, path = None):
		music_list = self.get_music()
		for i in xrange(1, len(music_list) + 1):
			music_name = music_list[i-1] + '.mp3'
			filename = self.path + '/' + music_name
			url = 'http://luoo-mp3.kssws.ks-cdn.com/low/luoo/radio' + str(self.number) + '/' + str("%02d" % i) + '.mp3'
			if not os.path.exists(filename):
				urllib.urlretrieve(url , filename)
				yield 'Download ' + music_name
			else:
				yield 'Exists ' + music_name
	
	def download_vol(self, number, path = None):
		self.set_number(number)
		self.set_path(path)
		if self.download_cover():
			print 'Download vol.' + str(self.number) + ' cover'
		else:
			print 'Exists vol.' + str(self.number) + ' cover'
		if self.download_desc():
			print 'Download vol.' + str(self.number) + ' description'
		
		music = self.download_music()
		for message in music:
			print message

		print '--------------vol.' + str(self.number) + ' Finish!!---------------'