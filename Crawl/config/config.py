#!/usr/bin/env python
#coding:utf-8
#2015-05-16

import os
import random

from pybloom import BloomFilter #存储已经有的URL

URL_SIMILARY_SET = BloomFilter(capacity=1000, error_rate=0.001) #

'''
参数配置
'''

DOWNLOAD_MODE = 0
'''
下载模式
静态模式    0
动态模式    1
动静模式    2
'''

SIMILARITY = 0 				#控制相似度
FETCH_TIME_INTERVAL = 5 	#抓取时间间隔
FETCH_TIME = 20 			#抓取时间
DEPTH = 5 					#最大爬去深度
FETCH_COUNT=200				#爬取页面的数量
FETCH_MODE=0				#默认使用深度优先爬取 0
THREAD_NUM = 10				#线程数量

HOST_KEYWORD=	['hupu.com']
'''
限定了网址的host部分
'''
URL_KEYWORD = ['nba', 'soccer', 'tennis']
'''
url中的关键字
'''
URL_IGNORE_KEYWORD = ['blog','v.opahnet']
'''
url中不允许出现的关键字
'''
#CUSTOM_KEY = ['home.php','forum.php']

START_URLS = '../data/starturls.txt'
'''
爬虫起始urls
'''



'''
0:深度优先爬取
1:广度优先爬取
2:优先级爬取
3:随机爬取
'''

#url后缀过滤
IGNORE_EXT = ('js','css','png','jpg','gif','bmp','svg','exif',\
            'jpeg','exe','doc','docx','ppt','pptx','pdf','ico',\
            'wmv','avi','swf','apk','xml','xls','thmx','py')

#content_type控制
IGNORE_HEADERS = frozenset([
  'set-cookie',
  'expires',
  'cache-control',

  # Ignore hop-by-hop headers
  'connection',
  'keep-alive',
  'proxy-authenticate',
  'proxy-authorization',
  'te',
  'trailers',
  'transfer-encoding',
  'upgrade',
])

#html类型
TRANSFORMED_CONTENT_TYPES = frozenset([
  "text/html",
  "text/css",
])

PROTOCOL = ('http', 'ftp','https')
'''
不期待文件后缀
'''
SPIDER_PROXY = False
'''
爬虫代理
'''
SPIDER_PROXY_DIC = {}
'''
爬虫代理ip字典
'''



'''
爬虫过滤关键字 字典  PS：列表形式
'''
def set_key_word(key):
    klist = key.split(',')
    return klist

#delete characters not in character_list 
def clean_url(url):
    character_list = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    while url[-1] not in character_list:
        url = url[:-1]
    return url


def format_url(url):
	temp_url = url
	if 'http://' not in url:
		temp_url = 'http://'+url
	# temp_url = clean_url(temp_url)
	return temp_url


def set_start_urls(key):
    '''get url from key
    Args:
    	key: could be file path, url str, ulr list
    Returns:
    	return url list, if url is None, return []
    '''
    #if key is file path
    temp_url_list = []
    if os.path.isfile(str(key)):
    	logging.info('start url from file: %s', key)
    	fp = open(key)    	
    	for line in fp.readlines():
    		if '\r\n' in line:
    			temp_url_list.append(format_url(line[:-2]))
    		elif '\n' in line:
    			temp_url_list.append(format_url(line[:-1]))
    		else:
    			temp_url_list.append(format_url(line))    	
    #if key is url list
    elif str(type(key)) == "<type 'list'>":
    	temp_url_list = key
    elif str(type(key)) == "<type 'str'>":
       	temp_url_list.append(format_url(key))
    else:
    	temp_url_list=[]
    return temp_url_list




#START_URLS = set_start_urls(START_URLS)

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

HEADERS = {'User-Agent':random.choice(USER_AGENTS)}

def random_header():
    return {'User-Agent':random.choice(USER_AGENTS)}



LOG_FILENAME = '../data/logging.log'

import logging
def log_start():
	logging.basicConfig(filename=LOG_FILENAME,
		level=logging.DEBUG
		)

