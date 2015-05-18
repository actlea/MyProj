#!/usr/bin/env python
#coding:utf-8
#2015-05-16

import urlparse
import threading
import Queue
import sys
import os
import logging
import time

sys.path.append('..')

from fetch import fetcher, fetch_mode
from config.config import *
from node import UrlNode, HtmlNode
from mythread import FetchThread,fetch_work


#global variables 
NOW_TIME = time.time()		#start time
EXIT_FLAG = 0 				#No. of thread exit
TOTAL_COUNT = 0				#No. of fetched pages

QUEUE_URLNODE = Queue.Queue()
QUEUE_HTMLNODE = Queue.Queue()
Share_Queue = Queue.Queue() #存储任务

def timestamp():
	return str(time.strftime("%y-%m-%d %H:%M:%S", time.localtime()))


def init_urlnode(start_urls_list):
	nodelist = []
	for i in start_urls_list:
		tmpnode = UrlNode(i, '',-1,0)
		nodelist.append(tmpnode)
	return nodelist


def server_exit_conditions(fetch_time, thread_num, fetch_count):
	'''contorl server to exit
	Args:
		fetch_time:	if server run time > fetch_time, exit
		thread_num: if all thread died, then exit
		fetch_count: if pages number > fetch_count, then exit
	Returns:
		False Or True
	'''

	if time.time() - NOW_TIME < fetch_time \
	   and EXIT_FLAG<thread_num \
	   and TOTAL_COUNT < fetch_count:
	   	return True
	else:
		return False	   	


def fetch_work(tuple_list, queue_htmlnode, download_mode):
	'''fetch html 
	Args:
		tuple_list: a tuple like(Queue.queue, thread_num)
		queue_htmlnode: Queue use to save HtmlNode
		download_mode:	0,1,2 or static,dynamic...
	Return:
		None
	'''
	global TOTAL_COUNT	#No. of fetched page
	global EXIT_FLAG	#No. of died thread
	global QUEUE_URLNODE

	stop_flag = 0
	while stop < 5: #最多重复下载5次
		if not tuple_list[0].empty():
			stop_flag = 0
			urlnode = tuple_list[0].get()	#get url node from queue

			html = fetcher(urlnode.url, download_mode)
			if len(html)>100:
				html_node = HtmlNode(urlnode.url, html, timestamp(), urlnode.depth)
				QUEUE_HTMLNODE.put(html_node)
				TOTAL_COUNT += 1	# get a new page

				print_info = timestamp()+'\t'+str(urlnode.url)+'\t'+str(node.depth)
				print print_info
				logging.info(print_info)
			else:
				logging.error('url: %s fetch error', urlnode.url)
		else:
			stop_flag += 1
			time.sleep(5)
		EXIT_FLAG += 1



def server(thread_num=THREAD_NUM, start_urls=START_URLS, fetch_time=FETCH_TIME, \
	host_keyword=HOST_KEYWORD, ignore_keyword=IGNORE_EXT,download_mode=DOWNLOAD_MODE,\
	max_depth=DEPTH, fetch_count=FETCH_COUNT, fetch_mode=FETCH_MODE, \
	similarity=SIMILARITY, focused_word=URL_KEYWORD):
	'''控制整个爬行的过程
	Args:
		host_keyword:	这是用于限定只爬取某个网站,如果为空，则无此限定
		ignore_keyword:	网址的后缀中不应该包含的字段，比如.jpg,.gif等
		focused_word:	网址中包含的关键字
	Returns:
		None
	'''

	
	global NOW_TIME	

	#update time
	NOW_TIME = time.time()
	#初始化url节点队列
	start_urls_list = set_start_urls(start_urls)
	start_nodes = init_urlnode(start_urls_list)
	for i in start_nodes:
		QUEUE_URLNODE.put(i)

	tuple_list = []
	for i in xrange(thread_num):
		tuple_list.append( (Queue.Queue(), str(i)) )

	#开启抓取线程
	thread_list = []
	for task in xrange(thread_num): 
		thread_list.append(FetchThread(fetch_work, tuple_list[task], QUEUE_HTMLNODE, download_mode))

	for task in thread_list:
		task.setDaemon(True) 	#在start之前设置为僵尸线程
		task.start()

	#开启数据库操作的线程
	db_engine = None




	#URL结点队列调度
	while server_exit_conditions(fetch_time, thread_num, fetch_count):
		
		# 取url
		for atom in tuple_list:
			if not QUEUE_URLNODE.empty() and atom[0].empty():
				QUEUE_URLNODE = fetch_mode(QUEUE_URLNODE, fetch_mode)
				urlnode = QUEUE_URLNODE.get()
				atom.put(urlnode)

		#放url
		if not QUEUE_HTMLNODE.empty():
			html_node = QUEUE_HTMLNODE.get()

			nodelist = crawler(html_node) # not yet write 



