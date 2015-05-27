'''
Created on May 27, 2015

@author: root
'''

from unittest import TestCase
from Fcrawler.items import UrlItem
from Utility import Redis_Priority_Set, Redis_Set

class Test_Redis_Priority_Set(TestCase):
    def __init__(self):
        self.priority_set = Redis_Priority_Set('test')
    
    def test(self):
        item1 = UrlItem()
        item2 = UrlItem()
        item3 = UrlItem()
        
        item1['url']='www.1.com'
        item1['depth']=1
        item1['priority'] = 2
        
        item2['url']='www.2.com'
        item2['depth']=2
        item2['priority'] = 4
        
        item3['url']='www.3.com'
        item3['depth']=1
        item3['priority'] = 5
        
        self.priority_set.push(item1)
        self.priority_set.push(item2)
        self.priority_set.push(item3)
        
        out1 = self.priority_set.pop()
        out2 = self.priority_set.pop()
        out3 = self.priority_set.pop()       
    
        print out1
        print out2
        print out3
        



if __name__=='__main__':
    t = Test_Redis_Priority_Set()
    t.test()
    