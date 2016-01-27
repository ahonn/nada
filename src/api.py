#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
		for x in xrange(1, 10):
			url = self.url + '/tag/' + type + '?p=' + str(x)
			soup = self.parser(url)
			
			for item in soup.find_all("a", class_="name"):
				vol = {
					"number" : item["href"].split('/')[-1],
					"name" : item.string.encode("utf-8"), 
					"url" : item["href"]
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

	def typelist(self):
		url = self.url + '/music/'
		soup = self.parser(url)

		typelist = []
		items = soup.find_all("a", class_="item")
		for x in xrange(1, len(items)):
			vtype = {
				"name" : items[x].text,
				"id" : items[x]["href"].split('/')[-1]
			}
			typelist.append(vtype)
		return typelist

		
		