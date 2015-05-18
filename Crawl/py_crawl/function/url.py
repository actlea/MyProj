#!/usr/bin/env python
#coding:utf-8
#2015-05-16

'''
实现对url的各种操作
'''

import lxml.html
import urlparse
import time
import sys
import Queue
import os
from pybloom import BloomFilter

sys.path.append('..')

from fetch import fetcher
from config.config import *
from node import UrlNode,HtmlNode

SIMILARY_SET = BloomFilter(capacity=1000, error_rate=0.001)



def timestamp():
	return str(time.strftime("%y-%m-%d %H:%M:%S", time.localtime()))


def url_filter_postfix_ignore(urlstr):
	'''过滤包含特定后缀的url
	Args:
		urlstr: url str
	Return:
		True, if urlstr not contain ignore postfix; or False
	'''
	#ignore postfix
	global IGNORE_EXT 
	postfix = urlparse.urlparse(urlstr)[2].split('.')[-1].lower()
	if postfix not in IGNORE_EXT:
		return True
	else:
		return False

def url_filter_protocol(urlstr):
	prefix = urlparse.urlparse(urlstr)[0].lower()
	if prefix not in PROTOCOL:
		return False
	return True

def url_domain_control(urlstr):
	pass


def url_format(urlstr):
	'''format url str
	策略是构建一个三元组
    第一项为url的netloc
    第二项为path
    第三项为query的每个参数名称(参数按照字母顺序排序，避免由于顺序不同而导致的重复问题)

	Args:

	Return:
		format url
	'''
	if urlparse.urlparse(urlstr)[2] =='':			
		urlstr = urlstr+'/'

	url_structure = urlparse.urlparse(urlstr)
	netloc = url_structure[1]	#www.jianshu.com
	path = url_structure[2]		#/path
	query = url_structure[4]	#sim=false&li=toc

	#依据query关键字的key进行排序
	query_list = sorted([i.split('=')[0] for i in query.split('&')]) #
	temp = str(netloc)+str(path)	
	for i in query_list:
		temp = temp+str(i)

	return temp



def url_crawler(html_node):
	global SIMILARY_SET
	link_list = []
	html = html_node.html
	url = html_node.url
	if len(html)<0:
		return []
	else:
		#get all links in html
		try:
			tmp = lxml.html.document_fromstring(html)
			tmp.make_links_absolute(url) #
			links = tmp.iterlinks()
			link_list = list(set([ i[2] for i in links]))		

		except Exception,e :
			pass

		#过滤不期待页面后缀和不期待的host
		try:
			temp_list = []
			for i in link_list:
				if url_filter_postfix_ignore(i) and url_filter_protocol(i):
					flag = ( SIMILARY_SET.add(url_format(i)) )
					if not flag and urlparse.urlparse(i)[2]!='':						
						temp_list.append(i)

			link_list = temp_list
		except Exception, e:
			print str(e)

		tmp_url_node = []

		for i in link_list:
			urllist = urlparse.urlparse(i)
			next_url = urlparse.urlunparse( (urllist[0], urllist[1], urllist[2],\
				urllist[3], urllist[4], '') )
				#default all priority are 0
			tmp_url_node.append( UrlNode( next_url ,url,len(html),timestamp(),'',html_node.depth, 0))
		return tmp_url_node


def hashPage(html, size=64000000):
	code=0
	for c in html:
		if c>'A' && c<'z':
			code = (code * 23 + c) % size
		pos = code / 8
		bits = 1 << (code % 8)








if __name__ == '__main__':
	url = 'http://www.jianshu.com'
	html = ''
	with open('2.html', 'r') as fr:
		html = fr.read()
	html_node = HtmlNode(url, html, timestamp(), 1)
	tmp_url_node = url_crawler(html_node)

	with open('url2.txt','w') as fw:
		for i in tmp_url_node:
			fw.write(str(i.url)+'\n')



