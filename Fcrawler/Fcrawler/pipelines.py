# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys

reload(sys) 
sys.setdefaultencoding('utf-8')  # @UndefinedVariable

from Fcrawler.spiders.url import Url
from Fcrawler.spiders.html import Html
from Fcrawler.spiders.database import HTML_URL_DB
from Fcrawler.spiders.config import *
from Fcrawler.spiders.stringHelper import *

import chardet

global HMTL_DIR


class FcrawlerPipeline(object):
#     def process_item(self, item, spider):
#         return item

    def process_item(self, item, spider):
        html = item['response'].body
        base_url = item['response'].url  
        encoding = item['response'].encoding
        
          
        #parse url and filter url
#         Url.url_todo(html, base_url)
        
        #parse html use class Html
        HT = Html(html,base_url)
        res = HT.parse()
        html_name = res[0]['hash']
        PH = HTML_URL_DB()
        PH.html_insert(res)
        PH.url_item_insert(html, base_url)
            
        with open(HMTL_DIR+ str(html_name)+'.html', 'wb') as fw:
            fw.write(html)    
          
        URL_VISITED_SET.push(base_url)
        Logger.info(base_url+'..........sucess')
        
        
        

