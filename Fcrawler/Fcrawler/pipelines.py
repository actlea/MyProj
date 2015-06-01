# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys

reload(sys) 
sys.setdefaultencoding('utf-8')  # @UndefinedVariable

from Fcrawler.spiders.url import Url
from Fcrawler.spiders.config import *
from Fcrawler.spiders.stringHelper import *

import logging

global HMTL_DIR


def timestamp():
    return str(time.strftime("%m%d%H%M%S", time.localtime()))

class FcrawlerPipeline(object):
#     def process_item(self, item, spider):
#         return item

    def process_item(self, item, spider):
        logging.info('process_item()')
        html = item['content']
        base_url = item['original_url']        
       
        
        #parse url and filter url
        Url.url_todo(html, base_url)
            
        with open(HMTL_DIR+timestamp()+'.html', 'wb') as fw:
            fw.write(html)    
        URL_VISITED_SET.push(base_url)
        
        
        

