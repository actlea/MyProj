# -*- coding: utf-8 -*-
'''
Created on May 27, 2015

@author: root
'''
import lxml.html
from stringHelper import *
import sys
import os
import jieba
import jieba.analyse
import re
import HTMLParser
import pickle

from config import *


from Fcrawler.items import PageItem
reload(sys) 
sys.setdefaultencoding('utf-8')  # @UndefinedVariable

Punctuation = "[！，。？：、]+"
USERDICT = DIR+'dict.txt'
NBA_DICT = DIR+'nba.txt'
HTML_DIR = DIR+'HTML/'

def stopwords(file):
    if os.path.exists('/opt/data/stopwords.dict'):
        pass
    
class Word:
    def __init__(self,sentence):
        self.sentence = sentence.decode('utf-8')  
        self.words = []
        jieba.load_userdict(USERDICT)
    
    def pucn_delete(self):
        '''replace Punctuation with NULL'''
        return re.sub(Punctuation.decode('utf-8'), "", self.sentence)   
    
    #搜索引擎模式
    def searchWord(self):
        self.sentence = self.pucn_delete()
        word_list = jieba.cut_for_search(self.sentence)
        
        self.words = ' '.join(word_list) 
        print self.words
    
    #精确模式
    def preciseWord(self):
        self.sentence = self.pucn_delete()
        word_list = jieba.cut(self.sentence, cut_all=False)
        
        self.words = ' '.join(word_list) 
        print self.words
    
    #very slow
    def topKWord(self, k=2):
        self.sentence = self.pucn_delete()
        tags = jieba.analyse.extract_tags(self.sentence, topK=k)
        print ' '.join(tags)
    
    def html_decode(self, sentence):
        h = HTMLParser.HTMLParser()  
        s = h.unescape(sentence)
        return s
    

class Html:
    def __init__(self, name, base_url=''):
        self.html = self.html_content(name)
        self.base_url = base_url
        self.hxs = lxml.html.fromstring(self.html)
    
    def html_content(self, name):
        '''html from file or str'''
        if os.path.exists(HTML_DIR+name):            
            with open(HTML_DIR+name, 'r') as fr:
                content = fr.read()
            return content
        else:
            return name
        
    
        
            
    def getMainText(self): 
        try:      
            text = ''.join(self.hxs.xpath('//a/text() | //p/text() | //span/text() | //h1/text()')).decode('utf-8')
            text = blank_delete(text)
#             print text
            return text
        except:
            print 'getMainText() error'      
        
        
        
    
    def parse(self):
        title = blank_delete( ext(self.hxs.xpath('//title/text()')) )
#         encode = blank_delete( ext( self.hxs.xpath('//meta/@charset')) )
        encode = re.search(r'charset=(.*).', self.html) 
        if encode: encode = encode.group(1)        
       
        #get main text
        main_text = self.getMainText()
        item = PageItem()
        item['original_url'] = self.base_url
        item['content'] = main_text #must be xml_content
        item['time'] = timestamp() 
        item['title'] = title
        item['encode']=encode
        
        d = pickle.dumps(item, protocol=-1)
        return d
    
        
        
    
    def page_score(self, keyword):
        
        pass
    
    
    
    
    
    
    
if __name__=='__main__':
    base_url = 'http://www.hupu.com/'
    with open('333', 'w') as fw:
        for i in os.listdir('../data/HTML'):  
            print i 
            HTML = Html(i, base_url)        
            d = HTML.parse()
            str = HTML.getMainText()
            fw.write(str+'\n')


    
   
    
    
    
    
 
 
 
 
 
 
 
 
 
 
 
 
    
    
    
    
    
    