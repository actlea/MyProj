# -*- coding: utf-8 -*-
# actlea  2015-05-20

import sys
from Fcrawler.spiders.config import *
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
from Utility import Redis_Set, Redis_Priority_Set

global IGNORE_EXT 	#url后缀过滤
global PROTOCOL
global Depth_Table


reload(sys) 
sys.setdefaultencoding('utf-8')


class Url:
	if  not os.path.exists(DIR):
		os.mkdir(DIR)	
	
		
	if not os.path.exists(HMTL_DIR):
		os.mkdir(HMTL_DIR)
					
				
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
		if len(purl)>2 and len(url)>2 and urll[-1]==purll[-1] and urll[-2]==purll[-2]:
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
	def url_keyword_ignore(cls,url):
		urlstruc = urlparse.urlparse(url)
		netloc = urlstruc[1]
		words = netloc.split('.')
		
		stop=1
		if len(words)>1:
			stop=2
	
		for i in words[0:stop]:
			for j in IGNORE_KEYWORD:
				if match(i, j):
					return True
		return False
		
	@classmethod
	def url_extract(cls, html, base_url):
		hxs = lxml.html.fromstring(html)
		a_tags = hxs.xpath('//a')	
		
		for a in a_tags:
			link = a.xpath('./@href') 
			anchor_text= a.xpath('./text()')			
			link = text_format(link)		
			
			link = cls.url_format(link, base_url)
			anchor_text = text_format(anchor_text)				

			yield (link, anchor_text)
		

	@classmethod
	def url_dup_filter(cls, url):
		'''
		if url duplicate or has been visited, return True, else return False
		'''		
		flag = url in URL_VISITED_SET.get_all()
		if flag: return True		
		#bloom filter	
		flag = URL_UNVISITED_SET.add(url)
		if flag: return True
		flag = URL_UNVISITED_RSET.push(url)==0 #push url into redis set
		if flag: return True

		return False
		
	
	@classmethod
	def url_filter(cls, html, domain_filter=True, base_url=''):	
				
		for link in cls.url_extract(html, base_url):
			url = link[0]
			#portocol filter
			portocol_flag = cls.url_portocol_filter(url)
			
						
			#domain filter
			if domain_filter:
				domain_flag =  domain_filter and cls.url_domain_control(url, base_url)
			else:
				domain_flag = True	
			
			keyword_filter_flag =  not cls.url_keyword_ignore(url)		
			#depth filter		
			depth_flag = cls.url_depth_control(url)
			if portocol_flag and domain_flag and depth_flag and keyword_filter_flag:			
				dup_flag = cls.url_dup_filter(url)			
				if  not dup_flag:			
					yield link
				
												
	
	@classmethod
	def urlItem(cls, link_anchor,purl, depth=0):
		item = UrlItem()
		item['url'] = link_anchor[0]
		item['purl'] = purl		
		item['depth'] = depth+1		
		item['priority'] = cls.url_priority(link_anchor)
		item['anchor'] = link_anchor[1]
		item['time'] = timestamp()
		return item		
		
	@classmethod	
	def url_priority(cls, link_anchor):
		return 0		
	
	
	@classmethod
	def urlItem__file_save(cls, urlItem_list):
		if not os.path.exists('../data'):
			os.mkdir('../data/')
		file = '../data/url_%s' %(str(time.strftime("%m%d%H%M", time.localtime())))
		with open(file, 'w')  as fw:
			for i in urlItem_list:
				try:
					tmp = i['url'] + ' | '+ str(i['depth'])+ ' | ' + i['anchor']+'\n'
					fw.write(tmp)
				except:
					continue
	@classmethod
	def urlItem_redis_save(cls, urItem):
		''' save urlitem in redis set'''
		try:
			URL_ITEM_UNV_SET.push(urItem)
		except Exception,e:
			print e
			
		
			
	@classmethod
	def url_todo(cls, html, purl, domain_control=False):
		#
		if urlparse.urlparse(purl)[2]=='':
			purl = purl+'/'			
		
		#depth of purl
		depth = cls.url_depth(purl)
		#generate UrlItem		
		for i in cls.url_filter(html, domain_control, purl):			
			item = cls.urlItem(i, purl,depth)			
			cls.urlItem_redis_save(item)
			yield item
		
		#save to file		
# 		cls.urlItem__file_save(urlitem_list)
		
		

def urlItem_read():
	with open('222','w') as fw:	
		for i in URL_ITEM_UNV_SET.get_all():
			url = i['url']
			if i['anchor']:
				anchor = i['anchor']
			else:
				anchor = ''
				
			if not Url.url_keyword_ignore(url):
				fw.write(url+' | ' + anchor+'\n')
			

def url_priority(urlItem):
	pass



if __name__ == '__main__':	

# 	with open('111', 'w') as fw:
# 		for i in URL_ITEM_UNV_SET.get_all():
# 			url = i['url']
# 			if i['anchor']:
# 				anchor = i['anchor']
# 			else:
# 				anchor = ''			
# 			fw.write(url+' | '+anchor+'\n')
 	with open(HMTL_DIR+'fde8c258f06d730dc2d2abd3ce95161bb5cb1a10.html','r') as fr:
 		html = fr.read()
 	Url.url_todo(html, '')	
# 	urlItem_read()
# 	with open('../data/HTML/0602152144.html', 'r') as fr:
# 		html = fr.read()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	