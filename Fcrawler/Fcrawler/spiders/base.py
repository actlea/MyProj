# -*- coding: utf-8 -*-
# actlea  2015-05-20

#ref: https://github.com/weizetao/spider-roach/blob/master/base.py#L110

import sys
sys.path.append('..')



global url_map
url_map = {}

'''
解析我们配置的地图
'''

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


class MapParse():
	html = None
	item = {}

	html = None
    item = {}
    
    def findrules(self,url):
        """Return the corresponding selection rules"""
        for k,v in url_maps.items():
            if re.match(k, url):
                return v
        return None

    def add_xpath2(self, name, xpath, split='|'):
        self.item[name] = '0'
        tmp = self.html.xpath(xpath)
        if not tmp:
            return False
        str = ''
        rlen = len(tmp)
        for i in range(0,rlen-1):
            temp = tmp[i].rstrip().lstrip()
            if not temp: continue
            str += temp + split
        str += tmp[rlen-1].rstrip().lstrip()
        self.item[name] = str
        return True

    def add_xpath(self, name, xpath):
        self.item[name] = ' '
        tmp = self.html.xpath(xpath)
        if tmp:
            self.item[name] = tmp[0].rstrip().lstrip()
        else:
            return False
        return True

    def get_id(self, url, str):
        pos = url.find(str) + len(str) 
        url_len = len(url)
        pos_end = pos
        while pos_end < url_len:
            if url[pos_end].isdigit():
                pos_end += 1
                continue
            else:
                break
        if pos > 0 and pos_end > pos:
            return url[pos:pos_end]
        else:
            return '0'
    
