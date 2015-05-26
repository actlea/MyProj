# -*- coding: utf-8 -*-
# actlea  2015-05-20

#ref: https://github.com/weizetao/spider-roach/blob/master/base.py#L110

import sys
from twisted.python import urlpath
sys.path.append('..')

import re

reload(sys) 
sys.setdefaultencoding('utf-8')  # @UndefinedVariable

global url_maps
url_maps = {}


'''
生成规则
'''
def map_read(cfg='map.cfg'):
	with open(cfg, 'r') as fr:
		content = fr.read()
		try:
			d = eval(content)
		except:
			print 'The Maps config is error! Please check it.'
			sys.exit()
    	return d
    
class RuleParse():
	html = None #html是lxml.html.fromstring生成的对象
	item = {}
	
	def findrules(self, url):       
        #url_maps is string from file
        for k,v in url_maps.items():
            if re.match(k, url):
                return v
        return None
	
    def add_xpath(self, name, xpath, split='|'):
    	'''
    	Args:
    		name:一般是你定义的key，比如title, anchor
    		xpath:在map中定义的xpath规则
    	'''
    	tmp = self.html.xpath(xpath) # tmp is a list
    	if not tmp:
    		return False
    	str = ''
    	rlen = len(tmp) #tmp has rlen element

    	for i in range(rlen-1):
    		temp = tmp[i].rstrip().lstrip()
    		if not temp: continue
    		str += temp + split
    	str += tmp[rlen-1].rstrip().lstrip()
    	self.item[name] = str
    	return True







