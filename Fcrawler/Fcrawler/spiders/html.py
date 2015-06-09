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
import chardet
from hashlib import sha1

try:    
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO
    
from config import *


from Fcrawler.items import PageItem
reload(sys) 
sys.setdefaultencoding('utf-8')  # @UndefinedVariable

Punctuation = "[！，。？：、]+"
USERDICT = DIR+'dict.txt'
NBA_DICT = DIR+'nba.txt'
HTML_DIR = DIR+'HTML/'

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
        self.hxs = lxml.html.fromstring(self.html)
    
    def html_content(self, filelike_or_str):
        '''html from file or str'''
        if os.path.exists(HTML_DIR+filelike_or_str):            
            with open(HTML_DIR+filelike_or_str, 'r') as fr:
                content = fr.read()           
            return content
        else:           
            return filelike_or_str         
            
    
    def parse(self):
        title = blank_delete( ext(self.hxs.xpath('//title/text()')) )
#         encode = blank_delete( ext( self.hxs.xpath('//meta/@charset')) )
        encode = re.search(r'charset=(.*).', self.html) 
        if encode: encode = encode.group(1)       
       
       
        item = PageItem()
        item['original_url'] = self.base_url
#         item['content'] = self.html 
        item['priority']=0
        item['main_text'] = get_main_text(self.html)
               
#         item['encode']=encode
        
        #hash html
        fp = sha1()
        fp.update(item['original_url'])
        fp.update(self.html)
        hash_code = fp.hexdigest()
        hash_code = int(hash_code, 16)
        item['hash'] = hash_code
        
        item['time'] = timestamp() 
        
        d = pickle.dumps(item, protocol=-1)
        return (d, HTML_FETCH_SET.push(hash_code) ) 
              
        
    
    


#use to compute html priority     
def extract(htmlstring_or_filelike):                  
    if os.path.exists(HTML_DIR+htmlstring_or_filelike):
        fr = open(HTML_DIR+htmlstring_or_filelike, 'r')
        return etv2.extract(fr)
    else:
        return etv2.extract(htmlstring_or_filelike)               
     
    

def exract_v2(htmlstring_or_filelike):
    import eatiht.v2 as v2
    if os.path.exists(HTML_DIR+htmlstring_or_filelike):
        fr = open(HTML_DIR+htmlstring_or_filelike, 'r')
        text = v2.extract(fr)
    else:
        text = v2.extract(htmlstring_or_filelike)
    return text




def get_main_text(htmlstring_or_filelike):
    tree = extract(htmlstring_or_filelike)
#         tree.bootstrapify()
    str = tree.get_html_string()
    return str
        
def test():
    import os
    if not os.path.exists(HTML_DIR+'/Text/'):
        os.mkdir(HTML_DIR+'/Text/')
    
    for i in os.listdir(HTML_DIR):        
        if os.path.isfile(HTML_DIR+i):
            str = get_main_text(i)
            if str:
                print '%s : succeed' %(i)
                name = i.split('.')[0]+'_.html'
                with open(HTML_DIR+'/Text/'+name, 'w') as fw:
                    fw.write(str)
                
    
    
    
if __name__=='__main__':
#     test()
    content = '''
    <html>
    <head></head>
    <body>
        <div>
            <article>
                <p>This is a story about the life of Foo</p>
                <p>The life of Foo was one of great foo</p>
                <p>Foo foo, foo foo foo. Foo, foofoo?</p>
                <p>Foo was no stranger to foo. For Foo did foo</p>
            </article>
        </div>
        <div>
            <div>
                <p>Buy Bar Now Buy Buy Buy Buy Buy Buy Buy Buy Buy Buy Buy!</p>
                <p>Get The Bar Next Door!</p>
                <p>Increase Your Bar!</p>
                <p>Never Bar again!</p>
            </div>
        <div>
            <footer>
                <p>Who the hell is Boo. Who the hell is Far?</p
            </footer>
        </div>
    </body>
</html>
'''
    import eatiht.v2 as v2
    file = '0602152604.html'
    print get_main_text(content)
#     res = v2.extract_more(content)
#     print res[0]
#     print res[1]
#     print res[2]
#     print res[3]
    


    
   
    
    
    
    
 
 
 
 
 
 
 
 
 
 
 
 
    
    
    
    
    
    