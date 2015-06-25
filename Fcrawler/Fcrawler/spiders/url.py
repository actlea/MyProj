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
		#get and set url depth		
		depth = 0
		if Depth_Hash_Table.isexist(url):
			depth = int(Depth_Hash_Table.get(url))+1
			Depth_Hash_Table.set(url,depth)
		else:
			Depth_Hash_Table.set(url,depth)
		return depth	
	
	@classmethod
	def url_domain_control(cls,url, purl):
		'''netloc filter, if url in domain, return True'''
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
		if depth > CRAWL_DEPTH:
			return False			
		return True
	
	@classmethod
	def url_portocol_filter(cls,url):
		'''if url portocol not in PROTOCOL return False'''
		urlstruc = urlparse.urlparse(url)
		if urlstruc[0] not in PROTOCOL:
			return False
		return True

	@classmethod
	def url_keyword_ignore(cls,url):
		'''if url has ignore keyword, return False'''
		urlstruc = urlparse.urlparse(url)
		netloc = urlstruc[1]
		words = netloc.split('.')
		
		#choose 0-stop word to find ignore key words
		stop=1
		if len(words)>1:
			stop=2
	
		for i in words[0:stop]:
			for j in IGNORE_KEYWORD:
				if match(i, j):
					return False
		return True
	
	@classmethod
	def url_keyword_focus(cls, url):
		'''if url has no keyword, return False'''
		for i in KEYWORD:
			if match(i, url):
				return True
		return False
		
	@classmethod
	def url_extract(cls, html, base_url):
		'''extract url and format url'''
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
		#redis hset filter
		flag = URL_VISITED_HSET.isexist(url)
		if flag: return True		
		#bloom filter	
		flag = URL_UNVISITED_SET.add(url)
		if flag: return True
		#redis set filter
		flag = URL_UNVISITED_RSET.push(url)
		if not flag: return True 
		
		return False
		
	@classmethod
	def url_filter(cls, html, domain_filter=True, base_url=''):
		'''filter non-need(domain,ignore keyword, duplicate, depth contorl) url''' 	
		
		#all url has been formatted
		for link in cls.url_extract(html, base_url):
			if link:url = link[0]
			else:continue
			
			#depth filter		
			depth_flag = cls.url_depth_control(url)
			if not depth_flag: continue
			
			#portocol filter
			portocol_flag = cls.url_portocol_filter(url)
			if not portocol_flag:continue	
			
			#keyword filter
			keyword_filter_flag =  cls.url_keyword_ignore(url)
			if not keyword_filter_flag: continue	
			
			#keyword focus
			if not cls.url_keyword_focus(url): continue
				
			#domain filter
			domain_flag = True
			if domain_filter:
				domain_flag =  cls.url_domain_control(url, base_url)
			if not domain_flag: continue		
					
			#duplicate filter
			dup_flag = cls.url_dup_filter(url)
			if not dup_flag:
				URL_UNVISITED_RSET.push(url) #push url into redis set
				yield link
			else:
				continue
												
	
	@classmethod
	def urlItem(cls, link_anchor,purl):
		item = UrlItem()
		item['url'] = link_anchor[0]
		item['purl'] = purl		
		item['depth'] = cls.url_depth(link_anchor[0])	
		item['priority'] = cls.url_priority(link_anchor)
		item['anchor'] = link_anchor[1]
		item['time'] = timestamp()
		return item		
		
	@classmethod	
	def url_priority(cls, link_anchor):
		return 0		
	
	@classmethod
	def url_todo(cls, html, purl=None, domain_control=False):		
		print 'url to do '
		if urlparse.urlparse(purl)[2]=='':
			purl = purl+'/'			
  	
		#generate UrlItem		
		for i in cls.url_filter(html, domain_control, purl):			
			item = cls.urlItem(i, purl)			
			cls.urlItem_redis_save(item)
			yield item
	
			
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
			Logger.error(e)
		

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
# 		
# 		for i in URL_ITEM_UNV_SET.get_all():
# 			url = i['url']
# 			if i['anchor']:
# 				anchor = i['anchor']
# 			else:
# 				anchor = ''			
# 			fw.write(url+' | '+anchor+'\n')
	with open(HMTL_DIR+'f61f4ea5ee707b91415dc0e4715dc825389614fe.html','r') as fr:
		html = fr.read()
	Url.url_filter(html, 'www.baidu.com')
	Url.url_todo(html, purl='www.baidu.com')	
# 	urlItem_read()
# 	print Url.url_depth('www.google.com')
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	