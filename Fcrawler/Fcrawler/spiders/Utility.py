# -*- coding: utf-8 -*-
# actlea  2015-05-21

  

import redis
import sys
import MySQLdb
import time
from scrapy.utils.request import request_fingerprint
from scrapy_redis.queue import Base
from scrapy_redis.dupefilter import RFPDupeFilter
import os
from scrapy.http import Request
import pickle



def getRedis(db=0):
    return redis.StrictRedis(host='localhost', port=6379, db=db)

def getMysql():
    return MySQLdb.connect(host='localhost',\
            user='root',passwd='zjm',db="spider_db",port=3306,charset="utf8")
    
 

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

    def request_dupe_filter(self, url):
        req = Request(url)      
        flag = self.df.request_seen(req)

        self.df.close('nothing')
        
        return flag



class Redis_Set(Base):
    def __init__(self, name):
        self.server = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
        self.key = 'Fcrawler:%s:set' %name
    
    def __len__(self):
        return self.server.scard(self.key)
    
    
    def _encode_(self, val):
        """Encode a val object"""
        return pickle.dumps(val, protocol=-1)
    
    def _decode_(self, val):
        return pickle.loads(val)
        
    def push(self, val):
        '''if val in set, return false, esle return true'''
        if isinstance(val, dict):
            flag = self.server.sadd(self.key, self._encode_(val))
        else:
            flag = self.server.sadd(self.key, val)
        return flag
    
    def pop(self):
        '''delete and return a number from set'''
        data = self.server.spop(self.key)
        if isinstance(data, dict):
            return self._decode_(data)
        return data
    
    def get_all(self, mode=True):
        '''Return Set, if mode=True, then use in URL_SET,else use in URL_ITEM_SET '''
        if mode:
            data = self.server.smembers(self.key)
        
        return data
        
        
    def isempty(self):
        len = self.server.scard(self.key)
        return len==0
    
        
    
class Redis_Priority_Set(Base):
        def __init__(self, name):
            self.server = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
            self.key = 'Fcrawler:%s:set' %name
        
        def __len__(self):
            return self.server.zcard(self.key)
        
        def _encode_(self, urlItem):           
            data = pickle.dumps(urlItem, protocol=-1)
            return data
        
        def _decode_(self, data):
            d = pickle.loads(data)
            return d  
           
        def get_all(self, mode=True):
            '''Return Set, if mode=True, then use in URL_SET,else use in URL_ITEM_SET '''
           
            results = self.server.zrange(self.key, 0, -1) 
            data=[]
            if results:
                for i in results:
                    yield self._decode_(i)
                                   
            
    
        def push(self, urlItem):
            data = self._encode_(urlItem)            
            pairs = {data: urlItem['priority']}
            self.server.zadd(self.key, **pairs)
        
        def pop(self, timeout=0):
            """
            Pop a request
            timeout not support in this queue class
            """
            # use atomic range/remove using multi/exec
            pipe = self.server.pipeline()
            pipe.multi()
            pipe.zrange(self.key, 0, 0).zremrangebyrank(self.key, 0, 0)
            results, count = pipe.execute()
            if results:
                return self._decode_(results[0])
            

    
    
if __name__=='__main__':
     from config import *
     res = URL_ITEM_UNV_SET.get_all()
     print res
     
     
        
        
       
       
        
        
   
        
    
    