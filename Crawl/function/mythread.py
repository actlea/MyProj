#!/usr/bin/env python
#coding:utf-8
#2015-05-16

import threading
import os
import sys
import Queue

sys.path.append('..')

from config.config import *
from fetch import fetcher, fetch_mode



class FetchThread(threading.Thread):

	def __init__(self, func, tuple_list, queue_htmlnode, download_mode):
		super(FetchThread, self).__init__()
		self.func = func
		self.tuple_list = tuple_list
		self.queue_htmlnode = queue_htmlnode
		self.download_mode = download_mode


	def run(self):
		self.func(tuple_list, queue_htmlnode, download_mode)




class DBThread(threading.Thread):
	def __init__(self, keyword, queue_complete, queue_smart_node, storage_model):
		super(DBThread, self).__init__()