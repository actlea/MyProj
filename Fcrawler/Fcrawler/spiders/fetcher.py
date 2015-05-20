# -*- coding: utf-8 -*-
# actlea  2015-05-18

import sys
sys.path.append('..')

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

from Fcrawler.items import UrlItem,PageItem

import time
import urlparse
from pybloom import BloomFilter
from hashlib import sha256

def timestamp():
	return str(time.strftime("%y-%m-%d %H:%M:%S", time.localtime()))


Depth_Table={}  #store url depth, url hashcode as key, url depth as value


from pybloom import BloomFilter #存储已经有的URL
URL_UNVISITED_SET = BloomFilter(capacity=1000, error_rate=0.001) #


class HupuSpider(CrawlSpider):
	name = 'hupu'
	start_urls = ['http://www.hupu.com/']
	allowed_domains = ['hupu.com']

	#set depth
	for link in start_urls:
		Depth_Table[ url_hashcode(link)]=0

	link_extractor = SgmlLinkExtractor(allow_domains=(allowed_domains))


	def parse(self, response):
		
			link_list.append(link.url)
			yield Request(link.url, callback=self.parse)


	def parse_html(self, response):
		hxs = Selector(response)
		purl = response.url
		time = timestamp()

		pageItem = PageItem()
		pageItem['title'] = hxs.select('//head/title/text()').extract()
		pageItem['header']  = response.headers
		pageItem['time'] = time
		pageItem['original_url'] = purl
		pageItem['priority'] = 0
		pageItem['links'] = extract_links(response)


	def extract_urlItem(self, response):
		#		
		url_bloom=BloomFilter(capacity=1000, error_rate=0.001)

		#link list get by SgmlLinkExtractor
		link_list = self.link_extractor.extract_links(response)
		for link in link_list:
			url_bloom.add(link)
		
		urlItem_list=[] 

		purl = response.url
		hxs = Selector(response)
		links = hxs.select('//a')

		#get pur depth
		key = url_hashcode(pur)
		depth = Depth_Table[key]+1

		for link in links:
			anchor_text = ''.join(link.select('./text()')).extract())
			url = ''.join(link.select('./@href')).extract())
			url_structure = urlparse.urlparse(url)			
			if netoc=='':
				url=purl+url
			if path =='':
				url = url+'/'

			flag = url_bloom.add(url)

			#if url in link_list
			if flag:
				urlItem_list.append( UrlItem(url=url, purl=purl,
					time=timestamp(), depth=depth, priority=0) )

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



			







