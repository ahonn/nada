#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import requests

class Echo:

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

    def recommend(self, page):
        url = 'http://echosystem.kibey.com/sound/hot?page=' + str(page) 
        request = requests.get(url)
        return self.song(request)

    def song(self, request):
        songs = []
        for item in request.json()['result']['data']:
            songs.append({
                "name" : item['name'],
                "url"  : item['source']
            })
        return songs







