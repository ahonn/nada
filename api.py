#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ahonn
# @Date:   2016-01-22 13:35:23
# @Last Modified by:   ahonn
# @Last Modified time: 2016-01-23 20:23:00

import os
import sys
import requests
from bs4 import BeautifulSoup

class Luoo:
	"""docstring for Luoo"""
	def __init__(self):
		self.url = 'http://www.luoo.net/'

	def parser(self, url):
		r = requests.get(url);
		return BeautifulSoup(r.content, "lxml")

	def music(self, type = ""):
		music = []
		url = self.url + '/tag/' + type + '?p=1'
		soup = self.parser(url)

		for item in soup.find_all("a", class_="name"):
			vol = {
				"number" : item['href'].split('/')[-1],
				"name" : item.string.encode("utf-8"), 
				"url" : item['href']
			}
			music.append(vol)
		return music

	def vol(self, number):
		url = self.url + '/music/' + number
		soup = self.parser(url)

		vol = {}
		vol['number'] = soup.find("span", class_="vol-number").text
		vol['title'] = soup.find("span", class_="vol-title").text

		song_num = 1;
		vol['song'] = []
		for item in soup.find_all("li", class_="track-item"):
			song = {
				"name" : item.find("a", class_="trackname").text.split(' ', 1)[1],
				"artist" : item.find("span", class_="artist").text,
				"url" : 'http://luoo-mp3.kssws.ks-cdn.com/low/luoo/radio' + number + '/' + str("%02d" % song_num) + '.mp3'
			}
			vol['song'].append(song)
			song_num += 1
		return vol


		
		