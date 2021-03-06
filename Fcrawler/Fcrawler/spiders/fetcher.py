# -*- coding: utf-8 -*-
# actlea  2015-05-18

import sys
sys.path.append('..')

# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
import time
from scrapy import log


# our own define 
import Utility 
from Fcrawler.items  import FetchItem
from config import *
from stringHelper import Logger
from Utility import DupeFilterTest



global UrlItem_UNV_Set

MAX_PAGE = 200
count=0



reload(sys) 
sys.setdefaultencoding('utf-8')  # @UndefinedVariable

log.start(logfile=SCRAPY_LOG, loglevel=log.DEBUG, logstdout=True)


''' 虎扑体育'''
class HupuSpider(CrawlSpider):
	name = 'hupu'
	start_urls = ['http://www.hupu.com/',
				'http://sports.sina.com.cn/',
				'http://sports.sina.com.cn/g/championsleague/',
				'http://sports.qq.com/',
				'http://sports.sohu.com/',
				'http://sports.ifeng.com/',
				'http://match.sports.sina.com.cn/index.html',
				'http://live.sports.ifeng.com/index.shtml'				
				]
		

	def parse(self, response):	
		global count		
		try:
			try:
				item = FetchItem()
				item['response']=response
				Logger.info(response.url+'  download')
				yield item		
			except:
				Logger.error('parse url error')			
					
			count+=1
			if count>=MAX_PAGE:
				return
			
# 			for url in Url.url_todo(html, purl):
			while not URL_ITEM_UNV_SET.isempty():				
# 				url = URL_UNVISITED_RSET.pop()
				url = URL_ITEM_UNV_SET.pop()['url']
				Logger.info('url:'+url+'.'*20)							
				try:
					request_dup = DupeFilterTest()
					flag = request_dup.request_dupe_filter(url)	
					if not flag:				
						yield Request(url, callback=self.parse)	
				except:
					continue
		except : 
			Logger.error('parse error')
		










