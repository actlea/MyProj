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

class PageItem(Item):
	original_url = Field()
	links = Field()
	time = Field()
	depth = Field()
	content = Field()
	header = Field()
	priority = Field()
	title = Field()



