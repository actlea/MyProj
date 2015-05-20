# -*- coding: utf-8 -*-
# actlea  2015-05-20

import sys
sys.path.append('..')

from items import UrlItem,PageItem

import time
import urlparse
from pybloom import BloomFilter
from hashlib import sha256
import lxml.html

from config import *

global IGNORE_EXT #url后缀过滤
global PROTOCOL
global Depth_Table


reload(sys) 
sys.setdefaultencoding('utf-8')


URL_UNVISITED_SET = BloomFilter(capacity=1000, error_rate=0.001) #


def timestamp():
	return str(time.strftime("%y-%m-%d %H:%M:%S", time.localtime()))


def url_format(url, base_url):

	#makes absolute links
	url = urlparse.urljoin(base_url, url)
	url_structure = urlparse.urlparse(url)

	scheme=url_structure[0]
	if scheme not in PROTOCOL:
		return ''
	netloc=url_structure[1]
	if netloc=='':
		url = url+'/'
	return url

def url_depth(url):
	#get pur depth
	key = url_hashcode(purl)
	depth=0
	if Depth_Table.has_key(key):
		depth = Depth_Table[key]+1
	return depth

#ll is list
def ext(ll):
	try:
		return ll[0]
	except IndexError:
		return ''
def anchor_format(anchor):
	

def extract_urlItem(html_content, purl):
		#
		if urlparse.urlparse(purl)[2]=='':
			purl = purl+'/'
		url_bloom=BloomFilter(capacity=1000, error_rate=0.001)		
		urlItem_list=[]

		hxs = lxml.html.fromstring(html_content)
		a_tags = hxs.xpath('//a')

		#all url depth
		depth = url_depth(purl)+1

		for a in a_tags:
			link = a.xpath('./@href') 
			link = ext(link)			
			anchor_text= a.xpath('./text()')
			anchor_text = ext(anchor_text)

			link = url_format(link, purl)
			flag = URL_UNVISITED_SET.add(link)
			if not flag:
				urlItem_list.append( UrlItem(url=link, purl=purl,
					time=timestamp(), depth=depth, priority=0,
					anchor=anchor_text) )
		with open('333','w') as fw:
			for i in urlItem_list:
				fw.write(i['url']+'|'+i['purl']+'|'+i['anchor']+'|'+str(i['depth'])+'\n')



def url_hashcode(url):
	code=None
	if type(url)==unicode:
		code = sha256(url.encode('utf-8')).hexdigest()
	else:
		code = sha256(url.__str__()).hexdigest()
	int_code = int(code, 16)
	return int_code


def url_priority(urlItem):
	pass



if __name__ == '__main__':
	html_content = ''
	link_list = []
	with open('2.html', 'r') as fr:
		html_content = fr.read()

	with open('222.txt', 'r') as f:
		for link in f.readlines():
			link_list.append(link)

	purl='http://www.hupu.com/'
	extract_urlItem(html_content, purl)
	