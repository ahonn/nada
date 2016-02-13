#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import requests

class Echo:

    def recommend(self):
        songs = []
        for page in xrange(1,10):
            url = 'http://echosystem.kibey.com/sound/hot?page=' + str(page) 
            request = requests.get(url)
            songs += self.song(request)
        return songs

    def daily(self):
        return self.hot("daily")

    def weekly(self):
        return self.hot("weekly")

    def monthly(self):
        return self.hot("monthly")

    def hot(self, type):
        url = 'http://echosystem.kibey.com/hot/sounds'
        request = requests.post(url, data = {'period' : type})
        return self.song(request)

    def song(self, request):
        songs = []
        for item in request.json()['result']['data']:
            songs.append({
                "name" : item['name'],
                "url"  : item['source']
            })
        return songs

    def hot_type(self):
        return self.type("hot")

    def new_type(self):
        return self.type("new")

    def type(self, order):
        url = 'http://echosystem.kibey.com/channel/get?limit=50&order=' + order
        request = requests.get(url)
        types = []
        for item in request.json()['result']['data']:
            types.append({
                "name" : item['name'],
                "id"  : item['id']
            })
        return types

    def vol(self, id):
        vols = []
        for page in xrange(1,10):
            url = 'http://echosystem.kibey.com/channel/info?id=' + str(id) + '&list_order=hot&page=' + str(page)
            request = requests.get(url)
            for item in request.json()['result']['data']['sounds']:
                vols.append({
                    "name" : item['name'],
                    "url"  : item['source']
                })
        return vols


if __name__ == '__main__':
    echo = Echo()
    for x in echo.hot_type():
        print x['name']







