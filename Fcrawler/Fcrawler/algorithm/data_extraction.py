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
                            self::strong \
                            )] \
                            /text()[string-length(normalize-space()) > 2]/..'


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
 

def gather_xpath(subtrees):
    #all xpaths
    paths = [subtree.parent_path for subtree in subtrees]     
    
    #[".//*[@id='topcont_schedule']/div[3]/div/div[2]", 'div[7]', 'div[2]', 'p']   
    splitpaths=[]
    for p in paths:
        if len(p.split('/'))>6:
            splitpaths.append(p.rsplit('/', 2))
        else:
            splitpaths.append((p,1))
    
    parentpaths = [p[0] for p in splitpaths]
    
    # build frequency distribution
    parentpaths_counter = Counter(parentpaths)
    return parentpaths_counter.most_common()


'''gather  path after first gather'''
def second_gather_xpath_util(paths):
    tmp = []
    splitpaths = [p[0].rsplit('/', 1) for p in paths] 
    
    parentpaths = [p[0] for p in splitpaths]
    
    # build frequency distribution
    parentpaths_counter = Counter(parentpaths)
    pre_paths = parentpaths_counter.most_common()   
    
    trie_obj = LBTrie()
    for path in paths:
        trie_obj.add(path[0])
        
    seen={}
       
    for pre in pre_paths:
        if pre[1]==1: break
#         if not trie_obj.isend(pre[0]):
        tmp.append(pre) 
    #remove pre_path in pre_path
    tmp = remove_prepath(tmp)
    
    for path in paths:
        flag = True
        for p in tmp:
            if pre_match(p[0], path[0]):
                if len(p[0].split('/'))+1<len(path[0].split('/')):
                    tmp.remove(p)
                    p = list(p)
                    p[1] = p[1]+1                
                    p = tuple(p)
                    tmp.append(p)
                flag=False
                break
        if flag:
            tmp.append(path)            
    tmp.sort(lambda p1, p2: p2[1]-p1[1])               
    return tmp  

def second_gather_xpath(paths):
    tmp = paths
    for i in range(3):
        tmp = second_gather_xpath_util(tmp)
    return tmp
    
'''test if parent_path in paths'''    
def is_path_in(parent_path, paths, trie_obj):
    if trie_obj.pre_search(parent_path):
        return True
    return False    

'''test if path1 if prefix of path2'''        
def pre_match(path1, path2):
    t1 = path1.split('/')
    t2 = path2.split('/')
    if len(t1)>=len(t2):
        return False
    for i in range(len(t1)):
        if t1[i] != t2[i]:
            return False
    return True
    
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
        word = word.split('/')
        for c in word:  
            if not c in p:  
                p[c] = {}  
            p = p[c]  
        if word != '':  
            #在单词末尾处添加键值''作为标记，即只要某个字符的字典中含有''键即为单词结尾  
            p[''] = '' 
                
    def isend(self, word):
        p = self.trie
        word = word.split('/')
        for c in word:
            if not c in p:
                return False
            p = p[c]
        if '' in p:
            return True
        return False
    
    def search(self, word):  
        p = self.trie 
        word = word.split('/')
        for c in word:  
            if not c in p:  
                return False  
            p = p[c]  
        #判断单词结束标记''  
        if '' in p:  
            return True  
        return False
    
    #查看某单词的前缀是否存在
    def pre_search(self, word):
        p=self.trie
        word = word.split('/')
        try:
            for c in word:
                p = p[c]
        except(KeyError):
            if c=='/':
                return True
        return False


'''test what kind of page it is'''
def kind_page(blocks):
    LINK_KIND = 0
    TOPIC_KIND = 1
    OTHER_KIND = 2
    
                

'''get block xpaths'''        
def parse(html_str, encoding='utf-8'):
    html_tree= get_html_tree(html_str, encoding)
    
    #only textnode and linknode reserved
    subtrees = get_textnode_subtrees(html_tree, xpath_to_text=TEXT_FINDER_XPATH2)    
    
    #first gather paths
    paths = gather_xpath(subtrees) 
       
#     #remove pre-path
    pre_removed_path = remove_prepath(paths)    
    
    #second gather path, this is blocks we get
    second_gather_paths = second_gather_xpath(pre_removed_path)
    
    trie_obj = LBTrie()
    for path in second_gather_paths: trie_obj.add(path[0])   
    
    
#     print block_subtrees(subtrees, second_gather_paths)
    for subtree in subtrees:
        print subtree.parent_path
    
    print '---'*40 
    for path in paths:
        print path   
    print '---'*40 
    for path in pre_removed_path:
        print path
    
    print '---'*40
    for path in second_gather_paths:
        print path
        
    return subtrees, second_gather_paths
    

'''classify subtrees into different blocks'''
def block_subtrees(subtrees, block_paths):
        
    #{'/html/body/div[1]':"['/html/body/div[1]/p[1]','/html/body/div[1]/p[2]',...]", ...}
    blocks={}
    trie_obj = LBTrie()
    for path in block_paths: trie_obj.add(path[0])
    
    target_subtrees = [subtree for subtree in subtrees
                       if is_path_in(subtree.parent_path, block_paths, trie_obj)]
    
    for block in block_paths:
        blocks[block[0]]=[]
        for subtree in subtrees:
            if pre_match( block[0], subtree.parent_path):
                blocks[block[0]].append(subtree)
    
    return blocks

'''select main text from blocks'''
def main_text(blocks):
    pass 
    

if __name__=='__main__':
#     file = 'b9083515bebb6458b429ff3e73753f6114520784.html'
    file = '51564764b7702d05b4715e55815d12f3d0367c5f.html'
    html=''
    with open(HMTL_DIR+file, 'r') as fr:
        html = fr.read()
    html,_ = encode_to_utf8(html)
#     subtrees, xpaths = parse(html)
#     blocks = block_subtrees(subtrees, xpaths)
    s1 = '/html/body/div[1]/div[4]/div[1]/div[1]/div[1]'
    s2 = '/html/body/div[1]/div[4]/div[1]/div[6]/div[2]/div[2]/ul'
    s3 = '/html/body/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]'
    s4 = '/html/body/div[1]/div[4]/div[1]/div[1]/div[1]/table/tbody/tr'
    a=[s1, s2 ,s3 ,s4]
    trie_obj = LBTrie()
    for i in a: trie_obj.add(i)  
    m = '/html/body/div[1]/div[4]/div[1]/div[1]'
    print trie_obj.isend(m)
    
    







      