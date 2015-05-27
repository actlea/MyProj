# -*- coding: utf-8 -*-
# actlea  2015-05-21

   
'''
数据库操作
'''
import redis

import redis
import sys
import MySQLdb
import time
from scrapy.utils.request import request_fingerprint

global url_maps
url_maps = {}


def getRedis(db=0):
    return redis.StrictRedis(host='localhost', port=6379, db=db)

def getMysql():
    return MySQLdb.connect(host='localhost',\
            user='root',passwd='zjm',db="spider_db",port=3306,charset="utf8")

def get_Maps(cfg='./maps.cfg'):
    map_file = open(cfg, "r")
    str = map_file.read()
    map_file.close()
    try:
        d = eval(str)
    except:
        print 'The Maps config is error! Please check it.'
        sys.exit()
    return d    

    
 

from scrapy_redis.dupefilter import RFPDupeFilter
import os
from scrapy.http import Request
# allow test settings from environment
REDIS_HOST = os.environ.get('REDIST_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

   
# 检查request是否重复 

class DupeFilterTest():   

    def __init__(self):
        self.setUp()
        
    def setUp(self):
        self.server = redis.Redis(REDIS_HOST, REDIS_PORT)
        self.key = 'Fcrawler:requests:dupefilter:'
        self.df = RFPDupeFilter(self.server, self.key) 
        
    def tearDown(self):
        self.server.delete(self.key)

    def test_dupe_filter(self, url):
        req = Request(url)      
        flag = self.df.request_seen(req)

        self.df.close('nothing')
        
        return flag



        
        
       
       
        
        
   
        
    
    