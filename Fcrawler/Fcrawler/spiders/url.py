# -*- coding: utf-8 -*-
# actlea  2015-05-20

import sys
sys.path.append('..')
import time
import urlparse
from pybloom import BloomFilter
import pickle

import lxml.html
import os

###################################################################
#my own function
from config import *
from stringHelper import *
from Fcrawler.items import UrlItem,PageItem
from Utility import DupeFilterTest,Redis_Set, Redis_Priority_Set

global IGNORE_EXT 	#url后缀过滤
global PROTOCOL
global Depth_Table


reload(sys) 
sys.setdefaultencoding('utf-8')


class Url:
				
	@classmethod
	def url_absolute(cls, url, base_url):
		#makes absolute links
		res = urlparse.urljoin(base_url, url)		
		return res	
			
	@classmethod
	def url_format(cls,url, base_url):	
		url = cls.url_absolute(url, base_url)			
		url_structure = urlparse.urlparse(url)
	
		scheme=url_structure[0]
		if scheme not in PROTOCOL:
			return ''
		path=url_structure[2]
		if path=='':
			url = url+'/'
		return url 
	
	@classmethod
	def url_depth(cls, url):		
		#get url depth
		key = url_hashcode(url)
		depth=0		
		if Depth_Table.has_key(key):
			depth = Depth_Table[key]+1				
		return depth	
	
	@classmethod
	def add_depth(cls, url):
		key = url_hashcode(url)
		depth = cls.url_depth(url)
		if Depth_Table.has_key(key):
			Depth_Table[key] = depth			
		
	@classmethod
	def url_domain_control(cls,url, purl):
		'''netloc filter'''
		url_d = urlparse.urlparse(url)[1] 
		purl_d = urlparse.urlparse(purl)[1]
	
		urll=url_d.split('.')
		purll = purl_d.split('.')
		if urll[-1]==purll[-1] and urll[-2]==purll[-2]:
			return True
		else:
			return False
		
	@classmethod
	def url_depth_control(cls, url,CRAWL_DEPTH=5):
		depth = cls.url_depth(url)
		cls.add_depth(url)	
		if depth > CRAWL_DEPTH:
			return False			
		return True
	
	@classmethod
	def url_portocol_filter(cls,url):
		urlstruc = urlparse.urlparse(url)
		if urlstruc[0] not in PROTOCOL:
			return False
		return True
		
	@classmethod
	def url_extract(cls, html, base_url):
		hxs = lxml.html.fromstring(html)
		a_tags = hxs.xpath('//a')
		link_anchor_list=[]
		
		for a in a_tags:
			link = a.xpath('./@href') 
			anchor_text= a.xpath('./text()')	
			link = text_format(link)
			
			link = cls.url_format(link, base_url)
			anchor_text = text_format(anchor_text)
			
			link_anchor_list.append((link, anchor_text))
		return link_anchor_list

	@classmethod
	def url_dup_filter(cls, url):
		'''
		if url duplicate, return True, else return False
		'''
		#bloom filter
		flag = URL_UNVISITED_SET.add(url)
		flag = flag or not URL_UNVISITED_Redis_SET.push(url) #push url into redis set
		
		#request filter
# 		request_dup = DupeFilterTest()
# 		flag = flag or request_dup.test_dupe_filter(url)
		return flag
		
	
	@classmethod
	def url_filter(cls, link_anchor_list, domain_filter=True, base_url=''):
		
		fi_link_anchor_list=[]
		
		for link in link_anchor_list:
			url = link[0]
			#portocol filter
			portocol_flag = cls.url_portocol_filter(url)			
			#domain filter
			domain_flag =  domain_filter and cls.url_domain_control(url, base_url)	
			#depth filter		
			depth_flag = cls.url_depth_control(url)
			if portocol_flag and domain_flag and depth_flag:			
				dup_flag = cls.url_dup_filter(url)			
				if  not dup_flag:
					fi_link_anchor_list.append( link )
				
		return fi_link_anchor_list			
												
	
	@classmethod
	def urlItem(cls, link_anchor,purl, depth=0):
		item = UrlItem()
		item['url'] = link_anchor[0]
		item['purl'] = purl
		item['time'] = timestamp()
		item['depth'] = depth+1		
		item['priority'] = cls.url_priority(link_anchor)
		item['anchor'] = link_anchor[1]
		return item		
		
	@classmethod	
	def url_priority(cls, link_anchor):
		return 0		
	
	
	@classmethod
	def urlItem__file_save(cls, urlItem_list):
		if not os.path.exists('../data'):
			os.mkdir('../data/')
		file = '../data/url_%s' %(str(time.strftime("%m-%d-%H:%M", time.localtime())))
		with open(file, 'w')  as fw:
			for i in urlItem_list:
				try:
					tmp = i['url'] + ' | '+ str(i['depth'])+ ' | ' + i['anchor']+'\n'
					fw.write(tmp)
				except:
					continue
	@classmethod
	def urlItem_redis_save(cls, urItem_list):
		''' save urlitem in redis set'''
		for i in urItem_list:
			try:
				UrlItem_UNV_Set.push(pickle.dumps(i, protocol=-1))
			except:
				continue
		
			
	@classmethod
	def url_todo(cls, html, purl, domain_control=True):
		#
		if urlparse.urlparse(purl)[2]=='':
			purl = purl+'/'		
		
		#all url has been format
		link_anchor_list = cls.url_extract(html, purl)
		
		#url filter
		link_anchor_list = cls.url_filter(link_anchor_list, domain_control, purl)
		
		#depth of purl
		depth = cls.url_depth(purl)
		#generate UrlItem
		urlitem_list=[]
		for i in link_anchor_list:			
			item = cls.urlItem(i, purl,depth)			
			urlitem_list.append(item)
			yield urlitem_list
		
		#save to file		
		cls.urlItem__file_save(urlitem_list)
		#save to redis
		cls.urlItem_redis_save(urlitem_list)
		
		#save Depth_Table to redis
	


		



def url_priority(urlItem):
	pass



if __name__ == '__main__':
	html_content = ''
	link_list = []
	with open('111', 'r') as fr:
		html_content = fr.read()

	purl='http://www.hupu.com/'
	Url.url_todo(html_content, purl)
	