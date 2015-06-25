#coding=utf-8
'''
Created on Jun 17, 2015

@author: root
'''

from eatiht.etv2 import *
from collections import Counter
from Fcrawler.spiders.config import *
from Fcrawler.spiders.html import encode_to_utf8 



TEXT_FINDER_XPATH2 = '//body\
                        //*[not(\
                            self::script or \
                            self::noscript or \
                            self::style or \
                            self::i or \
                            self::b or \
                            self::strong or \
                            self::span \
                            )] \
                            /text()/..'

def parse(html_str, encoding='utf-8'):
    html_tree= get_html_tree(html_str, encoding)
    
    #only textnode and linknode reserved
    subtrees = get_textnode_subtrees(html_tree, xpath_to_text=TEXT_FINDER_XPATH2)    
    
    #conuter paths
    paths = gather_xpath(subtrees) 
       
    #remove pre-path
    pre_removed_path = remove_prepath(paths)
    
    for path in pre_removed_path:
        print path

'''
if paths is a pre path in paths, then remove paths
'''
def remove_prepath(paths):    
    tmp=[]
    trie_obj = LBTrie()
    for path in paths:
        trie_obj.add(path[0])
    
    for path in paths:
        if trie_obj.isend(path[0]):
            tmp.append(path)
    return tmp
    

def pre_match(path1, path2):
    t1 = path1.split('/')
    t2 = path2.split('/')
    if len(t1)>=len(t2):
        return False
    for i in range(len(t1)):
        if t1[i] != t2[i]:
            return False
    return True
    

def gather_xpath(subtrees):
    #all xpaths
    paths = [subtree.parent_path for subtree in subtrees]
    
    #[".//*[@id='topcont_schedule']/div[3]/div/div[2]", 'div[7]', 'div[2]', 'p']
    splitpaths = [p.rsplit('/', 3) for p in paths]
    
    parentpaths = [p[0] for p in splitpaths]
    
    # build frequency distribution
    parentpaths_counter = Counter(parentpaths)
    return parentpaths_counter.most_common()

'''
use Trie Tree to remove pre path
'''
class LBTrie:  
    """ 
    simple implemention of Trie in Python by authon liubing, which is not  
    perfect but just to illustrate the basis and principle of Trie.  
    """  
    def __init__(self):  
        self.trie = {}  
        self.size = 0  
         
    #添加单词   
    def add(self, word):  
        p = self.trie
        for c in word:  
            if not c in p:  
                p[c] = {}  
            p = p[c]  
        if word != '':  
            #在单词末尾处添加键值''作为标记，即只要某个字符的字典中含有''键即为单词结尾  
            p[''] = '' 
                
    def isend(self, word):
        p = self.trie
        for c in word:
            p = p[c]
        
        if p.has_key('/'):
            return False
        return True
    


if __name__=='__main__':
    file = 'b9083515bebb6458b429ff3e73753f6114520784.html'
    html=''
    with open(HMTL_DIR+file, 'r') as fr:
        html = fr.read()
    html,_ = encode_to_utf8(html)
    parse(html)
    
    
    







      