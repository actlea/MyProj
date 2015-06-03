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
    def __init__(self, name, base_url=''):
        self.html = self.html_content(name)
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



def get_tree(html_string, encoding=''):
    if encoding:
        html_tree = lxml.html.parse(BytesIO(html_string), lxml.html.HTMLParser(encoding=encoding,remove_blank_text=True))
    else:
        html_tree = lxml.html.fromstring(html_string)        
    return html_tree
     
def extract(htmlstring_or_filelike):
    html_string = htmlstring_or_filelike
    if os.path.exists(HTML_DIR+htmlstring_or_filelike):
       with open(HTML_DIR+htmlstring_or_filelike, 'r') as fr:
                html_string = fr.read()
    
#     encoding = chardet.detect(html_string)['encoding']               
    html_tree = get_tree(html_string)      
       
    subtrees = etv2.get_textnode_subtrees(html_tree, xpath_to_text = TEXT_FINDER_XPATH)
    # calculate AABSL
    avg, _, _ = etv2.calcavg_avgstrlen_subtrees(subtrees)

    # "high-pass" filter
    filtered = [subtree for subtree in subtrees
                if subtree.ttl_strlen > avg]

    paths = [subtree.parent_path for subtree in filtered]

    hist = etv2.get_xpath_frequencydistribution(paths)

    target_subtrees = [stree for stree in subtrees
                       if hist[0][0] in stree.parent_path]
                
    title = html_tree.find(".//title")   
    if title:
        title_content = title.text_content()        
    else:
        title_content = ''

    return etv2.TextNodeTree(title_content, target_subtrees, hist)   

def get_main_text(htmlstring_or_filelike):
    try:
        tree = extract(htmlstring_or_filelike)
        str = tree.get_html_string()
        return str
    except:
        Logger.error(htmlstring_or_filelike+' extract() error')
        print htmlstring_or_filelike+' extract() error'
        return None
        
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
    str = get_main_text(content)
    print str


    
   
    
    
    
    
 
 
 
 
 
 
 
 
 
 
 
 
    
    
    
    
    
    