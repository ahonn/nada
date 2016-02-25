#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


class Luoo:
    def __init__(self):
        self.url = 'http://www.luoo.net'

    @staticmethod
    def parser(url):
        request = requests.get(url)
        return BeautifulSoup(request.content, "lxml")

    def new(self):
        return self.vols()

    def vols(self, vtype=''):
        vols = []
        for page in xrange(1, 10):
            url = self.url + '/tag/' + vtype + '?p=' + str(page)
            soup = self.parser(url)

            items = soup.find_all("a", class_="name")
            for item in items:
                vols.append({
                    "number": item["href"].split('/')[-1],
                    "name": item.string.encode("utf-8")
                })
        return vols

    def vol(self, number):
        url = self.url + '/music/' + number
        soup = self.parser(url)

        title = soup.find("span", class_="vol-title").text
        vol = {'number': number, 'title': title, 'songs': []}

        items = soup.find_all("li", class_="track-item")
        for i, item in enumerate(items):
            vol['songs'].append({
                "name": item.find("a", class_="trackname").text.split(' ', 1)[1],
                "artist": item.find("span", class_="artist").text,
                "source": 'http://luoo-mp3.kssws.ks-cdn.com/low/luoo/radio' + number + '/' + str(
                    "%02d" % (i + 1)) + '.mp3'
            })
        return vol

    def vtype(self):
        url = self.url + '/music/'
        soup = self.parser(url)

        vtype = []
        items = soup.find_all("a", class_="item")
        for item in items:
            if item.text == '最新期刊':
                continue
            vtype.append({
                "name": item.text,
                "number": item["href"].split('/')[-1]
            })
        return vtype


class Echo:
    def __init__(self):
        self.url = 'http://echosystem.kibey.com'

    def new(self):
        songs = {'number': 'new', 'songs': []}
        for page in xrange(1, 10):
            url = self.url + '/sound/hot?page=' + str(page)
            request = requests.get(url)
            items = request.json()['result']['data']
            songs['songs'] += self.songs(items)
        return songs

    def daily_hot(self):
        return self.hot("daily")

    def weekly_hot(self):
        return self.hot("weekly")

    def monthly_hot(self):
        return self.hot("monthly")

    def hot(self, vtype):
        url = self.url + '/hot/sounds'
        request = requests.post(url, data={'period': vtype})
        items = request.json()['result']['data']
        songs = {'number': vtype, 'songs': self.songs(items)}
        return songs

    @staticmethod
    def all_tag():
        tags = []
        items = [
            ['最新', '####'],
            ['最热', '####'],
            ['类型', '1006'],
            ['情绪', '1007'],
            ['3 D', '1008'],
            ['影视', '1009'],
            ['自然', '1010'],
            ['场景', '1011'],
            ['二次元', '1013'],
            ['搞笑', '1014'],
            ['品牌', '1015'],
            ['创作', '1016'],
            ['另类', '1017'],
            ['娱乐', '1018'],
            ['专题', '1019'],
            ['学术', '1020'],
            ['电台', '1135']
        ]
        for item in items:
            tags.append({
                "name": item[0],
                "number": item[1]
            })
        return tags

    def tag_vols(self, tag):
        url = self.url + '/channel/get?limit=100&order=hot&tag=' + str(tag)
        request = requests.get(url)

        vols = []
        items = request.json()['result']['data']
        for item in items:
            vols.append({
                "name": item['name'],
                "number": item['id']
            })
        return vols

    def hot_vols(self):
        return self.vols("hot")

    def new_vols(self):
        return self.vols("new")

    def vols(self, order):
        url = self.url + '/channel/get?limit=100&order=' + order
        request = requests.get(url)

        vols = []
        items = request.json()['result']['data']
        for item in items:
            vols.append({
                "name": item['name'],
                "number": item['id']
            })
        return vols

    def vol(self, number):
        vol = {'number': number, 'songs': []}
        for page in xrange(1, 20):
            url = self.url + '/channel/info?id=' + str(number) + '&list_order=hot&page=' + str(page)
            request = requests.get(url)
            items = request.json()['result']['data']['sounds']
            vol['songs'] += self.songs(items)
        return vol

    @staticmethod
    def songs(items):
        songs = []
        for item in items:
            songs.append({
                "name": item['name'],
                "artist": item['channel']['name'],
                "source": item['source']
            })
        return songs
