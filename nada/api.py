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


class Douban:
    def __init__(self):
        self.url = "https://music.douban.com"
        self.site_url = "https://site.douban.com/"
        self.play_url = "https://music.douban.com/j/artist/playlist"
        self.player_url = "https://music.douban.com/artists/player/"

    def parser(self, url):
        request = requests.get(url)
        return BeautifulSoup(request.content, "lxml")

    def hot(self):
        hots = []
        soup = self.parser(self.url)

        tag_block = soup.find("div", class_="tag-block")
        items = tag_block.find_all("a")
        for item in items:
            hots.append({
                "id": item["href"].split('/')[-2],
                "name": item.text
            })
        return hots[1:]

    def artists_list(self, id):
        artists = []
        url = self.url + '/artists/genre_page/' + str(id)
        soup = self.parser(url)

        items = soup.find_all("div", class_="photoin")
        for item in items:
            item = item.find("div", class_="ll").find("a")
            artists.append({
                "id": item["href"].split('/')[-2],
                "name": item.text
            })
        return artists

    def source(self, sids):
        list_url = self.player_url + '?sid=' + ",".join(sids) + '&source=site'
        soup = self.parser(list_url)
        content = soup.find_all("script")
        source = re.findall(' "url": "(.*?)", ', content[0].text)
        return source

    def artist_songs(self, artist):
        vol = {'id': artist["id"], 'songs': []}
        url = self.site_url + artist["id"]
        soup = self.parser(url)

        sids = []
        items = soup.find_all("td", class_="title player-playable")
        for item in items:
            sids.append(item["data-sid"])
        source = self.source(sids)
        n = 0
        for item in items:
            vol['songs'].append({
                "name": item.text.strip(),
                "artist": artist["name"],
                "source": source[n]
            })
            n += 2
        return vol

    def hot_songs(self):
        vol = {'id': 'hot_songs', 'songs': []}
        soup = self.parser(self.url)
        content = soup.find_all("script")
        sids_list = re.findall('{"index":(.*?)}', content[-7].text)

        sids = []
        name = []
        artist = []
        for item in zip(sids_list, xrange(10)):
            name.append(re.findall('"title":"(.*?)"', item[0])[0])
            artist.append(re.findall('"artist_name":"(.*?)"', item[0])[0])
            sids.append(re.findall('"sid":"(.*?)"', item[0])[0])
        source = self.source(sids)
        n = 0
        for x in xrange(len(name)):
            vol['songs'].append({
                "name": name[x],
                "artist": artist[x],
                "source": source[n]
            })
            n += 2
        return vol
