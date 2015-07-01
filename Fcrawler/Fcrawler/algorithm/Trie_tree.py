#coding=utf-8
'''
Created on Jun 30, 2015

@author: root
'''
from trie import Trie
'''
use Trie Tree to remove pre path
'''
class LBTrie(Trie):  
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
   
    #判断是否为前缀路径，即其后面还有标签          
    def isend(self, word):
        p = self.trie
        word = word.split('/')
        for c in word:
            if not c in p:
                return False
            p = p[c]
        if len(p)>1:
            return False
        return True
    
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
    
    #查看某单词的前缀是否trie中的完整的单词,不包括word本身
    def pre_search(self, word):
        p=self.trie
        word = word.split('/')
        try:
            for c in word:                
                p = p[c]
                if '' in p and p['']=='':
                    return True
        except(KeyError):
             return False
        return False
 
#节点总数+1   
def nodesCount(trie):    
    cnt = 0
    for k in trie.keys():        
       if trie[k] != '':
           cnt += len(trie[k])
           cnt += nodesCount(trie[k])
    return cnt
           
                
    
            
#路径总数  
def path_counts(trie):
    n = 0
    for k in trie.keys():
        if trie[k]=='':
            n += 1            
        else:            
            n = n  + path_counts(trie[k])
    return n  

          
if __name__ == '__main__':
    s1='/1/2/3/5'
    s2='/1/2/3/6'
    s3 = '/1/2/3/7'
    s4 = '/1/2/4/8'
    s5='/1/2/4/9'
    a=[s1,s2,s3,s4,s5]
    trie = LBTrie()
    for i in a: trie.add(i)
    
    trie = trie.trie
   
    from pprint import pprint
    pprint(trie)
    
    path_num = path_counts(trie)
    avg = nodesCount(trie)
    print 'path_num:%s' %path_num
    print 'avg:%s' %avg
        
        