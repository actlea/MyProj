# -*- coding: utf-8 -*-
# actlea  2015-05-20

import sys
sys.path.append('..')

from pybloom import ScalableBloomFilter
import random
from Utility import DupeFilterTest,Redis_Set, Redis_Priority_Set, Hash_Set



#url后缀过滤
IGNORE_EXT = ('js','css','png','jpg','gif','bmp','svg','exif',\
            'jpeg','exe','doc','docx','ppt','pptx','pdf','ico',\
            'wmv','avi','swf','apk','xml','xls','thmx','py')

#过滤netloc部分的关键字
IGNORE_KEYWORD=('comment', 'game', 'app', 'money', 'finance','sax','vip', 'stock','help','ka', 'auto',\
                'caipiao','ask','baby','astro','edu')
KEYWORD=('nba','soccer','sport','cba')

PROTOCOL = ('http', 'ftp','https')

CRAWL_DEPTH=5

#dir path
DIR = '/opt/Work/java_workspace/Fcrawler/Fcrawler/data/'
HMTL_DIR = DIR+'HTML/source/'
HTML_TEXT_DIR = DIR+'HTML/text/'
SCRAPY_LOG = '/opt/Work/java_workspace/Fcrawler/scrapy_log.log'     #scrapy log file

#redis set, hset, zset
Depth_Hash_Table = Hash_Set('url_depth')
URL_UNVISITED_SET = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH) 
URL_UNVISITED_RSET = Redis_Set('url_unvisited')                                     #url_unvisited_set
URL_ITEM_UNV_SET = Redis_Priority_Set('urlItem_unvisited')                          #urlitem_unvisited_set, url sorted by priority                                          
URL_VISITED_HSET = Hash_Set('url_visited')                                          #url hash been visited
HTML_FETCH_SET =  Redis_Set('HTML_TABLE')                                           #store html hashcode


ENCODING=('utf-8', 'GB2312', 'ISO-8859-2','GBK')
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









