#coding=utf-8
'''
Created on Jun 30, 2015

@author: root
'''

from eatiht.etv2 import *
from collections import Counter
from Fcrawler.spiders.config import *
from Fcrawler.spiders.html import encode_to_utf8 
from numpy.core.defchararray import isalnum
'''test if two nodes are same,
node is dict, like key:value
'''
from Trie_tree import LBTrie, path_counts, nodesCount



def Same(node1, node2):
    if len(node1) != len(node2):
        return False
    
    if isinstance(node1, dict) and isinstance(node2, dict):        
        for key in node1.keys():
            if key in node2:
                print key                
                return Same(node1[key], node2[key]) or Same(node2[key], node1[key])
            else:
                continue
    elif isinstance(node1, str) or isinstance(node2, str):
        return True
    else:
        return False

'''tag like div[1], return tag name'''
def tag_name(tag):
    res=''
    for i in tag:
        if i>= 'a' and i<='z':
            res += i
    return res
 
  
'''avg child numbers of one path''' 
def avg_child(trie_tree):  
    db1 =  nodesCount(trie_tree)
    db2 =  path_counts(trie_tree)
    res =  db1*1.0/db2
    if res < int(res)+0.5:
        res = int(res)
    else:
        res = int(res)+1
    return res
    

def has_num(str):
    for i in str:
        if i=='[':
            return True
    return False



#主干性标签
core_tag=['html','body','center']
    #典型的分支标签
brance_tag=['ul']

'''prun paths that has more than @avg_child_num child'''    
def prun_tree(trie_tree,avg_child_num):    
    
    if trie_tree is None: return {}    
    
    for key in trie_tree.keys():        
        if trie_tree[key]=='':
            continue
        #针对典型的分支标签，一定合并
        if tag_name(key) in brance_tag:
            del trie_tree[key]
            trie_tree[key]={'':''}
        
        #如果孩子数超过了平均值，则需要合并
        if len(trie_tree[key]) >= avg_child_num:
#             if key not in core_tag and has_num(key):
              if key not in core_tag or has_num(key):
                #如果只是删除，会导致路径缺失
                del trie_tree[key]
                #{'':''}表示路径到此截止，只是删除了路径之后的所有孩子
                trie_tree[key]={'':''}                
        
        
        prun_tree(trie_tree[key], avg_child_num)
            
    return trie_tree        


'''get all paths of trie tree'''   
def xpath_result(trie_tree, seen=[], result=[]): 
    if trie_tree:
        nextpaths = trie_tree.keys()
        for key in nextpaths:            
            if trie_tree[key]!='':
                nextseen=[]
                nextseen.extend(seen)
                nextseen.append(key)                
                xpath_result(trie_tree[key], nextseen, result)
            else:
                val=''
                for i in seen:
                    val += i+'/'
                val = val.rsplit('/',1)[0]
                result.append(val)
    return result
'''paths_nums is set of xpath
最多剪枝5次
'''            
def parse(html_str, encoding='utf-8', max_loop=5):
    html_tree= get_html_tree(html_str, encoding)
    
    #only textnode and linknode reserved
    subtrees = get_textnode_subtrees(html_tree, xpath_to_text=TEXT_FINDER_XPATH2) 
    
    xpath_set = [subtree.parent_path for subtree in subtrees]
    
    trie_obj = LBTrie()    
    
    for i in xpath_set: trie_obj.add(i)
    
    trie = trie_obj.trie
    
    
    avg_child_num_set=[]
    
    for i in range(max_loop):
        from pprint import pprint
        pprint(trie)
        
        avg_child_num = avg_child(trie)
        
        if avg_child_num_set and avg_child_num_set[-1]<=avg_child_num:
            break 
                  
        avg_child_num_set.append(avg_child_num)
        
        trie = prun_tree(trie, avg_child_num)
        
        print '---'*20,i,'---'*20
        result = []    
        seen=[]
        xpath_result(trie, seen, result)
        
    
    return result
    

if __name__=='__main__':
    a=[]
    file = 'c0f4979f563295f8ccd6663c55de77bf867f16be.html'
    with open(HMTL_DIR+file, 'r') as fr:
        html = fr.read()
    html,_ = encode_to_utf8(html)   
    
    tag='ul[2]'
    print tag_name(tag)
    
    result = parse(html)    
    for i in result:
        print i
    
        
    


