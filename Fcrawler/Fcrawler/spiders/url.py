# -*- coding: utf-8 -*-
# actlea  2015-05-20

import sys
sys.path.append('..')

from Fcrawler.items import urlitem,pageitem,UrlItem,PageItem
from Utility import DupeFilterTest

import time
import urlparse
from pybloom import BloomFilter
from hashlib import sha256
import lxml.html

from config import *

global IGNORE_EXT 	#url后缀过滤
global PROTOCOL
global Depth_Table	#depth table


reload(sys) 
sys.setdefaultencoding('utf-8')


URL_UNVISITED_SET = BloomFilter(capacity=1000, error_rate=0.001) #



def timestamp():
	return str(time.strftime("%y-%m-%d %H:%M:%S", time.localtime()))


#ll is list
def ext(ll):
	try:
		return ll[0]
	except IndexError:
		return ''

#去除多余的空格
def blank_delete(text):
	try:
		return ''.join(text.split())
	except Exception:
		return text


def text_format(text):
	if text:
		return blank_delete (ext(text))
	else:
		return text	
	
class Url:
				
	@classmethod
	def url_absolute(cls, url, base_url):
		#makes absolute links
		res = urlparse.urljoin(base_url, url)
		print res
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
		depth = cls.url_depth(url)
		key = url_hashcode(url)
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
		
		if depth > CRAWL_DEPTH:
			return False
		
		#add depth to Depth_Table
		cls.add_depth(url)
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
		
		#request filter
		request_dup = DupeFilterTest()
		flag = flag and request_dup.test_dupe_filter(url)
		return not flag
		
	
	@classmethod
	def url_filter(cls, link_anchor_list, domain_filter=True, base_url=''):
		
		fi_link_anchor_list=[]
		
		for link in link_anchor_list:
			url = link[0]
			#domain filter
			domain_flag =  domain_filter and cls.url_domain_control(url, base_url)
			depth_flag = cls.url_depth_control(url)
			dup_flag = cls.url_dup_filter(url)
			
			if domain_flag and depth_flag and not dup_flag:
				fi_link_anchor_list.append( link )
				
		return fi_link_anchor_list			
												
	
	@classmethod
	def urlItem(cls, link_anchor,purl):
		item = UrlItem
		item['url'] = link_anchor[0]
		item['purl'] = purl
		item['time'] = timestamp()
		item['depth'] = cls.url_depth(purl)+1		
		item['priority'] = cls.url_priority(link_anchor)
		item['anchor'] = link_anchor[1]
		return item		
		
	@classmethod	
	def url_priority(cls, link_anchor):
		return 0		
	
	
	@classmethod
	def urlItem_save(cls, urlItem_list):
		file = 'url_%s' %(timestamp())
		with open(file, 'w')  as fw:
			for i in urlItem_list:
				tmp = i['url'] + ' | '+ str(i['depth'])+ ' | ' + i['anchor']+'\n'
				fw.write(tmp)
			
	@classmethod
	def url_todo(cls, html, purl, domain_control=True):
		#
		if urlparse.urlparse(purl)[2]=='':
			purl = purl+'/'		
		
		#all url has been format
		link_anchor_list = cls.url_extract(html, purl)
		
		#url filter
		link_anchor_list = cls.url_filter(link_anchor_list, domain_control, purl)
		
		#generate UrlItem
		urlitem_list=[]
		for i in link_anchor_list:			
			item = cls.urlItem(i, purl)			
			urlitem_list.append(item)
		
		#save file
		cls.urlItem_save(urlitem_list)
	

class Html:
	def __init__(self, html, base_url):
		self.html = html
		self.base_url = base_url
		self.hxs = hxs = lxml.html.fromstring(html)
	
	def parse(self):
		title = blank_delete( ext(self.hxs.xpath('//title/text()')) )
		encode = blank_delete( ext( self.hxs.xpath('//meta/@charset')) )
		



def page_priority(html_content):
	return 0



def url_hashcode(url):
	code=None
	if type(url)==unicode:
		code = sha256(url.encode('utf-8')).hexdigest()
	else:
		code = sha256(url.__str__()).hexdigest()
	int_code = int(code, 16)
	return int_code


def url_priority(urlItem):
	pass



if __name__ == '__main__':
	html_content = ''
	link_list = []
	with open('111', 'r') as fr:
		html_content = fr.read()

	purl='http://www.hupu.com/'
	Url.url_todo(html_content, purl)
	