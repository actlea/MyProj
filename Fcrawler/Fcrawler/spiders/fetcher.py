# -*- coding: utf-8 -*-
# actlea  2015-05-18

import sys
sys.path.append('..')

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule


# from Fcrawler.items import UrlItem,PageItem
from items import UrlItem,PageItem
from util import *

reload(sys) 
sys.setdefaultencoding('utf-8')

global Depth_Table

class HupuSpider(CrawlSpider):
	name = 'hupu'
	start_urls = ['http://www.hupu.com/']
	allowed_domains = ['hupu.com']

	#set depth
	for link in start_urls:
		Depth_Table[ url_hashcode(link)]=0

	link_extractor = SgmlLinkExtractor(allow_domains=(allowed_domains))


	def parse(self, response):		
			try:
				with open('1111', 'w') as fw:
					fw.write(response.body)

				link_list = []
				for link in self.link_extractor.extract_links(response):
					link_list.append(link.url)
				with open('2222','a') as fw2:
					for link in link_list:
						fw2.write(link+'\n')
			except Exception,e:
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











