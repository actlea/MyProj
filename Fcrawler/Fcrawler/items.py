# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

# actlea  2015-05-18


from scrapy.item import Item, Field


class FcrawlerItem(Item):
	pass


class UrlItem(Item):
	url = Field()
	purl = Field()		# purl link to url
	time = Field()	
	depth = Field()
	priority = Field()
	anchor = Field()
	

def urlitem(url, purl, time, depth, priority, anchor):
	item = UrlItem()
	item['url'] = url
	item['purl'] = purl
	item['time'] = time
	item['depth'] = depth
	item['priority'] = priority
	item['anchor'] = anchor
	return item



class PageItem(Item):
	original_url = Field()	
	time = Field()
	depth = Field()
	content = Field()
	header = Field()
	priority = Field()
	title = Field()
	encode = Field()
	
def pageitem(original_url, time, depth, content, priority,title='', encode='',header={}):
	item = PageItem()
	item['original_url'] = original_url
	item['content'] = content #must be xml_content
	item['time'] = time
	item['depth'] = depth
	item['priority'] = priority
	item['header'] = header
	item['title'] = title
	item['encode']=encode


























