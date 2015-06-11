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
import eatiht.etv2 as etv2
import eatiht.v2 as v2
import chardet
from hashlib import sha1
from config import *
   
import chardet
import codecs


from Fcrawler.items import PageItem
reload(sys) 
sys.setdefaultencoding('utf-8')  # @UndefinedVariable

Punctuation = "[！，。？：、]+"
USERDICT = DIR+'dict.txt'
NBA_DICT = DIR+'nba.txt'


# decided to use backslashes for readability?
TEXT_FINDER_XPATH = '//body\
                        //*[not(\
                            self::script or \
                            self::noscript or \
                            self::style or \
                            self::i or \
                            self::b or \
                            self::strong or \
                            self::span or \
                            self::a)] \
                            /text()[string-length(normalize-space()) > 20]/..'



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
    def __init__(self, filelike_or_str, base_url='null'):
        self.html = self.html_content(filelike_or_str)               
        self.base_url = base_url
        
    def html_content(self, filelike_or_str):
        '''html from file or str'''
        if os.path.exists(HMTL_DIR+filelike_or_str):            
            with open(HMTL_DIR+filelike_or_str, 'r') as fr:
                content = fr.read()           
            return content
        else:           
            return filelike_or_str         
            
    def get_text(self):
        '''get html text without html tag'''
        try:
            text = ''.join(self.hxs.xpath('//a/text() | //p/text() | //span/text() | //h1/text() | //div/text()'))
            text = blank_delete(text)
            return text 
        except Exception,e:
            Logger.error(e)
            return None       
        
        
        
    def parse(self):        
        self.html, encode = encode_to_utf8(self.html)
        self.hxs = lxml.html.fromstring(self.html)
        title = blank_delete( ext(self.hxs.xpath('//title/text()')) ) 
        
        main_text = None
        try:
            main_text = blank_delete(get_main_text(self.html, encode))            
        except Exception,e:
            Logger.error(self.base_url+' error......')
            Logger.error(e) 
        if main_text is None:
            main_text = self.get_text()            
                    
        #hash html
        fp = sha1()
        fp.update(self.base_url)
        fp.update(self.html)
        hash_code = fp.hexdigest() 
        
        item = PageItem()
        item['original_url'] = self.base_url
        item['priority'] = 0        
        item['main_text'] = main_text
        item['hash'] = hash_code 
        item['encode']=encode                
        item['time'] = timestamp() 
            
        return (item, HTML_FETCH_SET.push(hash_code) ) 


#text is html document
def encode_to_utf8(text):
    stru = chardet.detect(text)
    precise = stru['confidence']
    encode1 = stru['encoding']
    encode2 = '' 
    charset = re.search(r'charset=(.*).', text)
    tmp = text
    if charset is not None:
        charset = charset.group(1)
        for i in ENCODING:
            if match(i, charset):
                encode2=i
                break
    if encode2=='':
        encode = encode1
    elif match(encode1, encode2):
        encode = encode1
    elif precise>0.9:  # @IndentOk
        encode = encode1
    else:
        encode = encode2     
    try: 
        if not match(encode, 'utf-8'):    
            text = text.decode(encode).encode('utf-8') 
    except Exception,e:
        print e
          
    return text,encode
    


def extract(htmlstring_or_filelike, encoding=None):                  
    if os.path.exists(HMTL_DIR+htmlstring_or_filelike):
        fr = open(HMTL_DIR+htmlstring_or_filelike, 'r')
        return etv2.extract(fr,encoding)
    else:
        return etv2.extract(htmlstring_or_filelike, encoding)               

def exract_v2(htmlstring_or_filelike):
    import eatiht.v2 as v2
    if os.path.exists(HMTL_DIR+htmlstring_or_filelike):
        fr = open(HMTL_DIR+htmlstring_or_filelike, 'r')
        text = v2.extract(fr)
    else:
        text = v2.extract(htmlstring_or_filelike)
    return text




def get_main_text(htmlstring_or_filelike,encoding=None):
    tree = extract(htmlstring_or_filelike,encoding)   
    str = tree.get_html_string()
    return str
   
        
def test():
    import os
    if not os.path.exists(HTML_TEXT_DIR):
        os.mkdir(HTML_TEXT_DIR)
    
    for i in os.listdir(HMTL_DIR):        
        if os.path.isfile(HMTL_DIR+i):
            str = get_main_text(i)
            if str:
                print '%s : succeed' %(i)
                name = i.split('.')[0]+'_.html'
                with open(HTML_TEXT_DIR+name, 'w') as fw:
                    fw.write(str)
                
    
    
    
if __name__=='__main__':
#     test()
        
    file = '1.html'
    with open(HMTL_DIR+file, 'r') as fr:
        html = fr.read()
    text,encode = encode_to_utf8(html)
    print blank_delete(get_main_text(text, encode))
    print encode

    


    
   
    
    
    
    
 
 
 
 
 
 
 
 
 
 
 
 
    
    
    
    
    
    