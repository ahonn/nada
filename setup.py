#!/usr/bin/env python
#encoding: UTF-8

from setuptools import setup, find_packages


setup(
    name = 'LuooMusic',
    version = '0.1',
    packages = find_packages(),

    include_package_data = True,

    install_requires = [
        'requests',
        'BeautifulSoup4',
        'lxml'
     ],

    entry_points = {
        'console_scripts' : [
            'luoo = src:start'
        ],
    },

    author = 'ahonn',
    author_email = 'ahonn95@outlook.com',
    url = 'https://github.com/ahonn/LuooMusic',
    zip_safe = False,
)