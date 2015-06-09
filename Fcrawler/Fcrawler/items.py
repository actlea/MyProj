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
	

class PageItem(Item):
	original_url = Field()	
	time = Field()	
	content = Field()
# 	header = Field()
	priority = Field()	
	hash = Field()
	main_text = Field()
	


class FetchItem(Item):
# 	original_url = Field()	
# 	content = Field()
# 	header = Field()
# 	meta = Field()		
# 	encode = Field()
	response = Field()























