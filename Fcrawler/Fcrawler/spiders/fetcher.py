# -*- coding: utf-8 -*-
# actlea  2015-05-18

import sys
sys.path.append('..')

# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
import time
import logging
import os

# our own define 
import Utility 
from Fcrawler.items  import FetchItem
from config import *
from stringHelper import Logger




global UrlItem_UNV_Set

MAX_PAGE = 200
count=0



reload(sys) 
sys.setdefaultencoding('utf-8')  # @UndefinedVariable


#log init
FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(filename = os.path.join(os.getcwd(), 'log.txt'), level = logging.DEBUG, format=FORMAT)


''' 虎扑体育'''
class HupuSpider(CrawlSpider):
	name = 'hupu'
	start_urls = ['http://www.hupu.com/',
				'http://sports.sina.com.cn/']	

	def parse(self, response):	
		global count
		
		try:		
			Logger.log_high('hupu spider start'+'.'*20)
			
			try:
				item = FetchItem()
				item['content'] = response.body
				item['original_url'] = response.url
				Logger.log_normal(response.url+'  download')
	# 			item['header'] = response.headers
	# 			item['meta'] = response.meta
	# 			item['encode'] = response.encoding
				yield item		
			except:
				Logger.log_fail('parse url error')			
					
			count+=1
			if count>=MAX_PAGE:
				return
			
# 			for url in Url.url_todo(html, purl):
			while not URL_UNVISITED_RSET.isempty():				
				url = URL_UNVISITED_RSET.pop()
				Logger.log_high('url:'+url+'.'*20)							
				try:					
					yield Request(url, callback=self.parse)	
				except:
					continue						
				
		except : 
			Logger.log_fail('parse error')
		










