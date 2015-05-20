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
	# def __init__(self, url, purl, time, depth, priority, anchor):
	# 	self.url = url
	# 	self.purl = purl
	# 	self.time = time
	# 	self.depth = depth
	# 	self.priority = priority
	# 	self.anchor = anchor

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

	# def __init__(self, original_url, time, depth, content, header, priority,title):
	# 	self.original_url = original_url
	# 	self.time = time
	# 	self.depth = depth
	# 	self.content = content
	# 	self.header = header
	# 	self.priority = priority
	# 	self.title = title
def pageitem(original_url, time, depth, content, header, priority,title):
	item = PageItem()
	item['original_url'] = original_url
	item['content'] = content
	item['time'] = time
	item['depth'] = depth
	item['priority'] = priority
	item['header'] = header
	item['title'] = title


