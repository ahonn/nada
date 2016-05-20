#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import requests
from bs4 import BeautifulSoup


class Luoo:
    def __init__(self):
        self.url = 'http://www.luoo.net'

    def parser(self, url):
        request = requests.get(url, timeout=5)
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
                    "id": item["href"].split('/')[-1],
                    "name": item.string.encode("utf-8")
                })
        return vols

    def vol(self, id):
        url = self.url + '/music/' + id
        soup = self.parser(url)

        title = soup.find("span", class_="vol-title").text
        vol = {'id': id, 'title': title, 'songs': []}

        items = soup.find_all("li", class_="track-item")
        for i, item in enumerate(items):
            vol['songs'].append({
                "name": item.find("a", class_="trackname").text.split(' ', 1)[1],
                "artist": item.find("span", class_="artist").text,
                "source": 'http://luoo-mp3.kssws.ks-cdn.com/low/luoo/radio' + id + '/' + str(
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
                "id": item["href"].split('/')[-1]
            })
        return vtype
