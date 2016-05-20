#!/usr/bin/env python
# encoding: UTF-8

from setuptools import setup, find_packages

setup(
    name='nada',
    version='1.0.1',
    keywords=['music', 'luoo', 'cli', 'player'],
    description="Luoo music command line player",
    license='MIT License',
    packages=find_packages(),

    include_package_data=True,

    install_requires=[
        'requests',
        'BeautifulSoup4',
        'lxml'
    ],

    entry_points={
        'console_scripts': [
            'nada = nada:start'
        ],
    },

    author='ahonn',
    author_email='ahonn95@outlook.com',
    url='https://github.com/ahonn/Nada',
    zip_safe=False,
)
