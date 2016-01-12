#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Ahonn
# @Date:   2016-01-12 00:15:44
# @Last Modified by:   Ahonn
# @Last Modified time: 2016-01-12 18:19:15
import sys
import time
from luoo import Luoo
reload(sys)
sys.setdefaultencoding('utf-8')

vlen = len(sys.argv)
if vlen == 1:
	print r"请输入落网期刊刊号！"
else:
	minn = int(min(sys.argv[1:]))
	maxn = int(max(sys.argv[1:])) + 1

	Luoo = Luoo()

	for i in xrange(minn, maxn):
		Luoo.download_vol(i)
		Luoo.log()
		time.sleep(1)


