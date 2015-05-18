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
import logging

sys.path.append('..')

from config.config import *
from node import UrlNode,HtmlNode


global URL_SIMILARY_SET	#use to filter repeated url


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
	'''过滤协议不符的URL
	PROTOCOL: defined in ../config.config.py
	'''
	prefix = urlparse.urlparse(urlstr)[0].lower()
	if prefix not in PROTOCOL:
		return False
	return True

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

def url_get(html):
	''' get url from html 
	Returns:
		url list
	'''	
	if len(html)<100:
		return []
	else:
		#get all links in html
		try:
			tmp = lxml.html.document_fromstring(html)
			tmp.make_links_absolute(url) #
			links = tmp.iterlinks()
			link_list = list(set([ i[2] for i in links]))
			return link_list
		except Exception,e :
			logging.error('url_get error')
			return []

def url_filter(url_list):
	'''filter url_list with bloom filter
	'''
	global URL_SIMILARY_SET
	#过滤不期待页面后缀和不期待的host
	try:
		temp_list = []
		for i in url_list:
			if url_filter_postfix_ignore(i) and url_filter_protocol(i):
				flag = ( URL_SIMILARY_SET.add(url_format(i)) )
				if not flag and urlparse.urlparse(i)[2]!='':						
					temp_list.append(i)

		link_list = temp_list
		return link_list
	except Exception, e:
		logging.error('url_filter error')
		return []

def url_generate_urlnode(urlstr, depth):
	'''constructor UrlNode with urlstr
	Args:
		urlstr: 
		depth: depth of urlstr
	Return:
		UrlNode
	'''
	urllist = urlparse.urlparse(urlstr)
	#sheme, netloc, path, params,query, fragment
	dest_url = urlparse.urlunparse( (urllist[0], urllist[1], urllist[2],urllist[3], urllist[4], '') )
	
	return UrlNode( dest_url=dest_url ,src_url=urlstr,
		html_length=len(html),time=timestamp(),
		html_title='',depth=int(depth)+1, priority=0)



def url_crawler(html_node):
	global URL_SIMILARY_SET
	link_list = []
	html = html_node.html
	url = html_node.url
	
	#get url from html
	link_list = url_get(html)

	#filter url 
	link_list = url_filter(link_list)
	
	tmp_url_node = []

	#构造UrlNode
	for i in link_list:						
		tmp_url_node.append(url_generate_urlnode(i, html_node.depth) )
	return tmp_url_node


def hashPage(html, size=64000000):
	code=0
	for c in html:
		if c>'A' and c<'z':
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
			fw.write(str(i.dest_url)+'\n')



