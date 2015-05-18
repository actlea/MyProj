#!/usr/bin/env python
#coding:utf-8
'''
Created on May 16, 2015

@author: root
'''

'''
1.only support static download now.



'''



import time
import os
import urlparse
import requests
import signal
import sys
import random
import logging

sys.path.append('..')

#for browser test
from splinter import Browser
from config.config import *

reload(sys) 
sys.setdefaultencoding('utf-8')  # @UndefinedVariable



def fetcher(url, DOWNLOAD_MODE=0):
    '''
    页面下载模块
    '''
#     time.sleep(FETCH_TIME_INTERVAL)            #抓取时间间隔

    if DOWNLOAD_MODE == 0:
        #static mode
        try:
            response = requests.get(url, timeout = 15, headers = random_header())
            if response.status_code == 200:
                return response.content
            else:
                return ""
        except Exception, e:
            logging.error("url: %s in mode: %d fetcher() error", url, DOWNLOAD_MODE)
    elif DOWNLOAD_MODE == 1:
        #动态模式
        try:
            browser = Browser('phantomjs')
            browser.visit(url)
            html = browser.html
            browser.quit()  
            return html
        except Exception, e:
            #差记录日志s
            logging.error("url: %s in mode: %d fetcher() error", url, DOWNLOAD_MODE)
            return ""
    elif DOWNLOAD_MODE == 2:
        return ""
        pass
    else:
        return ""


def fetch_mode(urlnode_queue, mode):
	'''we have depth-first-search, breadth-first-search, priority-first-search
	Args:
		urlnode_queue: Queue store UrlNode
		mode:
			0: depth-first-search
			1: breadth-first-search
			2: priority-first-search
			other: random search
	Returns:
		return url_node_queue arranged according to mode		
	'''
	templist = []
	templequeue = Queue.Queue()

	if not urlnode_queue.empty():
		while not urlnode_queue.empty():
			temp_node = urlnode_queue.get()
			templist.append(temp_node)
		#depth-first-search
		if int(mode) == 0:
			templist.sort(key=lambda node:node.depth, reverse=True)			
		#breadth-first-search
		elif int(mode) == 1:
			templist.sort(key=lambda node:node.depth)	
        #priority search		
		elif int(mode) == 2:
			templist.sort(key=lambda node:node.priority)
		else:
        #random search
			import random
			random.shuffle(templist)
		for node in templist:
				templequeue.put(node)
		return templequeue


def main():
    url = "http://www.jianshu.com/p/544d406e0875"
    html = fetcher(url)
    with open('./2.html', 'w') as fw:
    	fw.write(html)

if __name__ == '__main__':
    main()
