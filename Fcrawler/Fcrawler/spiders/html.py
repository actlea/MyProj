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

reload(sys) 
sys.setdefaultencoding('utf-8')  # @UndefinedVariable

Punctuation = "[！，。？：、]+"
USERDICT = '../data/dict.txt'
NBA_DICT = '../data/nba.txt'

def stopwords(file):
    if os.path.exists('../data/stopwords.dict'):
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
        
    

class Html:
    def __init__(self, html, base_url):
        self.html = html
        self.base_url = base_url
        self.hxs = lxml.html.fromstring(html)
    
    def getMainText(self):
        text = ''.join(self.hxs.select('a/text() | p/text() | span/text() | h1/text()').extract())
    
    def parse(self):
        title = blank_delete( ext(self.hxs.xpath('//title/text()')) )
        encode = blank_delete( ext( self.hxs.xpath('//meta/@charset')) )
        #get main text
        main_text = self.getMainText(self.html)
    
    def page_score(self, keyword):
        
        pass
    
    
    
    
    
    
    
if __name__=='__main__':
    sent = u'红军 热刺 曼联'    
    word = Word(sent)
    word.searchWord()
    word.preciseWord() 
    
    
    
    
 
 
 
 
 
 
 
 
 
 
 
 
    
    
    
    
    
    