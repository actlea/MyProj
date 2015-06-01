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
from url import Url
from Utility import Redis_Set

global Depth_Table
global HMTL_DIR
MAX_PAGE = 200
count=0



reload(sys) 
sys.setdefaultencoding('utf-8')  # @UndefinedVariable

def timestamp():
	return str(time.strftime("%m%d%H%M%S", time.localtime()))


''' 虎扑体育'''
class HupuSpider(CrawlSpider):
	name = 'hupu'
	start_urls = ['http://www.hupu.com/',]	

	def parse(self, response):	
		global count
		
		try:
			
			html = response.body
			purl = response.url	
			with open(HMTL_DIR+timestamp(), 'w') as fw:
				fw.write(html)	
			URL_Visited_SET.push(purl)
					
			count+=1
			if count>=MAX_PAGE:
				return
			
			for url in Url.url_todo(html, purl):
				try:					
					yield Request(url['url'], callback=self.parse)	
				except:
					continue						
				
		except : 
			print 'parse error'
		










