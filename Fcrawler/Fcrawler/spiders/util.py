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
	path=url_structure[2]
	if path=='':
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

#去除多余的空格
def blank_delete(text):
	try:
		return ''.join(text.split())
	except Exception:
		return text

def url_domain_control(url, purl):
	url_d = urlparse.urlparse(url)[1]
	purl_d = urlparse.urlparse(purl)[1]

	urll=url_d.split('.')
	purll = purl_d.split('.')
	if urll[-1]==purll[-1] and urll[-2]==purll[-2]:
		return True
	else:
		return False



def Item_extract(html_content, purl, domain_control=True):
		'''extract UrlItem and PageItem
		Args:
			html_content: content of html
			purl: url link to html
			domain_control: whether use domain control

		Returns:
			UrlItem and PageItem
		'''
		if urlparse.urlparse(purl)[2]=='':
			purl = purl+'/'
		url_bloom=BloomFilter(capacity=1000, error_rate=0.001)	
		url_bloom.add(purl)	

		urlItem_list=[]

		hxs = lxml.html.fromstring(html_content)
		a_tags = hxs.xpath('//a')

		#all url depth
		depth = url_depth(purl)+1

		for a in a_tags:
			link = a.xpath('./@href') 
			link = blank_delete (ext(link))	
			if domain_control and not url_domain_control(link, purl):
				continue

			anchor_text= a.xpath('./text()')
			anchor_text = blank_delete( ext(anchor_text))

			link = url_format(link, purl)
			flag = URL_UNVISITED_SET.add(link)
			if not flag:
				urlItem_list.append( UrlItem(url=link, purl=purl,
					time=timestamp(), depth=depth, priority=0,
					anchor=anchor_text) )

		# with open('333','w') as fw:
		# 	for i in urlItem_list:
		# 		# fw.write(i['url']+'|'+i['purl']+'|'+i['anchor']+'|'+str(i['depth'])+'\n')
		# 		fw.write(i['url']+'\n')

		############extract PageItem#####################
		title = blank_delete( ext(hxs.xpath('//title/text()')) )
		encode = blank_delete( ext( hxs.xpath('//meta/@charset')) )


		print '%s, %s' %(title, encode)





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
	with open('1111', 'r') as fr:
		html_content = fr.read()

	purl='http://www.hupu.com/'
	Item_extract(html_content, purl)
	