# -*- coding: utf-8 -*-
# actlea  2015-05-18

import sys
sys.path.append('..')

# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
import time
from scrapy_redis.spiders import RedisSpider

# our own define 
import Utility 
from Fcrawler.items  import UrlItem, PageItem
from config import *

global Depth_Table


reload(sys) 
sys.setdefaultencoding('utf-8')  # @UndefinedVariable

def timestamp():
	return str(time.strftime("%y-%m-%d %H:%M:%S", time.localtime()))


''' 虎扑体育'''
class HupuSpider(CrawlSpider):
	name = 'hupu'
	start_urls = ['http://www.hupu.com/',]
	
	

	def parse(self, response):	
			print 'parse start'	
			try:
				
				html = response.body
				purl = response.url		
				
				
				with open('111', 'w') as fw:
					fw.write(html)
				
			
# 				link_list, pItem = Item_extract(html,purl)
				link_list=[]
				pItem={}
				pItem['header']=response.header
				for url in link_list:
					print '%s start fetch' %(url)
					yield Request(url['url'], callback=self.parse)		
				
				yield pItem
				yield link_list	
				
			except Exception,e: 
				print 'parse error'
		










