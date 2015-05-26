# -*- coding: utf-8 -*-
# actlea  2015-05-18

import sys
sys.path.append('..')

# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector

import time
from scrapy_redis.spiders import RedisSpider

# our own define 
import Utility 
from Fcrawler.items  import UrlItem, PageItem
from util import Item_extract


reload(sys) 
sys.setdefaultencoding('utf-8')  # @UndefinedVariable

def timestamp():
	return str(time.strftime("%y-%m-%d %H:%M:%S", time.localtime()))


''' 虎扑体育'''
class HupuSpider(CrawlSpider):
	name = 'hupu'
	start_urls = ['http://www.hupu.com/']

	def parse(self, response):	
			print 'parse start'	
			try:
				html = response.body
				purl = response.url
				headers = response.header
				link_list, pItem = Item_extract(html,purl)
				
				
			except:
				print 'error'
			# yield Request(link.url, callback=self.parse)


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
		

		#link list get by SgmlLinkExtractor
		#link_list = self.link_extractor.extract_links(response)









