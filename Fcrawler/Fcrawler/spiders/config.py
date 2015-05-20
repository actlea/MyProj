# -*- coding: utf-8 -*-
# actlea  2015-05-20

import sys
sys.path.append('..')

from pybloom import BloomFilter


#url后缀过滤
IGNORE_EXT = ('js','css','png','jpg','gif','bmp','svg','exif',\
            'jpeg','exe','doc','docx','ppt','pptx','pdf','ico',\
            'wmv','avi','swf','apk','xml','xls','thmx','py')

PROTOCOL = ('http', 'ftp','https')

Depth_Table={}  #store url depth, url hashcode as key, url depth as value

