#!/usr/bin/env python
# coding:utf-8
# manning  2015-05-17

'''
创建的Page类
'''
import sys
sys.path.append('..')


from node import UrlNode,HtmlNode
from urlFilter import *
from config.config import *

from fetch import fetcher


class Page(object):

	def __init__(self):
		pass

	def page(self, url):
		

